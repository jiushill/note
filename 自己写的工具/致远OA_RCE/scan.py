#@author:九世
#@file:scan.py
#@time:2019/9/21

from multiprocessing import Process
from bs4 import BeautifulSoup
import gevent
import warnings
import requests
import sys
import os

warnings.filterwarnings("ignore")

class Rce_scan(object):
    def __init__(self,id,data):
        self.djcs=[]
        self.xcs=[]
        self.calc=0
        self.path='/weaver/bsh.servlet.BshServlet'
        self.guanjian='BeanShell'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        if id=='1':
            self.rd=str(data).rstrip('/')+self.path
            self.reqts(self.rd)
        elif id=='2':
            self.rd=data
            if os.path.exists(self.rd):
                self.file=data
                self.djc(self.rd)
            else:
                print('[file] {}文件不存在'.format(data))
                exit()
        else:
            print('[ERROR] 没有:{}这个选项'.format(id))

    def reqts(self,url):
        try:
            rqt=requests.get(url=url,headers=self.headers,timeout=10,allow_redirects=False,verify=False)
            if self.guanjian in rqt.text:
                print('[Loophole] {}'.format(rqt.url))
            else:
                print('[NO] {} http_statud_code:{}'.format(rqt.url,rqt.status_code))
        except Exception as r:
            print('[Warring] {}'.format(r))

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.reqts,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self,file):
        dk=open(file,'r',encoding='utf-8')
        for d in dk.readlines():
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()
            else:
                data="".join(d.split('\n'))+self.path
                self.djcs.append(data)
                self.calc+=1
        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
if __name__ == '__main__':
    obj=Rce_scan(sys.argv[1],sys.argv[2])
