#dll proxy
import pefile
import optparse
import os

def test(path):
    if os.path.exists(path)==False:
        print("[-] File Not Found:{}".format(path))
    else:
        dllname=str(path).split("\\")[-1].split(".")[0]
        print(dllname)
        formats="#pragma comment(linker,\"/export:{funcion}={dllname}.{funcion_},@{ordinal}\")"
        pe=pefile.PE(path)
        modules=pe.DIRECTORY_ENTRY_EXPORT.symbols
        for module in modules:
            modulename=module.name.decode()
            print(formats.format(funcion=modulename,dllname=dllname,funcion_=modulename,ordinal=module.ordinal))

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-f',dest="file",help="Dll Path")
    (option,args)=parser.parse_args()
    if option.file:
        test(option.file)
    else:
        print("Usage:python create2.py -f C:\\Windows\\System\\kernel32.dll")
        parser.print_help()