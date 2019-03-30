### LINUX简介 ###
LINUX是一套使用和自由传遍的类UNINX操作系统，是一个基于POSIX和UNIX的多用户，多任务支持多线程和多CPU的操作系统。目前更多企业将计划使用Linux服务器，在这方面超过了微软。因此掌握Lunux系统多一个渗透测试人员来说至关重要

### LINUX远程连接 ###
ssh连接
Telnet连接
推荐第一者

### LINUX的目录结构 ###
```
root--root用户目录
home--存储普通用户的个人文件
 user1
 user2
bin--系统启动时需要执行的文件（二进制）
sbin--可执行程序的目录，但大多存放涉及系统管理的命令。只有root权限才能执行
proc--虚拟，存在Linux内核镜像；保存所以内核参数及系统配置信息
 1--进程编号
usr--用户目录，存放用户级的文件
   bin--几乎所有用户所用的命令，另外存在于/bin,/usr/local/bin
   sbin--系统管理员命令，与用户相关，例如，大部分服务器程序
   include--存放C/C++头文件目录
   lib--固定的程序数据
   local--本地安装软件保存位置
   man--手工生成的目录
   info--信息文档
   doc--不同包文档信息
   tmp
   X11R6--该目录用于保存X-Windows所需的所有文件。该目录中还包含用于运行GUI要的配置文件和二进制文件
   X386--功能X11R6,X11发行版5的系统文件
boot--引导加载器所需文件，系统所需图片保存于此
lib--根文件系统目录下程序和核心模块的公共模块的公共库
 modules--可加载模块，系统奔溃后重启所需要的模块
dev--设备文件目录
etc--配置文件
 skel--home目录建立，该目录初始化
 sysconfig--网络，时间，键盘等配置记录
var
  file
  lib--该目录下的文件在系统运行时，会改变
  local--安装在/usr/local的程序数据，变化的
  lock--文件特定外设或文件，为其上锁，其他文件暂时不能访问
  log--记录日志
  run--系统运行合法信息
  spool--打印机，邮件，代理服务器等脱机目录
  tmp
  catman--缓冲目录
mnt--临时用于挂载文件系统的地方。一般情况下这个目录是空的，而在我们将要挂载分区时在这个目录下建立目录，再将我们将要访问的设备挂载在这个目录上，这样我们就可访问文件了。
tmp--临时文件目录，系统启动后的临时文件存放在/var/tmp/
lost+found--在文件系统修复时恢复的文件
```

### LINUX基础命令 ###
```
pwd 查看当前目录
ls 显示文件目录
mkdir 创建目录
rm 删除文件和目录
co 复制文件和目录
mv 移动文件和目录
cat 显示文件内容
cat /etc/passwd 查看所有用户
useradd 用户名 添加用户
passwd 给用户添加密码或修改密码
userdel 删除用户
cat /etc/group 查看所有用户组
groupadd 添加用户组
groupdel 删除用户组
tar czvf 创建一个压缩包
tar xvf 解压tgz压缩包
apt -get install 安装软件
apt search mysql 搜索所有mysql的包
apt-get remove vim 删除vim
ps aux 显示所有进程
killall 进程名 结束指定的进程
```