'''
加密过程:
先把key转成10进制然后全部相加，然后要加密的内容
也一样。如果加密的内容转成ascii全部相加后大于key
则base64编码然后将base64编码的结果在转换为ascii
然后在一次base64编码，然后在转为ascii编码。然后
加上最后转成的ascii编码然后在乘于key在base64编码
'''

import base64

class Jiami:
    def __init__(self,key,data):
        self.key=key
        self.data=data

    def jiami(self):
        pwd = 0
        dwd = 0
        for k in key:
            pwd += ord(k)

        for d in self.data:
            dwd += ord(d)

        if dwd > pwd:
            data =''
            dg=0
            jg = bytes.decode(base64.b64encode(str(dwd).encode('utf-8')))
            for j in jg:
                data += bytes.decode(base64.b64encode(str(ord(j)).encode('utf-8')))
            for i in data:
                dg+=ord(i)
                print(dg,file=open('save_id.txt','a',encoding='utf-8'))

            print(bytes.decode(base64.b64encode(str(dg*pwd).encode('utf-8'))))

    def jiemi(self,rk):
        pwd = 0
        dwd = 0
        for k in key:
            pwd += ord(k)

        for d in self.data:
            dwd += ord(d)
        yi=base64.b64decode(rk)
        number=bytes(yi).decode('utf-8')
        rb=int(int(number)/pwd)
        print(rb)


if __name__ == '__main__':
    key = 'haq'
    data = '卢本伟'
    obj=Jiami(key=key,data=data)
    obj.jiami()
