from concurrent.futures import ProcessPoolExecutor
import socket
import re
import IPy
import optparse

class OsScan(object):
    def scan(self,ip):
        self.socket=socket.socket()
        self.socket.settimeout(3)
        print("\rCuurent IP:{}    ".format(ip),end="")
        data=b"\x00\x00\x00\x2f\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x01\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xd5\x12\x00\x00\x00\x00\x00\x0c\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00"
        data2=b"\x00\x00\x00\x88\xff\x53\x4d\x42\x73\x00\x00\x00\x00\x18\x01\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xd5\x12\x00\x00\x00\x00\x0c\xff\x00\x00\x00\x00\xf0\x02\x00\x01\x00\x00\x00\x00\x00\x42\x00\x00\x00\x00\x00\x44\xc0\x00\x80\x4d\x00\x60\x40\x06\x06\x2b\x06\x01\x05\x05\x02\xa0\x36\x30\x34\xa0\x0e\x30\x0c\x06\x0a\x2b\x06\x01\x04\x01\x82\x37\x02\x02\x0a\xa2\x22\x04\x20\x4e\x54\x4c\x4d\x53\x53\x50\x00\x01\x00\x00\x00\x05\x02\x88\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x6e\x69\x78\x00\x53\x61\x6d\x62\x61\x00"
        try:
            self.socket.connect((ip,445))
            self.socket.sendall(data)
            self.socket.recv(1024)
            self.socket.sendall(data2)
            os=self.socket.recv(1024)
            os=re.findall("Windows.*",str(os))
            if len(os)>0:
                osname=str(os[0]).split("\\x00")[0]
            else:
                osname=""
            print("ip:{} port:445 os:{}".format(ip,osname))
            print("ip:{} port:445 os:{}".format(ip, osname), file=open("../save.txt", "a", encoding="utf-8"))
        except Exception as r:
            pass

if __name__ == '__main__':
    obj=OsScan()
    parser=optparse.OptionParser()
    parser.add_option('-i',dest='ip',help='ip/ip range-> 10.4.3.0/24')
    parser.add_option('-t',dest='process',help='process')
    (option,args)=parser.parse_args()
    if option.ip and option.process:
        ip=option.ip
        process=option.process
        if '/' in ip:
            ip=[str(x) for x in IPy.IP(ip,make_net=1)]
        else:
            ip=ip
        if isinstance(ip,list):
            with ProcessPoolExecutor(max_workers=int(process)) as Executer:
                Executer.map(obj.scan,ip)
        else:
            obj.scan(ip)

    else:
        parser.print_help()

