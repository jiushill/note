## 网络数据分析溯源(WebShell密码) ##
题目要求:
```
某公司安全工程师抓取到一段Wireshark数据包，发现其中一IP在连接某网站的木马，请你分析这段数据包找到木马的连接密码
```


## 解题思路 ##
搜索过滤表达式:http.request.method==POST，搜索字符串关键字:php
发现xiaoma.php的请求
![](https://s2.ax1x.com/2019/04/25/EZ06sK.png)

一开始以为是z0是答案，后面发现答案是:d76R3478

居然都是xiaoma.php了，那么key肯定是答案。。。

flag为
```
mozhed706bc28b003a6eacef46ce5def
```
