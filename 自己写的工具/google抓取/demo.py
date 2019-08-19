import random
import requests
import time
from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs

def read():
    dk=open('user_agents.txt','r',encoding='utf-8')
    for r in dk.readlines():
        data="".join(r.split('\n'))
        yield data

def reads():
    dk=open('domain.txt','r',encoding='utf-8')
    for r in dk.readlines():
        data="".join(r.split('\n'))
        yield data


def fenpei(proxy,search,page,sleep):
    user_agents=[]
    google_searchs=[]
    for ua in read():
        user_agents.append(ua)


    for domain in reads():
        google_searchs.append(domain)

    time.sleep(int(sleep))
    proxy={'http':'http://{}'.format(proxy),'https':'https://{}'.format(proxy)}
    domains=random.choice(google_searchs)
    u_s={'user-agent':random.choice(user_agents),'Content-type':"text/html;charset=utf-8"}
    url='https://{}/search?hl=Chinese&q={}&btnG=Search&gbv=10&start={}'.format(domains,search,page)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    rqt=requests.get(url=url,headers=u_s,allow_redirects=False,verify=False,proxies=proxy,timeout=30)
    return rqt.content
