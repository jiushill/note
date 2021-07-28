import socket
import chardet
import re
import optparse
from IPy import IP
from concurrent.futures import ProcessPoolExecutor

class OXIDGetInfo(object):
    def __init__(self):
        self.buffer=b'\x05\x00\x0b\x03\x10\x00\x00\x00H\x00\x00\x00\x01\x00\x00\x00\xb8\x10\xb8\x10\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\xc4\xfe\xfc\x99`R\x1b\x10\xbb\xcb\x00\xaa\x00!4z\x00\x00\x00\x00\x04]\x88\x8a\xeb\x1c\xc9\x11\x9f\xe8\x08\x00+\x10H`\x02\x00\x00\x00'
        self.buffer2=b"\x05\x00\x00\x03\x10\x00\x00\x00\x18\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00"
        self.port=135
        self.timeout=3

    def getinfo(self,ip):
        s=socket.socket()
        try:
            s.settimeout(self.timeout)
            s.connect((ip,self.port))
            s.sendall(self.buffer)
            s.recv(4096)
            s.sendall(self.buffer2)
            data=s.recv(4096)
            enc=chardet.detect(data)["encoding"]
            info=data.decode(enc)
            info="|".join("".join(re.findall("[0-9-A-Z-a-z-.-]{1,}",info.replace("","RaidEnMei"))).replace("RaidEnMei","|").split("|")[2:])
            print(info)
        except Exception as error:
            pass

if __name__ == '__main__':
    obj=OXIDGetInfo()
    parser=optparse.OptionParser()
    parser.add_option("-i",dest="IP",help="IP or IP Range")
    option,args=parser.parse_args()
    if option.IP:
        iplist=[str(ip) for ip in IP(option.IP)]
        print("[*] GetInfo Wait.....")
        with ProcessPoolExecutor(max_workers=10) as p:
            p.map(obj.getinfo,iplist)
    else:
        parser.print_help()