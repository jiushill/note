#@author:九世
#@time:2020/7/20
#@file:create.py

from colorama import Fore,init
import os

init(autoreset=True,wrap=True)
banner='''
 ▄████████    ▄████████    ▄████████    ▄████████     ███        ▄████████ 
███    ███   ███    ███   ███    ███   ███    ███ ▀█████████▄   ███    ███ 
███    █▀    ███    ███   ███    █▀    ███    ███    ▀███▀▀██   ███    █▀  
███         ▄███▄▄▄▄██▀  ▄███▄▄▄       ███    ███     ███   ▀  ▄███▄▄▄     
███        ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████     ███     ▀▀███▀▀▀     
███    █▄  ▀███████████   ███    █▄    ███    ███     ███       ███    █▄  
███    ███   ███    ███   ███    ███   ███    ███     ███       ███    ███ 
████████▀    ███    ███   ██████████   ███    █▀     ▄████▀     ██████████ 
             ███    ███                                                    
'''
print(banner)
class Createing(object):
    def __init__(self):
        '''主交互函数'''
        #字典列表
        self.dicts=[]
        self.command={"set":self.set,"show":self.show}
        self.regexs=[{"position":"None","help":"字典拼接位置设置 ((在首个字典的内容里插入))默认为最后一位:None，倒数第二位:-1)"},{"path":"","help":"字典路径设置,多个字典用逗号隔开"},{"inuse":"","help":"字典规则设置 Example(字典列表:[ac.txt,ab.txt,ax.txt]，指定特定组合的文件名:ac.txt&&ax.txt,ab.txt&&ax.txt)"},{"capital":"False","help":"指定位置的字母大写（默认设置False，最后一位:-1,第一位:0）"}]
        self.helps=["1.字典生成","2.规则设置","3.退出"]
        self.runs={"1":self.createpassword,"2":self.setregex,"3":exit}
        for h in self.helps:
            print(h)
        print('')
        while True:
            user=input(Fore.RED+"Settings$")
            if user in self.runs:
                self.runs[user](user)


    def createpassword(self,*args):
        regex={}
        path=[]
        inuse=[]
        reads=[]
        for b in self.regexs:
            name = list(b.keys())[0]
            #添加字段路径在列表
            if name=="path":
                for filename in b[name].split(","):
                    if os.path.exists(filename):
                        path.append(filename)
            elif name=="inuse":
                for filename in b[name].split(","):
                    if "&&" not in filename:
                        print(Fore.RED+"要使用的文件设置错误")
                    else:
                        inuse.append(filename)
            else:
                regex[name]=b[name]

        if len(inuse)>0:
            if len(path)>0:
                tmp=[]
                for b in inuse:
                    xs=b.split("&&")
                    for x in xs:
                        for f in path:
                            if x in f:
                                tmp.append(f)
                                if len(tmp)==2:
                                    reads.append({"1":tmp[0],"2":tmp[1]})
                                    tmp=[]
                for v in reads:
                    fp=open(v["1"],"r",encoding="utf-8").read().split('\n')
                    fp2=open(v["2"],"r",encoding="utf-8").read().split('\n')
                    for l1 in fp:
                        for l2 in fp2:
                            if regex["position"]=="None":
                                data = "{}{}".format(l1[0::], l2)
                            else:
                                data = "{}{}{}".format(l1[0:int(regex["position"])], l2, l1[int(regex["position"])::])

                            if regex["capital"]!="False":
                                capital = int(regex["capital"])
                                data=data.replace(data[capital],data[capital].upper())
                            print(data)


            else:
                print(Fore.RED+"设置的文件路径不存在")
        else:
            print(Fore.RED+"规则未设置")


    def setregex(self,*args):
        for b in self.regexs:
            name=list(b.keys())[0]
            print("name:{} status:{} help:{}".format(name,b[name],b["help"]))

        while True:
            user=input(Fore.RED+"Regexset$")
            cmd=user.split(" ")[0]
            if cmd=="break":
                break
            if cmd in self.command:
                self.command[cmd](user)

    def set(self,*args):
        sett=str(args[0]).split(" ")
        if len(sett)==3:
            for b in self.regexs:
                name = list(b.keys())[0]
                if sett[1]==name:
                    b[name]=sett[2]
                    print("SET {}=>{}".format(name,sett[2]))
        else:
            print(Fore.RED+"The parameters must be 3")

    def show(self,*args):
        sett = str(args[0]).split(" ")
        if sett[1]=="options":
            for b in self.regexs:
                name = list(b.keys())[0]
                print("name:{} status:{} help:{}".format(name, b[name], b["help"]))


if __name__ == '__main__':
    obj=Createing()