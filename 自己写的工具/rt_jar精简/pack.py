import os
import config
import shutil
import subprocess

class Pack(object):
    def __init__(self):
        self.blackpackge=[".jna."]
        [self.blackpackge.append(tmp) for tmp in config.BLACKPATH]
        self.runpath=config.RUNJARPATH
        self.rtjarpath=config.RTJARPATH
        self.jarname=self.rtjarpath.split(os.sep)[-1]
        self.upackcmd="jar xvf {}".format(self.jarname)
        self.packcmd="jar cvf output/{} com java javax META-INF org sun sunw".format(self.jarname)
        if os.path.exists("output"):
            shutil.rmtree("output")
            os.mkdir("output")
        else:
            os.mkdir("output")
        shutil.copy(self.rtjarpath,os.path.join(os.getcwd(),"output"))
        os.chdir(os.path.join(os.getcwd(),"output"))

    def getcore(self,commandresult):
        loaded=[]
        for tmp in commandresult.split("\n"):
            if "[Loaded" in tmp:
                packagename=tmp.split(" ")[1]
                if packagename not in self.blackpackge:
                    loaded.append(packagename)
        return loaded

    def main(self):
        cmdarg="java -jar -XX:+TraceClassLoading \"{path}\" aaaa".format(path=self.runpath)
        result=os.popen(cmdarg).read()
        core=self.getcore(result)
        print("[*] load class count:{}".format(len(core)))
        print("------Load Class------")
        for number in range(len(core)):
            print(core[number])
            core[number]=core[number].replace(".","/")
        upackcmd=self.upackcmd+" {}".format(" ".join(core))
        print("------Unpack {}------".format(self.jarname))
        print(upackcmd)
        subprocess.call(upackcmd.split(" "))
        os.mkdir("output")
        subprocess.call(self.packcmd.split(" "))
        print("[+] the rt.jar create ok path:{}".format(os.path.join(os.getcwd(),"output",self.jarname)))
if __name__ == '__main__':
    packs=Pack()
    packs.main()
