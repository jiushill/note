---
title: COM劫持学习
tags: Writing
abbrlink: 7dc498ec
date: 2019-06-21 23:34:31
---
<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=35848041&auto=1&height=66"></iframe>
### COM组件的来源 ###
COM component（COM组件）是微软公司为了计算机工业的软件生产更加符合人类的行为方式开发的一种新的软件开发技术。在COM构架下，人们可以开发出各种各样的功能专一的组件，然后将它们按照需要组合起来，构成复杂的应用系统。由此带来的好处是多方面的：可以将系统中的组件用新的替换掉，以便随时进行系统的升级和定制；可以在多个应用系统中重复利用同一个组件；可以方便的将应用系统扩展到网络环境下；COM与语言，平台无关的特性使所有的程序员均可充分发挥自己的才智与专长编写组件模块。

### COM组件的方法 ###
COM是开发软件组件的一种方法。组件实际上是一些小的二进制可执行程序，它们可以给应用程序，操作系统以及其他组件提供服务。开发自定义的COM组件就如同开发动态的，面向对象的API。

### COM组件的规则 ###
```
COM组件是以WIN32动态链接库（DLL）或可执行文件（EXE）形式发布的可执行代码组成。
COM组件是遵循COM规范编写的
COM组件是一些小的二进制可执行文件
COM组件可以给应用程序、操作系统以及其他组件提供服务
自定义的COM组件可以在运行时刻同其他组件连接起来构成某个应用程序
COM组件可以动态的插入或卸出应用
COM组件必须是动态链接的
COM组件必须隐藏（封装）其内部实现细节
COM组件必须将其实现的语言隐藏
COM组件必须以二进制的形式发布
COM组件必须可以在不妨碍已有用户的情况下被升级
COM组件可以透明的在网络上被重新分配位置
COM组件按照一种标准的方式来宣布它们的存在
```

<b>在开送之前先感谢@WBG老哥帮我编辑好的OleView.NET
以及一些前辈们的文章：</b>
[Lateral Movement via DCOM: Round 2 \| enigma0x3](https://enigma0x3.net/2017/01/23/lateral-movement-via-dcom-round-2/)
[com-and-powerhief](https://etherdream.github.io/jsproxy/-----https://labs.nettitude.com/blog/com-and-the-powerthief/)

### 环境准备 ###
```
OS:windows 7
exe:Registry,OleView.NET
```
Registry下载地址：
[Registry](https://www.lanzous.com/i1vym3g) 密码：black
[GitHub - tyranid/oleviewdotnet: A .net OLE/COM viewer and inspector to merge functionality of OleView and Test Container](https://github.com/tyranid/oleviewdotnet)

### 实验 ###
首先打开Oleview.NET，点击Registry->APPID （可以看到很多ID）
![Zp9E11.md.png](https://s2.ax1x.com/2019/06/21/Zp9E11.md.png)

根据上述的第一篇文章所说的操作，寻找程序启动权限为空的ID，点击：Mode->Complex，然后配置过滤规则
![Zp9mnK.md.png](https://s2.ax1x.com/2019/06/21/Zp9mnK.md.png)

后面我随手点开了一个ID
![Zp9QtH.md.png](https://s2.ax1x.com/2019/06/21/Zp9QtH.md.png)

查看一手 （设备启动权限为空）
![Zp981I.png](https://s2.ax1x.com/2019/06/21/Zp981I.png)

PS：看下图解释
![Zp9Gct.md.png](https://s2.ax1x.com/2019/06/21/Zp9Gct.md.png)

查看CLSID
![Zp9NB8.md.png](https://s2.ax1x.com/2019/06/21/Zp9NB8.md.png)

使用Registry定位到CLSID
![Zp9scq.md.png](https://s2.ax1x.com/2019/06/21/Zp9scq.md.png)

修改掉这个加载的exe就能完成劫持？（360主体防御拦截警告）
![Zp9qHO.md.png](https://s2.ax1x.com/2019/06/21/Zp9qHO.md.png)

根据文章中使用powershell查看COM中可用的操作
![ZpFBZV.png](https://s2.ax1x.com/2019/06/22/ZpFBZV.png)

经过搜索发现此COM为自定义COM，无法进行利用
![ZpFRMR.md.png](https://s2.ax1x.com/2019/06/22/ZpFRMR.md.png)

常见的COM劫持手法有：
```
增加缺少的CLSID进行利用 --- 失败
修改原有CLSID加载的程序 --- 失败
替换掉CLSID下加载路径的程序 --- 失败
```
果然，还是没成功。。。。不过起码学到怎么操作了，如果想复现上述文章作者的操作的话，可以自己试试。COM劫持横向发展也是牛逼...

### 使用应用程序快捷方式来劫持DXPServer.exe ###
![ZpkALq.md.png](https://s2.ax1x.com/2019/06/22/ZpkALq.md.png)
添加注册表
![ZpkGex.png](https://s2.ax1x.com/2019/06/22/ZpkGex.png)

再次运行，弹出calc
![Zpkafe.png](https://s2.ax1x.com/2019/06/22/Zpkafe.png)

我发现：
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths
```
这个注册表的路径和镜像劫持的功能一样，但是不会被杀软拦截
