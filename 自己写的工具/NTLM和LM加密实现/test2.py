from Crypto.Hash import MD4
from pyDes import *
import binascii


class NTLMencrypt(object):
    def md4encrypt(self,data):
        md4=MD4.new()
        md4.update(data.encode())
        return md4.hexdigest()

    def hextounicode(self,hexdata):
        calc=0
        calc2=2
        unicodedata=""
        while (calc2<=len(hexdata)):
            unicodedata+=hexdata[calc:calc2]+"00"
            calc+=2
            calc2+=2
        return unicodedata

    def ntlm(self,data):
        data=binascii.hexlify(data.encode()).decode()
        hexdata=self.hextounicode(data)
        md4data=self.md4encrypt(hexdata)
        return md4data

class LMercypt(object):
    def lm(self,data):
        data=str(data).upper()
        hexdata=binascii.hexlify(data.encode()).decode()
        leng=int(len(hexdata))*4 #转换后的十六进制字符串按照二进制计算只有48bit（12*4），为了满足14字节（112bits）的要求，所以需要补全到112bits，计算缺少的bit，(112-十六进制长度)/4=要填充0的数量
        if leng<112:
            number=int((112-leng)/4)*"0"
        else:
            number=""
        hexdata+=number
        startdata=hexdata[0:14] #分成56bits的字符串两组(56bits=14*4)
        enddata=hexdata[14::]
        binstartdata=str(bin(int(startdata,16))).lstrip("0b") #将两组56bits转换为二进制
        binenddata=str(bin(int(enddata,16))).rstrip("0b")
        if len(binstartdata)<56:
            binstartdata=str(binstartdata).rjust(56,"0")
        else:
            binstartdata=binstartdata

        if len(binenddata)<56:
            binenddata=str(binenddata).rjust(56,"0")
        else:
            binenddata=enddata

        data=binstartdata+binenddata
        splitdata=[]
        splitdata2=[]
        calc=0
        calc2=7
        while calc2<=len(data):
            if len(splitdata)<8:
                splitdata.append(data[calc:calc2]+"0")
                calc+=7
                calc2+=7
            else:
                splitdata2.append(data[calc:calc2]+"0")
                calc+=7
                calc2+=7


        key=""
        key2=""
        for d in splitdata:
            key+=str(hex(int(d[0:4],2))).replace("0x","")+str(hex(int(d[4::],2))).replace("0x","") #每4个二进制位转换为一个十六进制(注:不要用lstrip去除0x，如果hex后的值是0的话用了lstrip去除0x，就会变空。。奇葩)

        for d2 in splitdata2:
            key2 += str(hex(int(d2[0:4], 2))).replace("0x", "") + str(hex(int(d2[4::], 2))).replace("0x","")  # 每4个二进制位转换为一个十六进制(注:不要用lstrip去除0x，如果hex后的值是0的话用了lstrip去除0x，就会变空。。奇葩)

        key=binascii.a2b_hex(key)
        key2=binascii.a2b_hex(key2)
        key=self.desencrypt("KGS!@#$%",key)
        key2=self.desencrypt("KGS!@#$%",key2)
        key+=key2
        return key.decode()

    def desencrypt(self,string, Des_Key):
        k = des(Des_Key, ECB, pad=None)
        EncryptStr = k.encrypt(string)
        return binascii.b2a_hex(EncryptStr)


if __name__ == '__main__':
    data="admin"
    obj=NTLMencrypt()
    print("ntlm:{}".format(obj.ntlm(data)))

    obj2=LMercypt()
    print("LM:{}".format(obj2.lm(data)))




