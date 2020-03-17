#@author:九世
#@time:2020/3/17
#@file:jg.py
#注意事项：请确保手机屏幕常亮
import uiautomator2
import time

appname="com.alibaba.android.rimet"
startid=0 #1为需要自动打开钉钉
sleeps=2 #延时设置
id=0 #是否需要亮屏，可观性
appid=0 #app是否启动成功
name="" #班级群名
neiron="立即签到" #签到内容

def test():
    d=uiautomator2.connect('192.168.1.105')
    info=d.info
    if len(info)>0:
        print('[+] {} Connect Success'.format(info['productName']))
        for v in info:
            print('{}:{}'.format(v,info[v]))
        if id==1:
            print('[!] 检查是否亮屏')
            if d.info.get('screenOn')!=True:
                print('[+] 点亮屏幕中')
                d.screen_on()
                print('[+] 解锁屏幕')
                print('[!] 你有{}秒中的时间解锁屏幕'.format(sleeps))
                d.unlock()
                time.sleep(sleeps)
        qiandao(d)
    else:
        print('[-] Connect fail')

def qiandao(f):
    if startid==1:
        print('[+] start 钉钉')
        f.app_start(appname)
        appid=1
        if appid==1:
            print('[+] 钉钉启动成功')
            gaoshi(f)
    elif startid==0:
        print('[+] 由于设置为不自动启动钉钉，默认已在钉钉界面')
        gaoshi(f)

def gaoshi(d):
    zbocalc = 0
    calc=0
    time.sleep(sleeps)
    print('[!] 检测是否在群聊中')
    try:
        v=d(resourceId="com.alibaba.android.rimet:id/title").get_text()
        if v==name:
            print('[+] 已在指定的群里')
        else:
            print('[!] 不在指定的群里')
            d(resourceId="com.alibaba.android.rimet:id/back_layout").click()
            time.sleep(sleeps)
            print('[+] 打开群聊中')
            d(resourceId="com.alibaba.android.rimet:id/session_title", text=name).click()
            time.sleep(sleeps)
            print('[+] 打开{}群聊成功'.format(name))
    except:
        print('[!] 检测是否在群聊选择界面')
        if d(resourceId="com.alibaba.android.rimet:id/item_title", text="DING").get_text() == "DING":
            print('[+] 已在群聊选择界面')
        else:
            print('[!] 不在群聊选择界面')
            d.xpath( '//*[@resource-id="com.alibaba.android.rimet:id/home_bottom_tab_button_message"]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()

        print('[+] 打开群聊中')
        d(resourceId="com.alibaba.android.rimet:id/session_title", text=name).click()
        time.sleep(sleeps)
        print('[+] 打开{}群聊成功'.format(name))

    while True:
        try:
            d(description=neiron).click()
            calc+=1
            print('[+] 签到成功 成功次数:{}'.format(calc))
        except:
            print('[!] 暂时无签到')

        try:
            ns=d(resourceId="com.alibaba.android.rimet:id/tv_nick").get_text()
            print('[+] 发现直播，直播老师:{}'.format(ns))
            d(resourceId="com.alibaba.android.rimet:id/tv_play").click()
            zbocalc+=1
            print('[+] 直播老师:{} 打开直播成功 成功次数:{}'.format(ns,zbocalc))

            d(resourceId="com.alibaba.android.rimet:id/tv_nick").click()
            print('[+] 点击一下直播屏幕隐藏掉直播标题')
        except:
            print('[!] 无直播,或已经点开了直播')

        time.sleep(sleeps)
if __name__ == '__main__':
    test()