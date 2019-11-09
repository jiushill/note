#@author:九世
#@time:2019/11/9
#@file:proxiers.py

from gevent import monkey;monkey.patch_all()
import gevent
import aiohttp
import requests
import asyncio
import config
from bs4 import BeautifulSoup
from multiprocessing import Process

dl=[]
async def Reqt_url(url):
    async with aiohttp.ClientSession() as request:
        async with request.get(url=url,headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'},timeout=30) as response:
            b=BeautifulSoup(await response.text(),'html.parser')
            for tr in b.find_all('tr'):
                td=BeautifulSoup(str(tr),'html.parser').find_all('td')
                if len(td)>0:
                    ip=str(td[0]).replace('<td>','').replace('</td>','')
                    port=str(td[1]).replace('<td>','').replace('</td>','')
                    proxies={'http':'http://{}:{}'.format(ip,port),'https':'https://{}:{}'.format(ip,port)}
                    dl.append(proxies)

def keyon(proxies):
    try:
        rqt=requests.get(url='http://www.baidu.com',headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'},proxies=proxies,timeout=5)
        print('[+] 可用代理:{}'.format(proxies))
    except Exception as r:
        print('代理不可用:{} Error:{}'.format(proxies,r))

def xc(rw):
    xcs=[]
    for g in rw:
        xcs.append(gevent.spawn(keyon,g))
    gevent.joinall(xcs)
    xcs.clear()

def dls():
    data = []
    calc = 0
    for p in dl:
        if calc == 100:
            p=Process(target=xc,args=(data,))
            p.start()
            calc = 0
            data.clear()
            dl.clear()

        data.append(p)
        calc += 1

    if len(data)>0:
        p = Process(target=xc, args=(data,))
        p.start()
        calc = 0
        data.clear()
        dl.clear()

def run():
    data=[]
    calc=0
    loop=asyncio.get_event_loop()
    keys=list(config.PROXIERS)
    for p in range(1,int(config.PROXIERS[keys[0]])+1):
        if calc==100:
            loop.run_until_complete(asyncio.wait(data))
            calc=0
            data.clear()

        urls='{}{}'.format(keys[0],p)
        data.append(asyncio.ensure_future(Reqt_url(urls)))
        calc+=1

    if calc!=0:
        loop.run_until_complete(asyncio.wait(data))
        calc = 0
        data.clear()

    dls()

if __name__ == '__main__':
    run()