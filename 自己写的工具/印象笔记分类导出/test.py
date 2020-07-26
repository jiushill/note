from gevent import monkey;monkey.patch_all()
from bs4 import BeautifulSoup
import json
import re
import os
import sys
import config
import xmltodict
import gevent

def xmltojson(xmldata):
    xmlparse=xmltodict.parse(xmldata)
    jsondata=json.dumps(xmlparse,indent=1)
    data=json.loads(jsondata)
    export=data["en-export"]
    note=export["note"]
    temps=[]
    if isinstance(note,list)==True:
        for d in note:
            temps.append(gevent.spawn(chuli,d,export))
            if len(temps)==config.NUMBER:
                gevent.joinall(temps)
                temps.clear()
    else:
        chuli(note,export)

    if len(temps)>0:
        gevent.joinall(temps)
        temps.clear()

def chuli(note,export):
    global autor
    createnotetime="{}".format(export["@export-date"]).split("T")
    createnotetime="{}年{}月{}日 {}:{}".format(createnotetime[0][0:-4],createnotetime[0][-4:-2],createnotetime[0][-2::],createnotetime[1][0:2],createnotetime[1][2:4])
    version=export["@version"]
    application=export["@application"]
    title=note["title"]
    if "tag" in [x for x in note]:
        tag=note["tag"]
    else:
        tag="None"
    try:
        autor=note["note-attributes"]["author"]
    except:
        author=""

    content=note["content"]
    if "resource" in [x for x in note]:
        resure=note["resource"]
    else:
        resure=""

    en=re.findall('<en-media hash=".*?"/>',content)
   # print(en)

    '''获取图片base64'''
    texts=[]
    for e in en:
        hashs=BeautifulSoup(e,"html.parser").find_all("en-media")[0].get("hash")
        if isinstance(resure,list)==True:
            for j in resure:
             #   print(j,file=open("axc.txt","a",encoding="utf-8"))
                try:
                    id=j["recognition"]
                    if hashs in id:
                        text = j["data"]["#text"]
                        texts.append(text)
                except:
                    text = j["data"]["#text"]
                    texts.append(text)
        else:
            text = resure["data"]["#text"]
            texts.append(text)

    try:
        for e in range(0,len(en)):
            #print(en[e],texts[e])
            if "width" in en[e]:
                width = re.findall('width=".*"',en[e])[0]
                content = str(content).replace(en[e], '<img src="data:image/jpg;base64,{}" {}>'.format(texts[e],width))
            else:
                content=str(content).replace(en[e],'<img src="data:image/jpg;base64,{}">'.format(texts[e]))
    except:
        pass

    htmldata='''<html>
    <head>
    <title>{}</title>
    </head>
    <body>
    <b>作者:{}</b><br>
    <b>时间:{}</b><br>
    <b>使用系统:{}</b><br>
    <b>印象笔记版本:{}</b><br>
    <b>标签:{}</b><br>
    {}
    </body>
    </html>
    '''.format(title,autor,createnotetime,application,version,tag,content)

    if isinstance(tag,list)==True:
        pths="{}{}".format(outpath,"-".join(tag))
    else:
        pths="{}{}".format(outpath,tag)
    if os.path.exists(pths)==False:
        os.mkdir(pths)

    for t in  ["?","*"':','"',"<",">","\\","/","|"]:
        if t in title:
            title=str(title).replace(t,"")

    paths="{}{}{}.html".format(pths,pcth,title)
    print(htmldata,file=open("{}".format(paths),"a",encoding="utf-8"))
    print("[+] {} dump file ok".format(paths))

if __name__ == '__main__':
    path=config.FILEPATH
    outpath = str(config.OUTPUTFILE).rstrip("\\").rstrip("/")
    if sys.platform == "win32":
        pcth="\\"
        outpath += "\\"
    else:
        pcth="/"
        outpath += "/"

    if os.path.exists(outpath)==False:
        os.mkdir(outpath)
    if os.path.exists(path):
        if os.path.isfile(path):
            xmltojson(open("{}".format(path),"r",encoding="utf-8").read())
        else:
            paths_=os.walk(path)
            temp=[]
            for i in paths_:
                for f in i[-1]:
                    pach = "{}{}{}".format(i[0], pcth,f)
                    temp.append(gevent.spawn(xmltojson,open("{}".format(pach),"r",encoding="utf-8").read()))
                    if len(temp)==config.NUMBER:
                        gevent.joinall(temp)
                        temp.clear()

            if len(temp)>0:
                gevent.joinall(temp)
                temp.clear()
