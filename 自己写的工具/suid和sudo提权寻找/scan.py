import sys,requests,os
from bs4 import BeautifulSoup

class Search(object):
    def __init__(self):
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}
        self.url='https://gtfobins.github.io/'
        self.dicts={}
        self.timeout=10
        if len(sys.argv)<3:
            print('python scan.py [file] [suid/sudo].')
            exit()
        else:
            if sys.argv[2]=='suid':
                self.id="suid"
            elif sys.argv[2]=="sudo":
                self.id="sudo"
            else:
                print('Error: Not setting,suid or sudo')
                exit()

            if os.path.exists(sys.argv[1]):
                self.file=sys.argv[1]
                self.request()
                if len(self.dicts)<0:
                    print('Error:Reqeust timeout !')
                else:
                    self.filefind()
            else:
                print('Error:Not Found file.')
                exit()

    def request(self):
        try:
            rqt=requests.get(url=self.url,headers=self.headers,timeout=self.timeout)
            bt=BeautifulSoup(rqt.text,'html.parser')
            for a in bt.find_all('a',class_="bin-name"):
                self.dicts[a.get_text()]="{}{}".format(self.url,str(a.get('href')).lstrip('/'))
        except Exception as r:
            print('Error:{}.'.format(r))

    def returnjg(self,url):
        try:
            rqt2 = requests.get(url=url, headers=self.headers, timeout=self.timeout)
            bt2 = BeautifulSoup(rqt2.text, 'html.parser')
            for h2 in bt2.find_all('h2', class_="function-name"):
                if h2.get_text().lower() == self.id:
                    return url
        except Exception as r:
            print('Error:{}.'.format(r))

    def filefind(self):
        print('Looking for something to use:')
        with open(self.file, 'r', encoding='utf-8') as op:
            for r in op.readlines():
                data = "".join(r.split('\n')).split('/')[-1]
                if self.id=="suid":
                    if data in self.dicts:
                            ag=self.returnjg(self.dicts[data])
                            if ag!=None:
                                print('Available:{} exp url:{} type:{}'.format(data,ag,self.id))
                elif self.id=="sudo":
                    if self.id == "sudo":
                        if data in self.dicts:
                            ag = self.returnjg(self.dicts[data])
                            if ag != None:
                                print('Available:{} exp url:{} type:{}'.format(data, ag, self.id))

if __name__ == '__main__':
    print('[Search for places to claim]---------->:)')
    obj=Search()