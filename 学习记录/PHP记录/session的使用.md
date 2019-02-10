# session的使用 #

<b>Session的意义</b>
- - -
一个session代表用户打开浏览器连接网站，直到关闭浏览器为止的工作期间，此期间不论用户浏览该网站任何页面，甚至离开网站又返回来，对于网站而言都是一个session。

不过只要重新打开浏览器就是一个新的session
![session-in-php.png](https://www.sitesbay.com/php/images/session-in-php.png)

当网页程序使用session技术存储状态或数据时，无论是否为相同页面，只要在同一个session内即可访问同一份数据。如果是不同session，就算在同一台计算机、使用相同的浏览器、连接相同的网页、读写同一份数据，其所访问的仍然是两份不同状态的数据。
<b>Session的原理</b>
- - -
Session是一种将数据记录在数据库上的技术，下面是其运行示意图：
![wKiom1L4OH2S5JwHAAA5g2I22fE912.png](http://s1.51cto.com/wyfs02/M02/12/12/wKiom1L4OH2S5JwHAAA5g2I22fE912.png)
从上面的图可以看到，程序必须以Cookie来获取一个Session，一般情况下，Session会存放在没有过期的
Cookie内（但是其他的Session数据存储在服务器上），所以同一个网站的相同与不相同网页之间可以借助Cookie掌握同一个Session。

<b>访问Session</b>
- - -
在PHP中，只要先运行session_start()函数，打开session功能，即可在后续步骤中访问session。不过如前所述，Session默认使用Cookie传递Session ID，而Cookie信息会放在HTTP头中，并且HTTP头必须在所有输出之前提交，所以session_start()函数运行之前，如果有echo()或HTML标记等输出，将会导致session_start()函数运行报错，而无法使用session功能。

但是如果你非要输出的话也不是不行
```
ob_start() /*打开php缓冲区*/
echo xxx; /*打开缓存区后直到调用缓冲区前，输出的东西都放在缓冲区*/
session_start()
ob_end_flush() /*释放缓冲区里面的内容*/
```
创建session和修改session的示范如下：
注意：可以不用session_start()
```
session_start() /*打开session功能*/
$_SESSION['user']="admin"; /*创建session的user变量，并赋值为admin*/
$_SESSION['user']="public"; /*修改session的值为public*/
```

设置session变量之后，只要使用$_SESSION[name]即可读取前面所存的数据
```
echo $_SESSION['user'];
```

<b>删除session</b>
- - -
关闭浏览器时，就无法访问之前的session，但是很多时候，即时浏览器没有关闭，程序也有必要主动删除session。举例来说，银行会提供用户注销的按钮，让用户安心的退出。这时，程序就必须注销session，否则只要利用浏览器的“上一页”按钮返回到之前的网页，就可以使用原来的session。

下面的删除session的范例：
```
unset($_SESSION['x']); /*删除Session的x变量*/
session_unset(); /*删除所有session变量*/
```

<b>同一网页访问session</b>
- - -
代码如下：
```php
<?php
header("Content-type: text/html;charset=utf-8");
ob_start(); /*打开缓冲区*/
echo "demo";
session_start(); /*会话开始*/
$r=ob_end_flush(); /*释放缓冲区*/
echo $r."<br>";
$count=0;
if(isset($_COOKIE['FK'])) { /*判断是否存在cookie*/
    if(isset($_SESSION['entered'])) { /*判断是否存在会话，如果存在则cookie不加1，否则cookie+1。若无cookie则设置一个cookie然后设置session*/
        $count = $_COOKIE['FK'];
    }else {
        $count = $_COOKIE['FK'] + 1;
    }
}
setcookie('FK',$count,time()+20*60*800);
echo "这是第".$count."次访问";

$_SESSION['entered']=TRUE;
?>
```

测试结果如下：
![](https://s2.ax1x.com/2019/02/09/kUQ5rt.png)

<b>同一网站的不同网页访问相同的session</b>
- - -
demo_3.php代码如下：
```php
<?php
header("Content-type: text/html;charset=utf-8");
session_start();
date_default_timezone_set("Asia/Shanghai");
if (!isset($_SESSION['enterTime'])) {
    $_SESSION['enterTime'] = time();
}
?>

<html>
<head>
    <title>session测试2</title>
</head>
<body>
<p>本次进站时间是：
    <?php echo date("H 时 i 分 s 秒",$_SESSION['enterTime']);?>
</p>
<br>
<a href="demo_4.php">点我查看在本站逗留时间</a>
</body>
</html>
```

demo4_.php代码如下：
```php
<?php
header("Content-type: text/html;charset=utf-8");
session_start();
date_default_timezone_set("Asia/Shanghai");
$duration=0;
if (isset($_SESSION['enterTime'])){
    $duration=time()-$_SESSION['enterTime'];
    echo "已逗留本站".date("H 时 i 分 s 秒",$duration);
}
?>
```

![](https://s2.ax1x.com/2019/02/09/kU1t1J.png)

![kU1Nc9.md.png](https://s2.ax1x.com/2019/02/09/kU1Nc9.md.png)

<b>session的有效时间</b>
- - -
前面提到一个session代表浏览器打开到关闭为止的时间，所以理论上只要不关闭浏览器，就可以一直保持一份session数据。不过实际上在PHP中的session的有效时间并没有那么长。根据php.ini文件内的设置，默认会自动删除超过24分钟没有访问过session数据，session就会自动删除。

php.ini里面配置session的有效时间：
```
; After this number of seconds, stored data will be seen as 'garbage' and
; cleaned up by the garbage collection process.
; http://php.net/session.gc-maxlifetime
session.gc_maxlifetime = 1440
```
由于书里的例子过于老旧，自己写了一个
完全可以不用session_start()
```php
<html>
<head>
    <title>Sessions测试</title>
</head>
<body>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
    username:<input name="username" type="text"><br>
    password:<input name="password" type="password"><br>
    <input type="submit" name="submit" value="登录">
</form>
</body>
</html>

<?php
header("Content-type: text/html;charset=utf-8");
if(isset($_POST['submit'])) {
    if (isset($_POST['submit']) && !empty($_POST['username']) && !empty($_POST['password'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];
        $sq = ["username" => "admin", "password" => "admin"];
        if ($username == $sq['username'] && $password == $sq['password']) {
            $_SESSION['admin'] = 'admin';
            header("Location: index.php");
        } else {
            echo "用户名或密码错误";
        }
    }
}
?>

```
