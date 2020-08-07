from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from bs4 import BeautifulSoup
import asyncio
import requests
import re
import os
import sys
import gevent
import config

class GetHttpInfo(object):
    def __init__(self,file,process,reg):
        self.reg=reg
        self.calc=0
        self.calc2=0
        self.process_=process
        self.rf=[]
        self.processs=[]
        self.geven_=[]
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
        paths=set()
        if sys.platform=="win32":
            path_s="\\"
        else:
            path_s="/"
        for path in os.walk(file):
            for name in path[-1]:
                p="{}{}{}".format(path[0],path_s,name)
                paths.add(p)


        loop=asyncio.get_event_loop()
        tk=loop.create_task(self.getdomain(paths))
        loop.run_until_complete(tk)

    async def getdomain(self,filedict):
        for file in filedict:
            with open(file,"r",encoding="utf-8") as rfile:
                for f in rfile:
                    if self.reg==True:
                        domain=re.findall("domain:.*?\s",f.rstrip())
                        if len(domain)>0:
                            domain=str(domain[0]).rstrip().replace("domain:","")
                            if self.calc==self.process_:
                                p=Process(target=self.proc,args=(self.rf,))
                                p.start()
                                self.rf=[]
                                self.calc=0
                            self.rf.append(domain)
                            self.calc+=1
                    else:
                        if self.calc == self.process_:
                            p = Process(target=self.proc, args=(self.rf,))
                            p.start()
                            self.rf = []
                            self.calc = 0
                        self.rf.append(f)
                        self.calc += 1

        if len(self.rf)>0:
            p = Process(target=self.proc, args=(self.rf,))
            p.start()
            self.rf = []
            self.calc = 0

    def proc(self,data):
        for d in data:
            if self.calc2==self.process_:
                p=Process(target=self.genvt,args=(self.processs,))
                p.start()
                self.calc2=0
                self.processs=[]
            self.processs.append(d)
            self.calc2+=1

        if len(self.processs)>0:
            p = Process(target=self.genvt, args=(self.processs,))
            p.start()
            self.calc2 = 0
            self.processs = []

    def genvt(self,data):
        for d in data:
            self.geven_.append(gevent.spawn(self.gethttpinfo,d))
        gevent.joinall(self.geven_)
        self.geven_=[]

    def getresponse(self,rqt):
        title = BeautifulSoup(rqt.content.decode('utf-8'), "html.parser").find_all("title")
        resposneheaders = rqt.headers
        tmp = [x for x in resposneheaders]
        if "Server" in tmp:
            server = resposneheaders["Server"]
        else:
            server = ""

        if "X-Powered-By" in tmp:
            xby = resposneheaders["X-Powered-By"]
        else:
            xby = ""

        if len(title) > 0:
            title = str(title[0].get_text()).rstrip().lstrip().replace("\n", "")
        else:
            title = ""

        datas = {"title": title, "server": server, "x-powered-by": xby}
        return datas


    def gethttpinfo(self,domain):
        data = {"domain": "", "port": [], "ssl": False, "title": "", "ssltitle": "", "httpinfo": []}
        url = "http://{}".format(domain)
        url2 = "https://{}".format(domain)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
        try:
            rqt = requests.get(url=url, headers=headers, timeout=3)
            response = self.getresponse(rqt)
            if rqt != False:
                data["domain"] = domain
                data["port"].append("80")
                data["title"] = response["title"]
                data["httpinfo"].append(response["server"])
                data["httpinfo"].append(response["x-powered-by"])

            rqt2 = requests.get(url=url2, headers=headers, timeout=3)
            response = self.getresponse(rqt2)
            if rqt2 != False:
                data["ssl"] = True
                data["port"].append("443")
                data["ssltitle"] = response["title"]
                data["httpinfo"].append(response["server"])
                data["httpinfo"].append(response["x-powered-by"])

        except:
            pass

        print("domain:{} title:{} ssl:{} ssltitle:{} httpinfo:{} port:{}".format(data["domain"], data["title"],data["ssl"], data["ssltitle"],",".join(list(set(data["httpinfo"]))),",".join(data["port"])))
        print("domain:{} title:{} ssl:{} ssltitle:{} httpinfo:{} port:{}".format(data["domain"], data["title"],data["ssl"], data["ssltitle"],",".join(list(set(data["httpinfo"]))),",".join(data["port"])),file=open("save.txt","a",encoding="utf-8"))


if __name__ == '__main__':
    obj=GetHttpInfo(config.domainpath,config.process2,config.reg)
