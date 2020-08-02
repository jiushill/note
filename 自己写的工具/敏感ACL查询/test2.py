import re
import chardet
from colorama import init,Fore
init(wrap=True,autoreset=True)

class Search(object):
    def __init__(self,path,path2):
        self.path=path
        self.path2=path2
        self.acls=["GenericAll","GenericWrite","Self-Membership","WriteProperty","WriteOwner","WriteDacl"]

    def aclsearch(self):
        datas=[]
        tmp=[]
        guol=[]
        dk=open(self.path,'rb')
        encoding=chardet.detect(dk.read())['encoding']
        ok=open(self.path,'r',encoding=encoding)
        for d in ok.readlines():
            data="".join(d.split('\n'))
            if 'ObjectDN' in data or 'ActiveDirectoryRights' in data or 'SecurityIdentifier' in data:
                tmp.append(re.sub("\s.*[:]",":",data))
                if len(tmp)==3:
                    datas.append(tmp)
                    tmp=[]
        for d in datas:
            if len(re.findall('[-].*[-].*[-].*[-].*[-].*[-].*',d[2]))>0:
                for acl in self.acls:
                    if acl in d[1]:
                        sdata="{} {} {}".format(d[0],d[1],d[2])
                        guol.append(sdata)

        datas2=[]
        tmp2=[]
        dk = chardet.detect(open(self.path2, 'rb').read())
        enc = dk['encoding']
        dk2 = open(self.path2,"r", encoding=enc)
        for l in dk2.readlines():
            ldata="".join(l.split('\n'))
            if 'distinguishedname' in ldata or 'objectsid' in ldata:
                tmp2.append(re.sub("\s.*[:]",":",ldata))
                if len(tmp2)==2:
                    datas2.append(tmp2)
                    tmp2=[]

        sids=[]
        names=[]
        for x in datas2:
            for g in x:
                sid=re.findall('objectsid:.*',g)
                name=re.findall('distinguishedname:.*',g)
                if len(sid)>0:
                    sids.append(str(sid[0]).replace('objectsid:','').rstrip().lstrip())
                elif len(name)>0:
                    names.append(str(name[0]).replace('distinguishedname:','').rstrip().lstrip())

        for a in set(list(guol)):
            for sid in range(0,len(sids)):
                if sids[sid] in a:
                    print(Fore.GREEN+"[+] sid:{} user:{}".format(sids[sid],names[sid]))
                    print(a)

if __name__ == '__main__':
    path=r"C:\Users\JiuShi\Desktop\save.txt"
    path2=r"C:\Users\JiuShi\Desktop\user.txt"
    obj=Search(path,path2)
    obj.aclsearch()