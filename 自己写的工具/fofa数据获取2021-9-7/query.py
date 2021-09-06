import requests
import base64
import config
import os
import queue
import time
from multiprocessing import Pool
from bs4 import BeautifulSoup

def run(urlist):
    fofa = FofaQuery()
    P=Pool(maxtasksperchild=config.process)
    P.map(fofa.Getdata,urlist)

class FofaQuery(object):
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                      "Cookie":config.cookie}

    def Parse(self,data):
        html=BeautifulSoup(data,"html.parser")
        urllist=[str(url.get_text()) for url in html.find_all("span",class_="aSpan")]
        contentLeft=[str(c.get_text()) for c in html.find_all("div",class_="contentLeft")]
        for x in range(0,len(urllist)):
            jg="{} {}".format(urllist[x],contentLeft[x].replace("\n","").replace("\r","").rstrip().lstrip())
            print(jg)
            print(jg,file=open(config.filename,"a",encoding="utf-8"))

    def Getdata(self,url):
        while True:
            rqt=requests.get(url=url,headers=self.headers)
            if rqt.status_code==503:
                time.sleep(5)
            else:
                self.Parse(rqt.text)
                #print(rqt.text)
                break

if __name__ == '__main__':
    if os.path.exists("config.py"):
        print("[+] 读取配置文件")
    else:
        print("[-] 配置文件不存在")
        exit()

    print("======[Fofa info Query]======")
    url = config.url
    cookie = config.cookie
    search = base64.b64encode(config.search.encode()).decode()
    urllist = queue.Queue(maxsize=config.max)
    print("Search:{}".format(config.search))
    print("Page:{}".format(config.page))
    try:
        page = config.page
    except Exception as err:
        print("[-] 页面设置非整数，默认设置为5页")
        page = 5

    for page in range(0, page):
        url_ = str(url).format(search=search, page=page + 1)
        urllist.put(url_)
        if urllist.qsize() == config.max:
            urlist = [urllist.get() for k in range(urllist.qsize())]
            run(urlist)
    if urllist.qsize() != 0:
        urlist = [urllist.get() for k in range(urllist.qsize())]
        run(urlist)