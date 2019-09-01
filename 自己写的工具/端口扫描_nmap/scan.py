#@author:九世
#@file:scan.py
#@time:2019/9/1
'''
调用nmap模块实现的端口扫描
需要安装的模块：python-nmap
参考链接：
https://pypi.org/project/python-nmap/
http://xael.org/
https://blog.csdn.net/qq_36119192/article/details/83717690
'''
import nmap
import re
import time

class Nmap_scans(object):
    def __init__(self):
        self.ip='192.168.3.4' #Setting IP or IP segments
        self.command='-p 1-1000 -sV -sC' #set command

    def jiexi(self,n,ip):
        data=''
        print('')
        jg = n[str(ip)]
        print('[+] IP:{}'.format(jg['addresses']['ipv4']))
        tcp = jg['tcp']
        zz = re.findall('[0-9]{1,}[:]', str(tcp))
        for port in zz:
            lb=tcp[int(str(port).replace(':', ''))]
            data+='port:{} '.format(str(port).replace(':',''))
            for names in lb:
                data+='{}:{} '.format(names,tcp[int(str(port).replace(':', ''))][names]).replace('\n','')
            data+='\n'

        print(data)


    def scanner(self):
        start=time.time()
        n=nmap.PortScanner()
        n.scan(hosts=self.ip,arguments='{}'.format(self.command))
        print('[command]:{}'.format(n.command_line()))
        if len(n.all_hosts())>1:
            for ip in n.all_hosts():
                self.jiexi(n,ip)
        else:
            ip=n.all_hosts()[0]
            self.jiexi(n,ip)
        stop=time.time()
        print('[+] 耗时:{}'.format(stop-start))

if __name__ == '__main__':
    obj=Nmap_scans()
    obj.scanner()