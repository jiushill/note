## 前言 ##
- - -
临上学前，群内分享了一波遇见：安全狗等WAF如何通过一定的姿势绕过

## 正文 ##
- - -
这里我上google找了一个有安全狗的站。来进行测试
- 请求方式更改
- 隧道传输
- 边界传输
- 分块传输
- 边界+分块传输
- 边界+分块+注释干扰
- charset=ibm500,charset=ibm037编码绕过


<b>请求方式更改</b>
![kcIWIx.md.png](https://s2.ax1x.com/2019/02/19/kcIWIx.md.png)

改为POST
![7b81c691.png](:storage\f916cd10e8c61d02dccf\7b81c691.png)

<b>隧道传输</b>
说明:绕过一些老旧的WAF还行，新的安全狗不行
![kc5icQ.png](https://s2.ax1x.com/2019/02/19/kc5icQ.png)

先取消掉burp的Content-Length自动更新
![kc5Ans.png](https://s2.ax1x.com/2019/02/19/kc5Ans.png)

将Connection设置为：keep-alive
![kc5EBn.png](https://s2.ax1x.com/2019/02/19/kc5EBn.png)

将数据包复制到下面，注意空一行
![kc5mNV.png](https://s2.ax1x.com/2019/02/19/kc5mNV.png)

<b>边界传输</b>
点一下修改身体的编码(点一下，玩一年)
注意:记得开启Content-length自动更新
![kc58BR.png](https://s2.ax1x.com/2019/02/19/kc58BR.png)

![kc5YAx.md.png](https://s2.ax1x.com/2019/02/19/kc5YAx.md.png)

<b>分块传输</b>
添加Transfer-Encoding:chunked
![kc5rDA.png](https://s2.ax1x.com/2019/02/19/kc5rDA.png)

说明：
```
可以分成很变态的样子，看你怎么分，先写长度
如:
2
id
```
![kc5fgg.png](https://s2.ax1x.com/2019/02/19/kc5fgg.png)


<b>边界加分块传输</b>
![kcI8xg.png](https://s2.ax1x.com/2019/02/19/kcI8xg.png)

<b>边界分块传输+注释扰乱</b>
分块传输中可以用分号加载长度标识符后面来作为注释符，这样某些waf拼接起来也看不出来什么东西

![kcIYrj.png](https://s2.ax1x.com/2019/02/19/kcIYrj.png)

<b>charset=ibm037</b>
![kcI2ZR.png](https://s2.ax1x.com/2019/02/19/kcI2ZR.png)
