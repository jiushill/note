#@author:九世
#@time:2019/9/1
#@file:scan.py
'''
端口扫描器
'''

from gevent import monkey;monkey.patch_all()
import gevent
import IPy
import time
import socket
import chardet
import re
from multiprocessing import Process

class Port_scan(object):
    def __init__(self):
        self.port='1-1000' #Port range
        self.host='192.168.3.94' #IP settings
        self.process_calc=100 #Threads start a process to a certain extent
        self.sleep=2 #Jinc delay settings
        self.calc=0
        self.djcs=[]
        self.xcs=[]
        self.timeout=3 #Socket timeout settings

    def scan(self,port):
        try:
            with socket.socket() as s:
                s.settimeout(self.timeout)
                s.connect((self.host,port))
                s.sendall(b'banner')
                recvs = s.recv(1024)
                jm=chardet.detect(recvs)
                if jm['encoding']==None:
                    banner=recvs
                else:
                    banner=recvs.decode(jm['encoding'])

                print('[+] port:{}/open banner:{}'.format(port, banner))
        except:
            pass

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.scan,x)) for x in rw]
        gevent.joinall(self.xcs)

    def djc(self):
        fg=re.findall('[0-9]{1,}',self.port)
        for x in range(int(fg[0]),int(fg[1])):
            if self.calc==self.process_calc:
                time.sleep(self.sleep)
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()
            self.djcs.append(x)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()

if __name__ == '__main__':
    obj=Port_scan()
    obj.djc()