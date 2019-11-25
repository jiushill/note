#@author:九世
#@file:shen.py
#@time:2019/10/11


from colorama import init,Fore
import os
import sys
import time
import random

init(wrap=True)

write,flush=sys.stdout.write,sys.stdout.flush
class Shen(object):
    def __init__(self):
        self.dcits=['朋友','父亲','母亲','身份证号','手机号','邮箱','密码','网名','游戏名','女朋友名字']
        self.payload={}
        self.weizi=''
        self.zh=''

    def read_file(self,file):
        with open('files/{}'.format(file),'r',encoding='utf-8') as r:
            for k in r.readlines():
                data="".join(k.split('\n'))
                yield data

    def user_plnt(self):
        file=os.listdir('files')
        if int(len(file))>0:
            print(Fore.GREEN+'[READ] 读取字典中')
        else:
            print(Fore.RED+'[ERROR] 没有字典...')
            exit()

        for y in file:
            for datas in  self.read_file(str(y)):
                for q in self.payload.values():
                    if  self.weizi=='0':
                        password='{}{}'.format(self.zhuan(q),datas)
                    elif self.weizi=='-1':
                        password='{}{}'.format(datas,self.zhuan(q))
                    else:
                        dat=list(datas)
                        if int(self.weizi)<=int(len(dat)):
                            sz=str(dat[int(self.weizi)])
                            mm=sz.replace(sz,'{}{}'.format(sz,self.zhuan(q)))
                            dat[int(self.weizi)]=mm
                            password="".join(dat)
                        else:
                            password=datas

                    p='write:{}'.format(password)
                    write(p)
                    flush()
                    time.sleep(.5)
                    write('\x08'*len(p))
                    print(password,file=open('save.txt','a',encoding='utf-8'))
        print(Fore.BLUE+'保存完毕,文件名:save.txt')

    def rt(self):
        user=input('几个>')
        return int(user)

    def xw(self):
        print('[!] 从files文件夹中读取字典，请将字典放入files文件夹')
        print('1.社工字典生成')
        print('2.py式配置导入')
        user=input('选择>')
        print('[!] 请输入英文，中文也行吧随便你....')
        if user=='1':
            self.weizi+=input('在那个位置插入这些名称呢(0为首位，-1位尾部，输入其他数字将在指定的地方插入(当插入的位置大于密码的长度的时候将不插入))>')
            self.zh+=input('字母首个大写:0 字母尾部大写:1 全部大写:2 首字母和尾部同时大写:3 什么都不做:-1>')
            for i in self.dcits:
                print(Fore.YELLOW + '[INFO] {}'.format(i))
                while True:
                    try:
                        number=self.rt()
                        break
                    except:
                        print(Fore.RED, '请输入数字')

                if number!=0 and number!='':
                    for x in range(number):
                        vt=input('{}>'.format(i))
                        self.payload['{}{}'.format(i,x)]=vt

        elif user=='2':
            dr=__import__('tconfig')
            weizi=getattr(dr,'weizi')
            zh=getattr(dr,'zh')
            config=getattr(dr,'config')
            self.weizi=weizi
            self.zh=zh
            for name in config.keys():
                self.payload[name]=config[name]


        else:
            print(Fore.RED+'没有这个选项...')

    def zhuan(self,payload):
        if str.isalpha(payload):
            if self.zh=='0':
                return str(payload).capitalize()
            elif self.zh=='1':
                jg=str(payload)[::-1]
                data=jg.capitalize()
                return data[::-1]
            elif self.zh=='2':
                return str(payload).upper()
            elif self.zh=='3':
                data = str(payload).capitalize()
                jg = data[::-1]
                wz = jg[0].capitalize()
                jg = jg.replace(jg[0], wz)
                return jg[::-1]
            else:
                return str(payload)
        else:
            return payload

if __name__ == '__main__':
    obj=Shen()
    obj.xw()
    obj.user_plnt()