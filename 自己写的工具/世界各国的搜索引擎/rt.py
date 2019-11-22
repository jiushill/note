#@author:九世
#@time:2019/11/0
#@file:rt.py

import asyncio
import aiohttp
import requests
import re
from bs4 import BeautifulSoup

class Search_f(object):
    def __init__(self):
        self.url='https://www.dragon-guide.net/guobie/meizhou/America.htm'
        self.proxies={'http':'http://127.0.0.1:25378','https':'https://127.0.0.1:25378'}
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.links=[]
        self.ybs=[]

    async def get_url(self,url):
        async with aiohttp.ClientSession() as rqt:
            async with rqt.get(url=url,headers=self.headers) as response:
                titles=str(BeautifulSoup(await response.text(),'html.parser').find_all('title')[0]).replace('<title>','').replace('</title>','')
                url=BeautifulSoup(await response.text(),'html.parser')
                for div in url.find_all("div",class_='col-lg-3 col-md-3 col-sm-3 col-xs-6'):
                    if 'href' in str(div):
                        href=BeautifulSoup(str(div),'html.parser')
                        for fuck in href.find_all('a'):
                            if 'dragon-guide.net' not in fuck.get('href') and 'baidu.com' not in fuck.get('href'):
                                print(fuck.get('href'),fuck.get_text())
                                print(fuck.get('href'), fuck.get_text(),file=open('files/{}'.format(titles),'a',encoding='utf-8'))

    def load_link(self):
        try:
            rqt=requests.get(url=self.url,headers=self.headers,proxies=self.proxies)
            link=re.findall('https://www.dragon-guide.net/guobie/.*/.*',rqt.content.decode('utf-8'))
            for u in link:
                url=re.findall('[a-zA-z]+://[^\s]*',str(u))
                for x in url:
                    data=str(x).replace('"','')
                    self.links.append(data)

        except Exception as r:
            print('Error {}'.format(r))

    def link_run(self):
        for url in self.links:
            self.ybs.append(asyncio.ensure_future(self.get_url(url)))

        loop=asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.ybs))


if __name__ == '__main__':
    obj=Search_f()
    obj.load_link()
    obj.link_run()