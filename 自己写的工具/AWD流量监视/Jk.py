#@author:九世
#@time:2019/11/5
#@file:http_jk.py

from scapy.all import *
import threading
import time

class Http_sniff(object):
    def __init__(self):
        self.wlan0="Intel(R) Dual Band Wireless-AC 7265"
        self.filter="ip dst 192.168.1.104"
        self.calc=0

    def sniffs(self):
        sn=sniff(iface=self.wlan0,filter=self.filter,count=3)
        wrpcap("file/save.pcap{}".format(self.calc),sn)
        print('src:{}->dst:{} src_port:{}->dst_port:{}'.format(sn[0][1].src,sn[0][1].dst,sn[0][2].sport,sn[0][2].dport))
        self.calc+=1


if __name__ == '__main__':
    obj=Http_sniff()
    while True:
        t=threading.Thread(target=obj.sniffs,args=())
        t.setDaemon(True)
        t.start()
        t.join(3)