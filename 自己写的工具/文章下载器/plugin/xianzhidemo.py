import requests
from bs4 import BeautifulSoup

def geturl(url):
    urllist=[]
    rqt=requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
    html=BeautifulSoup(rqt.text,"html.parser").find_all("a",class_="topic-title")
    for data in html:
        urllist.append("https://xz.aliyun.com{}".format(data["href"]).lstrip())
    return urllist
if __name__ == '__main__':
    geturl("https://xz.aliyun.com/?page=2")