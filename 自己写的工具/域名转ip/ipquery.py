from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import asyncio
import gevent
import socket
import gevent
import sys

class ipquery(object):
    def __init__(self):
        self.process=500
        self.dicts=[]
        self.processruns=[]
        self.gevents=[]
        self.calc=0
        self.calc2=0

    async def readfile(self,file):
        with open(file,"r",encoding="utf-8") as rf:
            for data in rf:
                if self.calc==self.process:
                    p=Process(target=self.process_run,args=(self.dicts,))
                    p.start()
                    self.calc=0
                    self.dicts=[]
                self.calc+=1
                self.dicts.append(data.rstrip())

            if len(self.dicts)>0:
                p = Process(target=self.process_run, args=(self.dicts,))
                p.start()
                self.calc = 0
                self.dicts = []

    def process_run(self,data):
        for p in data:
            if self.calc2==self.process:
                p=Process(target=self.gevent_run,args=(self.processruns,))
                p.start()
                self.calc2=0
                self.processruns.clear()
            self.processruns.append(p)
            self.calc2+=1

        if len(self.processruns)>0:
            p = Process(target=self.gevent_run, args=(self.processruns,))
            p.start()
            self.calc2 = 0
            self.processruns.clear()

    def gevent_run(self,data):
        for d in data:
            self.gevents.append(gevent.spawn(self.test,d))
        gevent.joinall(self.gevents)
        self.gevents=[]

    def test(self,domain):
        try:
            socket.setdefaulttimeout(3)
            addrs=socket.getaddrinfo(domain,None)
            ip=addrs[0][4][0]
            data="domain:{} ip:{}".format(domain,ip)
            print(data)
            print(data,file=open("data.txt","a",encoding="utf-8"))
            print(ip,file=open("iplist.txt","a",encoding="utf-8"))
        except:
            pass

if __name__ == '__main__':
    obj=ipquery()
    loop=asyncio.get_event_loop()
    if len(sys.argv)>1:
        tk=loop.create_task(obj.readfile(sys.argv[1]))
        loop.run_until_complete(tk)
    else:
        print('[=] python ipquery.py <domain.txt>')