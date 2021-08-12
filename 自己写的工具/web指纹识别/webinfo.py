import os
import json
import requests
import queue
import hashlib
import re
import optparse
import warnings
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from multiprocessing import Process
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")
class Webinfo():
    def __init__(self):
        self.rulespath=os.path.join(os.getcwd(),"rules")
        self.rulesexclude=["custom","fofa"] #规则库排除
        self.ruledata=[]
        self.searchconfig=[['regexp'], #ok
                           ["search","text"], #ok
                           ['search', 'regexp'], #ok
      #                     ['md5', 'url'], #ok
      #                     ['url', 'md5'], #ok
       #                    ['url', 'md5', 'model'], #ok
                           ['search', 'regexp', 'offset'], #ok
                           ['status', 'text'], #ok
                           ['name', 'regexp', 'search'], #ok
                           ['name', 'search', 'regexp', 'offset'], #ok
                           ['search', 'regexp', 'name']] #规则过滤配置
        self.response=queue.Queue(maxsize=0)

    def Ruleacquisition(self,mode):
        if mode=="all":
            print(self.rulespath)
            for path in os.walk(self.rulespath):
                if len(path[1])==0:
                    if os.path.basename(path[0]) not in self.rulesexclude:
                        for p in path[-1]:
                            with open(os.path.join(path[0],p),"r",encoding="utf-8") as rd:
                                self.ruledata.append(json.loads(rd.read()))
        else:
            with open(mode, "r", encoding="utf-8") as rd:
                self.ruledata.append(json.loads(rd.read()))

        print("[*] Number of rules:{}".format(len(self.ruledata)))

    def RequestUrlinfo(self,url):
        info={}
        try:
            rqt=requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"},timeout=3,verify=False)
            info["url"]=url
            info["body"]=rqt.text
            info["status"]=rqt.status_code
            info["headers"]=rqt.headers
            info["script"]=BeautifulSoup(rqt.text,"html.parser").find_all("script")
            info["meta"]=BeautifulSoup(rqt.text,"html.parser").find_all("meta")
            info["cookies"]=requests.utils.dict_from_cookiejar(rqt.cookies)
            info["md5"]=hashlib.md5(rqt.content).hexdigest()
            self.response.put(info)
        except Exception as error:
            print("\r   [-] Reuqest url:{} Error:{}".format(url,error),end="")


    def JxInfo(self,httpinfo):
        print(httpinfo["url"])
        pluginlist=[]
        def pluginnameprint(data):
            pluginname = ""
            for key in range(len(list(data.keys()))-1):
                if "matches"!=list(data.keys())[key]:
                    pluginname += "{}:{} ".format(list(data.keys())[key], data[list(data.keys())[key]])
            pluginname = pluginname.rstrip()
            if pluginname not in pluginlist:
                print(pluginname)
            pluginlist.append(pluginname)


        for data in self.ruledata:
            matches = data["matches"]
            if len(matches) > 0:
              #  print(data["name"])
                for m in matches:
                    if data["name"] not in pluginlist:
                        if list(m.keys()) in self.searchconfig:
                            if list(m.keys()) == ['regexp']:
                               if re.search(m["regexp"],httpinfo["body"]) !=None:
                                    pluginnameprint(data)

                            if list(m.keys())==["search","text"]:
                                searchname=m["search"].split("[")
                                if len(searchname)==1:
                                    name=searchname[0]
                                    search=m["text"]
                                    if search in str(httpinfo[name]):
                                        pluginnameprint(data)
                                else:
                                    if searchname[1].rstrip("]") in httpinfo[searchname[0]]:
                                        if httpinfo[searchname[0]][searchname[1].rstrip("]")]==m["text"]:
                                            pluginnameprint(data)

                            if list(m.keys())==['search', 'regexp'] or list(m.keys())==['search', 'regexp', 'name'] or list(m.keys())==['search', 'regexp', 'offset'] or list(m.keys())==['name', 'search', 'regexp', 'offset'] or list(m.keys())==['name', 'regexp', 'search']:
                                searchname = m["search"].split("[")
                                if len(searchname) == 1: #顺便处理了script单个的非script[key]的
                                    if re.search(m["regexp"],httpinfo["body"]) !=None:
                                        pluginnameprint(data)
                                else:
                                    if searchname[0]=="headers" or searchname[0]=="cookies":
                                        if searchname[1].rstrip("]") in httpinfo[searchname[0]]:
                                           if re.search(m["regexp"],str(httpinfo[searchname[0]][searchname[1].rstrip("]")]))!=None:
                                                pluginnameprint(data)


                            if list(m.keys())==['status', 'text']:
                                if m["status"]==httpinfo["status"]:
                                    if m["text"] in httpinfo["body"]:
                                        pluginnameprint(data)

                            if list(m.keys())==['url', 'md5'] or list(m.keys())==['md5', 'url'] or list(m.keys())==['url', 'md5', 'model']:
                                print(data)
                                try:
                                    url="/".join(httpinfo["url"].split("/")[0:3])+"/"+m["url"]
                                    md5=m["md5"]
                                    requestmd5=hashlib.md5(requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"},timeout=3,verify=False).content).hexdigest()
                                    if requestmd5==md5:
                                        pluginnameprint(data)
                                except Exception as error:
                                    pass
        print("")

    def Parsing(self):
        for x in range(self.response.qsize()):
            httpinfo=self.response.get()
            self.JxInfo(httpinfo)

if __name__ == '__main__':
    urllist=open("url.txt","r",encoding="utf-8").read().split("\n")
    numbertasks=30
    tk=Webinfo()

    parser=optparse.OptionParser()
    parser.add_option('-u',dest="url",help="Specify URL")
    parser.add_option('-f',dest="file",help="Specify file")
    parser.add_option('-m',dest="model",help="Mode setting")
    option,args=parser.parse_args()
    if option.url and option.model:
        x = Thread(target=tk.Ruleacquisition, args=(option.model,))
        x.start()
        x.join()

        tk.RequestUrlinfo(option.url)
        tk.Parsing()
    elif option.file and option.model:
        x = Thread(target=tk.Ruleacquisition, args=(option.model,))
        x.start()
        x.join()
        if os.path.exists(option.file):
            with open(option.file,"r",encoding="utf-8") as rf:
                for r in rf.readlines():
                    urllist.append("".join(r.split("\n")))
                    if len(urllist)==numbertasks:
                        with ThreadPoolExecutor() as t:
                            t.map(tk.RequestUrlinfo, urllist)
                        Thread(target=tk.Parsing, args=()).start()
                        urllist=[]
            if len(urllist)!=0:
                with ThreadPoolExecutor() as t:
                    t.map(tk.RequestUrlinfo, urllist)
                Thread(target=tk.Parsing, args=()).start()
                urllist=[]
        else:
            print("[-] File Not Found:{}".format(option.file))

    else:
        print("python webinfo.py -u <url> -m all or python webinfo.py -u <url> -m <path>")
        print("python webinfo.py -f <file> -m all or python webinfo.py -f <file> -m <path>")
        parser.print_help()