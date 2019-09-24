@echo off
echo [*] 操作系统和体系结构和补丁
systeminfo
wmic qfe

echo ======================================================

echo [*] 环境变量
set

echo ======================================================

echo [*] 盘符
wmic logicaldisk get caption,description,providername

echo ======================================================

echo [*] 网络连接
net use

echo ======================================================

echo [*] 当前用户
whoami

echo ======================================================

echo [*] 当前用户权限
whoami /priv

echo ======================================================

echo [*] 系统上存在的用户
net user 

echo ======================================================

echo [*] 用户个人资料
dir /b /ad "C:\Users\"

echo ======================================================

echo [*] 当前在线的用户
query user

echo ======================================================

echo [*] 当前系统上的组
net localgroup

echo ======================================================

echo [*] 当前管理员组上有用户吗
net localgroup Administrators

echo ======================================================

echo [*] 用户自动登录注册表中的内容
reg query "reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"

echo ======================================================

echo [*] 用户保存在本地的凭证
cmdkey /list

echo ======================================================

echo [*] 安装了什么软件
dir /a "C:\Program Files"

echo ======================================================

echo [*] 文件夹或文件权限是否弱

icacls "C:\Program Files\*" 2>nul | findstr "(F)" | findstr "Everyone"
icacls "C:\Program Files (x86)\*" 2>nul | findstr "(F)" | findstr "Everyone"

icacls "C:\Program Files\*" 2>nul | findstr "(F)" | findstr "BUILTIN\Users"
icacls "C:\Program Files (x86)\*" 2>nul | findstr "(F)" | findstr "BUILTIN\Users" 

echo ======================================================

echo [*] 正在运行的进程

tasklist /svc

echo ======================================================

echo [*] 已启动的服务
net start


echo ======================================================

echo [*] 启动时运行了什么
wmic startup get caption,command

echo ======================================================
echo [*] 是否启用了AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

echo AlwaysInstallElevatedt提权:https://www.4hou.com/technology/19286.html

echo ======================================================

echo [*] 所有网络
ipconfig /all


echo ======================================================

echo [*] 路由表
route print

echo ======================================================

echo [*] ARP缓存表
arp -a


echo ======================================================

echo [*] 网络端口的开放
netstat -ano

echo ======================================================

echo [*] hosts文件中的内容
type C:\WINDOWS\System32\drivers\etc\hosts

echo ======================================================

echo [*] 防火墙是否打开
netsh firewall show state

echo ======================================================

echo [*] 防火墙的配置
netsh firewall show config

echo ======================================================

echo [*] 导出防火墙规则到firewall.txt
netsh advfirewall export "firewall.txt"

echo ======================================================

echo [*] SNMP配置信息
reg query HKLM\SYSTEM\CurrentControlSet\Services\SNMP /s


echo ======================================================

echo [*] 注册表中的密码

reg query HKCU /f password /t REG_SZ /s
reg query HKLM /f password /t REG_SZ /s 

echo ======================================================

echo [*] 是否有安装phpstudy、PHP、Apache
dir /s php.ini httpd.conf httpd-xampp.conf my.ini my.cnf

echo ======================================================

echo [*] Apache网络日志
dir /s access.log error.log


echo ======================================================

echo [*] 目录下有趣的文件
dir /s *pass* == *vnc* == *.config*

echo ======================================================

echo [*] 文件中包含password关键字的
findstr /si password *.xml *.ini *.txt *.config