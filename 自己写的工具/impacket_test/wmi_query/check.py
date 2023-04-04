import requests
import urllib.parse
import sys
import os
import re
from bs4 import BeautifulSoup

def process_check(processlist):
    tmp=[]
    result=""
    url="http://42.193.251.15/tasklist.php"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36","Content-Type":"application/x-www-form-urlencoded"}
    rqt=requests.post(url=url,headers=headers,data="avlist={}".format(urllib.parse.quote(processlist)),verify=False)
    html=BeautifulSoup(rqt.text,"html.parser")
    tdlist=html.find_all("td")
    for td in tdlist:
        tmp.append(td.get_text())
        if len(tmp)==2:
            find_pid=re.findall("{}.*".format(tmp[0]),processlist)
            pid=find_pid[0].split(" ")[1]
            result += "{}     {}    PID:{}\r\n".format(tmp[0], tmp[1],pid)
            tmp=[]
    print(result)