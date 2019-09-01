#@author:九世
#@file:scan.py
#@time:2019/8/28
'''
web目录扫描
'''
from gevent import monkey;monkey.patch_all()
from gevent.lock import RLock
from multiprocessing import Process
import requests
import gevent
import time
import warnings
import os

warnings.filterwarnings("ignore")
locks=RLock()
class Scan(object):
    def __init__(self):
        self.conf_path=['start','url.txt']
        self.ok=[] #A list without blacklist keywords
        self.no=[] #List with blacklist keywords
        self.code=[200,403]#http status code list
        self.black=['黑名单','拦截','WAF','360防火墙','防火墙','502','Not Found','拒绝访问','403','安全狗','云锁','找不到','不存在','404'] #black list
        self.proxies='' #For proxy settings, use the following formats: {http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
        self.djcs=[]
        self.xcs=[]
        self.calc=100
        self.path = os.listdir(self.conf_path[0])
        self.process=100 #When the number reaches this level, a process is executed.
        self.process_sleep=3 #Delay of execution process
        self.time=False #When this condition is true, a single thread is executed
        self.sleep=5 #delays
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self.timeout=10 #request time out

    def read_dict(self,file_name):
        with open(file_name,'r',encoding='utf-8') as dk:
            for path in dk:
                data="".join(path.split('\n'))
                yield data

    def pd(self,url,code,text):#Determine whether there is a blacklist keyword
        for balck in self.black:
            if code in self.code and not str(balck) in text:
                if url in self.ok:continue
                self.ok.append('url:{} code:{}'.format(url,code))
            else:
                self.no.append('url:{} code:{}'.format(url,code))

    def web_scan(self,urls):
        try:
            rqt=requests.get(url=urls,headers=self.headers,timeout=self.timeout,verify=False,proxies=self.proxies)
            self.pd(url=rqt.url,code=rqt.status_code,text=rqt.content.decode('utf-8'))
        except Exception as r:
            pass

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.web_scan,r))


        gevent.joinall(self.xcs)
        ok=list(set(self.ok))
        no=list(set(self.no))
        for g in ok:
            if g not in no:
                print('[+] {}'.format(g))
                print('[+] {}'.format(g),file=open('save.txt','a',encoding='utf-8'))
            else:
                print('[-] {}'.format(g))

    def djc(self):
        if self.time==False:
                for c in self.path:
                    paths='{}/{}'.format(self.conf_path[0],c)
                    try:
                        for r in self.read_dict(paths):
                            with open('url.txt', 'r', encoding='utf-8') as dks:
                                for d in dks.readlines():
                                    url='{}{}'.format(str(d).rstrip('/')+'/',r)
                                    if self.calc==self.process:
                                        time.sleep(self.process_sleep)
                                        p=Process(target=self.xc,args=(self.djcs,))
                                        p.start()
                                        self.djcs.clear()
                                        self.calc=0
                                    self.djcs.append(url)
                                    self.calc+=1
                    except:
                        pass
                if len(self.djcs)>0:
                    p = Process(target=self.xc, args=(self.djcs,))
                    p.start()
        else:
            for c in self.path:
                paths = '{}/{}'.format(self.conf_path[0], c)
                try:
                    for r in self.read_dict(paths):
                        time.sleep(self.sleep)
                        self.web_scan(r)
                except:
                    pass
if __name__ == '__main__':
    obj=Scan()
    print('name:web路径爆破\nversion:V1\nauthor:九世\n字典来源:7kb扫描器')
    obj.djc()