## mysql call函数的使用 ##
>MySQL 存储过程是从 MySQL 5.0 开始增加的新功能。存储过程的优点有一箩筐。
不过最主要的还是执行效率和SQL 代码封装。特别是 SQL 代码封装功能，
如果没有存储过程，在外部程序访问数据库时（例如 PHP），要组织很多 SQL 语句。
特别是业务逻辑复杂的时候，一大堆的 SQL 和条件夹杂在 PHP 代码中，让人不寒而栗。
现在有了 MySQL 存储过程，业务逻辑可以封装存储过程中，这样不仅容易维护，而且执行效率也高。


call相当于执行函数，类似于py里的def

例子:
```mysql
mysql> use test;
Database changed
mysql> create procedure demo() select user();
Query OK, 0 rows affected (0.02 sec)

mysql> call demo();
+----------------+
| user()         |
+----------------+
| root@localhost |
+----------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.02 sec)
``

是否存在注入要看定义函数里面的语句，和函数。有些函数是有设置参数的
还有要符合参数的，如果函数设置不当的话可能存在注入。

使用call函数的时候数据库里面必须要有这个函数不然会报错

有参数的函数例子
```mysql
mysql> create procedure demo(a int) select a;
Query OK, 0 rows affected (0.00 sec)

mysql> call demo(1);
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

参数可以限死类型，可以有效的防御sql注入，call函数是个防注入的不错选择

参考文章:https://www.cnblogs.com/you-zi/p/5519006.html