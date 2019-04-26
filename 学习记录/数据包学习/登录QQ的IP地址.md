## 网络数据分析溯源(登录QQ的IP地址)  ##
题目要求:
```
安全工程师“墨者”在维护日常网络时，抓取了一段Wireshark数据流量包，发现有违规QQ登录数据，你也来试试找到这个IP地址吧。
```


## 解题思路 ##
一开始想从UDP下手，后面想了一下发现qq只不过是个客户端。请求登录还是会发送http请求到qq.com然后进行登录验证。后面搜索过滤表达式
```
http.request.method==POST
关键字:qq.com
```
如图所示
![](https://s2.ax1x.com/2019/04/25/EZBrkQ.png)


提交IP即可获得flag
```
mozhe2fca66ed8676aba617548b28fd6
```
