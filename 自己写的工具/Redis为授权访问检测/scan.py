#@author:九世
#@time:2019/12/5
#@file:scan.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import asyncio
import gevent
import os
import sys
import redis

class Scaner(object):
    def __init__(self):
        self.djcs=[]
        self.ybs=[]
        self.xcs=[]
        self.calc=0
        self.calc2=0

    def redis_fuck(self,ip):
        try:
            pool = redis.ConnectionPool(host=ip, port=6379, password='', db=0,socket_connect_timeout=3)
            rt = redis.Redis(connection_pool=pool)
            js=rt.info()
            print('redis版本：{} OS：{}'.format(js['redis_version'],js['os']))
            print('[+] 发现Redis未授权 {}'.format(ip))
            print('[+] 发现Redis未授权 {}'.format(ip),file=open('save.txt','a',encoding='utf-8'))
        except Exception as r:
            if 'DENIED Redis is running' in str(r):
                print('[-] Redis需要密码,失败:{}'.format(ip))
            else:
                print('{} {}'.format(r,ip))

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.redis_fuck,r))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        for j in self.ybs:
            if self.calc2==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc2=0
                self.djcs.clear()

            self.djcs.append(j)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc2 = 0
            self.djcs.clear()

    async def yb(self):
        try:
            filename=sys.argv[1]
            if os.path.exists(filename):
                dk=open(filename,'r',encoding='utf-8')
                for r in dk.readlines():
                    dat="".join(r.split('\n'))
                    if self.calc==100:
                        self.djc()
                        self.calc=0
                        self.ybs.clear()

                    self.ybs.append(dat)
                    self.calc+=1

                if len(self.ybs)>0:
                    self.djc()
                    self.calc = 0
                    self.ybs.clear()

            else:
                print('[-] 文件不存在:{}'.format(filename))
                exit()
        except Exception as r:
            if 'list index' in str(r):
                print('执行方法：python scan.py [file]')
            else:
                print(r)

if __name__ == '__main__':
    obj=Scaner()
    loop=asyncio.get_event_loop()
    tk=loop.create_task((obj.yb()))
    loop.run_until_complete(tk)