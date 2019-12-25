RDP安全层协议
* 标准RDP 协议文档称为PROTOCOL_RDP
* SSL 协议文档为PROTOCOL_SSL
* CredSSP(NLA+SSL) 协议文档为PROTOCOL_HYBRID


三者的不同之处：
【图1】


RDP降级攻击
工具：https://github.com/citronneur/rdpy
【图2】

tscon认证绕过
当权高的时候想要切换到另外一个用户，但是不知道密码的话
使用tscon

命令格式：
query user #获取用户ID
tscon <USER_ID>

【图3】

通用性
Windows 2016
Windows 2012 R2
Windows 2008
Windows 10
Windows 7
Windows 2019 失败

无日志


RDP隧道
隧道程序   https://github.com/earthquake/UniversalDVC
Socks代理程序  https://github.com/securesocketfunneling/ssf


凭证目录
C:\Users\[User Profile]\AppData\Roaming\Microsoft\Credentials                                          (Windows Vista 以上)
C:\Users\[User Profile]\AppData\Local\Microsoft\Credentials                                                 (Windows Vista以上)
C:\Windows\system32\config\systemprofile\AppData\Local\Microsoft\Credentials           (Windows 8以上)
C:\Documents and Settings\[User Profile]\Application Data\Microsoft\Credentials              (Windows XP)
C:\Documents and Settings\[User Profile]\Local Settings\Application Data\Microsoft\Credentials (Windows XP)


凭证的内容有
exchange 的邮件帐户密码（ Outlook存储）
Windows Live会话信息
远程桌面  用户/密码信息
Internet Explorer 7.x和8.x： （“基础认证”或“摘要访问认证”）
MSN  / Windows Messenger 凭证


剪切板劫持
https://research.checkpoint.com/2019/reverse-rdp-attack-code-execution-on-rdp-clients/
https://paper.seebug.org/1074/
