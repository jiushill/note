#@author:九世
#@file:query.py
#@time:2019/9/18

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import gevent
import config
import time
import re

class Search(object):
    def __init__(self):
        self.time=config.SLEEP
        self.math=config.MATH
        self.values=config.PAGE+1
        self.save=config.FILE
        self.processread=config.THREADS
        self.cookies={}
        for ck in config.COOKIES.split(';'):
            key,value=str(ck).split('=',1)
            self.cookies[key]=value
        self.headers=config.HEADERS
        self.djcs=[]
        self.xcs=[]
        self.calc=0
        self.page=0
        self.pagex=[]
        self.guanjianzi=''

    def request_github(self,url,id=False):
        self.page+=1
        urbbr=url
        if id==False:
            q=re.findall('q=.*[&]',url)
            self.guanjianzi+=str(q[0]).replace('q=','').replace('&','')
        rqt=requests.get(url=url,headers=self.headers,cookies=self.cookies)
        pagez=re.findall('/search[?]p=[0-9]{1,}&amp[;]q='+'{}'.format(self.guanjianzi)+'[&]amp[;]type=Code',rqt.text)
        if len(pagez)>0:
            if id == False:
                for p in pagez:
                    page=re.findall('p=.*?[&]',str(p))
                    pages=str(page[0]).replace('&','').replace('p=','')
                    self.pagex.append(int(pages))
        else:
            self.pagex.append(1)
            print('[无法找到更多的页数] 代表最多页数为:1 ')

        self.pagex.sort()
        print('关键字:{} [页数]:{} [总页数]:{}'.format(self.guanjianzi,self.page,self.pagex[-1]))
        data=re.findall('<a title=".*" .*>.*</a>',rqt.text)
        if len(data)>0:
            for c in data:
                datas=BeautifulSoup(str(c),'html.parser')
                for s in datas.find_all('a'):
                    url='https://github.com{}'.format(s.get('href'))
                    print('[关键字:{}] url:{}'.format(self.guanjianzi,url))
        else:
            print('[关键字:{}] 没找到任何结果'.format(self.guanjianzi))
            exit()

        print('')

        if id==False:
            if self.pagex[-1]!=1:
                for y in range(2,int(self.pagex[-1])+1):
                    if self.values!=False and y==int(self.values):
                        exit()
                    urls='{}&p={}'.format(urbbr,y)
                    self.request_github(urls,id=True)

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.request_github,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self):
        for pay in self.math:
            if self.calc==self.processread:
                time.sleep(self.time)
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()
            else:
                urls='https://github.com/search?q={}&type=Code'.format(pay)
                self.calc+=1
                self.djcs.append(urls)

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()

if __name__ == '__main__':
    banner = '''
     88888888b                                  dP               .88888.  oo   dP   dP                dP       
     88                                         88              d8'   `88      88   88                88       
    a88aaaa    .d8888b. dP    dP 88d888b. .d888b88              88        dP d8888P 88d888b. dP    dP 88d888b. 
     88        88'  `88 88    88 88'  `88 88'  `88              88   YP88 88   88   88'  `88 88    88 88'  `88 
     88        88.  .88 88.  .88 88    88 88.  .88              Y8.   .88 88   88   88    88 88.  .88 88.  .88 
     dP        `88888P' `88888P' dP    dP `88888P8               `88888'  dP   dP   dP    dP `88888P' 88Y8888' 
                                                   oooooooooooo                                                
    歌词:抬起头闭上眼，所有烦恼看不见
    歌曲:童言无忌(Live)
    '''
    print(banner)
    obj=Search()
    obj.djc()