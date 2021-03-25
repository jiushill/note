import requests
import config
import re
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

conf = config.REQUEST_CONF
headers = conf["REQUEST_HEADER"]
timeout = conf["TIMEOUT"]
downloadmodule=config.DOWNLOAD_MODULE

def Discharge(text,domainurl):
    #分离js、css、img下载到本地
    urlformat=urlparse(domainurl)
    domain=urlformat.scheme+"://"+urlformat.netloc
    text=BeautifulSoup(text,"html.parser")
    title=text.find_all("title")
    link =text.find_all("link",attrs={"href":re.compile(".*")})
    script=text.find_all("script",attrs={"src":re.compile(".*")})
    img=text.find_all("img",attrs={"src":re.compile(".*")})
    downloadlist=[]
    if (len(title)>0):
        title=title[0].text
    else:
        title="{}_titme_:{}".format(urlformat.netloc,int(title.time())) #title找不到的时候使用:域名+时间戳作为文件名
    title=title.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace('"',"_").replace("(","_").replace(")","_").replace("<","_").replace(">","_").replace("|","_").replace("'","").replace(" ","").lstrip().rstrip()
    folderpath="save/{}".format(title) #保存html的根路径
    staticfolderpath="{}/assert".format(folderpath) #静态路径
    print("mkdir folder:{}".format(folderpath))
    print("mkdir static folder:{}".format(staticfolderpath))
    os.mkdir(folderpath)
    os.mkdir(staticfolderpath)

    #lnk标签静态路径替换
    if (len(link)>0):
        for url in link:
            hreffroamt=urlparse(url['href'])
            if(len(hreffroamt.scheme)==0): #判断是否存在http/https头如果没有的话代表是域名路径下的相反是别站的
                href=domain+url['href']
            else:
                href=url['href']
            includepath="assert/{}".format(href.split("/")[-1]) #html里的引用本地静态路径
            savepath="{}/{}".format(staticfolderpath,href.split("/")[-1])
            url['href']=includepath #替换html原来的路径
            downloadlist.append([href,savepath])

    #script标签静态替换
    if (len(script)>0):
        for url in script:
            srcformat=urlparse(url['src'])
            if (len(srcformat.scheme)==0):
                src=domain+url['src']
            else:
                src=url['src']

            suffix=src.split(".")
            if (len(suffix)>0 and suffix[-1]=="js"):
                includepath = "assert/{}".format(src.split("/")[-1])
                savepath="{}/{}".format(staticfolderpath,src.split("/")[-1])
                url['src']=includepath
                downloadlist.append([src,savepath])
    #img标签静态替换
    if (len(img)>0):
        for url in img:
            imgformat=urlparse(url['src'])
            if(len(imgformat.scheme) == 0):
                src = domain + url['src']
            else:
                src = url['src']

            includepath = "assert/{}".format(src.split("/")[-1])
            savepath="{}/{}".format(staticfolderpath,src.split("/")[-1])
            url['src']=includepath
            downloadlist.append([src,savepath])

    htmlpath="{}/{}.html".format(folderpath,title)
    print("save filepath:{}".format(htmlpath))
    print(text,file=open(htmlpath,"a",encoding="utf-8")) #保存html

    if(downloadmodule==0): #单线程
        for d in downloadlist:
            downloadfile(d[0],d[1])
    elif(downloadmodule==1): #多进程
        tmp=[]
        for x in downloadlist:
            tmp.append([x[0],x[1]])
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=config.PROCESS) as process:
            process.map(downloadfile,tmp,chunksize=1)

def downloadfile(*args,**kwargs):
    if(isinstance(args[0],list)==False):
        url=args[0]
        savepath=args[1]
    else: #多进程取参数的方法
        url = args[0][0]
        savepath = args[0][1]
    print("save filepath:{}".format(savepath))
    try:
        rqt=requests.get(url=url,headers=headers,timeout=timeout)
        dk=open(savepath,"wb")
        dk.write(rqt.content)
        dk.close()
    except Exception as error:
        print("Request Url:{} Error:{}".format(url,error))

def download(url):
    try:
        r=requests.get(url=url,headers=headers,timeout=timeout)
        Discharge(r.text,r.url)
    except Exception as Error:
        print("Request Url:{} Error:{}".format(url,Error))