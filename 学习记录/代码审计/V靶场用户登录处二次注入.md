## V靶场用户登录处二次注入 ##
- - -
先看user文件夹里面的
regCheck.php
```php
<?php
include_once('../sys/config.php');

if (isset($_POST['submit']) && !empty($_POST['user']) && !empty($_POST['passwd'])) {

	if (strlen($_POST['user'])>16) {
		$_SESSION['error_info'] = '用户名過長（用戶名長度<=16）';
		header('Location: reg.php');
		exit;
	}

	//过滤输入变量
	$clean_name = clean_input($_POST['user']);
	$clean_pass = clean_input($_POST['passwd']);
	$avatar = '../images/default.jpg';
	
	//判断用户名已是否存在
	$query = "SELECT * FROM users WHERE user_name = '$clean_name'";
    $data = mysql_query($query, $conn);
	if (mysql_num_rows($data) == 1) {
		$_SESSION['error_info'] = '用户名已存在';
		header('Location: reg.php');
	}
	//添加用户
	else {
		$_SESSION['username'] = $clean_name;
		$_SESSION['avatar'] = $avatar;
		$date = date('Y-m-d');
		$query = "INSERT INTO users(user_name,user_pass,user_avatar,join_date) VALUES ('$clean_name',SHA('$clean_pass'),'$avatar','$date')";
		mysql_query($query, $conn) or die("Error!!");
		header('Location: user.php');
	}
	mysql_close($conn);
}
else {
	not_find($_SERVER['PHP_SELF']);
}
?>
```

logCheck.php
```php
<?php
include_once('../sys/config.php');

if (isset($_POST['submit']) && !empty($_POST['user']) && !empty($_POST['pass'])) {
	$clean_name = clean_input($_POST['user']);
	$clean_pass = clean_input($_POST['pass']);
    $query = "SELECT * FROM users WHERE user_name = '$clean_name' AND user_pass = SHA('$clean_pass')";
    $data = mysql_query($query, $conn) or die('Error!!');

    if (mysql_num_rows($data) == 1) {
        $row = mysql_fetch_array($data);
		$_SESSION['username'] = $row['user_name'];
		$_SESSION['avatar'] = $row['user_avatar'];
		$ip = sqlwaf(get_client_ip());
		$query = "UPDATE users SET login_ip = '$ip' WHERE user_id = '$row[user_id]'";
		mysql_query($query, $conn) or die("updata error!");
        header('Location: user.php');
        }
	else {
        $query = "SELECT * FROM users WHERE user_name = '$clean_name' AND user_pass = SHA('$clean_pass')";
		$_SESSION['error_info'] = '用户名或密码错误,查询的语句是：'.$query;
		header('Location: login.php');
	}
	mysql_close($conn);
}
else {
	not_find($_SERVER['PHP_SELF']);
}
?>
```

user.php
```php
<?php
include_once '../sys/config.php';

if ( isset( $_SESSION['username'] ) ) {

	include_once '../header.php';

	if ( !isset( $SESSION['user_id'] ) ) {
		$query = "SELECT * FROM users WHERE user_name = '{$_SESSION['username']}'"; /*没对$_session['username']做任何过滤，存在注入*/
        echo $query;
		$data = mysql_query( $query, $conn ) or die( 'Error!!' );
		mysql_close( $conn );
		$result = mysql_fetch_array( $data );
		$_SESSION['user_id'] = $result['user_id'];
	}

	$html_avatar = htmlspecialchars( $_SESSION['avatar'] );
?>
<div class="row">
	<div style="float:left;">
		<img src="avatar.php" width="100" height="100" class="img-thumbnail" >
		<div class="text-center"><?php echo $_SESSION['username']?></div>
	</div>

	<div style="float:right;padding-right:900px">
		<div><a href="logout.php"><button type="button" class="btn btn-primary">退出</button></a></div>
		<br />
		<div><a href="edit.php"><button type="button" class="btn btn-primary">编辑</button></a></div>
		<br />
		<div><a href="../message.php"><button type="button" class="btn btn-primary">发留言</button></a></div><br /><br /><br /><br />
	</div>
</div>
<?php
	require_once '../footer.php';
}
else {
	not_find( $_SERVER['PHP_SELF'] );
}
?>
```

<b>整体思路</b>
```
注册用户名的时候，如果注册成功就将注册的用户名带入session然后在写入数据库里，然后跳转到user.php里面进行查询。
虽然user.php的查询没有做过滤$_SESSION['username']但是由于注册的哪里做了SQL过滤。所以带入sesion的时候已经被过滤了，所以注入不了
然后进行退出，重新登陆，虽然登录哪里做了过滤但是用户名成功查询到了，然后将查询到的用户名
带入session然后跳到user.php里面进行查询，由于直接将查询成功的用户名带入user.php查询中途没做任何过滤，user.php也没有过滤所以导致二次注入
```

<b>实验</b>
PS：首先说一下这个靶场的坑b之处，只要语句查询成功就不输出Error，是输出error不是mysql报错
也就是说完全是用来测试二次注入的。。这作者得挨打

先注册一个a'的用户名
下图为注册成功后调整到user.php
![krwiKs.md.png](https://s2.ax1x.com/2019/02/15/krwiKs.md.png)

处理注册的php
![krwkbq.png](https://s2.ax1x.com/2019/02/15/krwkbq.png)

退出重新登陆
![krwZ5T.png](https://s2.ax1x.com/2019/02/15/krwZ5T.png)

处理登陆的php
![krwmPU.png](https://s2.ax1x.com/2019/02/15/krwmPU.png)

这里的查询语句输出我自己加上去的，方便看效果