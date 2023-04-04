from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcom.wmi import IWbemServices
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dtypes import NULL
from impacket.structure import Structure
from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_PRIVACY
import logging
import sys
import time
from io import StringIO
import optparse
import colorama

def printReply(iEnum):
    current=sys.stdout
    sys.stdout = StringIO()
    printHeader = True
    while True:
        try:
            pEnum = iEnum.Next(0xffffffff, 1)[0]
            record = pEnum.getProperties()
            if printHeader is True:
                print('|', end=' ')
                for col in record:
                    print('%s |' % col, end=' ')
                print()
                printHeader = False
            print('|', end=' ')
            for key in record:
                if type(record[key]['value']) is list:
                    for item in record[key]['value']:
                        print(item, end=' ')
                    print(' |', end=' ')
                else:
                    print('%s |' % record[key]['value'], end=' ')
            print()
        except Exception as e:
            if logging.getLogger().level == logging.DEBUG:
                import traceback
                traceback.print_exc()
                sys.exit(1)
            if str(e).find('S_FALSE') < 0:
                raise
            else:
                break

    result=sys.stdout.getvalue()
    sys.stdout = current
    return result
    iEnum.RemRelease()
    sys.stdout=current


def wmiconnect(ip='', username='', password='',domain='',hashes='',aesKey=''):
    if len(hashes) > 0:
        lmhash, nthash = hashes.split(':')
    else:
        lmhash, nthash = ("", "")

    result=""
  #  smbConnection = SMBConnection(ip, ip)
    try:
        dcom = DCOMConnection(ip, username, password, domain, lmhash, nthash, aesKey, oxidResolver=True,doKerberos=False, kdcHost=None)
        iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        return (dcom,iWbemLevel1Login)

    except  (Exception, KeyboardInterrupt) as e:
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        logging.error(str(e))
       # if smbConnection is not None:
       #     smbConnection.logoff()
        dcom.disconnect()
        sys.stdout.flush()
        sys.exit(1)

    dcom.disconnect()
    sys.exit(1)


def getProcessList(ip='', username='', password='',domain='',hashes='',aesKey='',query=False):
    print("[*] Get Process List")
    result_echoformat=""
    dcom,iWbemLevel1Login=wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin("//./root/cimv2", NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32Process, _ = iWbemServices.GetObject("Win32_Process")
    ProcessList = iWbemServices.ExecQuery("SELECT * from Win32_Process")
    process_result = printReply(ProcessList)
    split_process_result=process_result.split("\n")
    for process in range(1,len(process_result)):
        try:
            fg_process=split_process_result[process].split("|")
            processname=fg_process[1].lstrip().rstrip()
            create_process_time=time.strftime("%Y-%m-%d-%H:%M:%S",time.strptime(fg_process[9].split(".")[0].lstrip().rstrip(),"%Y%m%d%H%M%S"))
            processpid=fg_process[10].lstrip().rstrip()
            commandline=fg_process[-2].lstrip().rstrip()
            echoformat="{} {} {} {}".format(processname,processpid,commandline,create_process_time)
            result_echoformat+=echoformat+"\r\n"
            print(echoformat)

        except Exception as error:
            pass

    if query == True:
        print("========================================TASKLIST QUERY====================================================")
        print()
        import check
        check.process_check(result_echoformat)
    dcom.disconnect()


def userquery(ip='', username='', password='',domain='',hashes='',aesKey=''):
    print("[*] UserAccount")
    dcom,iWbemLevel1Login=wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin("//./root/cimv2", NULL, NULL)
    iWbemLevel1Login.RemRelease()
    win32UserAccount, _ = iWbemServices.GetObject("Win32_UserAccount")
    UserAccount = iWbemServices.ExecQuery("SELECT * from Win32_UserAccount")
    userlist=printReply(UserAccount)
    user_splist = userlist.split("\n")
    for user in range(0, len(user_splist)):
        try:
           print(user_splist[user])

        except Exception as error:
            pass

    dcom.disconnect()

def enablerdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)!=1 and int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()

    print("[*] Enable/Disable RDP")
    dcom,iWbemLevel1Login=wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2/TerminalServices', NULL, NULL)
    iWbemServices.get_dce_rpc().set_auth_level(RPC_C_AUTHN_LEVEL_PKT_PRIVACY)
    iWbemLevel1Login.RemRelease()
    WQL = r"""SELECT * FROM Win32_TerminalServiceSetting"""
    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    if int(isenable)==1:
        iWbemClassObject.SetAllowTSConnections(1, 1) #Enable RDP
    else:
        iWbemClassObject.SetAllowTSConnections(0, 0)  # Disable RDP

    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    result = dict(iWbemClassObject.getProperties())
    if result['AllowTSConnections']['value']==1:
        print("[+] Enable RDP Open Sucess")
    elif result['AllowTSConnections']['value']==0:
        print("[+] Disable RDP Sucess")
    iWbemServices.RemRelease()

    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")
    rdpport=StdRegProv.GetDWORDValue(2147483650,"SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp","PortNumber")
    print("[*] RDP Port:{}".format(rdpport.uValue))
    dcom.disconnect()

