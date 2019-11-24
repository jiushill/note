#@author:九世
#@time:2019/11/23
#@file:scan.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import Fore,init
import gevent
import asyncio
import requests
import sys
import time
import os

init(wrap=True)
class Fck(object):
    def __init__(self):
        self.color=[Fore.YELLOW,Fore.RED,Fore.BLUE,Fore.WHITE] #color
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.timeout=10
        self.write,self.flush=sys.stdout.write,sys.stdout.flush
        self.upload_paths=[]
        self.version_paths=[]

        self.ybs=[]
        self.xcs=[]
        self.calc=0

    def read_files(self):
        if os.path.exists('file'):
            print('[*] file文件夹存在')
        else:
            print('[-] file文件夹不存在')
            exit()

        dk=open('file/upload.txt','r',encoding='utf-8')
        for j in dk.readlines():
            data="".join(j.split('\n'))
            self.upload_paths.append(data)


        dk=open('file/version.txt','r',encoding='utf-8')
        for d in dk.readlines():
            data="".join(d.split('\n'))
            self.version_paths.append(data)

    def dirpaths(self,url):
        print('[*] 检测FCKeditorb版本路径')
        for u in self.version_paths:
            urls='{}{}'.format(url.rstrip(),u)
            try:
                rqt=requests.get(url=urls,headers=self.headers,timeout=self.timeout,allow_redirects=False)
                if len(rqt.text)!=0 and rqt.status_code==200 and u in rqt.url:
                    print('[+] FCKeditorb版本路径:{}'.format(rqt.url))
                    print(rqt.url,file=open('save.txt','a',encoding='utf-8'))
            except Exception as r:
                print('[-] Error:{}'.format(r))
            neiron='路径:{}'.format(urls)
            self.write(neiron)
            time.sleep(1)
            self.write('\x08'*len(neiron))
            self.flush()

        print('')
        print('[*] 检测FCKeditorb上传路径')
        for u in self.upload_paths:
            urls='{}{}'.format(url.rstrip(),u)
            try:
                rqt=requests.get(url=urls,headers=self.headers,timeout=self.timeout,allow_redirects=False)
                if len(rqt.text)!=0 and rqt.status_code==200 and u in rqt.url:
                    print('[+] FCKeditorb上传路径:{}'.format(rqt.url))
                    print(rqt.url, file=open('save.txt', 'a', encoding='utf-8'))
            except Exception as r:
                print('[-] Error:{}'.format(r))
            neiron='路径:{}'.format(urls)
            self.write(neiron)
            self.flush()
            time.sleep(1)
            self.write('\x08'*len(neiron))

    def pd(self,url):
        try:
            rqt = requests.get(url=url, headers=self.headers, timeout=self.timeout, allow_redirects=False)
            if len(rqt.text) != 0 and rqt.status_code == 200:
                print('[+] FCKeditorb路径:{}'.format(rqt.url))
                print(rqt.url, file=open('save.txt', 'a', encoding='utf-8'))
        except Exception as r:
            print('[-] Error:{}'.format(r))

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.pd,r))

        gevent.joinall(self.xcs)
        self.xcs.clear()


    async def yb(self,xw):
        if os.path.exists(xw):
            print('[*] {}:存在'.format(xw))
        else:
            print('[-] {}:不存在'.format(xw))
            exit()

        print('[*] 检测FCKeditorb路径')
        self.read_files()
        dk=open(xw,'r',encoding='utf-8')
        for j in dk.readlines():
            for g in self.version_paths:
                if self.calc==100:
                    self.xc(self.ybs)
                    self.ybs.clear()
                    self.calc=0

                url="{}{}".format("".join(j.split('\n')),g)
                if url in self.ybs:continue
                self.ybs.append(url)
                self.calc+=1

            if len(self.ybs)>0:
                self.xc(self.ybs)
                self.ybs.clear()
                self.calc = 0

            for g in self.upload_paths:
                if self.calc == 100:
                    self.xc(self.ybs)
                    self.ybs.clear()
                    self.calc = 0

                url = "{}{}".format("".join(j.split('\n')), g)
                if url in self.ybs:continue
                self.ybs.append(url)
                self.calc += 1

            if len(self.ybs) > 0:
                self.xc(self.ybs)
                self.ybs.clear()
                self.calc = 0


    def option(self):
        while True:
            print('[!] 单个url检测（单线程），批量检测（变态检测）')
            print('1.单个url检测')
            print('2.批量检测')
            print('3.退出')
            user=input('ID:')
            if user=='1':
                xw=input('url:')
                self.dirpaths(xw)
            elif user=='2':
                loop=asyncio.get_event_loop()
                user=input('file:')
                tk=loop.create_task(self.yb(user))
                loop.run_until_complete(tk)

            elif user=='3':
                exit()
            else:
                print('[-] 没有这个选项')
            print('')

if __name__ == '__main__':
    obj=Fck()
    obj.read_files()
    obj.option()