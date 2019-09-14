#@author:九世
#@file:dll_hijack.py
#@timeout:2019/9/11

import csv
import os
import re

class Hijack(object):
    def __init__(self,path):
        self.path=path
        self.xbs=[]
        self.xcs=[]

    def search(self):
        with open(self.path,'r',encoding='utf-8') as rb:
            cv=csv.DictReader(rb)
            for lt in cv:
                if '.DLL' in lt['Path']:
                    self.xbs.append('Process Name:{} Path:{}'.format(lt['Process Name'],lt['Path']))

    def chuli(self):
        for j in self.xbs:
            data=str(j).split('\\')
            self.xcs.append(data[-1])
            if data[-1] in self.xcs:
                print(data[-1])

if __name__ == '__main__':
    user=input('csv path:')
    if os.path.isfile(user):
        path=user
        obj=Hijack(path)
        obj.search()
        obj.chuli()
    else:
        print('[-] 文件不存在:{}'.format(user))
        exit(1)

