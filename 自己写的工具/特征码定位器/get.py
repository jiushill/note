import os
import binascii
import pefile
import optparse

fpath="样本2"
dpath=os.path.join(fpath,"dump")
if os.path.exists(fpath)==False:
    os.mkdir(fpath)

if os.path.exists(dpath)==False:
    os.mkdir(dpath)

def removefiles():
    for px in os.walk(fpath):
        [os.remove(os.path.join(px[0],p)) for p in px[-1]]

def bytesplit(data,basename,startaddress,endaddress):
    byteuser=input("字节分割>")
    try:
        number=int(byteuser)
    except:
        print("[-] 不是数字...")
        exit()

    id=1
    while True:
        startdata=data[0:startaddress]
        tmp=b""
        serialnumber={}
        for num in range(startaddress,endaddress):
            tmp+=data[num:num+1]
            if len(tmp)==number:
                startdata+=tmp
                if id==1:
                    print("size:{} byte:{} Hex:{}".format(len(startdata),tmp,binascii.hexlify(tmp)),file=open("{}out.txt".format(basename),"a"))
                serialnumber[len(startdata)]={"Data":tmp,"Hex":binascii.hexlify(tmp)}
                with open(os.path.join(fpath,"{}{}.bin".format(basename,len(startdata))),"wb") as f:
                    f.write(startdata)
                tmp=b""
        startfiles=os.listdir(fpath)
        user=input("等待文件全部写入完毕后，杀毒扫描文件夹并删除所有被杀文件后进入下一步 （建议等待个几秒，有些杀毒检测会延迟几秒才弹出被杀文件）（按任意键进入特征码检测）>")
        endfiles=os.listdir(fpath)
        for e in endfiles:
            for s in startfiles[:]:
                if e==s:
                    startfiles.remove(s)

        listnumber=[]
        for nbr in startfiles:
            name=nbr.replace(basename,"").replace(".bin","")
            listnumber.append(name)
        listnumber=sorted(listnumber) #从小到大排序找出第一个被检测出有特征码的文件
        if len(listnumber)>0:
            print("特征码:")
            if int(listnumber[0]) in serialnumber:
                ma=serialnumber[int(listnumber[0])]
                signature=serialnumber[int(listnumber[0])]["Data"]
                print(ma)
                data=data.replace(signature,b"\x00\x00\x00\x00") #特征码替换为4个0重新检测
            else:
                print("没有发现特征码")
                user=input("是否继续检测，有些杀毒会有一些问题。例如火绒，到没有发现特征码程序结束后又会弹出杀的文件 (输入y继续检测/非y退出)")
                if user=="y":
                    continue
                else:
                    break
        else:
            print("没有发现特征码")
            break
        id += 1

def getdaata(path):
    fdata=open(path,"rb").read()
    pe=pefile.PE(path)
    sectionlist={}
    for section in pe.sections:
        sectionlist[section.Name.decode().replace("\x00","")]={"RVA":section.PointerToRawData,"VASize":section.Misc_VirtualSize,"End":section.PointerToRawData+section.Misc_VirtualSize}
    print(sectionlist)
    user=input("地址范围设置>").split("-")
    if len(user)==2:
        try:
            startaddress = int(user[0])
            endaddress = int(user[1])
            bytesplit(fdata,os.path.basename(path), startaddress, endaddress)
        except Exception as error:
            print("[-] 错误的地址范围设置....")
            print(error)
            exit()
    else:
        print("[-] 范围设置错误")

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-f',dest='path',help='寻找特征码的文件')
    (option,args)=parser.parse_args()
    if option.path:
        path=option.path
        if os.path.exists(path):
            removefiles()
            getdaata(path)
        else:
            print('[-] path not found')
    else:
        print("python3 get.py -f <path>")
        parser.print_help()