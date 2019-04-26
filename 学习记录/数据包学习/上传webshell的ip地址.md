## 网络数据分析溯源(上传WebShell的IP地址)  ##
题目要求：
```
某公司安全工程师抓取到一段Wireshark数据包，发现有人成功上传了WebShell，请找到上传者的IP地址。
```


## 解题思路 ##
居然是文件上传，那么请求方式肯定是POST，过滤掉请求方式。然后搜索关键字
```
http.request.method==POST #过滤请求方式，注意POST是大写的
关键字:upload
```

然后在某条数据里发现小马：
![](https://s2.ax1x.com/2019/04/25/EZwfg0.png)

提交IP获取flag即可
```
mozhed86aaea8d976f0f7475b72b2b68
```
