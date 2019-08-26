## SSH隧道学习 ##

参考文章：

https://www.cnblogs.com/williamjie/p/9684684.html

https://blog.csdn.net/jackliu16/article/details/80640467



常用的地方：

公司内部不允许连接某些网站，咳咳，不能连外网（企业都是通过路由器然后在到防火墙进行连接外网）。你的老逗在路由器上干了xx手脚导致你不能上xx网

![](https://s2.ax1x.com/2019/08/26/mRjAbV.png)



针对允许外网流量进入而不允许内网流量出

将外网流量转发到本地指定端口的命令：

```
ssh -N -f -L 4444:204.69.153.64:80 192.168.3.6
ssh -N -f -L [本地端口]:[外网IP]:[外网端口] [本机IP地址]
```

此时访问127.0.0.1:4444即可访问到外网服务器



例如这里将windows的3389转发到本地的4444端口

```
windows server 2008:192.168.241.129
Debain:192.168.241.150
```

![](https://s2.ax1x.com/2019/08/26/mRvpdK.png)



server 2008

![](https://s2.ax1x.com/2019/08/26/mRvuo8.png)



远程连接

![](https://s2.ax1x.com/2019/08/26/mRvyO1.md.png)



将本机映射出去的好像失败了，这里就不弄了