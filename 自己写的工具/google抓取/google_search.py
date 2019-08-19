from gevent import monkey;monkey.patch_all()
from bs4 import BeautifulSoup
import chardet
import os
import urllib.parse
import re
import random
from demo import fenpei
import configparser
import requests
import gevent

class Google_Disk(object):
    def __init__(self):
        self.conf={}
        self.iplist=[]
        self.calc=0
        self.html=b''
        self.cookies={}
        self.cookie='HSID=AnOingRydX5d2psm6; SSID=ADt9T-YUVJhcGL4qL; APISID=wJEaAiaIyzvEaudB/AcoN5lpzTLnX5Reo_; SAPISID=f7PURACCKCHWwSNN/AzvNr8jk9DaahBOjn; CONSENT=YES+CN.zh-CN+20170611-09-0; SID=BQd-7E64xr8N2KPkSozUAhhUGA1yC2pOm44rxZeltI5oyZczMhTQXcaLdnFMy6KuYM7CVQ.; _ga=GA1.1.1066659943.1561908462; _gcl_au=1.1.1103150496.1563265661; ANID=AHWqTUkF83QBPYbfQq0kmzf1KcFRM9zsr6E6DzhE_HothF5Y28xI_VdxHrB1fMar; SEARCH_SAMESITE=CgQIzY0B; GOOGLE_ABUSE_EXEMPTION=ID=becbf893a4904d44:TM=1566184449:C=r:IP=47.75.69.236-:S=APGng0se1h0QgE8PglXBZJi1H6W3jRYdzw; NID=188=I04uuKTsGOjSp5c3G9QzFnfHqsL7ZQE3t9FdHLq25aPPiAHLfdWBsh3j3v14esoRRMVNXV6Pg8WXsqliJ8c7G46efNs-16lEr8ZZn6Fvz0GzYcw6wzcJ78OWUOuiz0K8W63M0zuBNTUDDmzVBxiud788TjTvbI5CZurTIcD6z2TTwQ_TuoGvjP2cuutFWcs5C8_11nk35jERGC2_A2UPda-AtI2mnVspSF5NNpawFUwW8PgQpxM; DV=oylrE6tRiwhOECBuCtWvdH13M-J_yhYIrTZO_A7m2wIAAABsoyqeic4gCwEAAFj9N_RUZyHkUQAAAA; 1P_JAR=2019-8-19-3; SIDCC=AN0-TYtz7HmrYpB6Cyw9ogysPbuDr2AY0pBl89HytGxEBiBr2lsZ4ceFMNWkG4Efolz2ihLVoMth'
        for v in self.cookie.split(';'):
            key,value=v.split('=',1)
            self.cookies[key]=value

        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self.host='https://www.google.tw/search?'
        if os.path.exists('Config.ini'):
            print('[~] 读取配置文件')
            config=configparser.ConfigParser()
            config.read("Config.ini",encoding='utf-8')
            self.conf['proxy']=config['config']['proxy']
            self.conf['save']=config['config']['save_name']
            self.conf['search']=config['config']['search_grammar']
            self.conf['page']=config['config']['page']
            self.conf['sleep']=config['config']['sleep']
            print('[+] 读取完成')
        else:
            print('[-] 找不到配置文件')
            exit()

        if os.path.exists('iplist.txt'):
            print('[~] 检测到iplist.txt,采用每次请求随机抽取一个IP')
            dk=open('iplist.txt','r')
            for r in dk.readlines():
                data="".join(r.split('\n'))
                self.iplist.append(data)
            proxy=self.iplist
        else:
            proxy=self.conf['proxy']

        print('[config] 代理设置:{}'.format(proxy))
        print('[config] 搜索语法:{}'.format(self.conf['search']))
        print('[config] 抓取的页数:{}'.format(self.conf['page']))
        print('[config] 保存文件名:{}'.format(self.conf['save']))

    def search(self):
        for p in range(0,int(self.conf['page'])):
            page=p*10
            if len(self.iplist)>0:
                proxy=random.choice(self.iplist)
            else:
                proxy=self.conf['proxy']
            try:
                html=fenpei(proxy=proxy,search=self.conf['search'], page=page,sleep=self.conf['sleep'])
                if b'302 Moved' not in html:
                    print(html)
                    self.html+=html
                else:
                    print('[-] Google又要你输验证码啦...')
            except Exception as r:
                print(r)

    def chuli(self):
        try:
            bt = BeautifulSoup(self.html, 'html.parser')
            for h in bt.find_all('h3'):
                href=re.findall('[a-zA-z]+://[^\s]*[&]',str(h))
                hrefs=re.findall('[a-zA-z]+://[^\s]*;',str(href[0]))
                jg='标题:{} url:{}'.format(h.get_text(),urllib.parse.unquote(str(hrefs[0]).replace('&amp;sa=U&amp;','').replace('&amp;','')))
                print(jg)
                print(jg,file=open(self.conf['save'],'a'))
        except:
            pass

if __name__ == '__main__':
    obj=Google_Disk()
    obj.search()
    obj.chuli()