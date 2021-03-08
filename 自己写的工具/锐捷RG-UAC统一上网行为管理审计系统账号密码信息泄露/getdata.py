from concurrent.futures import ProcessPoolExecutor
import requests
import os
import optparse
import re
import warnings
import multiprocessing

warnings.filterwarnings("ignore")

class getdata(object):
    def __init__(self):
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        self.timeout=3
        self.thread=50

    def searchdata(self,url):
        if len(url)==0:
            return 0
        rqt=requests.get(url=url,headers=self.headers,timeout=self.timeout,verify=False)
        search=re.findall("\[.*\]",rqt.text)
        if(len(search)>0):
            print("发现泄露,url:{}".format(url))
            print("发现泄露,url:{}".format(url),file=open("save.txt","a",encoding="utf-8"))
            data=search[0]
            names=re.findall("\"name\":\".*?\"",data)
            passwords=re.findall("\"password\":\".*?\"",data)
            for n in range(0,len(names)):
                username,password=(str(names[n]).replace('"',""),str(passwords[n]).replace('"',""))
                print(username,password)
                print(username,password,file=open("save.txt","a",encoding="utf-8"))
            print("")
            print("",file=open("save.txt","a",encoding="utf-8"))
        else:
            print("没有发现信息泄露,url:{}".format(url))

if __name__ == '__main__':
    obj=getdata()
    parser=optparse.OptionParser()
    parser.add_option('-u',dest='url',help="检查的url")
    parser.add_option('-f',dest='file',help="待批量检测的url(文件)")
    (option,args)=parser.parse_args()
    if(option.url):
        obj.searchdata(option.url)
    elif(option.file):
        if(os.path.exists(option.file)):
            data=open(option.file,"r",encoding="utf-8").read().split("\n")
            with ProcessPoolExecutor(max_workers=obj.thread) as Process:
                Process.map(obj.searchdata,data,chunksize=20)
        else:
            print("File Not Found:{}".format(option.file))
    else:
        parser.print_help()
        print("python getdata.py -u <url>\npython getdata.py -f <file>")