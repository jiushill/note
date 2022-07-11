import binascii
import re
import optparse
import os

def unicode_enc(searchdata):
    result={}
    for textdata in searchdata:
        textdata=textdata.split("(")[0]
        tmp=""
        for text in textdata:
            if text!=".":
                hexdata = "\\u00{}".format(binascii.hexlify(text.encode()).decode())
                tmp+=hexdata
            else:
                tmp+=text
        result[textdata]=tmp
    return result

def main(webshellfilename):
    savefilename=webshellfilename.split(".")
    del savefilename[-1]
    savefilename="{}_unicode_utf_16.txt".format(".".join(savefilename))
    rdata=open(webshellfilename,"r",encoding="utf-8").read()
    search=re.findall("[.][a-z-A-Z-0-9-.]{1,}[(]",rdata)
    if len(search)>0:
        enc=unicode_enc(search)
        for keyname in enc.keys():
            rdata=rdata.replace(keyname,enc[keyname])
    print(rdata)
    print(rdata,file=open(savefilename,"a",encoding="utf-8"))
    print("[+] save file in:{}".format(savefilename))
if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-f",dest="file",help="要编码的webshell文件")
    (option,args)=parser.parse_args()
    if(option.file):
        file=option.file
        if os.path.exists(file):
            print("[+] unicode utf16 encode")
            main(file)
        else:
            print("[-] file:{} not found".format(file))
            exit()
    else:
        print("usage:python enc.py -f <webshell_path>")
        parser.print_help()