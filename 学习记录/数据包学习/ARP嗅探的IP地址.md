## 网络数据分析溯源(ARP嗅探的IP地址)  ##
目标:
```
安全工程师“墨者”在维护日常网络时，抓取了一段Wireshark数据流量包，发现有违规QQ登录数据，你也来试试找到这个IP地址吧。
```

## 解题思路 ##
纠结了几乎20分钟做了出来= =。首先apr嗅探，也就是arp广播：
arp广播的原理是：你的mac地址广播到ff:ff:ff:ff:ff:ff。ff:ff:ff:ff:ff:ff去广播局域网或者的IP地址或mac地址，然后你获得存活的mac地址和ip地址

搜索过滤表达式
```
eth.dst==ff:ff:ff:ff:ff:ff
```
发现有几条，一个我卡是华硕的，一个是vm里面发出来广播请求的
![](https://s2.ax1x.com/2019/04/25/EZsotg.md.png)

提交了华硕的发现不对，提交了vm的ip地址发现对了
flag为
```
mozhef27ee80925297d15528bd29ed5d
```
