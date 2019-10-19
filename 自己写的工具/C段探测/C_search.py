#@author:九世
#@time:2019/10/20
#@file:C_search.py

import asyncio
import aiohttp
import IPy
import config
import sys
from colorama import Fore,init
from bs4 import BeautifulSoup

init(wrap=True)
class C_scan(object):
    def __init__(self):
        self.port=config.PORT_LIST
        self.timeout=config.TIMEOUT
        self.calc=0
        self.ybs=[]
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    async def reqt_c(self,url):
        async with aiohttp.ClientSession() as request:
            try:
                async with request.get(url=url,headers=self.headers,timeout=self.timeout,verify_ssl=False) as response:
                    if response:
                        html=await response.text(encoding='utf-8')
                        text=BeautifulSoup(html,'html.parser').find_all('title')
                        if len(text)>0:
                            title=str(text[0]).replace('<title>','').replace('</title>','').replace('\n','')
                        else:
                            title=''
                        print(Fore.GREEN+'[+] '+Fore.WHITE+'URL:{} http_status_code:{} title:{}'.format(response.url,response.status,title))
                        print('URL:{} http_status_code:{} title:{}'.format(response.url,response.status,title),file=open('save.txt','a',encoding='utf-8'))
            except Exception as r:
                pass

    def create_ipranges(self,hosts):
        host=IPy.IP(hosts)
        for ip in host:
            for port in self.port:
                data="http://{}:{}".format(ip,port)
                if self.calc==100:
                    loop=asyncio.get_event_loop()
                    loop.run_until_complete(asyncio.wait(self.ybs))
                    self.calc=0
                    self.ybs.clear()

                self.ybs.append(asyncio.ensure_future(self.reqt_c(data)))
                self.calc+=1

        if len(self.ybs)>0:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(self.ybs))

if __name__ == '__main__':
    obj=C_scan()
    try:
        obj.create_ipranges(sys.argv[1])
    except Exception as r:
        print(Fore.YELLOW+'[!] '+Fore.WHITE+'执行方式为:python C_search.py [IP/Subnet_mask]')