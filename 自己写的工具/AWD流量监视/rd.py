import os
import binascii

dk2=open('jg.pcap','wb')
class Rfile(object):
    def __init__(self):
        self.calc=0
    def read_file(self,file):
        dk=open(file,'rb').read()
        if self.calc>0:
            data=binascii.unhexlify(bytes.decode(binascii.hexlify(dk)).replace('d4c3b2a1020004000000000000000000ffff000001000000',''))
        else:
            data=dk

        dk2.write(data)
        self.calc+=1

if __name__ == '__main__':
    obj=Rfile()
    files_list=os.walk('file')
    for c in files_list:
        for k in c[2]:
            obj.read_file('file/{}'.format(k))
    print('写入pcap文件完成')