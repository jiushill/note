#@author:九世
#@file:pping.py
#@time:2019/8/6
'''
通过ping实现存活查询
'''
from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import os
import IPy
import gevent
import sys
import time

class Scan(object):
    def __init__(self,host):
        self.host=host
        print('范围:{}'.format(self.host))
        self.djs=[]
        self.xcs=[]
        self.calc=0
        if sys.platform=='win32':
            self.command='ping.exe -n'
            self.pd='ms'
        else:
            self.command='ping -c'
            self.pd='bytes from'

    def scan_range(self,host):
        zx=os.popen('{} 1 {}'.format(self.command,host))
        if self.pd in zx.read():
            print('[+] 存活IP:{}'.format(host))

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.scan_range,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self):
        for host in IPy.IP(self.host):
            if self.calc==100:
                time.sleep(.5)
                p=Process(target=self.xc,args=(self.djs,))
                p.start()
                self.calc=0
                self.djs.clear()

            self.djs.append(str(host))
            self.calc+=1

        if len(self.djs)>0:
            p = Process(target=self.xc, args=(self.djs,))
            p.start()

if __name__ == '__main__':
    try:
        obj=Scan(sys.argv[1])
        obj.djc()
    except Exception as r:
        if 'list index out of range' in str(r):
            print('[!] 需要一个参数 ')