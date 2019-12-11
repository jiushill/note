widnwos下的用户模式和内核模式的运行方式
![QtqwFg.png](https://s2.ax1x.com/2019/12/07/QtqwFg.png)


## 环境子系统和子系统DLL
每个可执行映像（exe）都被绑定到唯一的一个子系统上。映像文件运行时，负责创建进程的代码会检查该映像头部的子系统类型代码，所以它可以通知正确的子系统，有新的进程被创建。
（用户应用程序并不是直接调用windows服务而是通过一个或者多个子系统DLL来进行）
windows子系统DLL：Kernel32.dll、Advapi32.dll、User32.dll和Gdi32.dll）实现了WIndows API函数。SUA子系统DLL（Psxdll.dll）实现了SUA API函数。

## 实验：查看可执行映像的子系统类型
准备工具：
```
Depends
```
打开cmd.exe
![QtXT6s.png](https://s2.ax1x.com/2019/12/07/QtXT6s.png)

当应用程序调用子系统DLL时可能会发生以下的三种情况
1.该函数完全是在该子系统DLL中实现的，在用户模式下运行。该函数并没有给环境子系统进程发送消息，也没有调用windows执行体系统服务。该函数在用户模式下完成的，运行结果返回给调用者。此类函数的例子有GetCurrentProcess（它总是返回-1，在所有与进程相关的函数中，-1被定义为当前进程）和GetCurrentProcessId(对于一个正在运行的进程，进程ID不会改变，所以进程ID可以从某个缓存的地方获取，从而避免调用至内核中)

2.该函数要求调用Windows执行体一次或多次。例如，widnows的ReadFile和WriteFile函数分别要调用底层内部的（且无文档）Windows I/O系统服务NtReadFile和NtWriteFIle

3.该函数要求在环境子系统中完成某些工作（环境子系统进程运行在用户模式下，负责维护那些在其控制下运行的客户应用程序状态）。在这种情况下，该函数通过消息的形向环境子系统发送客户机/服务器请求，从而让子系统执行某个操作。然后子系统让DLL等待应答，收到应答之后再返回给调用者。
![QtzF7q.png](https://s2.ax1x.com/2019/12/07/QtzF7q.png)

## 子系统启动
子系统是由会话管理器（Smss.exe）进程启动起来的，子系统的启动信息保存在注册表键`HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems`的下面
![QNSqFP.png](https://s2.ax1x.com/2019/12/07/QNSqFP.png)

1.Debug的值用于内部测试一般为空
2.Kmode的键值Win32.sys是windows内核部分的文件
3.Posix表名了SUA子系统会按需启动

## Widnows子系统
![QNiYCt.png](https://s2.ax1x.com/2019/12/07/QNiYCt.png)

crss.exe的功能
```
1.创建或删除进程和线程
2.对16位DOS虚拟机（VDM）进程的部分支撑（仅32位WIndows）
3.SxS/Fusion和清单文件（manifest）支持
4.其他一些函数，比如GetTempFile、DefineDosDevice、ExitWidnowsEx以及几个自然语言支持函数
```

win32.sys
```
1.窗口管理器：控制窗口显示、管理屏幕输出、采集来自键盘和鼠标或其他设备的输入，同时将用户消息传递给应用程序
2.图形设备接口：针对图形输出设备的函数库，其中包含线段、文本和图形的绘制函数，以及图形控制函数
3.DirectX功能的包装函数：WIndows对Direct X的支持是在另一个内核驱动程序（Dxgkrnl.sys）中实习的
```

Conhost.exe功能
```
提供了对控制台（字符环境）应用程序的支持
```

子系统DLL
```
Kernel32.dll、Advapi32.dll、User32.dll、Gdi32.dll将已文档化的Windows API函数，转译成
Ntoskrnl.exe和Win32k.sys中恰当的且绝大多数未文档化的内核模式系统服务调用
```

图形设备驱动程序
```
图形设备驱动程序，与硬件相关的图形显示器驱动程序、打印机程序和视频微端口驱动程序
```

## 控制台窗口宿主程序
子系统进程负责管理控制窗口，每个控制台应用程序（比如Cmd.exe，“命令提示符”程序）与Csrss进行通信。现在WIndows为系统中的每个控制台窗口使用了一个单独的进程：控制台窗口宿主进程（Conhost.exe）。多个控制台应用程序可以共享同一个控制台窗口，比如在从命令提示符窗口中发起一个新的命令提示符窗口。默认情况下，第二个命令提示符窗口共享前者的控制台窗口

无论何时，只要控制台应用程序向当前会话中正在运行的Csrss实例注册其自身，Csrss就利用客户进程的安全令牌，而不是Csrss的System令牌来创建Conhost实例。然后，它映射一个共享内存区，让所有的Conhost都可以与Csrss共享一部分内存，以便于高效地处理缓冲区。
![QNlJc4.png](https://s2.ax1x.com/2019/12/07/QNlJc4.png)

Conhost是用用户凭证运行的（意味着用户的特权级别），并且也运行在一个与控制台应用程序相关联的进程中，所以，用户界面特权隔离安全机制也适用于控制台进程。而且，CPU制约的控制台应用程序可能会被识别为它们背后的控制台宿主进程（若有必要，用户可以杀掉它）。

## UNIX应用子系统
针对UNIX应用子系统使得可以在一台运行WIdnows server系统，或者WIndows客户系统的企业或旗舰版本上编译和运行UNIX应用程序。SUA提供了将近2000个UNIX函数和300个UNIX类的工具和实用程序。

