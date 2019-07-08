## php cookie的使用 ##
setcookie($key,$value,$time,$path)

$key是用于设置cookie的名称

$value是与设置cookie的值

$time是设置cookie的有效时间

$path是用于设置cookie的访问内容

例子：
```php
<?php
setcookie("name",1,time()+20*60,'/'); /*设置cookie的名称为name,值为1，到期为现在的时间20分钟后，就是获取cookie的时间+20分钟,并且同一网站中的所有目录都可以访问此cookie*/
setcookie("name",2,mktime(1,2,3,10,5,2020),'/data'); /*设置cookie的有效期为2020年10月5号1点2分3秒,访问范围是data目录下的都可以访问此cookie*/
setcookie("name",3,time()-1); /*这样设置时间为负数代表cookie过期,默认不设置则为同一目录下能访问此cookie*/
?>
```

实战
```php
<?php
if(isset($_POST['color'])){ /*先判断是否有表单数据如果有就将color设置为对应的,并设置cookie*/
    echo "post:".$_POST['color'];
    $color=htmlentities($_POST['color']);
    setcookie("color",$_POST['color'],time()+20*60);
}else if(isset($_COOKIE['color'])){ /*如果没有表单数据就判断是否有cookie数据，如果有，就设置cookie的值对应的颜色*/
    echo "Cookie:".$_COOKIE['color'];
    $color=htmlentities($_COOKIE['color']);
}else{ /*如果两者都没有就设置为黑色在给予一个新的cookie*/
    $color="black";
    setcookie("color",$color,time()+20*60);
}
?>
<html>
<head>
    <style>
    div {float:left;margin:10px;text-aligin:center;color:<?php echo $color;?>}
    </style>
    <title>cookie的使用</title>
</head>
<body>
<div>
    <p>nethack之偷钥匙暗无天日</p>
</div>
    <form method="post" accept-charset="<?php echo $_SERVER['PHP_SELF'];?>">
        <select name="color">
            <option value="red">红</option>
            <option value="green">绿</option>
            <option value="blue">蓝</option>
        </select>
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

注意事项：
```
前面说了在用setcookie()之前不能有任何输出，但是如果你非要输出的话也不是
不行。
方法如下：
<?php
ob_start(); /*开启数据缓冲区*/
echo "xxx"; /*输出的数据都会到缓冲区*/
setcookie("name",666,time+20*69);
ob_end_flush() /*释放缓冲区里的数据*/
?>
```

读取设置的cookie
$_COOKIE['$name']

$name为cookie的名称
```
<?php
echo $_COOKIE['a']; /*读取cookie a*/
?>
```
