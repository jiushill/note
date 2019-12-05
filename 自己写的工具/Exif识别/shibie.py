'''
#@author:九世
#@time:2019/11/28
#@file:shibie.py
'''

import exifread
import os
import re


class Query(object):
    def __init__(self):
        print('Exif信息查询')
        print('1.单个图片查询')
        print('2.批量查询')
        xw=input('Please>')
        if xw=='1':
            file=input('文件路径>')
            if True==self.pd(file):
                self.query(file)

        elif xw=='2':
            files=input('文件夹路径>')
            if True==self.pd(files):
                self.listfile(files)

    def zuanhuan(self,text):
        jv=[]
        for r in text:
            jv.append(str(r).replace(' ',''))

        data=str(float(jv[0]) + float(jv[1])/60 + float(jv[2])/3660)
        return data

    def query(self,file):
        print('图片名称:{}'.format(file))
        dk=open(file,'rb')
        exif_data=exifread.process_file(dk)
        try:
            g=[c for c in exif_data]
            if 'GPS GPSVersionID' in g:
                print('[+] 发现GPS信息')
                jd=str(exif_data['GPS GPSLatitude']).replace('[','').replace(']','').split(',')
                jds=""
                jdss=[]
                for y in range(0,len(jd)):
                    if '/' in jd[y]:
                        data=jd[y].split('/')
                        jds+=str(int(data[0].lstrip())/int(data[1]))
                        jdss.append(str(int(data[0].lstrip())/int(data[1])))
                    else:
                        jds+=jd[y]
                        jdss.append(jd[y])

                    if y==0:
                        jds+="°"
                    elif y==1:
                        jds+="'"
                jds=jds.replace(' ','')+'"'

                wd = str(exif_data['GPS GPSLongitude']).replace('[', '').replace(']', '').split(',')
                wds=""
                wdss=[]
                for y in range(0,len(wd)):
                    if '/' in wd[y]:
                        data=wd[y].split('/')
                        wds+=str(int(data[0].lstrip())/int(data[1]))
                        wdss.append(str(int(data[0].lstrip())/int(data[1])))
                    else:
                        wds+=wd[y]
                        wdss.append(wd[y])

                    if y==0:
                        wds+="°"
                    elif y==1:
                        wds+="'"

                wds=wds.replace(' ','')+'"'

                print('纬度:{} 纬度度分秒格式:{}'.format(jds,self.zuanhuan(jdss)))
                print('经度:{} 经度度分秒格式:{}'.format(wds,self.zuanhuan(wdss)))
            else:
                print('[-] 无GPS信息')

            if 'Image Make' in g:
                print('制造商:{}'.format(exif_data['Image Make']))
            else:
                print('[-] 无制造商信息')

            if 'Image Model' in g:
                print('型号:{}'.format(exif_data['Image Model']))
            else:
                print('[-] 无型号信息')

            if 'Image DateTime' in g:
                print('拍摄时间:{}'.format(exif_data['Image DateTime']))
            else:
                print('[-] 无拍摄时间信息')
        except Exception as r:
            print('Error {}'.format(r))
        dk.close()
        print('')

    def pd(self,file):
        if os.path.exists(file):
            return True
        else:
            print('[-] {}不存在'.format(file))

    def listfile(self,file):
        hq=os.listdir(file)
        for u in hq:
            path='{}/{}'.format(file,u)
            self.query(path)

if __name__ == '__main__':
    obj=Query()