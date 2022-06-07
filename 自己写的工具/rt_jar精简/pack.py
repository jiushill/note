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
        self.upackcmd="jar xvf rt.jar"
        self.packcmd="jar cvf output/rt.jar com java javax META-INF org sun sunw"
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
        print("------Unpack rt.jar------")
        print(upackcmd)
        subprocess.call(upackcmd.split(" "))
        os.mkdir("output")
        subprocess.call(self.packcmd.split(" "))
        print("[+] the rt.jar create ok path:{}".format(os.path.join(os.getcwd(),"output","rt.jar")))
if __name__ == '__main__':
    packs=Pack()
    packs.main()
