#@author:九世
#@time:2020/1/24
#@file:jx.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import gevent
import asyncio
import socket
import ssl
import IPy
import os
import optparse

banner=r''' .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |    _______   | || |    _______   | || |   _____      | |
| |   /  ___  |  | || |   /  ___  |  | || |  |_   _|     | |
| |  |  (__ \_|  | || |  |  (__ \_|  | || |    | |       | |
| |   '.___`-.   | || |   '.___`-.   | || |    | |   _   | |
| |  |`\____) |  | || |  |`\____) |  | || |   _| |__/ |  | |
| |  |_______.'  | || |  |_______.'  | || |  |________|  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' '''

class SSLjk(object):
    def __init__(self):
        self.djcs=[]
        self.xcs=[]
        self.ybs=[]
        self.calc=0
        self.calc2=0

        self.help='\npython jx.py -f [file] -t [thread]\npython jx.py -d [data]\npython jx.py -i 192.168.1.0/24 -t [thread]\n--------------------------'
        parser=optparse.OptionParser(self.help)
        parser.add_option('-f',dest='domain_file',help='Domain file')
        parser.add_option('-d',dest='data',help='domain')
        parser.add_option('-i',dest='ip',help='IP range')
        parser.add_option('-t',dest='thread',help='Thread settings')
        (option,args)=parser.parse_args()
        print(banner)
        if option.data:
            self.sslconnect(option.data)
        elif option.domain_file and option.thread:
            self.thread=option.thread
            self.id=0
            loop=asyncio.get_event_loop()
            tk=loop.create_task(self.plquery(option.domain_file))
            loop.run_until_complete(tk)
        elif option.ip and option.thread:
            self.thread = option.thread
            self.id=1
            loop = asyncio.get_event_loop()
            tk = loop.create_task(self.plquery(option.ip))
            loop.run_until_complete(tk)
        else:
            parser.print_help()
            exit()

    def yb(self,rw):
        for k in rw:
            self.xcs.append(gevent.spawn(self.sslconnect,k))
        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        for p in self.ybs:
            if self.calc2==self.thread:
                p=Process(target=self.yb,args=(self.djcs,))
                p.start()
                self.djcs.clear()
                self.calc2=0
                p.join()
            self.djcs.append(p)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.yb, args=(self.djcs,))
            p.start()
            self.djcs.clear()
            self.calc2 = 0
            p.join()

    async def plquery(self,file):
        if self.id!=1:
            if os.path.exists(file):
                dk=open(file,'r',encoding='utf-8')
                for r in dk.readlines():
                    if self.calc == self.thread:
                        self.djc()
                        self.calc = 0
                        self.ybs.clear()
                    data = "".join(r.split('\n'))
                    self.ybs.append(data)
                    self.calc += 1
            else:
                print('[-] The file does not exist:{}'.format(file))
                exit()
        else:
            try:
                dk=IPy.IP(file)
                for r in dk:
                    if self.calc == self.thread:
                        self.djc()
                        self.calc = 0
                        self.ybs.clear()
                    self.ybs.append(r)
                    self.calc += 1
            except:
                pass

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs.clear()

    def sslconnect(self,hostname):
        hostname=str(hostname).rstrip().lstrip()
        try:
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
            s.settimeout(5)
            s.connect((hostname, 443))
            certs = s.getpeercert()['subjectAltName']
            print('-------- Parsing:{} --------'.format(hostname))
            for c in certs:
                print(c[1])
                print(c[1],file=open('{}.txt'.format(hostname),'a',encoding='utf-8'))
        except Exception as r:
            pass
if __name__ == '__main__':
    obj=SSLjk()