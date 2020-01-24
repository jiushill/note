#@author:九世
#@time:2020/1/23
#@file:query.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import gevent
import asyncio
import censys.ipv4
import censys.data
import censys.certificates
import censys
import optparse
import os

class Censys_search(object):
    def __init__(self):
        self.calc=0
        self.calc2=0
        self.xcs=[]
        self.djcs=[]
        self.ybs=[]
        args=optparse.OptionParser()
        args.add_option('-a',dest='api',help="This is Censys API ID")
        args.add_option('-s',dest='api_secret',help='This is api_secret')
        args.add_option('-d',dest='data',help='Search content')
        args.add_option('-f',dest='file',help='Bulk search')
        args.add_option('-m',action='store_true',dest='domain',help='domain query')
        (option,argss)=args.parse_args()
        if option.api and option.api_secret and option.data and option.domain:
            self.api=option.api
            self.api_secret=option.api_secret
            self.data=option.data
            self.load()
            self.IPV4SEARCH(self.data)
        elif option.api and option.api_secret and option.file and option.domain:
            self.api=option.api
            self.api_secret=option.api_secret
            self.data=option.file
            self.load()
            loop=asyncio.get_event_loop()
            tk=loop.create_task(self.readfiles(self.data))
            loop.run_until_complete(tk)
        else:
            args.print_help()
            exit()

    def load(self):
        try:
            self.c = censys.certificates.CensysCertificates(api_id=self.api, api_secret=self.api_secret)
            print('[+] API validation successful')
        except Exception as r:
            if 'HTTPSConnectionPool' in str(r):
                print('[-] Cesys connection timed out')
            else:
                print('[-] API validation failed')
            exit()

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.IPV4SEARCH,r))
        gevent.joinall(self.xcs)
        self.xcs.clear()


    def djc(self):
        for j in self.ybs:
            if self.calc2==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc2=0
                self.djcs.clear()
                p.join()
            self.djcs.append(j)
            self.calc2+=1
        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc2 = 0
            self.djcs.clear()
            p.join()

    async def readfiles(self, filename):
        if os.path.exists(filename):
            dk = open(filename, 'r', encoding='utf-8')
            for y in dk.readlines():
                if self.calc == 100:
                    self.djc()
                    self.calc = 0
                    self.ybs.clear()
                data = "".join(y.split('\n'))
                self.ybs.append(data)
                self.calc += 1
            if len(self.ybs) > 0:
                self.djc()
                self.calc = 0
                self.ybs.clear()
        else:
            print('[-] file does not exist')
            exit()

    def IPV4SEARCH(self,data):
        print('[+] Searched Domain:{}'.format(data))
        self.searcs='parsed.names: {}'.format(data)
        crs=self.c.search(self.searcs,fields=['parsed.names'])
        try:
            for r in crs:
                if 'parsed.names' in [x for x in r]:
                    for jg in r['parsed.names']:
                        print(jg)
                        print(jg,file=open('{}.txt'.format(data),'a',encoding='utf-8'))

        except Exception as r:
            print('[-] Error:{}'.format(r))

if __name__ == '__main__':
    obj=Censys_search()