from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import os
import time
import re
import sqlite3

max_workers=10
timeout=60
sleeptime=1
number={}
sougousearchurl="https://weixin.sogou.com/weixin?type=1&query={}&ie=utf8"

def readconfig():
    if os.path.exists("number.txt"):
        print("[+] Read number")
        with open("number.txt","r",encoding="utf-8") as rfile:
            for r in rfile.readlines():
                data="".join(r.split("\n")).split("-")
                if len(data)>2:
                    tp=["-"+j for j in data[1:-1]]
                    number[data[0]+"".join(tp)]=data[-1]
                else:
                    number[data[0]]=data[-1]
    else:
        print("[-] number.txt not found")
        exit()

def db(title,url,times,numbername):
    conn = sqlite3.connect("data.db")
    c=conn.cursor()
    pd=c.execute("select title,url from WX where title=\"{}\"".format(title))
    tk=[k[0] for k in pd]
    if len(tk)==0:
        try:
            c.execute("insert into WX(title,url,time,numbername) VALUES (\"{}\",\"{}\",\"{}\",\"{}\")".format(title,url,str(times),numbername))
            conn.commit()
            print("INSERT OK :{}".format(title,url,times))
        except Exception as Error:
            print("[-] SQL INSERT Error {}".format(Error))
            print("[-] SQL INSERT Error {}".format(Error),file=open("log.txt","a",encoding="utf-8"))
    else:
        print("数据已存在") #测试使用

def getcookie():
    #从搜狗视频获取cookie，防止傻逼搜狗机制检测
    url = 'https://v.sogou.com/v?ie=utf8&query=&p=40030600'
    headers = {'User-Agent': UserAgent().random}
    rst = requests.get(url=url,headers=headers,allow_redirects=False)
    cookies = rst.cookies.get_dict()
    return cookies


def getdata(*args,**kwargs):
    number,name=args
    cookie=getcookie()
    print("正在抓取:{}-{}".format(name,number))
    headers={"User-Agent": UserAgent().random}
    session=requests.session()
    rqt=session.get(url=sougousearchurl.format(number),headers=headers,timeout=timeout,cookies=cookie)
    lnk=BeautifulSoup(rqt.content.decode('utf-8'),"html.parser").find_all("a",uigs="account_article_0")
    if len(lnk)>0:
        url=lnk[0]['href']
        title=lnk[0].get_text()
        jumpurl="https://weixin.sogou.com/{}".format(url.lstrip('/'))
    #    headers["X-Requested-With"]="XMLHttpRequest"
   #     uuid=str(re.findall("uuid = \".*\"",rqt.text)[0]).split('"')[1]
   #     token=str(re.findall("ssToken = \".*\"",rqt.text)).split('"')[1]
   #     data="uuid={}&token={}&from=outer&channel=result_account".format(uuid,token)
        wexin=session.get(url=jumpurl,headers=headers,cookies=cookie)
        urlx=re.findall("url.*",wexin.text)
        wxurl=""
        for k in range(1,len(urlx)):
            space=urlx[k].split("'")
            if len(space)>1:
                wxurl+=space[1]
        db(title,wxurl,int(time.time()),name)

    else:
        print("[-] 傻逼验证码,验证码:{}".format(rqt.url))

class Main():
    def __init__(self):
        for x in number:
            getdata(x,number[x])

if __name__ == '__main__':
    readconfig()
    while True:
        Main()
        print("休眠5分钟后继续") #测试
        time.sleep(360)
