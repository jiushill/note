#@author:九世
#@time:2019/11/9

from gevent import monkey;monkey.patch_all()
from colorama import init,Fore
from multiprocessing import Process
from bs4 import BeautifulSoup
import gevent
import asyncio
import random
import time
import requests
import os

init(wrap=True)
class Google_query(object):
    def __init__(self):
        self.timeout=3
        self.calc=0
        self.url='/search?q={search}&btnG=Search&safe=active&gbv=1'
        self.gdomain=[]
        #self.calc2=0
        self.djcs=[]
        self.search=['site:{domain} inurl:upload','site:{domain} inurl:admin']
        self.domains=[]
        self.ip=[]
        self.xcs=[]
        #self.ybs=[]
        self.ua=[]
        self.payload=[]

    def google_search(self,ua,url,proxies,sleep):
        try:
            time.sleep(int(sleep))
            rqt=requests.get(url=url,headers={'user-agent':ua},timeout=3,proxies=proxies)
            if 'and not a robot.' in rqt.text:
                print(Fore.YELLOW+'[!] '+Fore.WHITE+'发现Google验证码')
                exit()
            else:
                b=BeautifulSoup(rqt.text,'html.parser').find_all('h3')
                if len(b)==0:
                    print('不存在要寻找的内容，请的url:{}'.format(url))
                else:
                    print(Fore.GREEN+'[+] '+Fore.WHITE+'链接数量:{} 请求的url:{}'.format(len(b),url))
                    for a in b:
                        data=BeautifulSoup(str(a),'html.parser')
                        for u in data.find_all('a'):
                            print(Fore.GREEN+'[+] '+Fore.WHITE+'URL:{} title:{}'.format(str(u.get('href')).replace('/url?q=',''),u.get_text()))
                            print('URL:{} title:{}'.format(str(u.get('href')).replace('/url?q=', ''), u.get_text()),file=open('jg/save.txt','a',encoding='utf-8'))

        except Exception as r:
           print(Fore.RED+'[-] '+Fore.WHITE+'Error {}'.format(r))


    def xc(self,rw):
        for z in rw:
            for y in self.search:
                url='https://'+random.choice(self.gdomain)+self.url.format(search=str(y).format(domain=z['domain']))
                self.xcs.append(gevent.spawn(self.google_search,ua=z['user-agent'],url=url,proxies=z['proxies'],sleep=z['sleep']))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        data={}
        domain_number=len(self.domains)
        for x in range(domain_number):
            if self.calc==100:
                p=Process(target=self.xc,args=(self.payload,))
                p.start()
                self.payload.clear()
                self.calc=0
                data={}

            data['user-agent']=random.choice(self.ua)
            data['domain']=self.domains[x]
            data['proxies']={'http':'http://{}'.format(random.choice(self.ip)),'https':'https://{}'.format(random.choice(self.ip))}
            data['sleep']=random.choice([x for x in range(1,30)])
            self.payload.append(data)
            data = {}
            self.calc+=1

        if len(self.payload)>0:
            p = Process(target=self.xc, args=(self.payload,))
            p.start()
            self.payload.clear()
            self.calc = 0
            data = {}

    def read_file(self,file):
        dk = open(file, 'r', encoding='utf-8')
        for d in dk.readlines():
            data="".join(d.split('\n'))
            yield data

    async def yb(self):
        if os.path.exists('files/UA.txt') and os.path.exists('files/file.txt') and os.path.exists('files/ip.txt') and os.path.exists('files/domain.txt'):
            print(Fore.BLUE+'[+] '+Fore.WHITE+'加载所需文件中...')
        else:
            print(Fore.RED+'[-] '+Fore.WHITE+'缺少所需文件..请填补文件')
            exit()

        print(Fore.GREEN+'[~] '+Fore.WHITE+'开始查找')

        for u in self.read_file('files/UA.txt'):
            self.ua.append(u)

        for d in self.read_file('files/file.txt'):
            self.domains.append(d)

        for d in self.read_file('files/ip.txt'):
            self.ip.append(d)

        for g in self.read_file('files/domain.txt'):
            self.gdomain.append(g)

        self.djc()




if __name__ == '__main__':
    obj=Google_query()
    loop=asyncio.get_event_loop()
    tk=loop.create_task(obj.yb())
    loop.run_until_complete(tk)