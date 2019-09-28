#@author:九世
#@time:2019/9/28
#@file:qz.py

import winreg

class Diaocha(object):
    def __init__(self):
        self.path=winreg.HKEY_USERS

    def client_name(self):
        data=''
        datas=''
        jg=[]
        jg2=[]
        try:
            key=winreg.OpenKey(self.path,None,0,winreg.KEY_ALL_ACCESS)
            ckey=winreg.QueryInfoKey(key)[0]
            for c in range(int(ckey)):
                name=winreg.EnumKey(key,c)
                if len(name)>8 and len(name)<54:
                    jg.append(name)

            winreg.CloseKey(key)
            dk=winreg.OpenKey(self.path,'{}\\Volatile Environment'.format(jg[0]),0,winreg.KEY_ALL_ACCESS)
            yk=winreg.QueryInfoKey(dk)[0]
            for v in range(yk):
                gs=winreg.EnumKey(dk,v)
                dv=winreg.OpenKey(self.path,'{}\\Volatile Environment\\{}'.format(jg[0],gs),0,winreg.KEY_ALL_ACCESS)
                qzhi_value=winreg.QueryValueEx(dv,'SESSIONNAME')
                client_naems=winreg.QueryValueEx(dv,'CLIENTNAME')
                data+='会话名称:{}'.format(qzhi_value[0])
                data+=' 登录本机的客户端名称:{}'.format(client_naems[0])
            winreg.CloseKey(dv)
            winreg.CloseKey(dk)
            print('[+] :{}'.format(data))
            dk = winreg.OpenKey(self.path, '{}\\Software\\Microsoft\\Terminal Server Client\\Servers'.format(jg[0]), 0, winreg.KEY_ALL_ACCESS)
            vt=winreg.QueryInfoKey(dk)[0]
            for y in range(int(vt)):
                values = winreg.EnumKey(dk, y)
                jg2.append(values)
            winreg.CloseKey(dk)
            for u in jg2:
                dk=winreg.OpenKey(self.path,'{}\\Software\\Microsoft\\Terminal Server Client\\Servers\\{}'.format(jg[0],u),0,winreg.KEY_ALL_ACCESS)
                quzhi=winreg.QueryValueEx(dk,'UsernameHint')[0]
                print('[+] 登录过的RDP连接:{} 登录使用的用户名:{}'.format(u,quzhi))
                winreg.CloseKey(dk)
            dk=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,'SYSTEM\\CurrentControlSet\\services\\eventlog\\Security')
            qz=winreg.QueryValueEx(dk,'MaxSize')[0]
            print('[+] 日志最大限制:{}'.format(qz))
            winreg.CloseKey(dk)

            dk=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,'System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\RDP-Tcp',0,winreg.KEY_ALL_ACCESS)
            portnumber=winreg.QueryValueEx(dk,'PortNumber')[0]
            print('[+] 本机RDP端口:{}'.format(portnumber))
            winreg.CloseKey(dk)

        except Exception as r:
            print('Error {}'.format(r))

if __name__ == '__main__':
    obj=Diaocha()
    obj.client_name()
