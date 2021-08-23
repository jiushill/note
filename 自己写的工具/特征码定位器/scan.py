import pefile
import os
import optparse

fpath="样本2"
dpath=os.path.join(fpath,"dump")
if os.path.exists(fpath)==False:
    os.mkdir(fpath)

if os.path.exists(dpath)==False:
    os.mkdir(dpath)

for px in os.walk(fpath):
    [os.remove(os.path.join(px[0],p)) for p in px[-1]]

def Sectionfill(path):
    basename=os.path.join(dpath,os.path.basename(path))
    data=open(path,"rb").read()
    sectionlist={}
    sectiondata={}
    pe=pefile.PE(path)
    for section in pe.sections:
       # print(section)
        sectionlist[section.Name.decode().replace("\x00","")]={"RVA":section.PointerToRawData,"VASize":section.Misc_VirtualSize}


    for k in sectionlist:
        sectionrva=sectionlist[k]["RVA"]
        sectionsize=sectionlist[k]["VASize"]
        end=sectionrva+sectionsize
        sectiondata[k]=data[sectionrva:end]

    print("[*] 区段单独dump")
    for name in sectiondata:
        print("name:{} 位置范围:{}-{} 数据:{}".format(name,sectionlist[name]["RVA"],sectionlist[name]["RVA"]+sectionlist[name]["VASize"],sectiondata[name]))
        fw=open("{}_{}".format(basename,name),"wb")
        fw.write(sectiondata[name])

    print("[*] 区段组合dump测试 (求可能性)")
    calc=0
    for d in range(len(sectiondata)):
        print("x:{}".format(d))
        tname="填充了"
        for c in range(calc,d+1):
            keyname=list(sectiondata.keys())[c]
            tname+=keyname
            print("填充{}".format(tname))
            fb=open(os.path.join(fpath,tname),"wb")
            fb.write(data.replace(sectiondata[keyname],b"\x00"))
            calc = c

        if d+1==len(sectiondata):
            keyname=list(sectiondata.keys())[d]
            tname="填充{}".format(keyname)
            print("填充:{}".format(tname))
            fb = open(os.path.join(fpath, tname), "wb")
            fb.write(data.replace(sectiondata[keyname], b"\x00"))

    startfilelist=os.listdir(fpath)
    input("等待文件全部写入完毕后，杀毒扫描文件夹并删除所有被杀文件后进入下一步 （建议等待个几秒，有些杀毒检测会延迟几秒才弹出被杀文件）（按任意键进入特征码检测）>")
    endfilelist=os.listdir(fpath)
    for e in endfilelist:
        for s in startfilelist[:]:
            if e==s:
                startfilelist.remove(s)

    sec=set()
    for c in endfilelist:
        name=c.replace("填充了","").split(".")
        if len(name)==2:
            sec.add(".{}".format(name[-1]))

    print("[*] 被杀区段定位 (在按下任意键后还弹出杀毒拦截删除文件，请忽略这个文件的结果)")
    print(sec)

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-f',dest='path',help='待检测的文件')
    (option,args)=parser.parse_args()
    if option.path:
        if os.path.exists(option.path):
            Sectionfill(option.path)
        else:
            print("[-] file not found")
    else:
        print("python3 get.py -f <path>")
        parser.print_help()