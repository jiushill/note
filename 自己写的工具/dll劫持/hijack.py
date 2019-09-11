from collections import Counter
import csv
import re
import sys

banner='''
*******************************************************************************
________  .____    .____           ___ ___ .__     __               __        *
\______ \ |    |   |    |         /   |   \|__|   |__|____    ____ |  | __    *
 |    |  \|    |   |    |        /    ~    \  |   |  \__  \ _/ ___\|  |/ /    *
 |    `   \    |___|    |___     \    Y    /  |   |  |/ __ \\  \___|    <     *
/_______  /_______ \_______ \_____\___|_  /|__/\__|  (____  /\___  >__|_ \    *
        \/        \/       \/_____/     \/    \______|    \/     \/     \/    *
帮助:用于可能存在DLL劫持的路径                                                *
********************************************************************************
'''
print(banner)

def fuck(demos,ck):
    demo=[]
    sb=[]

    for d in demos:
        data=str(d).split('\\')
        demo.append(data[-1])

    jg=Counter(demo)
    for j in jg:
        if jg[j]>=3:
            print(j,jg[j])
            for c in demos:
                if j in c:
                    rpq=str(j).split('\\')
                    if rpq[-1] == j:
                        sb.append(c)




    list2=[]
    for gg in sb:
        if sb.count(gg)==1:
            list2.append(gg)

    print('[!] 可能存在DLL劫持的路径:')
    for dll in list2:
        for b in ck:
            if dll in b:
                print(b)
                print('copy demo.dll {}'.format(dll),file=open('demo.bat','a',encoding='utf-8'))

    print('生成测试bat完成')


demos=[]
ck=[]
try:
    dk=open('{}'.format(sys.argv[1]),'r',encoding='utf-8')
    yy=csv.DictReader(dk)
    for j in yy:
        ck.append('Process Name:{} Path:{}'.format(j['Process Name'],j['Path']))

    for g in ck:
        zz=re.findall('Path[:].*',str(g))
        demos.append(str(zz[0]).replace('Path:',''))

    fuck(demos,ck)
except Exception as r:
    print('[(] 你需要一个参数,例如:hijack.py [xxx.csv]')