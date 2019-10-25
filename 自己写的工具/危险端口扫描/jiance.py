#@author:九世
#@time:2019/10/25
#@file:jiance.py

import matplotlib.pyplot as plt

class Tonji(object):
    def __init__(self,port,bdy):
        self.black_port={} #黑名单端口
        for j in port:
            self.black_port[j]=0

        self.bdy=bdy #黑名单端口对应的名称

    def open_files(self):
        dk=open('save.txt','r',encoding='utf-8')
        for t in dk.readlines():
            data="".join(t.split('\n'))
            yield data

    def create_img(self):
        for u in self.open_files():
            dc=str(u).split(':')
            host=dc[0]
            port=dc[1]
            if port in self.black_port:
                self.black_port[port]+=1

        plt.axes(aspect=1)
        plt.pie(x=self.black_port.values(), labels=self.bdy, autopct='%3.1f%%',labeldistance=1.15)  # 饼图设置plt.pie()
        plt.legend(loc='lower right')
        plt.title('Port statistics')
        plt.savefig('port.png')
        plt.show()

if __name__ == '__main__':
    obj=Tonji(['1433','3306','80','554','139'],['MSSQL','MYSQL','Web','Video source','shared'])
    obj.create_img()
