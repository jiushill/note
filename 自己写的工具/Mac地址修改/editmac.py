import winreg
import random
import re

class MacEdit(object):
    def __init__(self):
        self.networkname='Intel(R) Wi-Fi 6 AX200 160MHz' #要修改的网卡的名称
        self.path=r"SYSTEM\CurrentControlSet\Control\Class"

    def randommac(self):
        data = ["2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        data2 = ["2", "6", "A", "E"]
        hz = ""
        for k in range(0,9):
            hz += random.choice(data)
        mac = "0{}{}".format(random.choice(data2), hz)
        while len(mac)!=12:
            mac+=random.choice(data)
        return mac

    def foreachkey(self,key,path):
        i = 0
        subkeys = []
        try:
            while True:
                subkey = winreg.EnumKey(key, i)
                subkeys.append(path + "\\" + subkey)
                i += 1
        except Exception as r:
            if "[WinError 259]" in str(r):
                return subkeys



    def searchnetwork(self):
        key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self.path)
        ID=self.foreachkey(key,self.path)
        winreg.CloseKey(key)
        print("[<*>] Search Key ing")

        networkpath=[]
        for k in ID:
            if '08002be10318}' in str(k).lower():
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, k)
                names=self.foreachkey(key,k)
                winreg.CloseKey(key)
                for n in names:
                    if len(re.findall("[0-9]{1,}",n))!=0:
                        try:
                            o=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,n)
                            DriverDesc=winreg.QueryValueEx(o,'DriverDesc')
                            winreg.CloseKey(o)
                            if self.networkname==DriverDesc[0]:
                                networkpath.append(n)
                        except Exception as r:
                            if "[WinError 5]" in str(r):
                                pass
                      #  value=winreg.QueryValueEx(o,'DriverDesc')
        if len(networkpath)==0:
            print("[<->] No network card")
            exit()

        mac=self.randommac()
      #  print(networkpath[0])
        try:
            key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,networkpath[0],0,winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key,'NetWorkAddress','',winreg.REG_SZ,mac)
            print('[<+>] setting Mac Address:{}'.format(mac))
            winreg.CloseKey(key)
        except Exception as r:
            if '[WinError 5]' in str(r):
                print('[<->] Access is Denied,Set Mac failure')

if __name__ == '__main__':
    obj=MacEdit()
    obj.searchnetwork()
