#@author:九世
#@file:query_domain.py
#@time:2019/9.15

from gevent import monkey;monkey.patch_all()
from bs4 import BeautifulSoup
from multiprocessing import  Process
import requests
import gevent
import sys
import socket
import time

write,flush=sys.stdout.write,sys.stdout.flush
class API_Query(object):
    def __init__(self,domain):
        self.host='http://api.hackertarget.com/hostsearch/?q={}'.format(domain)
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        self.domains=[]
        self.hosts={}
        self.calc=0
        self.xcs=[]
        self.code=[200,403]
        self.dport=[80,443]
        self.start=[]
        self.ojbk=[]

    def request(self):
        try:
            rqt=requests.get(url=self.host,headers=self.headers)
            if 'error check your search parameter' in rqt.text:
                print('[-] 找不到此域名的子域')
                exit()
            jg=rqt.text.split('\n')
            size=int(len(jg))
            for z in range(0,size):
                data=str(jg[z]).split(',')
                if len(data)==1:
                    pass
                else:
                    self.domains.append(data[0])
                    self.hosts[data[0]]=data[1]
        except Exception as r:
            print('[-] Errors:{}'.format(r))

    def rbts(self,url):
        try:
           rqt=requests.get(url=url,headers=self.headers,timeout=3)
           if rqt.status_code in self.code:
                text=BeautifulSoup(rqt.text,'html.parser').find_all('title')[0]
                for c in self.hosts:
                    if c in rqt.url:
                        ip=self.hosts[c]
                jgb='[+] {}==>{} title:{} ip:{}'.format(rqt.status_code,rqt.url,str(text).replace('<title>','').replace('</title>','').replace('\n',''),ip)
                self.ojbk.append(jgb)
        except:
            pass

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.rbts,x)) for x in rw]
        gevent.joinall(self.xcs)
        qc=list(set(self.ojbk))
        for jg in qc:
            print(jg)

    def found(self):
        s=socket.socket()
        s.settimeout(3)
        for doamin in self.domains:
            test='{}'.format(doamin)
            write(test)
            flush()
            time.sleep(0.5)
            write('\x08'*len(test))
            if self.calc==100:
                p=Process(target=self.xc,args=(self.start,))
                p.start()
                self.start.clear()
                self.calc=0
            for port in self.dport:
                try:
                    s.connect((doamin,port))
                    if port==80:
                        self.start.append('http://{}'.format(doamin))
                    elif port==443:
                        self.start.append('https://{}'.format(doamin))
                    self.calc+=1
                except:
                    pass

        if len(self.start)>0:
            p = Process(target=self.xc, args=(self.start,))
            p.start()

if __name__ == '__main__':
    try:
        obj=API_Query(sys.argv[1])
        obj.request()
        obj.found()
    except Exception as r:
        if 'list index out of range' in str(r):
            print('[-] 至少需要一个参数,例如:python query_domain.py baidu.com')