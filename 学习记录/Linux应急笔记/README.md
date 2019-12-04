# Linux应急

Linux应急分为4个环节
1.发现主机的异常现象，识别出病毒的可疑现象
2.然后定位具体的病毒进程以及病毒文件，进行清除
3.检查启动项等防止病毒在次被创建
4.系统加固，防止病毒再次从缺口进入


![MqloTJ.md.png](https://s2.ax1x.com/2019/11/23/MqloTJ.md.png)

# 0x01识别现象
第一个环节要做的通过系统允许状态、安全设备告警，发现主机异常现象，已经确认病毒的可疑行为。

系统CPU是否异常
枚举系统进程，CPU降序排序：top
![Mq3XZD.png](https://s2.ax1x.com/2019/11/23/Mq3XZD.png)

![Mq8tY9.md.png](https://s2.ax1x.com/2019/11/23/Mq8tY9.md.png)

寻找command里面的可疑字符和注意某进程CPU运行率超过50%的
![Mq8f6P.png](https://s2.ax1x.com/2019/11/23/Mq8f6P.png)

找出与之通信的C2 IP地址
![MqGKtH.png](https://s2.ax1x.com/2019/11/23/MqGKtH.png)

寻找指定IP
while true;do netstat -antp | grep [IP];done

![MqGHHO.png](https://s2.ax1x.com/2019/11/23/MqGHHO.png)

![MqGO4H.png](https://s2.ax1x.com/2019/11/23/MqGO4H.png)

如果防火墙给出是个域名的话，修改/etc/hosts文件给域名一个随机IP然后在监控这个IP
![MqGxgI.png](https://s2.ax1x.com/2019/11/23/MqGxgI.png)

![MqJZ2n.png](https://s2.ax1x.com/2019/11/23/MqJZ2n.png)

寻找可疑的历史命令history
![MqJ2sP.png](https://s2.ax1x.com/2019/11/23/MqJ2sP.png)

# 0x02清除病毒
定位可疑进程，结束进程
ps -elf | grep [关键内容]
kill -9 []pid]
快速结束多个PID的方法：
```
kill -9 `ps -elf | grep [内容] | awk '{print $2}'`
```
![MqYI0K.png](https://s2.ax1x.com/2019/11/23/MqYI0K.png)

![MqN9Dx.png](https://s2.ax1x.com/2019/11/23/MqN9Dx.png)

定位病毒路径
ls -al /proc/[pid]/exe
rm -rf [path]
![Mqtd4e.png](https://s2.ax1x.com/2019/11/23/Mqtd4e.png)

![MqtRUS.png](https://s2.ax1x.com/2019/11/23/MqtRUS.png)

# 0x03清除维持后门
枚举定时任务
crontab -l
![MqNriF.png](https://s2.ax1x.com/2019/11/23/MqNriF.png)

![MqNgMR.png](https://s2.ax1x.com/2019/11/23/MqNgMR.png)

查看anacron异步定时任务
cat /etc/anacrontab
![MqN7zd.png](https://s2.ax1x.com/2019/11/23/MqN7zd.png)

检查是否存在恶意服务
service --status-all
![MqUiyn.png](https://s2.ax1x.com/2019/11/23/MqUiyn.png)

检查系统文件是否被劫持
枚举系统文件夹的文件，按修改事件排序查看7天内被修改过的文件
find /usr/bin/ /usr/sbin/ /bin/ /usr/local/bin/ -type f -mtime +7 | xargs ls -la 
![MqUWlj.png](https://s2.ax1x.com/2019/11/23/MqUWlj.png)

监控守护进程的行为：
lsof -p [pid]
strace -tt -T -e trace=all -p pid
![MqauAf.png](https://s2.ax1x.com/2019/11/23/MqauAf.png)

枚举/扫描是否存在恶意驱动
lsmod
![MqdCbq.png](https://s2.ax1x.com/2019/11/23/MqdCbq.png)

![MqdVGF.md.png](https://s2.ax1x.com/2019/11/23/MqdVGF.md.png)

# 0x04查询登录成功的用户和history
history
![](http://ww1.sinaimg.cn/large/006LG7Nygy1g9l42m1u7gj30ow0oo40w.jpg)

顺便记录一下grep命令的正则提取
```
grep -P "正则" -o #使用正则匹配，只输出正则匹配到的东西
```
![](http://ww1.sinaimg.cn/large/006LG7Nygy1g9l44pr5o7j31980komyi.jpg)

last命令，对应的日志文件/var/log/wtmp； 成功登录用户
lastb命令，对应的日志文件/var/log/btmp； 尝试登录信息
lastlog命令，对应的日志文件/var/log/lastlog； 显示最近登录信息

# 0x05系统加固
发现攻击者从什么地方进来的，及时修复漏洞。并进一步加固 

查询log主机登录日志
![Mqd2ss.png](https://s2.ax1x.com/2019/11/23/Mqd2ss.png)

打补丁，加固配置等
![Mqd7z4.md.png](https://s2.ax1x.com/2019/11/23/Mqd7z4.md.png)