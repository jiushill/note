## wireshark之文件还原  ##
题目链接：https://www.mozhe.cn/bug/detail/L2F5TmNjeVlNYkk2Sy9xb0VuRmtMZz09bW96aGUmozhe

![](https://s2.ax1x.com/2019/04/24/EVLOhj.png)


给了墨币买了题后，访问链接下载压缩包
![](https://s2.ax1x.com/2019/04/24/EVOCHU.png)

## 解题操作 ##

<b>题目要求</b>
```
某公司网络管理员抓取一段Wireshark数据包，发现某人从xxx.com网站上下载一压缩包，请找到压缩包内容
```

unzip解压压缩包，wireshark打开数据包，搜索关键字:zip
得到两个结果
```
1.zip
key.zip #肯定是key.zip啦～
```
![](https://s2.ax1x.com/2019/04/24/EVOG8A.png)

![](https://s2.ax1x.com/2019/04/24/EVO0Ug.md.png)

追踪TCP数据流，以原数据导出
![](https://s2.ax1x.com/2019/04/24/EVO2rV.png)

![](https://s2.ax1x.com/2019/04/24/EVOfVU.png)

![](https://s2.ax1x.com/2019/04/24/EVO454.png)

命令解压，压缩包
![](https://s2.ax1x.com/2019/04/24/EVOLqK.png)

查看key.jpg图片
![](https://s2.ax1x.com/2019/04/24/EVOjaD.md.png)

输入ea6a87获取flag
```
mozhee74c52eb006a01b5ddfa197cd4d
```
