#@author:九世
#@time:2020/4/25
#@file:fuzz.py

from gevent import monkey;monkey.patch_all()
from multiprocessing import Process
from colorama import Fore,init
import asyncio,os,config,chardet,aiohttp

init(wrap=True,autoreset=True)
class Fuzz(object):
    def __init__(self,filename):
        self.pathlist=[] #file path list
        self.onelist=[] #Association
        self.twolist=[] #Multiprocess
        self.calc=0 #Coroutine counter
        self.calc2=0 #Multiprocess counter
        self.threelist=[] #Aiohttp preparation
        self.timeout=3 #aiohttp Timeout settings
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}
        if os.path.exists(filename):
            if os.path.isdir(filename):
                dirs=os.walk(filename)
                for path in dirs:
                    for dir in path[-1]:
                        name='{}/{}'.format(path[0],dir).split('.')
                        if name[-1] in config.whitelist:
                            self.pathlist.append(".".join(name))
            else:
                self.pathlist.append(filename)
        else:
            print(Fore.RED+'Error:not found file')
            exit()

        print(Fore.YELLOW+"Number of dictionaries:{}".format(len(self.pathlist)))
        loop=asyncio.get_event_loop()
        tk=loop.create_task(self.one())
        loop.run_until_complete(tk)

    async def one(self):
        for file in self.pathlist:
            if os.path.isfile(file):
                with open(file, 'r', encoding="utf-8") as openfile:
                    for r in openfile.readlines():
                        if self.calc == config.process:
                            self.two()
                            self.onelist.clear()
                            self.calc = 0
                        data = "".join(r.split('\n'))
                        self.onelist.append(data)
                        self.calc += 1

            elif os.path.isdir(file):
                if config.fileenc==True:
                    enc=chardet.detect(open(file,'rb').read())
                    if enc['encoding'] !="":
                        encode=enc["encoding"]
                    else:
                        encode="utf-8"
                else:
                    encode="utf-8"
                with open(file,'r',encoding=encode) as openfile:
                    for r in openfile.readlines():
                        if self.calc==config.process:
                            self.two()
                            self.onelist.clear()
                            self.calc=0
                        data="".join(r.split('\n'))
                        self.onelist.append(data)
                        self.calc+=1

            if len(self.onelist) > 0:
                self.two()
                self.onelist.clear()
                self.calc = 0


    def two(self):
        for data in self.onelist:
            if self.calc2==config.process:
                p=Process(target=self.three,args=(self.twolist,))
                p.start()
                self.calc2=0
                self.twolist.clear()
            self.twolist.append(data)
            self.calc2+=1

        if len(self.twolist)>0:
            p = Process(target=self.three, args=(self.twolist,))
            p.start()
            self.calc2 = 0
            self.twolist.clear()

    def three(self,payloads):
        for pay in payloads:
            payload=str(config.url).replace('FUZZ',pay)
            self.threelist.append(self.fuzzing(payload))

        event_loop=asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(*self.threelist))

    async def fuzzing(self,url):
        color=""
        word=""
        async  with aiohttp.ClientSession() as requests:
            async with requests.get(url=url,headers=self.headers,timeout=self.timeout) as Response:
                if Response.status==config.blacklist["code"]:
                    color+=Fore.RED

                if len(config.blacklist["word"])>0:
                    for words in config.blacklist["word"]:
                        if words in await Response.text():
                            color += Fore.RED
                            word+="{}".format(words)
                            break

                print(color+"Result url:{} code:{} word:{}".format(Response.url,Response.status,word))
                if color==Fore.RED:
                    print(color + "Result url:{} code:{} word:{}".format(Response.url, Response.status, word),file=open('result/blacklist.txt','a',encoding='utf-8'))
                else:
                    print(color + "Result url:{} code:{} word:{}".format(Response.url, Response.status, word),file=open('result/fuzz.txt', 'a',encoding='utf-8'))

if __name__ == '__main__':
    obj=Fuzz(config.path)