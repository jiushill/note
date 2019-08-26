#@author:九世
#@time:2019/8/25
#@file:query.py
from gevent import monkey;monkey.patch_all()
import requests
import re
import gevent
import sys
from bs4 import BeautifulSoup
from multiprocessing import Process
from gevent.lock import RLock
import time
import random
import config

locks=RLock()
write,flush=sys.stdout.write,sys.stdout.flush
st=[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
ua=[]
dk=open('user_agents.txt','r')
for d in dk.readlines():
    data="".join(d.split('\n'))
    ua.append(data)

class Quert(object):
    def __init__(self):
        self.url='http://ip.bczs.net/city'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self.lb={}
        self.djcs=[]
        self.xcs=[]
        self.calc=0

    def sheng_ip(self,ip):
        ips=ip.split('-')
        start_ip=ips[0].split('.')
        stop_ip=ips[1].split('.')
        for s in range(int(start_ip[0]),int(stop_ip[0])+1):
            for s0 in range(int(start_ip[1]), int(stop_ip[1]) + 1):
                for s1 in range(int(start_ip[2]), int(stop_ip[2]) + 1):
                    for s2 in range(int(start_ip[3]), int(stop_ip[3]) + 1):
                        ip='{}.{}.{}.{}'.format(s,s0,s1,s2)
                        yield ip

    def getip(self):
        rqt=requests.get(url=self.url,headers=self.headers,timeout=3)
        zz=BeautifulSoup(rqt.text,'html.parser')
        for c in zz.find_all('tbody'):
            jg=re.findall('<tr class="ip[0-9]{1,}"><td>[0-9]{1,}</td><td title=".*?"><a href="/city/.*?">',str(c))
            for g in jg:
                th=re.subn('<tr class="ip.*?"><td>.*?</td><td title=".*?">.*</td><td>0</td><td>.*</td>','',str(g))
                href=re.findall('href=".*?"',th[0])
                titles=re.findall('title=".*?"',th[0])
                self.lb[str(titles[0]).replace('title=','').replace('"','')]=str(href[0]).replace('href=','').replace('"','')

        print('[+] 可选择城市')
        for j in self.lb:
            print(j)

        print('')
        user=input('请输入要进行爬取的城市列表：')
        if user in self.lb:
            urls='http://ip.bczs.net/{}'.format(self.lb[user])
            self.ip_query(urls)

    def query(self,ip,id):
        if id==1:
            miao=0
        else:
            miao=random.choice(st)

        time.sleep(miao)
        headers={'user-agent':random.choice(ua)}
        calc=1
        try:
            url='https://site.ip138.com/{}/'.format(ip)
            rqt=requests.get(url=url,headers=headers)
            token=re.findall('[0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z][0-9-a-z]',rqt.text)
            while True:
                try:
                    url='https://site.ip138.com/index/querybyip/?ip={}&page={}&token={}'.format(ip,calc,token[1])
                    rqt=requests.get(url=url,headers=headers,timeout=10)
                    js=rqt.json()
                    print(js)
                    if str(js['status'])=='True':
                        name=[x for x in js]
                        if 'data' in name:
                            print('{}查询结果'.format(ip))
                            print('{}查询结果'.format(ip),file=open('save.txt','a'))
                            for data in js['data']:
                                print(data['domain'])
                                print(data['domain'],file=open('save.txt','a'))
                            calc+=1
                        else:
                            print('IP:{} 查询不到,或已经到结尾'.format(ip))
                            break
                    else:
                        print('[-] 查询频率过高,等待几秒重新执行')
                        time.sleep(60)
                        self.query(ip,0)
                except Exception as r:
                    print('Err:{}'.format(r))

        except Exception as r:
            print('Err:{}'.format(r))

    def xc(self,urls):
        locks.acquire()
        for u in urls:
            self.xcs.append(gevent.spawn(self.query,u,1))
        locks.release()
        gevent.joinall(self.xcs)

    def djc(self,rw):
        for ip in rw:
            url=ip
            if self.calc==config.PROCESS:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.djcs.clear()
                self.calc=0
            self.djcs.append(url)
            self.calc+=1
        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()

    def ip_query(self,urls):
        rqt = requests.get(url=urls,headers=self.headers,timeout=3)
        ip=re.finditer('(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)[-](25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',rqt.text)
        if config.ID==1:
            for c in ip:
               self.djc(self.sheng_ip(c.group()))
        else:
            for c in ip:
                for hosts in self.sheng_ip(c.group()):
                    self.query(hosts,1)

if __name__ == '__main__':
    obj=Quert()
    obj.getip()