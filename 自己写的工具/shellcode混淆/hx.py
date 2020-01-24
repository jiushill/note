#@author:九世
#@time:2019/11/10
#@file:hx.py

from colorama import init,Fore
import binascii
import base64
import string
import os

init(wrap=True)
class Hun(object):
    def __init__(self):
        self.xw=['1.base64+ascii混淆','2.base64变中文','3.base64+Xor编码','4.十六进制化之摩斯码','5.exit']
        self.inputs={'1':self.base6hx,'2':self.chinaencode,'3':self.xoren,'4':self.shiliumsm,'5':exit}
        self.white=Fore.WHITE
        self.blue=Fore.BLUE
        self.red=Fore.RED
        self.yellow=Fore.YELLOW
        self.data=""
        self.xwen=input
        while True:
            self.data=""
            for c in self.xw:
                print(self.yellow+c)
            user=input(self.white+'选择>')
            if user in self.inputs: 
                self.inputs[user]()
                print('')

    def readfiles(self,file):
        if os.path.exists(file):
            print(self.blue+'[+] '+self.white+'读取文件:{}'.format(file))
            dk=open(file,'r',encoding='utf-8')
            for d in dk.readlines():
                data="".join(d.split('\n'))
                yield data
        else:
            print(self.red+'[-] '+self.white+'{}文件不存在'.format(file))
            Hun()

    def base6hx(self):
        print(self.blue+'[+] '+self.white+'base64+ascii混淆')
        for x in self.readfiles(self.xwen('文件路径>')):
            self.data+=x
        xw=input('几次base64加密>')
        yuan = binascii.hexlify(bytes(self.data, encoding='utf-8'))
        for x in range(1,int(xw)+1):
            jiami=base64.b64encode(yuan)
            yuan=jiami

        hou=""
        zui=bytes.decode(yuan)
        for x in zui:
            if str(x)!='=':
                hou+=str(ord(str(x)))+'@'

            if str(x)=='=':
                hou+="HAQ?"

        print(hou)
        print(hou,file=open('base64_ascii.txt','a',encoding='utf-8'))

    def chinaencode(self):
        print(self.blue+'[+] '+self.white+'base64变中文')
        payload=['王','神','乱','邪','舒','屈','死','暗','乱','魔','刃','寂','亡','希','圣','善','何','安','圻','欣','饕','餮','早','奴','隶','缰','剑','口','屠','戮','斩','光','明','佐','助','鸣','人','囚','徒','自','暗','裔','杀','总','终','源','狱','地','轨','鬼','核','抛']
        pd={}
        zmu=string.ascii_letters
        for u in range(0,len(zmu)):
            pd[zmu[u]]=payload[u]
        pd['=']='卍'
        pd['0']='~'
        pd['1']='!'
        pd['2']='@'
        pd['3']='#'
        pd['4']='$'
        pd['5']='%'
        pd['6']='^'
        pd['7']='&'
        pd['8']='*'
        pd['9']='('
        pd['0']=')'

        for x in self.readfiles(self.xwen('文件路径>')):
            self.data+=x

        xw=input('几次base64加密>')
        yuan = binascii.hexlify(bytes(self.data, encoding='utf-8'))
        for x in range(1,int(xw)+1):
            jiami=base64.b64encode(yuan)
            yuan=jiami

        hou=""
        zui=bytes.decode(yuan)
        for k in zui:
            if k in pd:
                hou+=pd[k]

        print(hou)
        print(hou,file=open('chinse.txt','a',encoding='utf-8'))

    def xorens(self,zui):
        data=[x for x in range(0,99999)]
        for l in zui:
            for c in data:
                a=int(c)
                b=9
                c=a^b
                if c==int(ord(l)):
                    yield (a,b)

    def xoren(self):
        print(self.blue + '[+] ' + self.white + 'base64+Xor编码')
        for x in self.readfiles(self.xwen('文件路径>')):
            self.data += x
        xw = input('几次base64加密>')
        yuan = binascii.hexlify(bytes(self.data, encoding='utf-8'))
        for x in range(1, int(xw) + 1):
            jiami = base64.b64encode(yuan)
            yuan = jiami

        hou = ""
        zui = bytes.decode(yuan)
        for l in self.xorens(zui):
            hou+=str(l[0])
            hou+='nmsl'

        print(hou)
        print(hou,file=open('xor.txt','a',encoding='utf-8'))

    def shiliumsm(self):
        dx = string.ascii_uppercase + '0123456789'
        data = ".-,- ...,- .- .,- ..,.,..- .,- - .,....,..,.- - -,- .-,.- ..,- -,- .,- - -,.- - .,- - .-,.- .,...,-,..-,...-,.- -,- ..-,- .- -,- - ..,- - - - -,.- - - -,..- - -,...- -,....-,.....,- ....,- - ...,- - - ..,- - - - ."
        datas = data.split(',')
        pd = {}
        for x in range(0, len(dx)):
            pd[dx[x]] = datas[x]

        print(self.blue+'[+] '+self.white+'十六进制化之摩斯码变化')
        for x in self.readfiles(self.xwen('文件路径>')):
            self.data += x

        hou=""
        jg=bytes.decode(binascii.hexlify(bytes(self.data,encoding='utf-8')).upper())
        for f in jg:
            if f in pd:
                hou+=pd[f]+'Virgil'

        print(hou)
        print(hou,file=open('moss_code.txt','a',encoding='utf-8'))



if __name__ == '__main__':
    obj=Hun()