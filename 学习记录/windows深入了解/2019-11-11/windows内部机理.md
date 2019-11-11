# 挖掘Windows内部机理

可以用于查看windows内部机理的工具
```
Startup Programs Viewer
Access Check
Dependency Walker
Global Flags
Handle Viewer
Kernel debuggers
Object Viewer
(Performance Monitor)
Pool Monitor
Process Explorer
Process Monitor
Task List
任务管理器
```

![MQ820P.png](https://s2.ax1x.com/2019/11/11/MQ820P.png)


# 内核调试所需要的符号
符号文件包含了函数和变量的名称。以及数据结构的布局和格式。它们是由链接器产生的。在调试绘画装备，调试器用来引用和显示这些名称。这些名称信息通常并不存储在二进制映像文件中，因为在执行代码的时候并不需要用它们。这意味着二进制映像文件更小巧也更加快速。在调试的时候，你必须确保在一个调试绘画中，调试器才能够访问与当前引用的印象文件和相关联的符号文件。

要使用任何一个内核调试工具来检查windows内核的内部数据结构。（比如进程列表、线程块、已加载的驱动程序列表、内存使用信息等...），必须至少得到了内核映像Ntoskrnl.exe的正确符号文件。符号表文件必须与这些符号表所在的映像文件的版本完全匹配。例如，打了一个更新内核服务的补丁（Service Pack（服务补丁）或者Hot Fix(热补丁)），那么必须获取匹配、更新的符号文件

用户的调试模式
1.侵入式的
2.非侵入式的 
![MQN2i6.png](https://s2.ax1x.com/2019/11/11/MQN2i6.png)

Tips:也可以用工具来打开进程转存储的文件

调试内核的工具有两种：
命令行的kd.exe
GUI界面的Windbg.exe

这两个调试工具，可调试以下的玩意
* 崩溃的转储文件
* 连接到正在运行上的系统，并检查该系统的状态；或者，如果正在调试设备驱动程序的代码，则可以设置断点。这种操作要求有两台计算机----目标计算机和控制主机。目标计算机指要调试的目标系统，控制主机是指运行调试器的主机。目标系统可以通过零调制解调器线、IEEE 1394线或者USB调试线连接至控制主机。目标系统必须按调试模式引导（可以在引导过程按下F8键，然后选择调试模式，或者利用Bcedit或Msconfig.exe工具将系统设置为调试模式来引导）

* windows系统也允许连接本地系统上，然后检查系统的状态。这称为本地内核调试。为了在WinDbg中启动本地内核调试模式，打开File菜单，选择“Kernel Debug”，单击Local选项卡，然后单击OK按钮。

windbg下载和教程：
[setup-windbg](https://download.microsoft.com/download/E/1/B/E1B0E6C0-2FA2-4A1B-B322-714A5586BE63/windowssdk/winsdksetup.exe)
[Windbg调试工具 - 奋斗的coder](http://my.2bgg.com/article-detials/409)
[windbg使用超详细教程(我是新手，大佬轻虐) - 知乎](https://zhuanlan.zhihu.com/p/43972006) (安装教程)
[windbg配置符号文件](https://blog.csdn.net/chaootis1/article/details/79834117)

![MQfFbt.png](https://s2.ax1x.com/2019/11/11/MQfFbt.png)

得先开启调试模式，否则windbg会给出以下错误
>The system does not support local kernel debugging.
Local kernel debugging requires Administrative
privileges, and is not supported by WOW64.
Only a single local kernel debugging session can run at a time.
Local kernel debugging is disabled by default. You must run ‘bcdedit -debug on’ and reboot to enable it.

开启调试模式的命令，之后重启computer，并用Administrator权限打开windbg
```
bcdedit -debug on
```
参考链接：[The system does not support local kernel debugging – Alfred Myers](https://alfredmyers.com/2017/11/26/the-system-does-not-support-local-kernel-debugging/)

![MQfoIf.png](https://s2.ax1x.com/2019/11/11/MQfoIf.png)

成功启动windbg如下
![MQ4iAP.png](https://s2.ax1x.com/2019/11/11/MQ4iAP.png)

显示内核符号中所包含的类型信息的内核结果列表， 在调试器输入net !_*
![MQLKHg.png](https://s2.ax1x.com/2019/11/11/MQLKHg.png)

例如dt命令查看指定的数据结构
```
dt <数据结构类型>
```
![MQL0UJ.png](https://s2.ax1x.com/2019/11/11/MQL0UJ.png)

# livekd
可以使用livekd工具来转储windows上的错误
下载地址：[LiveKd - Windows Sysinternals \| Microsoft Docs](https://docs.microsoft.com/zh-cn/sysinternals/downloads/livekd)

