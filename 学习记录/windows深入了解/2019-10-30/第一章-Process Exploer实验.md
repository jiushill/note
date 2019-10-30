# 基础概念和术语
## windows API：
windows API是针对windows操作系统家族的用户模式系统编程接口。在64位版本被推广以前，32位版本windows操作系统的编程接口被称为win32 API。相应的以前的16位接口被称为win 16API

windows API参考文档
```
https://www.msdn.microsoft.com
```

windows API可调用的函数分为：
* 基本服务
* 组件服务
* 用户界面服务
* 图形和多媒体服务
* 网络
* web服务

## 关于.NET
.NET框架是由一个被称为框架类库和一个提供托管代码执行环节的公共语言运行库组成的。
后者提供的托管代码执行环节包含以下特性：
* 即时编译
* 类型检验
* 垃圾回收和代码访问

C#在.NET平台上工作

## 服务、函数和列程
* windows API函数：指Windows API已经被文档化、可调用的子例程，例如CreateProcess、CreateFile和GetMessage

* 原生系统服务（或者系统调用）：指操作系统中未文档化的、可在用户模式下调用的底层服务。例如，NtCteateUserProcess是一个内部系统服务

* 内核支持函数（或例程）：指位于windows操作系统内部而且只能在内核模式下调用的子例程。例如ExAllocatePoolWithTag就是一个这样的例程，设备驱动程序调用该例程调用可以向windows系统堆（称为内存池）申请内存

* windows服务：指由windows服务控制管理启动的进程。例如，Task Scheduler服务运行在用户模式进程中，它支持at命令（类似于UNIX命令at或cron）。

* DLL（动态链接库）：指一组可调用的子例程，合起来被链程一个二进制文件，使用这些子例程的应用程序可以动态加载此二进制文件。例如：Kernel32.dll(一个windows API子系统库)



## 进程、线程和作业
程序：是指一静态的指令序列
进程：包了执行程序的特定实例时所用到的各种资源

* 私有的虚拟地址空间，指该进程可以使用的一组虚拟内存地址
* 可执行的程序，它定义了初始的代码和数据，并且被映射到进程的虚拟地址空间
* 已打开句柄的列表，这些句柄指向各自系统资源，比如信号量、通信端口和文件，该进程内所有的线程都可以访问这些系统资源
* 被称为访问令牌的安全环境，它标识了与该进程相关联的用户、安全组、特权、UAC（用户账户控制）虚拟化状态、会话，已经有限的用户账户状态
* 被称为进程ID的唯一标识符（在内部，进程ID还是标识符客户ID的一部分）
* 至少一个执行进程（尽管“空”进程也是有可能的，但没有用处）

## 实验-查看进程树
```C
#include <stdio.h>
#include <windows.h>
#include <string.h>
#include <tlhelp32.h>

int main(){
    PROCESSENTRY32 pe32;
    pe32.dwSize= sizeof(pe32); //初始化
    HANDLE  CL=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0); //获取系统句柄
    if(CL==INVALID_HANDLE_VALUE){ //返回结果等于INVALID_HANDLE_VALUE则为枚举失败
        printf("CreateToolhelp32Snapshot Error\n");
    }
    BOOL bprocess=Process32First(CL,&pe32);
    while (bprocess){
        printf("%s---%d\n",pe32.szExeFile,pe32.th32ProcessID);
        bprocess=Process32Next(CL,&pe32); //windows API文档上提到的指针都要用取址符,如果不重新赋结果给bprocess会造成死循环
    }
    CloseHandle(CL);
    return 0;
}
```
![](https://s2.ax1x.com/2019/10/30/K4LXMd.png)

枚举所有进程和PID原理：
1.获取系统所以快照
2.使用Process32EFirst来获取对应的PID和进程名
3.循环输出，在循环后面使用Process32Next进行下一个获取

参考链接：
[使用CreateToolHelp32Snapshot函数列出所有进程](https://blog.csdn.net/qq_41917908/article/details/81350930)
[Process32Next \| Microsoft Docs](https://docs.microsoft.com/en-us/previous-versions/aa908729%28v%3dmsdn.10%29)
[Process32First function (tlhelp32.h) \| Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32first)
[PROCESSENTRY32 (tlhelp32.h) \| Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32)
[SECURITY_ATTRIBUTES structure (Windows) \| Microsoft Docs](https://docs.microsoft.com/zh-cn/previous-versions/windows/desktop/legacy/aa379560(v=vs.85))

使用API的几点小结：
* 有类似于`指向XXX结构的指针`是让你定义一个这个类型指针的变量，点进去仔细看
![K4O6eI.png](https://s2.ax1x.com/2019/10/30/K4O6eI.png)

![K4OHwq.png](https://s2.ax1x.com/2019/10/30/K4OHwq.png)

* 函数让你传入什么类型的参数你就定义什么类型的参数，根据文档走
![K4XktK.png](https://s2.ax1x.com/2019/10/30/K4XktK.png)

可以使用自带的任务管理器或procexp（Process Explorer）来查询进程
![K4xHvF.png](https://s2.ax1x.com/2019/10/30/K4xHvF.png)

父进程与子进程
![K4jiuj.png](https://s2.ax1x.com/2019/10/30/K4jiuj.png)


![K4zHit.png](https://s2.ax1x.com/2019/10/30/K4zHit.png)

Process Explorer简单说明：
* 将鼠标移动到进程名上时，提示框会显示它所宿纳的服务
![K5SBSf.png](https://s2.ax1x.com/2019/10/30/K5SBSf.png)

* 进程的目标
* 宿纳与进程内的COM对象
* 子进程

基本功能：
1.默认配置下，宿纳服务的进程被加亮显示为粉色，而你自己的进程加亮显示为蓝色
![K59NGt.png](https://s2.ax1x.com/2019/10/30/K59NGt.png)

2.将鼠标移动到进程的映像名上，可以提示信息中看到完整的路径名
3.单机view菜单，打开Select Columns对话框，在Process Image选项卡中加入Image Path列 （可以看到勾选了的内容）
![K59bJ1.png](https://s2.ax1x.com/2019/10/30/K59bJ1.png)

4.在View菜单中，不要选择Show Process From All Users以只显示你自己的进程
![K5CkSP.png](https://s2.ax1x.com/2019/10/30/K5CkSP.png)

5.在Options菜单中，选择Difference Highlight Duaration命令，将相应的值设置为5秒
|
|----启动一个进程以绿色显示5秒
|----结束一个进程以红色显示5秒

可以看到系统中创建和结束的进程

6.最后，在某个进程上双机可以看到进程属性对话框的各个选项卡中查看各种信息


