#@author:九世
#@file:spliter.py
#@time:2019/10/10


import scrapy
import re
import time
import socket
from colorama import Fore
from bs4 import BeautifulSoup
from .start import Options,init

init(wrap=True)

name=time.time()
name=str(name).replace('.','')
obj = Options()
user = input('Please domain (例如:baidu.com) >')

print('')
dicts=obj.load_files(user)

print('')
class Domain(scrapy.Spider,Options):
    name = 'domain'
    def start_requests(self):
        for url in dicts:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        if response.url:
            zz = str(re.findall('^https?:\/\/[^\/\?#:]+', response.url)[0]).replace('http://', '').replace('https://', '')
            host = socket.gethostbyname(zz)
            title=str(BeautifulSoup(response.text,'html.parser').find_all('title')[0]).replace('<title>','').replace('</title>','')
            headers=response.headers
            if 'Server' in headers:
                server=str(headers['Server']).replace('b','').replace("'",'')
            else:
                server='NULL'

            if 'X-Powered-By' in headers:
                powered=str(headers['X-Powered-By']).replace('b','').replace("'",'')
            else:
                powered='NULL'
            print(Fore.GREEN+'[DOMAIN]'+ 'domain:{} http_statuscode:{} IP:{} title:{} headers:{} X-Powered-By:{}'.format(zz,response.status,host,title,server,powered))
            print('domain:{} http_statuscode:{} IP:{} title:{} headers:{} X-Powered-By:{}'.format(zz, response.status, host, title, server, powered),file=open('save/{}.txt'.format(name),'a',encoding='utf-8'))