from gevent import monkey;monkey.patch_all()
from colorama import Fore,init
from multiprocessing import Process
import gevent
import asyncio
import os
import dns.resolver
import warnings
import config

warnings.filterwarnings("ignore")

init(autoreset=True,wrap=True)

class Domain_Query(object):
    def __init__(self,domain,file,level,process):
        self.domain=domain
        self.level=level
        try:
            self.ptc=int(process)
        except:
            print(Fore.RED+"[-] "+"Please enter the number")
            exit()
        self.resolver = dns.resolver.Resolver(configure=config.defaultdns)
        self.dicts=set()
        self.calc=0
        self.calc2=0
        self.process_=[]
        self.asyncs_=[]
        self.gevent_=[]
        self.blackiplist=config.blackiplist
        self.file=""
        self.opendoamin="{}.txt".format(self.domain)
        if os.path.exists(file):
            self.file=file
            loop=asyncio.get_event_loop()
            tk=loop.create_task(self.load_file(file))
            loop.run_until_complete(tk)
        else:
            print(Fore.RED+"[-] "+"File Not Found:{}".format(file))
            exit()

    async def load_file(self,file):
        with open(file,"r",encoding="utf-8") as rfile:
            if self.level==1:
                for f in rfile:
                    if self.calc==self.ptc:
                        p=Process(target=self.processrun,args=(self.dicts,))
                        p.start()
                        self.calc=0
                        self.dicts.clear()

                    self.dicts.add(str(f).rstrip()+"."+self.domain)
                    self.calc+=1
            else:
                tmp=set()
                code = ""
                code2 = ""
                space = ""
                for j in range(0, 2):
                    code += "{}for data{} in rfile:\n".format(space, j)
                    code2 += "str(data{}).rstrip()+'.'+".format(j)
                    if j != 0:
                        code += " "
                    space += "    "

                code2 = space + "tmp.add(" + code2.rstrip("+") + "+" + "self.domain)\n".format(
                    space + " ")
                code += code2
                exec(code)

                for d in tmp:
                    if self.calc==self.ptc:
                        p=Process(target=self.processrun,args=(self.dicts,))
                        p.start()
                        self.calc=0
                        self.dicts.clear()

                    self.dicts.add(d)
                    self.calc+=1

            if len(self.dicts)>0:
                p = Process(target=self.processrun, args=(self.dicts,))
                p.start()
                self.calc = 0
                self.dicts.clear()

    def processrun(self,data):
        for d in data:
            if self.calc2==self.ptc:
                p=Process(target=self.geven_,args=(self.process_,))
                p.start()
                self.calc2=0
                self.process_=[]
            self.process_.append(d)
            self.calc2+=1

        if len(self.process_)>0:
            p = Process(target=self.geven_, args=(self.process_,))
            p.start()
            self.calc2 = 0
            self.process_ = []

    def geven_(self,data):
        for d in data:
            self.gevent_.append(gevent.spawn(self.domain_query,d))
        gevent.joinall(self.gevent_)
        self.gevent_=[]

    def get_type_id(self,name):
        return dns.rdatatype.from_text(name)

    def domain_query(self,domain):
        ipaddress=[]
        cnames=[]
        try:
            record = self.resolver.query(domain)
            for A_CNAME in record.response.answer:
                for item in A_CNAME.items:
                    if item.rdtype == self.get_type_id('A'):
                        if str(item) in self.blackiplist:
                            break
                        else:
                            ipaddress.append(str(item))
                    elif item.rdtype == self.get_type_id('CNAME'):
                        cnames.append(str(item))
        except:
            pass

        if len(cnames)>0:
            cname=",CNAME {}".format(",".join(cnames))
        else:
            cname=""

        if len(ipaddress)>1:
            print("domain:{} ip:{} CDN:{} DNS type:{} {}".format(domain, ",".join(ipaddress), "存在", "A", cname))
            print("domain:{} ip:{} CDN:{} DNS type:{} {}".format(domain,",".join(ipaddress),"存在","A",cname),file=open(self.opendoamin,"a",encoding="utf-8"))
        elif len(ipaddress)==1:
            print("domain:{} ip:{} CDN:{} DNS type:{} {}".format(domain, ",".join(ipaddress), "不存在", "A", cname))
            print("domain:{} ip:{} CDN:{} DNS type:{} {}".format(domain,",".join(ipaddress), "不存在", "A",cname),file=open(self.opendoamin,"a",encoding="utf-8"))



if __name__ == '__main__':
    banner='''                                                                                                                   
YYYYYYY       YYYYYYY                                        iiii  
Y:::::Y       Y:::::Y                                       i::::i 
Y:::::Y       Y:::::Y                                        iiii  
Y::::::Y     Y::::::Y                                              
YYY:::::Y   Y:::::YYYaaaaaaaaaaaaayyyyyyy           yyyyyyyiiiiiii 
   Y:::::Y Y:::::Y   a::::::::::::ay:::::y         y:::::y i:::::i 
    Y:::::Y:::::Y    aaaaaaaaa:::::ay:::::y       y:::::y   i::::i 
     Y:::::::::Y              a::::a y:::::y     y:::::y    i::::i 
      Y:::::::Y        aaaaaaa:::::a  y:::::y   y:::::y     i::::i 
       Y:::::Y       aa::::::::::::a   y:::::y y:::::y      i::::i 
       Y:::::Y      a::::aaaa::::::a    y:::::y:::::y       i::::i 
       Y:::::Y     a::::a    a:::::a     y:::::::::y        i::::i 
       Y:::::Y     a::::a    a:::::a      y:::::::y        i::::::i
    YYYY:::::YYYY  a:::::aaaa::::::a       y:::::y         i::::::i
    Y:::::::::::Y   a::::::::::aa:::a     y:::::y          i::::::i
    YYYYYYYYYYYYY    aaaaaaaaaa  aaaa    y:::::y           iiiiiiii
                                        y:::::y                    
                                       y:::::y                     
                                      y:::::y                      
                                     y:::::y                       
                                    yyyyyyy                        
                雷电女王的鬼凯                            '''
    print(banner)
    file=config.dictpath
    doamin=config.domain
    level=config.level
    if '-' in level:
        level=str(level).split("-")
        for x in range(int(level[0]),int(level[1])):
            obj=Domain_Query(doamin,file,x,config.process)
    else:
        obj = Domain_Query(doamin, file, level, config.process)