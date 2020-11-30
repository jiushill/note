from bs4 import BeautifulSoup
import optparse

class nmap_fuck(object):
    def __init__(self,filepath):
        path=open(filepath,"r",encoding="utf-8").read()
        xml=BeautifulSoup(path,"lxml")
        hosts=xml.find_all("host")
        for h in hosts:
            status=h.find_all("status")
            address=h.find_all("address")
            ports=h.find_all("ports")
            if status[0].get("state")=="up":
                print(address[0].get("addr"))
                port=ports[0].find_all("port")
                os = h.find_all('os')
                for data in port:
                    state=data.find_all('state')
                    service=data.find_all('service')
                    service_name=service[0].get('name')
                    service_product=service[0].get('product')
                    version=service[0].get('version')
                    extrainfo=service[0].get('extrainfo')
                    if service_product==None:
                        service_product=""

                    if version==None:
                        version=""

                    if extrainfo==None:
                        extrainfo=""

                    print("{} {}/{} 服务:{} 组件:{} 版本:{} 附件信息:{}".format(data.get('protocol'),data.get("portid"),state[0].get('state'),service_name,service_product,version,extrainfo))

                print("os-->")
                for o in os:
                    for name in o.find_all('osmatch'):
                        print(name.get("name"))

                print('\n'*2)
               # exit()
if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-i',dest="file",help="nmap output xml path")
    (option,args)=parser.parse_args()
    if option.file:
        import os
        if os.path.exists(option.file):
            obj=nmap_fuck(option.file)
        else:
            print('[-] Not Found file:{}'.format(option.file))
            exit()
    else:
        parser.print_help()
        exit()