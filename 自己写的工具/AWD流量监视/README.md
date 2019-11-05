# 流量监视脚本
所需模块：
```text
scapy
```

根据规则捕获数据包，默认设置是`ip dst 192.168.1.104`捕获目的地址IP为`192.168.1.104`的流量，这是我局域网内的IP。按自身需求来修改流量。由于scapy
的wrpcap保存数据包函数每次包含会创建一个新的文件，我只好把它写入file文件夹下。然后单独写个脚本读取所有pcap并写入到一个pcap里
```text
Jk.py - 根据规则捕获流量
rd.py - 读取file文件夹下所有pcap文件并写入到一个pcap文件里（jg.pcap）
```
![](https://s2.ax1x.com/2019/11/05/M9mnBj.png)

![](https://s2.ax1x.com/2019/11/05/M9mQNq.png)

![](https://s2.ax1x.com/2019/11/05/M9nS2T.png)