from concurrent.futures import  ProcessPoolExecutor
import socket
import os
import optparse


class domain_query(object):
    def __init__(self,domain,ip):
        print(domain,ip)
        self.currentip=ip
        self.domain="{}."+domain
        self.file=r"dict.txt"
        if os.path.exists(self.file)==False:
            print("[-] 字典文件找不到")
            exit()
        self.dicts=[]
        with open(self.file,"r") as fs:
            for r in fs.readlines():
                self.dicts.append(r.rstrip("\n"))

        with ProcessPoolExecutor(max_workers=30) as executer:
            executer.map(self.getip,self.dicts)

    def getip(self,dict):
        domain=self.domain.format(dict)
        domains,n,ip=socket.gethostbyname_ex(domain)
        if self.currentip!="none" and self.currentip in ip:
            print("{} {}".format(domains,ip))
        elif self.currentip=="none":
            print("{} {}".format(domains,ip))

if __name__ == '__main__':
    p=optparse.OptionParser()
    p.add_option('-d',dest='domain',help='指定要爆破的域名')
    p.add_option('-i',dest='host',help="匹配指定IP的域名")
    (option,args)=p.parse_args()
    if option.host:
        domain_query(option.domain,option.host)
    else:
        print("Exmaple:\n不指定匹配IP爆破域名:python query_domain.py -d baidu.com -i none\n指定匹配IP爆破域名:python query_domain.py -d baidu.com -i 1.1.1.1")
        p.print_help()