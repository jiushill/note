#@author:九世
#@time:2019/10/15
#2file:found_cz.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import gevent
import requests
import time
import re

class yanz(object):
    def __init__(self):
        self.filename='save.txt'
        self.dk=[]
        self.xcs=[]
        self.clac=0

    def qq(self,proxy):
        try:
            rqts=requests.get(url='http://www.baidu.com',headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},timeout=10,proxies=proxy)
            print('[+] 活着的代理:{}'.format(proxy))
            print('[+] 活着的代理:{}'.format(proxy),file=open('save2.txt','a',encoding='utf-8'))
        except:
            print('[-] 死了的代理:{}'.format(proxy))

    def xc(self,rw):
        for q in rw:
            q=eval(q)
            self.xcs.append(gevent.spawn(self.qq,q))

        gevent.joinall(self.xcs)

    def djc(self):
        dk=open(self.filename,'r',encoding='utf-8')
        for q in dk.readlines():
            if self.clac==100:
                p=Process(target=self.xc,args=(self.dk,))
                p.start()
                self.clac=0
                self.dk.clear()

            data="".join(q.split('\n'))
            hosts=str(re.findall('IP地址:.*? ',data)[0]).replace('IP地址:','').rstrip()
            port=str(re.findall('端口:[0-9]{1,}',data)[0]).replace('端口:','').rstrip()
            time.sleep(0.01)
            self.dk.append("{'http':'"+"http://{}:{}'".format(hosts,port)+",'https':'"+"https://{}:{}'".format(hosts,port)+"}")
            self.clac+=1

        if len(self.dk)>0:
            p = Process(target=self.xc, args=(self.dk,))
            p.start()

if __name__ == '__main__':
    obj=yanz()
    obj.djc()