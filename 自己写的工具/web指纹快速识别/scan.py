#@author:九世
#@file:scan.py
#@time:2019/9/9

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import gevent
import time
import os
import sys


class Scan(object):
    def __init__(self):
        self.headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        self.djcs=[]
        self.xcs=[]
        self.calc=0

    def web_request(self,payload):
        data=''
        try:
            rqt=requests.get(url=payload,headers=self.headers,timeout=3,verify=False,allow_redirects=False)
            data+='url:{}\n'.format(rqt.url)
            data+='http_status_code:{}\n'.format(rqt.status_code)
            header=[x for x in rqt.headers]
            if 'X-Powered-By' in header:
                data+='脚本类型:{}\n'.format(rqt.headers['X-Powered-By'])

            if 'Server'in header:
                data+='Server:{}\n'.format(rqt.headers['Server'])

            tl=BeautifulSoup(rqt.text,'html.parser')
            data+='title:{}'.format(str(tl.find_all('title')[0]).replace('<title>','').replace('</title>',''))
        except Exception as r:
            print('[-] Error:{}'.format(r))

        print(data)
        print('')

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.web_request,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self,type):
        if type=='1':
            p=Process(target=self.web_request,args=(sys.argv[2],))
            p.start()

        elif type=='2':
            files=sys.argv[2]
            if os.path.exists(files):
                print('[+] 找到文件:{}'.format(files))
            else:
                print('[-] 找不到文件:{}'.format(files))
                exit()

            dk=open(files,'r',encoding='utf-8')
            for r in dk.readlines():
                dat="".join(r.split('\n'))
                if self.calc==100:
                    time.sleep(.3)
                    p=Process(target=self.xc,args=(self.djcs,))
                    p.start()
                    self.djcs.clear()
                    self.calc=0
                self.djcs.append(dat)
                self.calc+=1


            if len(self.djcs)>0:
                p = Process(target=self.xc, args=(self.djcs,))
                p.start()

if __name__ == '__main__':
    obj=Scan()
    obj.djc(sys.argv[1])