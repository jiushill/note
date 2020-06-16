#@author:jiushi
#@time:2020/6/16
#@file:ipscan.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from scapy.all import srp,Ether,ARP,conf
import asyncio
import socket
import os
import IPy
import platform
import gevent
import optparse
#import threadpool

class Scan(object):
    def __init__(self,ip,port,thread):
        #定义奇奇怪怪的东西
        if platform.system()=="Windows":
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():
                pass
            else:
                print('[-] Please run with The Administrator permission')
                exit()
            self.commandargs='-n'
        elif platform.system()=="Linux":
            if os.getuid()!=0:
                print('[-] Please run with root permission')
                exit()
            self.commandargs='-c'
        self.iplist=ip
        self.portlist=port
        self.processlist=[]
        self.gevnetlist=[]
        self.asynciolist=[]
        self.calc=0
        self.calc2=0
        self.sucess=[] #最终结果
        try:
            self.prochread=thread #并发任务数量满足条件
        except:
            print('[-] Concurrent condition settings are wrong, please enter a number')


    async def _asyncstart(self):
        #异步加速
        for ip in self.iplist:
            if self.calc==self.prochread:
                self._processstart(self.asynciolist)
                self.calc=0
                self.asynciolist.clear()
            self.asynciolist.append(ip)
            self.calc+=1

        if len(self.asynciolist)>0:
            self._processstart(self.asynciolist)
            self.calc = 0
            self.asynciolist.clear()

    def _processstart(self,data):
        #多进程提速
        for d in data:
            if self.calc2==self.prochread:
                p=Process(target=self._geventstart,args=(self.processlist,))
                p.start()
                self.processlist.clear()
                self.calc2=0
            self.processlist.append(d)
            self.calc2+=1

        if len(self.processlist)>0:
            p = Process(target=self._geventstart, args=(self.processlist,))
            p.start()
            self.processlist.clear()
            self.calc2 = 0

    def _geventstart(self,data):
        #协程提速
        for d in data:
            self.gevnetlist.append(gevent.spawn(self.Survive,d))
        gevent.joinall(self.gevnetlist)
        self.gevnetlist.clear()

    def getmac(self,ip):
        try:
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=ip), timeout=2, verbose=False)
        except Exception as e:
            print(str(e))
            return ''
        else:
            for snd, rcv in ans:
                list_mac = rcv.sprintf("%Ether.src%")
                return list_mac

    def portscan(self,data):
        #端口扫描
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((data['ip'], data['port']))
            print('{} {}/open'.format(data['ip'],data['port']))
        except Exception as r:
            pass

    def Survive(self,ip):
        #主操作实现
        print('\r->Current ip:{}    '.format(ip),end='')
        command='ping {} 1 {}'.format(self.commandargs,ip)
        ping=os.popen(command).read()
        if 'ttl' in ping or 'TTL' in ping:
            try:
                netbios=socket.gethostbyaddr(ip)
                computername=netbios[0]
            except:
                computername = ''

            _mac=self.getmac(ip)
            if _mac!='':
                mac=_mac
            else:
                mac=''

            print('\rip:{} computername:{} mac:{}'.format(ip,computername,mac))
            test=[]
            for port in self.portlist:
                test.append(gevent.spawn(self.portscan,{"ip": ip, "port": int(port)}))
            gevent.joinall(test)
            test.clear()
          #  rtx=threadpool.makeRequests(self.portscan,[{"ip":ip,"port":int(port)} for port in self.portlist])
          #  pool=threadpool.ThreadPool(50)
          #  for t in rtx:
          #      pool.putRequest(t)
          #  pool.wait()
           # print('')

if __name__ == '__main__':
    print('''          _  _                  _                           
          ' /' `               /' `\                         
          /'                 /'   ._)                        
        /'  ____            (____    ____     ____     ,____ 
      /'  /'    )--              ) /'    )--/'    )   /'    )
    /'  /'    /'               /'/'       /'    /'  /'    /' 
(,/(_,/(___,/'        (_____,/' (___,/   (___,/(__/'    /(__ 
    /'         -------                                       
  /'                                                         
/'         ''')
    parser=optparse.OptionParser()
    parser.add_option('-i',action='store',dest='iplist',help='setting scan ip')
    parser.add_option('-p',action='store',dest='portlist',help='setting port')
    parser.add_option('-t',action='store',dest='processthread',help='Concurrent condition settings')
    option,args=parser.parse_args()
    if option.iplist and option.portlist and option.processthread:
        try:
            iplist=[str(ip) for ip in IPy.IP(option.iplist,make_net=True)]
        except:
            print('[-] Ip generation failed')
            exit()

        if ',' in option.portlist:
            portlist=str(option.portlist).split(',')
        elif '-' in option.portlist:
            tmp=str(option.portlist).split('-')
            portlist=[x for x in range(int(tmp[0]),int(tmp[1])+1)]
        else:
            print("[-] There's no such format.")
            print('')
            parser.print_help()
            exit()

        obj=Scan(iplist,portlist,option.processthread)
        loop=asyncio.get_event_loop()
        task=loop.create_task(obj._asyncstart())
        loop.run_until_complete(task)
    else:
        parser.print_help()





