import requests
import re
import config
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor

url=config.url
jdurl=config.jdurl
jdid=config.jdid
save=config.save
filename=config.filename

class Notebook(object):
    def __init__(self,url):
        self.url=url
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        self.notebooklist={}
        self.extract()


    def extract(self):
        rqt=requests.get(url=self.url,headers=self.headers,timeout=10)
        html=BeautifulSoup(rqt.text,"html.parser")
        notebookname=html.find_all("p",attrs={"style":re.compile(".*")})
        start=0
        keyname=""
        models = []
        for n in range(0,len(notebookname)):
            if len(re.findall("【[0-9-+]{3,}——[0-9-+]{3,}】",str(notebookname[n].get_text())))>0:
                start+=n
                break

        for x in range(start, len(notebookname)):
            data = str(notebookname[x].get_text()).split("\n")
            if len(data[0])==0:
                if len(re.findall("【[0-9-+]{3,}——[0-9-+]{3,}】", str(notebookname[x+1].get_text())))==0:
                    break
            elif len(data[0])>0:
                t=str(data[0])
                if len(re.findall("【[0-9-+]{3,}——[0-9-+]{3,}】",t)) > 0:
                    keyname=t
                    self.notebooklist[t]=[]
                else:
                    if "无产品可选" not in t:
                        self.notebooklist[keyname].append(t)

        for k in self.notebooklist:
            print(k) #大致价格
            if save == 1:
                print(k,file=open(filename, "a", encoding="utf-8"))
            if len(self.notebooklist[k])>0:
                for n in self.notebooklist[k]:
                    if "【" not in n:
                        print(n)
                        if save==1:
                            print(n,file=open(filename,"a",encoding="utf-8"))
                        #models.append(n)
                        results=self.jdsearch(n)
                        if len(results)>0:
                            for r in results:
                                print(r)
                                if save == 1:
                                    print(r, file=open(filename, "a", encoding="utf-8"))
                    else:
                        print(n)
                        if save==1:
                            print(n,file=open(filename,"a",encoding="utf-8"))
                print("")
                if save == 1:
                    print("", file=open(filename, "a", encoding="utf-8"))

       # with ProcessPoolExecutor(max_workers=5) as p:
       #     for r in p.map(self.jdsearch,models):
       #         if r!=None:
       #             print(r)


    def jdsearch(self,n):
        url = jdurl.format(n)
        rqt = requests.get(url=url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"})
        html = BeautifulSoup(rqt.text, "html.parser")
        data = html.find_all("li", class_="gl-item")
        result = []
        for d in data:
            html2 = BeautifulSoup(str(d), "html.parser")
            strong = html2.find_all("strong")
            price = str(strong[0].get_text()).lstrip().rstrip()
            href = html2.find_all("a", target="_blank", attrs={"href": re.compile("//item.jd.com/.*")})
            lnk = str("https:" + href[1].get("href")).lstrip().rstrip()
            text = str(href[1].get_text()).lstrip().rstrip().replace("\n", "")
            store = html2.find_all("span", class_="J_im_icon")
            id = html2.find_all("i", class_="goods-icons J-picon-tips J-picon-fix")
            if len(store) > 0:
                storename = str(store[0].get_text()).lstrip().rstrip()
            else:
                storename = ""

            if len(id) > 0:
                idname = str(id[0].get_text()).lstrip().rstrip()
            else:
                idname = ""

            string = "价格:{}   链接:{}   描述:{}   店名:{}   是否自营:{}".format(price, lnk, text, storename, idname)
            if jdid==1 and len(id)>0:
                result.append(string)
            if jdid==0:
                result.append(string)

        return result


if __name__ == '__main__':
    n = Notebook(url=url)
