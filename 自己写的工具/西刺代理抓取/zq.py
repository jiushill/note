'''
抓取高匿代理将url设置为:https://www.xicidaili.com/nn/，普通代理设置为:https://www.xicidaili.com/nt/,https代理设置为:https://www.xicidaili.com/wn/,http代理设置为:https://www.xicidaili.com/wt/
根据要抓取的代理设置为指定的URL
'''
#@author:九世
#@time:2019/10/5
#@file:zq.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import requests
import gevent
import re
import sys
import time

class found_anonymous_IP(object):
    def __init__(self):
        #设置的URl
        self.url='https://www.xicidaili.com/nn/'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.djcs=[]
        self.xcs=[]
        self.calc=0
        self.calc2=0
        self.title=['IP地址:',' 端口:',' http/https:',' 存活时间:']

    def page_found(self):
        try:
            rqt=requests.get(url=self.url,headers=self.headers,timeout=10)
            if rqt.status_code!=200:
                print('[-] 不小心封IP了')
            page=re.findall('href="/nn/[0-9]{4,}"',rqt.text)[-1]
            page=str(page).replace('href="','').replace('/','').replace('"','').replace('nn','')
            return page
        except Exception as r:
            if 'Connection' in str(r):
                exit()
            else:
                print('[Error] {}'.format(r))

    def zhua(self,url):
        jg=''
        try:
            rqt=requests.get(url=url,headers=self.headers,timeout=10)
            if rqt.status_code != 200:
                print('[-] 不小心封IP了')
            data=re.findall('<td>.*</td>',rqt.text)
            for u in data:
                if self.calc2==0:
                    jg+=self.title[0]
                elif self.calc2==1:
                    jg += self.title[1]
                elif self.calc2==2:
                    jg += self.title[2]
                elif self.calc2==3:
                    jg += self.title[3]
                elif self.calc2==4:
                    print(jg)
                    print(jg,file=open('save.txt','a',encoding='utf-8'))
                jg+=str(u).replace('<td>','').replace('</td>','')
                self.calc2+=1
                if self.calc2==5:
                    self.calc2=0
                    jg=''
        except Exception as r:
            if 'Connection' in str(r):
                exit()
            else:
                print('[Error] {}'.format(r))

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.zhua,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self):
        for u in range(1,int(self.page_found())+1):
            url='{}{}'.format(self.url,u)
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()
            time.sleep(0.01)
            self.djcs.append(url)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()

if __name__ == '__main__':
    obj=found_anonymous_IP()
    obj.djc()