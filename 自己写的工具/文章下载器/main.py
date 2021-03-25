#@author:Jiushi
#@time:2021/3/25
#@filename:main.py
import os
import config
from plugin import download
from concurrent.futures import ProcessPoolExecutor

class Download(object):
    def __init__(self,mode):
        pass

    def fileopendownload(self):
        filepath=input("filepath:")
        if (os.path.exists(filepath)):
            filepath=filepath
        else:
            print("[-] Not Found Filepath:{}...".format(filepath))
            exit()

        print("read file...")
        fdata=open(filepath,"r",encoding="utf-8").read().split("\n")
        print("Number of tasks:{}".format(len(fdata)))
        with ProcessPoolExecutor(max_workers=config.PROCESS) as process:
            process.map(download.download,fdata,chunksize=1)

    def customize(self):
        #预留函数调用处
        func=config.RESERVE
        urllist=func("https://xz.aliyun.com/?page=2") #返回要被爬取的url列表
        print("urllist tasks:{}".format(len(urllist)))
        with ProcessPoolExecutor(max_workers=config.PROCESS) as process:
            process.map(download.download, urllist, chunksize=1)

if __name__ == '__main__':
    MODE_FUNCTION = {"1": Download.fileopendownload,"2":Download.customize}  # MODE对应函数名
    for k in config.MODE:
        print("{}:{}".format(k,config.MODE[k]))
    user=input("Mode>")
    if(user in MODE_FUNCTION):
        MODE_FUNCTION[user](0)
    else:
        print("[-] Not Found Module")