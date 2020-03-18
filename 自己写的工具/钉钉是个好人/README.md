## Fuckingdingding ##
### 前因 ###
不点签到扣我分？直播时间不够又扣我分？我每天早上还要8点起床？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？，我受够了。所以写了这个玩意
![](https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=917609066,2557158547&fm=11&gp=0.jpg)

### 适用于 ###
* 在线课堂签到
* 指定群聊有直播自动打开

### 准备工作 ###
注意：确保手机长时间亮屏

需要安装的库：
```
uiautomator2
pillow
```

需要设置的地方：  
<b>将192.168.1.105这个IP改为你手机的IP</b>
```python
startid=0 #1为需要自动打开钉钉
sleeps=2 #延时设置
id=0 #是否需要亮屏，可观性
appid=0 #app是否启动成功
name="卢本伟打牌群" #班级群名
neiron="立即签到" #签到内容识别并点击的关键词
```

需要安装ATX.APK：
手机接上电脑，在adb devices出现设备的时候，执行：python -m uiautomator2 init。给手机安装ATX.apk

效果如下：  
![](https://s1.ax1x.com/2020/03/17/8aFagU.png)

![8aARne.png](https://s1.ax1x.com/2020/03/17/8aARne.png)

![](https://s1.ax1x.com/2020/03/17/8aACeH.png)

![8aAt6U.png](https://s1.ax1x.com/2020/03/17/8aAt6U.png)

参考链接：  
[python uiautomator2 环境搭建 - 镜轩思雨 - 博客园](https://www.cnblogs.com/yutongX/p/9608729.html)  
[使用 python 实现 Android Uiautomator 自动化测试脚本开发和实战 · TesterHome](https://testerhome.com/articles/21317)  
[python3+uiautomator2获取控件属性_Python_默金-CSDN博客](https://blog.csdn.net/qq_42846555/article/details/94459003)  
[Python钉钉打卡程序_Python_qq_41323133的博客-CSDN博客](https://blog.csdn.net/qq_41323133/article/details/86094761)
