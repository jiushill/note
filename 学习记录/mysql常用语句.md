### mysql语句学习 ###
创建一个新的数据库
```mysql
create database 数据库名称
例子:create database tests

mysql> create database tests;
Query OK, 1 row affected (0.00 sec)
```

创建表名
```mysql

create table table_name（xxxx）

例子：
mysql> create table demo(
    -> name varchar(100) not null,
    -> id int not null auto_increment,
    -> primary key(id))ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.04 sec)
```
创建表名出现InnoDB的解决方法：https://blog.csdn.net/wuzeyuphp/article/details/78056903
```
打开my.ini
修改default-storage-engine=InnoDB
然后删除mysql 删除data目录下ib开头的日志文件重新启动
如果你不想字段为 NULL 可以设置字段的属性为 NOT NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
AUTO_INCREMENT定义列为自增的属性，一般用于主键，数值会自动加1。
PRIMARY KEY关键字用于定义列为主键。 您可以使用多列来定义主键，列间以逗号分隔。
ENGINE 设置存储引擎，CHARSET 设置编码。

```

插入数据到表
```mysql
insert into table_name(xx,xx) values (xx,xx)

例子：
mysql> insert into demo(id,name) values (1,'Demo');
Query OK, 1 row affected (0.02 sec)
```

查询一下看看有没有成功插入数据
```mysql
mysql> select * from demo;
+------+----+
| name | id |
+------+----+
| Demo |  1 |
+------+----+
1 row in set (0.00 sec)
```

修改数据
```mysql
update table_name set column_name='xxx'

例子：
mysql> update demo set name="demos";
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from demo;
+-------+----+
| name  | id |
+-------+----+
| demos |  1 |
+-------+----+
1 row in set (0.00 sec)
```

删除表
```mysql
drop table table_name

例子：
mysql> drop table demo;
Query OK, 0 rows affected (0.02 sec)
```

删除数据库
```mysql
drop database database_name

例子：
mysql> drop database tests;
Query OK, 0 rows affected (0.02 sec)
```

16进制加密和解码的用法
```
hex(xxx) #16进制编码
unhex(xxx) #16进制解码

例子：
mysql> select hex('ts');
+-----------+
| hex('ts') |
+-----------+
| 7473      |
+-----------+
1 row in set (0.00 sec)

mysql> select unhex('7473');
+---------------+
| unhex('7473') |
+---------------+
| ts            |
+---------------+
1 row in set (0.00 sec)
```

一些常用的函数
```mysql
version()
user()
@@basedir
@@datadir
ascii()
sleep()
substr(())
load_file()
updatexml()
concat()
count()
```

information_schema数据库
```mysql
select table_name from information_schema.tables where table_schema="数据库名"
select column_name from information_schema.columns where table_name="表名"
```

mysql修改密码
```mysql
set password for root@localhost=password('新密码')
```

mysql查看当前用户
```mysql
mysql> select Host,User,Password from mysql.user;
+-----------+------+-------------------------------------------+
| Host      | User | Password                                  |
+-----------+------+-------------------------------------------+
| localhost | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
| 127.0.0.1 | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
| ::1       | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
+-----------+------+-------------------------------------------+
3 rows in set (0.00 sec)
```