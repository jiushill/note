## 网络数据分析溯源(连接login.php的IP)  ##
题目要求:
```
某公司安全工程师抓取到一段Wireshark数据包，其中有一个IP连接过/admin_d98gD2@k/login.php。
```

## 解题思路  ##
搜索过滤表达式
```
http.request
搜索字符串关键字:/admin_d98gD2@k/login.php
```
提交IP即可获得flag
![](https://s2.ax1x.com/2019/04/25/EZyRC4.png)

flag
```
mozhefc1b0eb9952e927516be5bd4f53
```
