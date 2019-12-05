#@author:九世
#@time:2019/11/30
#@file:baidu_search.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import asyncio
import gevent
import requests
import re
import json
import config
import xlsxwriter

workbook = xlsxwriter.Workbook('save.xlsx')
xls = workbook.add_worksheet()
xls.set_column('A:A', 20)
xls.set_column('B:B', 20)
xls.set_column('C:C', 20)
xls.set_column('D:D', 20)
xls.set_column('E:E', 20)

xls.write('A1', 'title')
xls.write('B1', 'url')
xls.write('C1', 'http_code')
xls.write('D1', 'X-Powered-By')
xls.write('E1', 'Server')


class Baidu(object):
    def __init__(self):
        headers='''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: www.baidu.com
Pragma: no-cache
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'''
        self.headers={}
        calc=0
        key=re.findall(': .*',headers)
        value=re.findall('.*:',headers)
        for y in range(0,len(key)):
            self.headers[str(value[y]).replace(':','').rstrip().lstrip()]=str(key[y]).replace(':','').rstrip().lstrip()

        self.cookies={}
        for c in str(config.cookies).split(';'):
            key,value=c.split('=',1)
            self.cookies[key]=value

        self.ybs=[]
        self.djcs=[]
        self.xcs=[]
        self.calc=0
        self.calc2=0

        self.js=2


    def searchs(self,urls):
        try:
            rqt=requests.get(url=urls,headers=self.headers,timeout=10,cookies=self.cookies)
            text=re.findall('data-tools=\'.*\'>',rqt.content.decode('utf-8'))
            if len(text)>0:
                for c in text:
                    data=json.loads(str(c).replace('>','').replace("'",'').replace('data-tools=',''))
                    rbt=requests.get(url=data['url'],headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'},timeout=5)
                    if 'X-Powered-By' in [x for x in rbt.headers]:
                        powerd=rbt.headers['X-Powered-By']
                    else:
                        powerd='None'

                    if 'Server' in [x for x in rbt.headers]:
                        server=rbt.headers['Server']
                    else:
                        server='None'
                    print('title:{} url:{} http_code:{} X-Powered-By:{} Server:{}'.format(data['title'],rbt.url,rbt.status_code,powerd,server))
                    xls.write('A{}'.format(self.js), data['title'])
                    xls.write('B{}'.format(self.js),rbt.url)
                    xls.write('C{}'.format(self.js),rbt.status_code)
                    xls.write('D{}'.format(self.js),powerd)
                    xls.write('E{}'.format(self.js),server)
                    self.js+=1

        except Exception as r:
            print('Error {}'.format(r))

    def xc(self,rw):
        for c in rw:
            self.xcs.append(gevent.spawn(self.searchs,c))

        gevent.joinall(self.xcs)
        self.xcs.clear()
        workbook.close()

    def djc(self):
        for g in self.ybs:
            if self.calc2==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.djcs.clear()
                self.calc2=0

            self.djcs.append(g)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.djcs.clear()
            self.calc2 = 0


    async def yb(self):
        for c in config.data:
            for p in range(0,int(config.page)):
                urls = 'https://www.baidu.com/s?wd={}&pn={}'.format(c, p*10)
                if self.calc==100:
                    self.djc()
                    self.calc=0
                    self.ybs.clear()

                self.ybs.append(urls)
                self.calc+=1

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs.clear()

if __name__ == '__main__':
    if config.cookies!="" and config.page!="" and len(config.data)!=0:
        obj=Baidu()
        loop=asyncio.get_event_loop()
        tk=loop.create_task(obj.yb())
        loop.run_until_complete(tk)
    else:
        print('[-] 搜索内容、页数、COOKIE 不能为空')