from gevent import monkey;monkey.patch_all()
import os
import platform
import hashlib
import threadpool
import time

class Check(object):
    def __init__(self):
        try:
            import config
        except:
            print('[-] Not Found config')
            exit()

        self.dirs=config.dirpaths
        self.suffix=config.suffix
        self.task=config.task
        """
        判断操作系统
        """
        if platform.system()=="Windows":
            self.p="\\"
        elif platform.system()=="Linux":
            self.p="/"
        else:
            self.p="/"

        self.founddirs=[] #存在的文件夹路径
        self.ffixpaths=[] #符合后缀名的路径
        self.calc=0 #任务计数器
        self.pool=threadpool.ThreadPool(config.thread) #并非最大进程设置
        self.save=config.save #是否开启保存
        self.filename=config.savefilename #保存文件名
        self.sleep=config.sleep #动态检测开启后，隔指定的秒数进行循环检查
        self.hashfile=[] #成功获取hash的文件与对应的hash
        self.echo=config.echo #是否输出成功获取文件的hash
        self.check=config.check #是否开启动态监测
        self.checkfilelist=[] #从检测开始后文件放在这
        self.id=0 #表明函数调用的次数

    def direxists(self):
        #判断文件夹路径是否存在
        for path in self.dirs:
            if os.path.exists(path):
                self.founddirs.append(path)
            else:
                print('\r [-] Not Found dir path:{}  '.format(path),end='')


    def walk(self):
        #遍历文件夹获取所有文件
        for path in self.founddirs:
            data=os.walk(path)
            for d in data:
                for pv in d[-1]:
                    ffix=str(pv).split('.')
                    if ffix[-1] in self.suffix:
                        path_="{}{}{}".format(d[0],self.p,pv)
                        if self.calc==self.task:
                            self.process_()
                        self.ffixpaths.append(path_)
                        self.calc+=1

        if len(self.ffixpaths)>0:
            self.process_()


    def process_(self):
        rqts=threadpool.makeRequests(self.gethash,self.ffixpaths)
        for r in rqts:
            self.pool.putRequest(r)
        self.pool.wait()
        self.calc = 0
        self.ffixpaths.clear()

    def gethash(self,path):
        #获取文件hash
        if self.id==0:
            listsselect=self.hashfile
        else:
            listsselect=self.checkfilelist

        with open(path,"rb") as op:
            md5=hashlib.md5()
            md5.update(op.read())
            if self.save==False:
                if self.echo==True:
                    print("file:{} md5:{}".format(path,md5.hexdigest()))
                listsselect.append({"file":path,"hash":md5.hexdigest()})
            else:
                if self.echo==True:
                    print("file:{} md5:{}".format(path, md5.hexdigest()))
                print("file:{} md5:{}".format(path, md5.hexdigest()),file=open(self.filename,'r'))

    def checks(self):
        #用于检查开始监测后文件数量是否相等，hash是否一致
        if self.id==0:
            countname=self.hashfile
        else:
            countname=self.checkfilelist

        print('\r[+] get file hash sucess,file count:{}    '.format(len(countname)),end='')
        time.sleep(1)
        if self.id!=0:
            try:
                for nzv in range(0,len(self.checkfilelist)):
                    _=self.hashfile[nzv]
                    if self.checkfilelist[nzv] not in self.hashfile:
                        try:
                            dictsdata_=self.hashfile[self.hashfile.index(self.checkfilelist[nzv])]
                        except:
                            print('\nOriginal file->')
                            afterfile=self.checkfilelist[nzv]['file']
                            afterhash=self.checkfilelist[nzv]['hash']
                            for c in self.hashfile:
                                oritinqlfile=c['file']
                                originalhash=c['hash']
                                if oritinqlfile==afterfile:
                                    print('file:{} md5:{}'.format(oritinqlfile,originalhash))
                                    print('After modification->')
                                    print('file:{} md5:{}'.format(afterfile,afterhash))
                                    self.hashfile.remove(c)
                                    self.hashfile.append(self.checkfilelist[nzv])
                                    break

            except:
                print('\n[!] Increased number of files')
                for x in range(0,len(self.checkfilelist)):
                    if self.checkfilelist[x] not in self.hashfile:
                        filename=self.checkfilelist[x]['file']
                        md5=self.checkfilelist[x]['hash']
                        print('file:{} md5:{}'.format(filename,md5))
                        print('{}'.format(open(filename,'r').read()))
                        self.hashfile.append(self.checkfilelist[x])


            print('\reverything is normal  ',end='')
            time.sleep(1)

if __name__ == '__main__':
    checks=Check()
    checks.direxists()
    print('[*] Walk get file path')
    if checks.check == True:
        print('[+] Start monitoring')
        while True:
            checks.walk()
            checks.checks()
            checks.id+=1
            checks.checkfilelist.clear()
            time.sleep(checks.sleep)
    else:
        checks.walk()
        checks.checks()