import os
import optparse
import data

lists=data.data


def query(*args,**kwargs):
    file=args[0]
    if os.path.exists(file):
        print("[*] Query SUID")
        dk=open(file,"r",encoding="utf-8").read().split("\n")
        for uid in dk:
            data=uid.split("/")[-1]
            for v in lists.keys():
                if v==data:
                    print("! UID command:{}".format(v))
                    print("Exec Command:")
                    print(lists[data])
                    print("")

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-f',dest='file',help='set file')
    (option,args)=parser.parse_args()
    if option.file:
        query(option.file)
    else:
        parser.print_help()
        exit()