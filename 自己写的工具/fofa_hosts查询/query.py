#@author:九世
#@file:query.py
#@time:2019/9/12

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import gevent
import requests
import re
import sys
import os

class Fofa(object):
    def __init__(self):
        self.url='https://www.fofa.so/hosts/'
        self.url2='https://fofa.so/ajax/get_rules?ip=ips&key=keys'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
        self.calc=0
        self.timeouts_calc=0
        self.proce=[]
        self.gev=[]


    def get_keys(self,url):
        try:
            rqt = requests.get(url=url, headers=self.headers, timeout=10)
            if not '无相关信息' in rqt.text:
                key=re.findall('var key = ".*"',rqt.text)
                return str(key[0]).replace('var','').replace('=','').replace('key','').replace(' ','').replace('"','').rstrip().lstrip()
            else:
                print('[-] 找不到有关IP的信息')
        except Exception as r:
            self.timeouts_calc+=1
            print('[-] Error:{}'.format(r))
            if 'ConnectionPool' in str(r):
                print('[!] 尝试重连中,次数:{}'.format(self.timeouts_calc))
                self.get_keys(url)

    def requet(self,url):
        keys=self.get_keys(url)
        hosts=re.search('(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',url)
        print('[{}]查询结果'.format(hosts[0]))
        url=self.url2.replace('ips',hosts[0]).replace('keys',keys)
        rbt=requests.get(url=url,headers=self.headers,timeout=10)
        jsons=rbt.json()
        print('状态:{}'.format(jsons['status']))
        datas=''
        for s in jsons['rules']:
            for c in jsons['rules'][s]['data']:
                for v in c:
                    datas+='{}:{}'.format(v,c[v])+' '
            print('Port banner:{}:{}'.format(s,datas))

    def xc(self,rw):
        [self.gev.append(gevent.spawn(self.requet,self.url+x)) for x in rw]
        gevent.joinall(self.gev)

    def djc(self,id,data):
        if id==str(1):
            urls=self.url+data
            self.requet(urls)
        elif id==str(2):
            if os.path.exists(data):
                print('[+] Found File: {}'.format(data))
                print('read file:{}'.format(data))
                dk = open(data, 'r', encoding='utf-8')
                for r in dk.readlines():
                    datas = "".join(r.split('\n'))
                    if self.calc == 100:
                        p = Process(target=self.xc, args=(self.proce,))
                        p.start()
                    else:
                        self.calc += 1
                        self.proce.append(datas)

                if len(self.proce) > 0:
                    p = Process(target=self.xc, args=(self.proce,))
                    p.start()
            else:
                print('[-] Not Found File:{}'.format(data))
                exit()
        else:
            print('[-] Not Choice')


if __name__ == '__main__':
    obj=Fofa()
    try:
        obj.djc(id=sys.argv[1],data=sys.argv[2])
    except Exception as r:
        if 'list index out of range'==str(r):
            print('[-] Please Run query.py [id] [data]\n'
                  'id==1 url data==url\n'
                  'id==2 file data==file\n')
        else:
            print(r)