def enable_pth_login_rdp(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)!=1 and int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()
    print("[*] Enable/disable pth login rdp")
    dcom,iWbemLevel1Login=wmiconnect(ip,username,password,domain,hashes,aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    StdRegProv, resp = iWbemServices.GetObject("StdRegProv")

    if int(isenable)==1:
        pth_open=StdRegProv.SetDWORDValue(2147483650,"System\\CurrentControlSet\\Control\\Lsa","DisableRestrictedAdmin",0)
        if pth_open.ReturnValue==0:
            print("[+] Enable PTH Rdp Login Sucess")
    else:
        pth_open = StdRegProv.DeleteValue(2147483650, "System\\CurrentControlSet\\Control\\Lsa","DisableRestrictedAdmin")
        if pth_open.ReturnValue == 0:
            print("[+] Disable PTH Rdp Login Sucess")
    dcom.disconnect()

def winrm_enable(ip='', username='', password='',domain='',hashes='',aesKey='',isenable=0):
    if int(isenable)!=1 and int(isenable)!=0:
        print("[-] Pluse Query Help,Thanks....")
        exit()
    print("[*] Enable/Disable winrm")
    dcom, iWbemLevel1Login = wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
    WQL = 'select * from Win32_Service where Name="WinRM"'
    iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
    iWbemClassObject = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
    if int(isenable)==1:
        if iWbemClassObject.StartService().ReturnValue==0 or iWbemClassObject.StartService().ReturnValue==10:
            print("[+] winrm Service Start")
    elif int(isenable)==0:
        stopcode=iWbemClassObject.StopService().ReturnValue
        print("[*] WinRm Stop Service Return Code:{}".format(stopcode))
        if stopcode==0 or stopcode==5:
            print("[+] winrm Service Stop")


    if int(isenable) == 1:
        print("[*] Enable Winrm Service")
        InstanceIDlist=["WINRM-HTTP-In-TCP","WINRM-HTTP-In-TCP-PUBLIC"]
        try:
            iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
        except Exception as error:
            if "WBEM_E_INVALID_NAMESPACE" in str(error):
                iWbemServices=None

        if iWbemServices!=None:
            for InstanceIDName in InstanceIDlist:
                try:
                    WQL2 = "SELECT * FROM MSFT_NetProtocolPortFilter where InstanceID = \"{}\"".format(InstanceIDName)
                    firewall_list = iWbemServices.ExecQuery(WQL2)
                    while True:
                            pEnum = firewall_list.Next(0xffffffff, 1)[0]
                            InstanceID = pEnum.InstanceID
                            print("[*] Enable Firewall Rule InstanceID:{}".format(InstanceID))
                            MSFT_NetProtocolPortFilter = iWbemServices.ExecQuery(
                                "select * from MSFT_NetFirewallRule where InstanceID=\"{}\"".format(InstanceID)).Next(0xffffffff, 1)[0]
                            result = dict(MSFT_NetProtocolPortFilter.getProperties())
                            Enabled = MSFT_NetProtocolPortFilter.Enabled
                            if Enabled == 2:
                                firewall_Instance = MSFT_NetProtocolPortFilter.SpawnInstance()
                                firewall_Instance.Enabled = 1
                                firewall_Instance.CreationClassName = "fuckyouaasasasaasas"
                                firewall_Instance.PolicyRuleName = ""
                                firewall_Instance.SystemCreationClassName = ""
                                firewall_Instance.SystemName = ""
                                # allow=2, allowBypass=3, Block=4
                                firewall_Instance.Action = 2
                                firewall_Instance.Caption = ""
                                firewall_Instance.CommonName = ""
                                firewall_Instance.ConditionListType = 3
                                firewall_Instance.Description = ""
                                firewall_Instance.Direction = 1
                                firewall_Instance.DisplayGroup = ""
                                firewall_Instance.DisplayName = "AAAAAAAAAAAAAAA"
                                firewall_Instance.EdgeTraversalPolicy = 0
                                firewall_Instance.ElementName = "                 "
                                firewall_Instance.EnforcementStatus = [0]
                                firewall_Instance.ExecutionStrategy = 2
                                firewall_Instance.LocalOnlyMapping = False
                                firewall_Instance.LooseSourceMapping = False
                                firewall_Instance.Mandatory = ""
                                firewall_Instance.Owner = ""
                                firewall_Instance.PolicyDecisionStrategy = 2
                                firewall_Instance.PolicyKeywords = ""
                                firewall_Instance.PolicyRoles = ""
                                firewall_Instance.PolicyStoreSource = "PersistentStore"
                                firewall_Instance.PolicyStoreSourceType = 1
                                firewall_Instance.PrimaryStatus = 1
                                firewall_Instance.Profiles = 0
                                firewall_Instance.RuleGroup = ""
                                firewall_Instance.RuleUsage = ""
                                firewall_Instance.SequencedActions = 3
                                firewall_Instance.Status = "The rule was parsed successfully from the store."
                                firewall_Instance.StatusCode = 65536
                                iWbemServices.PutInstance(firewall_Instance.marshalMe())
                except Exception as error:
                    if "WBEM_S_FALSE" in str(error):
                         break
                    else:
                        print(error)
                        exit(1)
                print("[+] Enable WinRm Firewall allow Rule ok")
        else:
            print("[*] The OS possible:Windows7/Windows Server 2008,Not Found //./root/StandardCimv2 NameSpace\nUnable to configure firewall rules")
    dcom.disconnect()

def FirewallRule_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    if arg[0:5]!="query" and arg!="enable" and arg!="disable" and arg!="delete":
        print("[-] Pluse Query Help,Thanks....")
        exit()

    dcom, iWbemLevel1Login = wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
    if arg == "query1": #查启用
        wql="select * from MSFT_NetFirewallRule where Enabled=1"
        print("[*] Select Enable Firewall Rule")
    if arg == "query2": #查禁用
        wql="select * from MSFT_NetFirewallRule where Enabled=2"
        print("[*] Select Disable Firewall Rule")
    if arg == "query": #查全部
        wql="select * from MSFT_NetFirewallRule"
        print("[*] Select all Firewall Rule")
    if arg=="querya": #查入站
        wql="select * from MSFT_NetFirewallRule where Direction=1"
        print("[*] Select inbound Firewall Rule")
    elif arg=="queryb": #查出站
        wql="select * from MSFT_NetFirewallRule where Direction=2"
        print("[*] Select outbound Firewall Rule")
    elif arg=="query1a": #查启用的入站
        wql = "select * from MSFT_NetFirewallRule where Direction=1 and Enabled=1"
        print("[*] Select Enable inbound Firewall Rule")
    elif arg=="query2a": #查禁用的入站
        wql = "select * from MSFT_NetFirewallRule where Direction=1 and Enabled=2"
        print("[*] Select Disable inbound Firewall Rule")
    elif arg=="query1b": #查启用的出站
        wql = "select * from MSFT_NetFirewallRule where Direction=2 and Enabled=1"
        print("[*] Select Enable outbound Firewall Rule")
    elif arg=="query2b": #查禁用的出站
        wql = "select * from MSFT_NetFirewallRule where Direction=2 and Enabled=2"
        print("[*] Select Disable outbound Firewall Rule")
    elif arg=="query3": #特定ID查询
        user=input("InstanceID:")
        wql="select * from MSFT_NetFirewallRule where InstanceID=\"{}\"".format(user)
        print("[*] Select InstanceID Query")


    wql2 = "select * from MSFT_NetFirewallRule where InstanceID="
    if "query" in arg:
        MSFT_NetFirewallRule = iWbemServices.ExecQuery(wql)
        while True:
            try:
                pEnum = MSFT_NetFirewallRule.Next(0xffffffff, 1)[0]
                action=int(pEnum.Action)
                Description=pEnum.Description
                DisplayName=pEnum.DisplayName
                ElementName=pEnum.ElementName
                InstanceID=pEnum.InstanceID
                Enabled=int(pEnum.Enabled)
                if action==4:
                    type_="block connection"
                elif action==2:
                    type_="allow connection"
                if Enabled==1:
                    color=colorama.Fore.GREEN
                    enable_status=True
                else:
                    color=colorama.Fore.RED
                    enable_status=False
                MSFT_NetProtocolPortFilter=iWbemServices.ExecQuery("select * from MSFT_NetProtocolPortFilter where InstanceID=\"{}\"".format(InstanceID)).Next(0xffffffff, 1)[0]
                MSFT_NetProtocolPortFilter_LocalPort=MSFT_NetProtocolPortFilter.LocalPort
                MSFT_NetProtocolPortFilter_RemotePort=MSFT_NetProtocolPortFilter.RemotePort
                MSFT_NetProtocolPortFilter_Protocol=MSFT_NetProtocolPortFilter.Protocol
                output=color+"Type:{} {} {} {} InstanceID:{} Enable:{} || Protocol:{} LocalPort:{} RemotePort:{}".format(type_,Description,DisplayName,ElementName,InstanceID,enable_status,MSFT_NetProtocolPortFilter_Protocol,MSFT_NetProtocolPortFilter_LocalPort,MSFT_NetProtocolPortFilter_RemotePort)+colorama.Style.RESET_ALL
                print(output)
            except Exception as error:
                if "WBEM_S_FALSE" in str(error):
                    break
                else:
                    pass
    elif arg=="disable" or arg=="enable": #禁用防火墙某条规则
        print("[*] {} FirewallRule".format(arg))
        InstanceID=input("Input {} InstanceID:".format(arg))
        if arg=="disable":
            status=2
        elif arg=="enable":
            status=1
        wql2+='"{}"'.format(InstanceID)
        print(wql2)
        # 不能直接调用Disable方法，无法调用成功。只能强制覆盖
        '''
        disable = iWbemServices.ExecQuery(wql2)
        pEnum = disable.Next(0xffffffff, 1)[0]
        print(pEnum.Disable)
        '''
        try:
            iEnumWbemClassObject = iWbemServices.ExecQuery(wql2)
            firewall_RuleClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
            # firewall_RuleClass.Enable
            record = firewall_RuleClass.getProperties()
            record = dict(record)
            firewall_Instance = firewall_RuleClass.SpawnInstance()
            firewall_Instance.Enabled = status
            firewall_Instance.CreationClassName = "fuckyouaasasasaasas"
            firewall_Instance.PolicyRuleName = ""
            firewall_Instance.SystemCreationClassName = ""
            firewall_Instance.SystemName = ""
            # allow=2, allowBypass=3, Block=4
            firewall_Instance.Action = 2
            firewall_Instance.Caption = ""
            firewall_Instance.CommonName = ""
            firewall_Instance.ConditionListType = 3
            firewall_Instance.Description = ""
            firewall_Instance.Direction = 1
            firewall_Instance.DisplayGroup = ""
            firewall_Instance.DisplayName = "AAAAAAAAAAAAAAA"
            firewall_Instance.EdgeTraversalPolicy = 0
            firewall_Instance.ElementName = "                 "
            firewall_Instance.EnforcementStatus = [0]
            firewall_Instance.ExecutionStrategy = 2
            firewall_Instance.LocalOnlyMapping = False
            firewall_Instance.LooseSourceMapping = False
            firewall_Instance.Mandatory = ""
            firewall_Instance.Owner = ""
            firewall_Instance.PolicyDecisionStrategy = 2
            firewall_Instance.PolicyKeywords = ""
            firewall_Instance.PolicyRoles = ""
            firewall_Instance.PolicyStoreSource = "PersistentStore"
            firewall_Instance.PolicyStoreSourceType = 1
            firewall_Instance.PrimaryStatus = 1
            firewall_Instance.Profiles = 0
            firewall_Instance.RuleGroup = ""
            firewall_Instance.RuleUsage = ""
            firewall_Instance.SequencedActions = 3
            firewall_Instance.Status = "The rule was parsed successfully from the store."
            firewall_Instance.StatusCode = 65536
            print(iWbemServices.PutInstance(firewall_Instance.marshalMe()))
        except Exception as error:
            if str(error).find("S_FALSE")>0:
                print("[-] Not Found InstanceID:{} Firewall a Roule".format(InstanceID))

    elif arg=="delete":
        ID=input("Delete Firewall InstanceID:")
        try:
            iEnumWbemClassObject = iWbemServices.ExecQuery("SELECT * FROM MSFT_NetFirewallRule where InstanceID = \"%s\"" % ID)
            firewall_RuleClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
            record = dict(firewall_RuleClass.getProperties())
            print(iWbemServices.DeleteInstance('MSFT_NetFirewallRule.CreationClassName="{}",PolicyRuleName="{}",SystemCreationClassName="{}",SystemName="{}"'.format(record['CreationClassName']['value'],record['PolicyRuleName']['value'],record['SystemCreationClassName']['value'],record['SystemName']['value'])))
        except Exception as error:
            if str(error).find("S_FALSE")>0:
                print("[-] Not Found InstanceID:{} Firewall a Roule".format(ID))
    dcom.disconnect()

def Firewall_setting(ip='', username='', password='',domain='',hashes='',aesKey='',arg=""):
    if arg[0:5] != "query" and arg != "start" and arg != "stop":
        print("[-] Pluse Query Help,Thanks....")
        exit()


    dcom, iWbemLevel1Login = wmiconnect(ip, username, password, domain, hashes, aesKey)
    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/StandardCimv2', NULL, NULL)
    WQL="SELECT * FROM MSFT_NetFirewallProfile"
    if "query"==arg:
        firewall_list=iWbemServices.ExecQuery(WQL)
        while True:
            try:
                pEnum = firewall_list.Next(0xffffffff, 1)[0]
                InstanceID=pEnum.InstanceID
                Name=pEnum.Name
                EnableID=pEnum.Enabled
                if int(EnableID)==1 or int(EnableID)==2:
                    status="ON"
                else:
                    status="OFF"
                print("InstanceID:{} Name:{} EnableID:{}".format(InstanceID,Name,status))
            except Exception as error:
                if "WBEM_S_FALSE" in str(error):
                    break
    elif "stop"==arg or "start"==arg:
        print("[*] {} Firewall".format(arg))
        if arg=="start":
            status=2
        elif arg=="stop":
            status=0
        user=input("Firewall Name:")
        WQL+=" where Name=\"{}\"".format(user)
        iEnumWbemClassObject = iWbemServices.ExecQuery(WQL)
        firewall_ProfileClass = iEnumWbemClassObject.Next(0xffffffff, 1)[0]
        record = firewall_ProfileClass.getProperties()
        record = dict(record)
        firewall_ProfileInstance = firewall_ProfileClass.SpawnInstance()
        firewall_ProfileInstance.DisabledInterfaceAliases = ""
        firewall_ProfileInstance.Caption = "" if record['Caption']['value'] == None else record['Caption']['value']
        firewall_ProfileInstance.Enabled = status
        firewall_ProfileInstance.Description = "" if record['Caption']['value'] == None else record['Caption']['value']
        iWbemServices.PutInstance(firewall_ProfileInstance.marshalMe())
    dcom.disconnect()




if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-i",dest="ip",help="target IP")
    parser.add_option("-u",dest="username",help="auth username")
    parser.add_option("-d",dest="domain",help="target domain")
    parser.add_option("-p",dest="password",help="auth password")
    parser.add_option("-n",dest="ntlm",help="auth ntlm/lm")
    parser.add_option("-g",dest="get_process",action='store_true',help="get process list")
    parser.add_option("-q",dest="process_query",action='store_true',help="query Av/EDR/Process")
    parser.add_option("-U",dest="user_query",action='store_true',help="user list query")
    parser.add_option("-R",dest="enable_rdp",help="enable rdp/disable rdp")
    parser.add_option("-E",dest="enable_pth",help="enable rdp pth login")
    parser.add_option("-W",dest="enable_winrm",help="enable winrm service")
    parser.add_option("-F",dest="netfirewallrule",help="Query/Enable/Disable NetFirewallRule")
    parser.add_option("-f",dest="firewall",help="Start/Stop firewall")
    (option,args)=parser.parse_args()
    ip = option.ip
    if option.domain != None:
        domain = option.domain
    else:
        domain = ""
    username = option.username
    password = option.password
    if option.ip and option.username and (option.password!=None or option.ntlm !=None) and (option.get_process or (option.get_process and option.process_query)):
        if option.password!=None:
            getProcessList(ip=ip, domain=domain,username=username, password=password,query=option.process_query)
        elif option.ntlm!=None:
            getProcessList(ip=ip, domain=domain,username=username, hashes=option.ntlm, query=option.process_query)
    elif  option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.user_query:
        if option.password != None:
            userquery(ip=ip, domain=domain, username=username, password=password)
        elif option.ntlm != None:
            userquery(ip=ip, domain=domain, username=username, hashes=option.ntlm)
    elif option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.enable_rdp:
        if option.password != None:
            enablerdp(ip=ip, domain=domain, username=username, password=password,isenable=option.enable_rdp)
        elif option.ntlm != None:
            enablerdp(ip=ip, domain=domain, username=username, hashes=option.ntlm,isenable=option.enable_rdp)
    elif option.ip and option.username and (option.password!=None or option.ntlm !=None) and option.enable_pth:
        if option.password != None:
            enable_pth_login_rdp(ip=ip, domain=domain, username=username, password=password,isenable=option.enable_pth)
        elif option.ntlm != None:
            enable_pth_login_rdp(ip=ip, domain=domain, username=username, hashes=option.ntlm,isenable=option.enable_pth)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.enable_winrm:
        if option.password != None:
            winrm_enable(ip=ip, domain=domain, username=username, password=password, isenable=option.enable_winrm)
        elif option.ntlm != None:
            winrm_enable(ip=ip, domain=domain, username=username, hashes=option.ntlm,isenable=option.enable_winrm)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.netfirewallrule:
        if option.password != None:
            FirewallRule_setting(ip=ip, domain=domain, username=username, password=password,arg=option.netfirewallrule)
        elif option.ntlm != None:
            FirewallRule_setting(ip=ip, domain=domain, username=username, hashes=option.ntlm,arg=option.netfirewallrule)
    elif option.ip and option.username and (option.password != None or option.ntlm != None) and option.firewall:
        if option.password != None:
            Firewall_setting(ip=ip, domain=domain, username=username, password=password,arg=option.firewall)
        elif option.ntlm != None:
            Firewall_setting(ip=ip, domain=domain, username=username, hashes=option.ntlm,arg=option.firewall)
    else:
        print("Usage:\npython wmi_query -i <target> -u <username> -p <password> -g #Get Process List\n"
              "python wmi_query -i <target> -u <username> -p <password> -g -q #query Av/EDR/Process\n"
              "python wmi_query -i <target> -u <username> -p <password> -U #User Query\n"
              "python wmi_query -i <target> -u <username> -p <password> -R 1 #Enable rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -R 0 #Disable rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -E 1 #Enable PTH rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -E 0 #Disable PTH rdp\n"
              "python wmi_query -i <target> -u <username> -p <password> -W 1 #Enable winrm service\n"
              "python wmi_query.py -i 192.168.3.11 -u Administrator -p Hxc123456! -W 0\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query # query all Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1 #query Enable Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2 #query Disable Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F querya #query inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F queryb #query outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1a #query Enable inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2a #query Disable inbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query1b #query Enable outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query2b #query Disable outbound Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F query3 #query InstanceID Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F delete #delete InstanceID Firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F disable #Disable a firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -F enable #Enable a firewall rule\n"
              "python wmi_query -i <target> -u <username> -p <password> -f query #query Firewall\n"
              "python wmi_query -i <target> -u <username> -p <password> -f stop #stop Firewall\n"
              "python wmi_query -i <target> -u <username> -p <password> -F start #start Firewall\n")
        parser.print_help()