#@author:九世
#@time:2020/2/14
#@file:cnvd.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import asyncio
import gevent
import re

class Zhua(object):
    def __init__(self):
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.url='https://www.cnvd.org.cn/'
        self.timeout=5
        self.djcs=[]
        self.xcs=[]
        self.ybs=[]
        self.calc=0
        self.calc2=0

    def fg(self,data):
        try:
            rtt=requests.get(url=data['url'],headers=self.headers,timeout=5)
            br=BeautifulSoup(rtt.text,'html.parser')
            print('title:{} url:{}'.format(data['title'],data['url']))
            for t in br.find_all('tr'):
                tds=t.find_all('td')
                if len(tds)==2:
                    print('{}:{}'.format(re.sub('\s','',str(tds[0].get_text()).rstrip('').lstrip('').replace(' ','')),re.sub('\s',"","".join(str(tds[1].get_text()).replace('\r','').replace('\n','').replace(' ','').lstrip().replace(' ','').rstrip().split(' ')))))

            print('')
        except:
             print('[-] 获取漏洞内容失败')

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.fg,r))
        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        for t in self.ybs:
            if self.calc2==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc2=0
                self.djcs.clear()
                p.join()
            self.djcs.append(t)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc2 = 0
            self.djcs.clear()
            p.join()

    async def yb(self):
        data=[]
        dc={}
        print('[+] 上周最受关注的漏洞')
        dick=[]
        nls=[]
        try:
            rqt=requests.get(url=self.url,headers=self.headers,timeout=5)
            b=BeautifulSoup(rqt.text,'html.parser')
            for j in b.find_all('div',class_='s_w'):
                span=j.find_all('span',class_='t_gz_sz_span')
                if len(span)>0:
                    for x in span:
                        dick.append(x.get_text())
                l=j.find_all('li')
                if len(l)>0:
                    for c in l:
                        a=c.find_all('a')
                        if len(a)>0:
                            for x in a:
                                uri='{}'.format(x.get('href'))
                                title='{}'.format(x.get('title'))
                                nls.append('title:{} url:{}'.format(title,self.url+uri))
        except Exception as r:
            print('[-] Error:{}'.format(r))
            exit()

        for j in range(0,len(nls)):
            print(nls[j]+' 点击次数:{}'.format(dick[j]))

        print('\n[+] 获取最新漏洞列表信息')
        try:
            rbt=requests.get(url='https://www.cnvd.org.cn/flaw/list.htm',headers=self.headers,timeout=self.timeout)
            tx=BeautifulSoup(rbt.text,'html.parser')
            for t in tx.find_all('tbody'):
                for a in t.find_all('a'):
                    uri=a.get('href')
                    title=a.get('title')
                    dc['title']=title
                    dc['url']=self.url.rstrip('/')+uri
                    data.append(dc)
                    dc={}
        except Exception as r:
            print('[-] Error;{}'.format(r))
            exit()

        for j in data:
            if self.calc==100:
                self.djc()
                self.calc=0
                self.ybs.clear()
            self.ybs.append(j)
            self.calc+=1

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs.clear()
if __name__ == '__main__':
    obj=Zhua()
    loop=asyncio.get_event_loop()
    task=loop.create_task(obj.yb())
    loop.run_until_complete(task)