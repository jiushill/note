# Windows的核心系统文件
|文件名称|组件|
|-|-|
Ntoskrnl.exe|执行体和内核
Ntkrnlpa.exe（仅用于32位系统）|执行体和内核，支持物理地址扩展（PAE），使得32位系统可寻址多达64GB物理内存，以及将内存标记位不可执行的
Hal.dl|硬件抽象层
Win32k.sys|Windows子系统的内核模式部分
Ntdll.dll|内部支持函数，以及执行体函数的系统服务分发存根（stub）
Kernel32.dll,Advapi32.dll,User32.dll,Gdi32.dl|Windows的核心子系统DLL

# 可移植性
Widnows在设计时，就确定要能够运行在各种不同的硬件体系架构之上。Windows的初始发行版本支持x86和MIPS体系架构。稍后又加入了对DEC。在Widnows NT 3.51中又加入了对第四种处理器架构Motorola PowerPC的支持。然而，由于市场需求的变化，在windows2000开发前夕，对MIPS和PowerPC体系架构的支持被放弃了。后来，Compaq又撤销了AlphaAXP体系架构的支持，所以最终的结果是，Widnows 2000只支持x86体系架构。Widnows Xp和Windows Server 2003增加了三种对64位处理器家族的支持，分别是Intel Itanium IA-64族、AMD64族，以及Intel针对x86的64位扩展技术（EM64T，它与AMD64体系架构相兼容，但在所支持的指令方面略有差别）。后两种处理器族称为64位扩展系统。

![006LG7Nygy1g919z4loyfj30mr0d8gtm.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g919z4loyfj30mr0d8gtm.jpg)

# 对称多处理
多任务是指让多个执行线程共享同一个处理器的操作系统技术。然而，当一台计算机有不止一个处理器时，它可以同时执行多个线程。因此，虽然一个多任务操作系统只不过看起来好像同一时刻可以执行多个线程，但是，一个多处理器操作系统可以真正地做到同一时刻执行多个线程，在每个处理器上执行一个线程。

Windows的一个关键设计目标是，必须能够很好地在多处理器计算机系统上运行。*Windows是一个对称多处理器*操作系统。没有主处理器————操作系统和用户线程可以被调度到任何处理器上运行。而且，所有的处理器共享唯一的内存空间。这种模型与*非多对称出来*不同，在一个典型的非对称多处理器操作系统中，系统选择其中一个处理器来执行操作系统内核代码，而其他的处理器只运行用户代码。

![006LG7Nygy1g91aqq9snaj30ov0dqn33.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g91aqq9snaj30ov0dqn33.jpg)

# 超线程
超线程是intel引入的一项技术，它可以在每个物理核上提供多个逻辑处理器。每个逻辑处理器都有自己的CPU状态，但是执行引擎和片上缓存则是共享的。这使得一个逻辑CPU可以在其他逻辑CPU停转（比如缓存未命中，或者分支预测错误）的时候继续执行。调度算法已经被该进过了，因而可以最佳地利用支持超线程的机器，例如，原来的做法就是将线程调度到一个空闲的无聊处理器上，现在则该进为“选择一个物理处理器上的空闲逻辑处理器”。

![006LG7Nygy1g91axkkvk5j30q50anq7m.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g91axkkvk5j30q50anq7m.jpg)












