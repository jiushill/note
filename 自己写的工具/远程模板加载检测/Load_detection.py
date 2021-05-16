import zipfile
import os
import optparse
from bs4 import BeautifulSoup

def test(file):
    print("file--->:{}".format(file))
    hz=["doc","docx","xlsm","xls","docm","pptm","xlsx","pptx","ppt","dotm"]
    ez=b"<?xml"
    if os.path.exists(file):
        z=zipfile.ZipFile(file,"r")
        for pathname in z.namelist():
            data=z.open(pathname).read()
            if ez==data[0:5]:
                xml=BeautifulSoup(data,"lxml")
                relationships=xml.find_all("relationship")
                if len(relationships)!=0:
                    for r in relationships:
                        hz_=r["target"]
                        if str(hz_).split(".")[-1] in hz or "http" in hz:
                            print("fileanme:{} --- {}".format(pathname,hz_))
    else:
        print("File Not Found:{}".format(file))

if __name__ == '__main__':
    print("Remote template loading detection")
    parser=optparse.OptionParser()
    parser.add_option('-f',dest="file",help="set file")
    option,args=parser.parse_args()
    if option.file:
        test(option.file)
    else:
        print("Load_detection.py -f test.doc")
        parser.print_help()