#@author:九世
#@time:2019/10/24
#@file:port_scanner.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import init,Fore
import gevent
import time
import socket
import IPy
import asyncio
import sys



init(wrap=True)

try:
    tar=sys.argv[1]
    tar2=sys.argv[2]
except:
    sys.exit(Fore.YELLOW+'[!] '+Fore.WHITE+'python port_scanner.py [IP/MASK] [port_range(例如:80,443,3306,445或80或1-65535)]')

class Port_scanners(object):
    def __init__(self):
        self.open_port=[] #开放的端口
        self.djcs=[]
        self.xcs=[]
        self.yb=[]
        self.calc=0
        self.n=0


    async def create_ips(self, host,rang):
        if '-' in rang:
            da=str(rang).split('-')
            start=da[0]
            stop=da[1]

            for ips in IPy.IP(host):
                for port in range(int(start), int(stop)): #设置端口扫描范围
                    data = '{}:{}'.format(ips, port)
                    if self.n==100:
                        self.djc()
                        self.n=0
                        self.yb.clear()

                    self.yb.append(data)
                    self.n+=1

        elif ',' in rang:
            da=str(rang).split(',') #分割要是扫描的端口
            for ips in IPy.IP(host):
                for port in da:
                    data = '{}:{}'.format(ips, port)
                    if self.n==100:
                        self.djc()
                        self.n=0
                        self.yb.clear()

                    self.yb.append(data)
                    self.n+=1

        else:
            for ips in IPy.IP(host):
                data = '{}:{}'.format(ips, rang) #拼接要扫描的端口
                if self.n == 100:
                    self.djc()
                    self.n = 0
                    self.yb.clear()

                self.yb.append(data)
                self.n += 1

    def stop_ap(self):
        if len(self.yb)>0:
            self.djc()

    def port_scan(self,host,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((str(host), int(port)))
            print(Fore.BLUE + '[+] ' + Fore.WHITE + '{}:{}/open'.format(host,port))
            print('{}:{}'.format(host,port),file=open('save.txt','a',encoding='utf-8'))
        except Exception as r:
            pass

    def xc(self,rw):
        for y in rw:
            data = str(y).split(':')
            host = data[0]
            port = data[1]
            self.xcs.append(gevent.spawn(self.port_scan,host,port))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        for u in self.yb:
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()

            time.sleep(0.01)
            self.djcs.append(u)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc=0
            self.djcs.clear()




if __name__ == '__main__':
    obj=Port_scanners()
    loop=asyncio.get_event_loop()
    tg=loop.create_task(obj.create_ips(tar,tar2))
    loop.run_until_complete(tg)
    obj.stop_ap()