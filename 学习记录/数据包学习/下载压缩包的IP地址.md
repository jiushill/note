## 网络数据分析溯源(下载压缩包的IP地址)  ##
题目要求:
```
某公司安全工程师抓取到一段wireshark数据包，其中有多个IP对目标服务器做访问，其中一个IP下载走一个DB.ZIP 的压缩包。
```

## 解题思路 ##
wireshark搜索过滤表达式
```
http.request
字符串关键字:DB.zip
```

![](https://s2.ax1x.com/2019/04/25/EZ60iD.png)

提交IP即可获得flag
```
mozhe9189a32649cd7f2657d29009d92
```
