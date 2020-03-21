#@author:九世
#@file:webshell_scan.py
#@time:2020/3/21

from gevent import monkey;monkey.patch_all()
from colorama import init,Fore
import gevent
from multiprocessing import Process
import asyncio
import requests
import os
import optparse
import warnings
warnings.filterwarnings("ignore")

init(wrap=True)

class Scan(object):
    def __init__(self):
        self.djcs=[]
        self.xcs=[]
        self.ybs=[]
        self.calc=0
        self.calc2=0
        self.url="https://webshellchop.chaitin.cn"
        self.thread=100
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarye7y6B4Fd4BNTlV6j",
        "Referer": "https://webshellchop.chaitin.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"}
        self.timeout=10
        self.data="""------WebKitFormBoundarye7y6B4Fd4BNTlV6j\r\nContent-Disposition: form-data; name="inputfile"; filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n{data}\r\n------WebKitFormBoundarye7y6B4Fd4BNTlV6j\r\nContent-Disposition: form-data; name="fileId"\r\n\r\n837_{name}\r\n------WebKitFormBoundarye7y6B4Fd4BNTlV6j\r\nContent-Disposition: form-data; name="initialPreview"\r\n\r\n[]\r\n------WebKitFormBoundarye7y6B4Fd4BNTlV6j\r\nContent-Disposition: form-data; name="initialPreviewConfig"\r\n\r\n[]\r\n------WebKitFormBoundarye7y6B4Fd4BNTlV6j\r\nContent-Disposition: form-data; name="initialPreviewThumbTags"\r\n\r\n[]\r\n------WebKitFormBoundarye7y6B4Fd4BNTlV6j--"""
        parser=optparse.OptionParser()
        parser.add_option('-i',dest='id',help='id为0为单个文件上传，id为1将整个文件夹的文件进行上传')
        parser.add_option('-f',dest='path',help='文件路径')
        parser.add_option('-a',dest='hou',help='后缀定义，满足定义的后缀才上传检测')
        (option,args)=parser.parse_args()
        if option.id=="0" and option.path:
            self.level=0
            if os.path.exists(option.path):
                path=option.path
                self.upload(path)
            else:
                print('[-] 文件:{}不存在'.format(option.path))
        elif option.id=="1" and option.path and option.hou:
            self.level=1
            path=option.path
            self.hou=option.hou
            loop=asyncio.get_event_loop()
            tk=loop.create_task(self.pilang(path))
            loop.run_until_complete(tk)
        else:
            parser.print_help()
            print('单个 检测:python webshell_scan.py -i 0 -f /var/www/html/zzh.php')
            print('批量检测:python webshell_scan.py -i 1 -f /var/www/ -a php,asp,jsp')

    def upload(self,filename):
        if self.level==1:
            filenames=filename.split('.')
            if filenames[-1] in self.hou:
                filename=filename
            else:
                filename=""

        if filename!="":
            color = Fore.WHITE
            wx = "+"
            try:
                rqt = requests.post(url=self.url, headers=self.headers,
                                    data=self.data.format(name=filename, data=open(filename, 'r', encoding='utf-8').read()),
                                    timeout=self.timeout, verify=False)
                jsons = rqt.json()
                level = jsons["data"]["level"]
                types = jsons["data"]["type"]
                if level > 3:
                    wx = "危险!"
                    color = Fore.RED
                elif level == 3:
                    wx = "危险"
                    color = Fore.RED
                elif level < 3 and level != 0:
                    wx = "可疑"
                    color = Fore.YELLOW
                elif level == 0:
                    wx = "安全"
                    color = Fore.GREEN
                print(color + '[{}] 文件名:{} 文件类型:{} 等级:{}'.format(wx, filename, types, level) + Fore.WHITE)
                if level >= 3:
                    print('=' * 30 + "[{}]".format(filename) + '=' * 30)
                    dks = open(filename, 'r')
                    for j in dks.readlines():
                        dc = "".join(j.split('\n'))
                        print(dc)
                    print('')
            except Exception as Error:
                print('[-] Error:{}'.format(Error), file=open('error.log', 'a', encoding='utf-8'))

    def xc(self,rw):
        for r in rw:
            self.xcs.append(gevent.spawn(self.upload,r))
        gevent.joinall(self.xcs)
        self.xcs=[]

    def djc(self):
        for r in self.ybs:
            if self.calc2==self.thread:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc2=0
                self.djcs=[]
            self.djcs.append(r)
            self.calc2+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()
            self.calc2 = 0
            self.djcs = []

    async def pilang(self,filename):
        paths=os.walk(filename)
        for p in paths:
            if self.calc == self.thread:
                self.djc()
                self.calc = 0
                self.ybs=[]
            try:
                for j in p[-1]:
                    pth = "{}\\{}".format(p[0], j)
                    self.ybs.append(pth)
                    self.calc+=1
            except:
                pass

        if len(self.ybs)>0:
            self.djc()
            self.calc = 0
            self.ybs=[]

if __name__ == '__main__':
    print(Fore.GREEN+'长亭webshell上传检测'+Fore.WHITE)
    obj=Scan()