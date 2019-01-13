#coding:utf-8
'''
@atuhor:九世
@time:2019/1/1
'''
import requests
import threading
import os
import re

id_list=[]

print('网易云音音下载')
print('请输入文件名：')

user = input('music_file:')
dk=open('{}'.format(user),'r')
if os.path.exists(user):
    print('[+] Found {}'.format(user))
else:
    print('[-] Not Found {}'.format(user))
    exit()

for k in dk.readlines():
    qc="".join(k.split('\n'))
    tq=re.findall('id=.*&',str(qc))
    for l in tq:
        sc=str(l).replace('id=','').replace('&','')
        id_list.append(sc)

headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
def demo(url,userid):
    rqt=requests.get(url=url,headers=headers)
    if rqt.status_code==200:
        dk=open('{}.mp3'.format(userid),'wb')
        dk.write(rqt.content)
        dk.close()
        if os.path.exists('{}.mp3'.format(userid)):
            print('[+] Foubd {}.mp3'.format(userid))
        else:
            print('[-] Not Found {}.mp3'.format(userid))
if __name__ == '__main__':
    for p in id_list:
        user_id=p
        rgt='http://music.163.com/song/media/outer/url?id={}'.format(user_id)
        rq=requests.get(url=rgt,headers=headers)
        url="{}".format(rq.url)
        t=threading.Thread(target=demo,args=(url,user_id))
        t.start()
