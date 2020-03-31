#@author:九世
#@time:2020/3/26
#@file:jiexi.py

import os
import json
import chardet
import sys

class Jiexi(object):
    def __init__(self):
        self.name='files/computers.txt'
        self.name2='files/domains.txt'
        self.name3='files/gpos.txt'
        self.name4='files/groups.txt'
        self.name5='files/ous.txt'
        self.name6='files/users.txt'


    def jiexi(self,name):
        end=chardet.detect(open(name,'rb').read())
        dk=open(name,'r',encoding=end['encoding'])
        for j in dk.readlines():
            data=json.loads("".join(j.split('\n')))
            if "computers" in name:
                print('[+] wait write file:{}'.format(self.name))
                computers=data['computers']
                for c in computers:
                    print('=' * 90,file=open(self.name,'a',encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier',c['ObjectIdentifier']),file=open(self.name,'a',encoding=end['encoding']))
                    Aces=c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r,k[r]),file=open(self.name,'a',encoding=end['encoding']))
                        print('',file=open(self.name,'a',encoding=end['encoding']))
                    Properties=c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p,Properties[p]),file=open(self.name,'a',encoding=end['encoding']))
                    print('',file=open(self.name,'a',encoding=end['encoding']))

                meta = data['meta']
                for m in meta:
                    print('{}:{}'.format(m, meta[m]), file=open(self.name, 'a', encoding=end['encoding']))

            elif "domains" in name:
                print('[+] wait write file:{}'.format(self.name2))
                computers = data['domains']
                for c in computers:
                    print('=' * 90, file=open(self.name2, 'a', encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier', c['ObjectIdentifier']),
                          file=open(self.name2, 'a', encoding=end['encoding']))
                    Aces = c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r, k[r]), file=open(self.name2, 'a', encoding=end['encoding']))
                        print('', file=open(self.name2, 'a', encoding=end['encoding']))
                    Properties = c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p, Properties[p]), file=open(self.name2, 'a', encoding=end['encoding']))
                    print('', file=open(self.name2, 'a', encoding=end['encoding']))

                meta=data['meta']
                for m in meta:
                    print('{}:{}'.format(m,meta[m]),file=open(self.name2,'a',encoding=end['encoding']))

            elif 'gpos' in name:
                print('[+] wait write file:{}'.format(self.name3))
                computers = data['gpos']
                for c in computers:
                    print('=' * 90, file=open(self.name3, 'a', encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier', c['ObjectIdentifier']),
                          file=open(self.name3, 'a', encoding=end['encoding']))
                    Aces = c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r, k[r]), file=open(self.name3, 'a', encoding=end['encoding']))
                        print('', file=open(self.name3, 'a', encoding=end['encoding']))
                    Properties = c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p, Properties[p]), file=open(self.name3, 'a', encoding=end['encoding']))
                    print('', file=open(self.name3, 'a', encoding=end['encoding']))

                meta = data['meta']
                for m in meta:
                    print('{}:{}'.format(m, meta[m]), file=open(self.name3, 'a', encoding=end['encoding']))

            elif 'groups' in name:
                print('[+] wait write file:{}'.format(self.name4))
                computers = data['groups']
                for c in computers:
                    print('=' * 90, file=open(self.name4, 'a', encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier', c['ObjectIdentifier']),
                          file=open(self.name4, 'a', encoding=end['encoding']))
                    Aces = c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r, k[r]), file=open(self.name4, 'a', encoding=end['encoding']))
                        print('', file=open(self.name4, 'a', encoding=end['encoding']))
                    Properties = c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p, Properties[p]), file=open(self.name4, 'a', encoding=end['encoding']))
                    print('', file=open(self.name4, 'a', encoding=end['encoding']))

                meta = data['meta']
                for m in meta:
                    print('{}:{}'.format(m, meta[m]), file=open(self.name4, 'a', encoding=end['encoding']))

            elif 'ous' in name:
                print('[+] wait write file:{}'.format(self.name4))
                computers = data['ous']
                for c in computers:
                    print('=' * 90, file=open(self.name5, 'a', encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier', c['ObjectIdentifier']),
                          file=open(self.name5, 'a', encoding=end['encoding']))
                    Aces = c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r, k[r]), file=open(self.name5, 'a', encoding=end['encoding']))
                        print('', file=open(self.name5, 'a', encoding=end['encoding']))
                    Properties = c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p, Properties[p]), file=open(self.name5, 'a', encoding=end['encoding']))
                    print('', file=open(self.name5, 'a', encoding=end['encoding']))

                meta = data['meta']
                for m in meta:
                    print('{}:{}'.format(m, meta[m]), file=open(self.name5, 'a', encoding=end['encoding']))

            elif 'users' in name:
                print('[+] wait write file:{}'.format(self.name4))
                computers = data['users']
                for c in computers:
                    print('=' * 90, file=open(self.name6, 'a', encoding=end['encoding']))
                    print('{}:{}'.format('ObjectIdentifier', c['ObjectIdentifier']),
                          file=open(self.name6, 'a', encoding=end['encoding']))
                    Aces = c['Aces']
                    for k in Aces:
                        for r in k:
                            print('{}:{}'.format(r, k[r]), file=open(self.name6, 'a', encoding=end['encoding']))
                        print('', file=open(self.name6, 'a', encoding=end['encoding']))
                    Properties = c['Properties']
                    for p in Properties:
                        print('{}:{}'.format(p, Properties[p]), file=open(self.name6, 'a', encoding=end['encoding']))
                    print('', file=open(self.name6, 'a', encoding=end['encoding']))

                meta = data['meta']
                for m in meta:
                    print('{}:{}'.format(m, meta[m]), file=open(self.name6, 'a', encoding=end['encoding']))


    def openfiles(self,path):
        for j in os.walk(path):
            for p in j[-1]:
                filelpath='{}/{}'.format(j[0],p)
                self.jiexi(filelpath)

if __name__ == '__main__':
    print('-BloodHound information analysis')
    obj=Jiexi()
    if len(sys.argv)>1:
        obj.openfiles(sys.argv[1])
    else:
        print('python jiexi.py <Folder_path>')