#@author:九世
#@file:spliter.py
#@time:2019/10/10

from colorama import init,Fore,Style
import os

init(wrap=True)

class Options(object):
    def __init__(self):
        self.dicts=[]


    def read_data(self,name,domain):
        with open(name,'r',encoding='utf-8') as r:
            for x in r.readlines():
                data='http://'+"".join(x.split('\n'))+'.'+str(domain)
                yield data

    def load_files(self,domain):
        if os.path.exists('dicts'):
            print(Fore.YELLOW+'[INFO] 字典文件夹是存在的')
        else:
            print(Fore.RED+'[ERROR] 字典文件夹是不存在的')
            exit()

        paths=os.listdir('dicts')
        if int(len(paths))==0:
            print(Fore.RED+'[INTO] 字典不存在，将无法进行爆破')
        else:
            print(Fore.WHITE+'[INFO] 发现如下字典:{}'.format(paths))
            print('[LOAD] 读取字典中')
            for file_name in paths:
                for g in self.read_data('dicts/{}'.format(file_name),domain=domain):
                    self.dicts.append(g)

            print(Fore.YELLOW+'[INFO] 加载字典完成,字典数量:{}'.format(len(self.dicts)))
            return self.dicts