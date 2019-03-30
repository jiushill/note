#### powershell简介 ####
windows Powershell是一种美丽行外壳程序和脚本环境，使命令行用户和脚本编写者可以利用.NET Framework的强大功能。它引入了许多非常有用的新概念，从而进一步扩展了您在windows命令提示符和windows Script Host环境中获得的知识和创建的脚本。windows powershell v3将伴随着MicrosofHyper-V3.0将windows server 2012发布。powerhsell v3是一个windows任务自动化的框架，它由一个命令行shell和内置在这个.NET框架上的编程语言组成。

powershell v3采用新的cmdet让管理员能够更深入到系统进程中，这些进程可执行的文件或脚本（script）。一条cmdlet是一条轻重量命令，windows powershell运行时间在自动化脚本的环境里调用它
cmdlet包括显示当前目录Get-Location,访问文件内容的Get-Content和结束运行进程的Stop-Process

Powershell V3在widnows server 8中装载了windows Management Framework 3.0.powershell运行时间也能嵌入到其他应用


#### powershell的使用 ####
powershell是运行在windows机器上实现系统和应用程序管理自动化的命令行脚本环境。你可以把它看成是命令行提示符cmd.exe的扩展，不对，应当是颠覆。powershell需要.NET环境的支持，同时支持.NET对象。微软之所以将powershell定位为Power，并不是夸大其词，因为它完全支持对象。其可读性，易用性，可以位居当前所有shell之首，当前powershell有4个版本，分别为：1.0，2.0,3.0,4.0

系统和powershell版本对应：
```
windows 7 or windows server 2008      powershell 2.0
windows8 or widnows server 2012       powershell 3.0
windows 8.1 or windows server 2012 R2  powershell 4.0
```

进入powershell后输入help查看帮助命令
![kjinsS.png](https://s2.ax1x.com/2019/03/05/kjinsS.png)

使用help命令查看指定命令的使用
例如：help ac 或 ac ? 或man ac 或get-help ac
![kjiNsU.png](https://s2.ax1x.com/2019/03/05/kjiNsU.png)

得到技术类信息使用man 要查询的命令 -full
例如：man ac -full

如果我们想查content相关的命令可以输入get-command *content
*是通配符代表全部
![kjAprT.png](https://s2.ax1x.com/2019/03/05/kjAprT.png)

#### 简单的脚本编写 ####
```
‘“Hello powershell”’ > demo.ps1
更改脚本执行策略
set-ExecutionPolicy RemoteSigned
./demo.ps1
```
![kjAOeO.png](https://s2.ax1x.com/2019/03/05/kjAOeO.png)

```
Get-Date 输出当前日期
$Env:CommonProgramFiles 输出CommonprogramFiles输出CommonProgramFiles环境目录
(ls).count 输出ls命令下查询的文件数
```
![kjEiOf.png](https://s2.ax1x.com/2019/03/05/kjEiOf.png)

使用powershell添加用户：(我实验失败了)
```
$objOu = [ADSI]"WinNT://rmt_client1"                 #rmt_client1为执行脚本的当前计算机名

$objUser = $objOU.Create("User", "hacker")        #用户名hacker 

$objUser.setpassword("hacker123")                      #密码hacker123  

$objUser.SetInfo()                                                  #创建帐号

$objUser.description = "Test Comm"                    #用户名描述 

$objUser.SetInfo()                                                  #修改用户描述


```

使用cmd运行ps1脚本：
```
powershell -command ".\xx.ps1"
```