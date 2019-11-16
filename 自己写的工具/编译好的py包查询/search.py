#@author:九世
#@time:2019/11/16
#@file:search.py

from bs4 import BeautifulSoup
from colorama import init,Fore
import requests

class Searchs(object):
    def __init__(self,name):
        self.url='https://www.lfd.uci.edu/~gohlke/pythonlibs/'
        self.download='https://download.lfd.uci.edu/pythonlibs/t7epjj8p/{name}'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.search=name
        self.name=''

    def rqts(self):
        rqt=requests.get(url=self.url,headers=self.headers)
        data=BeautifulSoup(rqt.text,'html.parser')
        for x in data.find_all('strong'):
            if  self.search==x.get_text() or self.search.upper()==str(x.get_text()).upper() or self.search.lower()==str(x.get_text()).lower():
                self.name=x.get_text()
                print(Fore.GREEN + '[+] ' + Fore.WHITE + '找到要搜索的模块名:{}'.format(self.search))

        if self.name=='':
            print(Fore.BLUE + '[-] ' + Fore.WHITE + '找不到要搜索的模块名:{}'.format(self.search))
        else:
            print(Fore.GREEN+'[+] '+Fore.WHITE+' 以下模块版本有')
            for u in data.find_all('a',href='javascript:;'):
                name=u.get_text()
                if self.search in str(name) or self.search.lower() in str(name).lower() or self.search.upper() in str(name).upper():
                    print(name)

            users = input('输入版本:')
            if users != '':
                downloadurl = self.download.format(name=users)
                self.downloads(downloadurl,users)

    def downloads(self,url,name):
        dat=open(name,'wb')
        url=url.replace('‑','-')
        rgt=requests.get(url=url,headers=self.headers)
        dat.write(rgt.content)
        dat.close()

        print(Fore.BLUE+'[+] '+Fore.WHITE+'{}下载完成'.format(name))
        print('')


if __name__ == '__main__':
    while True:
        user=input('搜索的模块名称:')
        if user=='q':
            break
        else:
            print('')
            obj=Searchs(user)
            obj.rqts()