#@author:九世
#@time:2019/12/21
#@file:bao.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from bs4 import BeautifulSoup
import gevent
import asyncio
import sys
import dns.resolver
import os
import re
import requests
import time

class Baopo:
    def __init__(self,proces,level,sleeps,domain):
        self.proces=int(proces)
        self.level=int(level)
        self.sleeps=float(sleeps)
        self.domain=domain
        self.dictpath=os.listdir('files')
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.xcs=[]
        self.djcs=[]
        self.ybs=[]
        self.calc=0
        self.calc2=0

    def rdfile(self,file):
        dk=open(file,'r',encoding='utf-8')
        for j in dk.readlines():
            data="".join(j.split('\n'))
            yield data

    def dnsjiexi(self,domain):
        try:
            A = dns.resolver.query(domain,'A')
            for i in A.response.answer:
                if 'CNAME' in str(i):
                    do=re.findall('.*IN',str(i))
                    jg=re.findall('.*{}'.format(self.domain),do[0])
                    if len(jg)>0:
                        jr=jg[0]
                        http=self.htttpreqts(jr)
                        print('domain:{} http_code:{} title:{} server:{} X-Powered-By:{}'.format(jr,http['code'],str(http['title']).replace('\n',''),http['server'],http['X-Powered-By']))
                        print('domain:{} http_code:{} title:{} server:{} X-Powered-By:{}'.format(jr, http['code'], str(http['title']).replace('\n', ''), http['server'], http['X-Powered-By']),file=open('{}.txt'.format(self.domain),'a',encoding='utf-8'))

        except:
            pass

    def htttpreqts(self,domain):
        try:
            data={}
            url='http://{}'.format(domain)
            rqt=requests.get(url=url,headers=self.headers,timeout=10)
            headers=[x for x in rqt.headers]
            title=BeautifulSoup(rqt.content.decode('utf-8'),'html.parser').find('title')
            data['code']=rqt.status_code
            data['title']=title.get_text()
            if 'Server' in headers:
                data['server']=rqt.headers['Server']
            else:
                data['server']='NULL'

            if 'X-Powered-By' in headers:
                data['X-Powered-By']=rqt.headers['X-Powered-By']
            else:
                data['X-Powered-By']='NULL'

            return data
        except:
            return False

    def xc(self,rw):
        for w in rw:
            domain='{}{}'.format(w,self.domain)
            self.xcs.append(gevent.spawn(self.dnsjiexi,domain))

        gevent.joinall(self.xcs)
        self.xcs.clear()


    def djc(self):
        if self.level==2:
            for u in self.ybs:
                if self.calc2==self.proces:
                    p=Process(target=self.xc,args=(self.djcs,))
                    p.start()
                    self.calc2=0
                    self.djcs.clear()

                self.djcs.append(u+".")
                self.calc2+=1

            if len(self.djcs)>0:
                p = Process(target=self.xc, args=(self.djcs,))
                p.start()
                self.calc2 = 0
                self.djcs.clear()
        else:
            space=''
            space2=''
            space3=''
            da=''
            data=''
            for l in range(self.level):
                da+='{}for a{} in self.ybs:\n'.format(space,l)
                space+='    '
                data+='a{}+"."+'.format(l)

            jg=da+space+'data={}'.format(data.rstrip('+"."+'))
            jg+='+"."'+'\n'
            jg+='{}if self.calc2==self.proces:\n'.format(space)
            space2+=space
            space2+='   '
            jg+='{}p=Process(target=self.xc,args=(self.djcs,))\n'.format(space2)
            jg+='{}p.start()\n'.format(space2)
            jg+='{}self.calc2=0\n'.format(space2)
            jg+='{}self.djcs.clear()\n'.format(space2)
            jg+='{}self.djcs.append(data)\n'.format(space)
            jg+='{}self.calc2+=1\n'.format(space)
            jg+='if len(self.djcs)>0:\n'
            space3+='   '
            jg+='{}p = Process(target=self.xc, args=(self.djcs,))\n'.format(space3)
            jg+='{}p.start()\n'.format(space3)
            jg+='{}self.calc2 = 0\n'.format(space3)
            jg+='{}self.djcs.clear()\n'.format(space3)
            exec(jg)

    async def yb(self):
        for d in self.dictpath:
            for u in self.rdfile('files/{}'.format(d)):
                if self.calc==self.proces:
                    self.djc()
                    self.calc=0
                    self.ybs.clear()

                time.sleep(self.sleeps)
                self.calc+=1
                self.ybs.append(u)

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs.clear()


if __name__ == '__main__':
    try:
        number=sys.argv[1]
        level=sys.argv[2]
        sleeps=sys.argv[3]
        domain=sys.argv[4]
    except:
        print('python bao.py [number] [level] [sleeps] [domain]\n例如:python bao.py 100 2 0.003 baidu.com')
        exit()

    obj=Baopo(number,level,sleeps,domain)
    loop=asyncio.get_event_loop()
    tk=loop.create_task(obj.yb())
    loop.run_until_complete(tk)