## 网络数据分析溯源(ping服务器的IP地址)  ##
题目要求:
```
某公司安全工程师抓取到一段Wireshark数据包，其中有一个IP不间断的在ping服务器，,请找到这个ip地址。
```


## 解题思路  ##
wireshark搜索关键过滤表达式
```
icmp
```

发现203.39.8.77这个IP一直在ping，提交这个ip即可获得flag

flag
```
mozhe9e7f246cb5e6fc1dec9a6cef027
```
