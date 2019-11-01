#@author:九世
#@time:2019/11/1
#@file:sql_inject.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import init,Fore
import requests
import asyncio
import gevent
import os

init(wrap=True)

class Injections(object):
    def __init__(self):
        self.djcs=[]
        self.xcs=[]
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.payloads=[]
        self.calc=0
        self.calc2=0
        self.xcs=[]
        self.urls=[]
        self.blacks=[]
        self.on_black=[]
        self.injection=[]

    def reqt(self,url):
        for p in self.payloads:
            urls1=url+p[0]
            urls2=url+p[1]
            try:
                rqt=requests.get(url=urls1,headers=self.headers,timeout=3)
                rqt2=requests.get(url=urls2,headers=self.headers,timeout=3)
                for y in self.blacks:
                    if y in rqt.text or y in rqt2.text:
                        print(Fore.YELLOW+'[X] '+Fore.WHITE+'发现黑名单关键字 url:{}'.format(url))
                        self.on_black.append(url)
                        break

                if rqt.text != rqt2.text and len(rqt.text)!=len(rqt2.text) and url not in self.on_black:
                    print(Fore.BLUE+'[+] '+Fore.WHITE+'Sql injection URL:{}'.format(url))
                    print('Sql injection URL:{}'.format(url),file=open('sql_inject_ok.txt','a',encoding='utf-8'))
                    break
                elif url in self.on_black:
                    break
                else:
                    print(Fore.RED+'[-] '+Fore.WHITE+'Not Sql injection URL:{} http_status_code:{}'.format(rqt.url,rqt.status_code))
            except Exception as r:
                print(Fore.RED+'[-] '+Fore.WHITE+'Error {} url:{}'.format(r,url))
                print('Error {} url:{}'.format(r, url),file=open('sql_inject_error.log','a',encoding='utf-8'))

    def xc(self,rw):
        for y in rw:
            self.xcs.append(gevent.spawn(self.reqt,y))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        for u in self.urls:
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.djcs.clear()
                self.calc=0

            self.djcs.append(u)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.djcs.clear()
            self.calc=0

    def file_pd(self,file):
        if os.path.exists(file):
            print(Fore.BLUE+'[+] '+Fore.WHITE+'{}文件存在'.format(file))
        else:
            print(Fore.BLUE + '[-] ' + Fore.WHITE + '{}文件不存在'.format(file))
            exit()

    async def ybs(self):
        print('--------------------[读取所需文件]--------------------')
        self.file_pd('url.txt')
        self.file_pd('black.txt')
        self.file_pd('payload.txt')

        calc=0
        dk=open('payload.txt','r',encoding='utf-8')
        for d in dk.readlines():
            calc+=1
            data="".join(d.split('\n')).split(':')
            self.payloads.append(data)

        dks=open('black.txt','r',encoding='utf-8')
        for b in dks.readlines():
            datas="".join(b.split('\n'))
            self.blacks.append(datas)

        dkx=open('url.txt','r',encoding='utf-8')
        for b in dkx.readlines():
            datas="".join(b.split('\n'))
            self.urls.append(datas)

        print('--------------------[注入判断]--------------------')
        self.djc()

if __name__ == '__main__':
    banners = '''
                       ___                        ___           ___                   
           ___        /  /\\           ___        /  /\\         /  /\\          ___     
          /__/\\      /  /::|         /__/\\      /  /::\\       /  /::\\        /__/\\    
          \\__\\:\\    /  /:|:|         \\__\\:\\    /  /:/\\:\\     /  /:/\\:\\       \\  \\:\\   
          /  /::\\  /  /:/|:|__   ___ /  /::\\  /  /::\\ \\:\\   /  /:/  \\:\\       \\__\\:\\  
       __/  /:/\\/ /__/:/ |:| /\\ /__/\\  /:/\\/ /__/:/\\:\\ \\:\\ /__/:/ \\  \\:\\      /  /::\\ 
      /__/\\/:/~~  \\__\\/  |:|/:/ \\  \\:\\/:/~~  \\  \\:\\ \\:\\_\\/ \\  \\:\\  \\__\\/     /  /:/\\:\\
      \\  \\::/         |  |:/:/   \\  \\::/      \\  \\:\\ \\:\\    \\  \\:\\          /  /:/__\\/
       \\  \\:\\         |__|::/     \\__\\/        \\  \\:\\_\\/     \\  \\:\\        /__/:/     
        \\__\\/         /__/:/                    \\  \\:\\        \\  \\:\\       \\__\\/      
                      \\__\\/                      \\__\\/         \\__\\/                  
                       ___           ___     
           ___        /  /\\         /  /\\    
          /__/\\      /  /::\\       /  /::|   
          \\__\\:\\    /  /:/\\:\\     /  /:|:|   
          /  /::\\  /  /:/  \\:\\   /  /:/|:|__ 
       __/  /:/\\/ /__/:/ \\__\\:\\ /__/:/ |:| /\\\\
      /__/\\/:/~~  \\  \\:\\ /  /:/ \\__\\/  |:|/:/
      \\  \\::/      \\  \\:\\  /:/      |  |:/:/ 
       \\  \\:\\       \\  \\:\\/:/       |__|::/  
        \\__\\/        \\  \\::/        /__/:/   
                      \\__\\/         \\__\\/    
                      
    '''
    print(banners)
    obj=Injections()
    loop=asyncio.get_event_loop()
    tk=loop.create_task(obj.ybs())
    loop.run_until_complete(tk)