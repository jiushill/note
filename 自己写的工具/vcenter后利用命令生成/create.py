import os
import re

class Createcommand(object):
    def __init__(self):
        if os.path.exists("command.txt") and os.path.exists("data.txt"):
            pass
        else:
            print("[-] Not Found command.txt")
            exit(1)

        data=open("data.txt","r",encoding="utf-8").read()
        dcAccount=re.findall("dcAccount\".*",data)[0].split(" ")[-1].replace('"',"")
        dcAccountDN=re.findall("dcAccountDN\".*",data)[0]
        dc=re.findall("dc=.*",dcAccountDN)[0].replace('"',"")
        dcAccountPassword=re.findall("dcAccountPassword\".*",data)[0].split("REG_SZ")[-1].rstrip().lstrip().rstrip('"').lstrip('"')
        if '\\"' in dcAccountPassword or "'" in dcAccountPassword:
            dcAccountPassword=f"\"{dcAccountPassword}\""
        else:
            dcAccountPassword=f'\'{dcAccountPassword}\''
        print(f"[+] dcAccount:{dcAccount}")
        print(f"[+] dcAccountPassword:{dcAccountPassword}")
        print(f"[+] dc:{dc}")
        command=open("command.txt","r",encoding="utf-8").read().format(dcAccount=dcAccount,dcAccountPassword=dcAccountPassword,dc=dc)
        print(command)

if __name__ == '__main__':
    obj=Createcommand()
