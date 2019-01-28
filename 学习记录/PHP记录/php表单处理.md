## 正文 ##
html表单处理是为了防止接收数据，攻击者插入xss语句或者插入SQL注入语句，引发
攻击。

<b>显示在网页上的处理过程</b>

当表单接收到表单字段传来的数据的时候可以使用htmlspecialchars()来对特殊的字符串
进行实体化，从而杜绝了xss注入的发生

用到htmlspecialchars()用于要输出在页面上的字符才进行处理

表单处理过程：接收到数据->get_magic_quotes_qpc是否开启->如果开启
删除掉开启后对待特殊字符串添加的反斜杠，然后htmlsepcilchars()实体编码

数据库处理后面在说..

例子：
```
<html>
<head>
<title>表单文字处理</title>
</head>
<body>
<form action="<?php echo $_SERVER['PHP_SELF'];?>" method="post">
    请输入您的名称:<input type="text" name="name" required><br>
    <input type="submit" value="提交">
</form>
</body>
</html>

<?php
function check($value){
    if(get_magic_quotes_gpc()){
        $dele=stripslashes($value);
        $dele=htmlspecialchars($dele);
        return $dele;
    }else{
        $rd=htmlspecialchars($value);
        return $rd;
    }
}

if(!empty($_POST['name'])){
    $name=$_POST['name'];
    $kr=check($name);
    echo "<b>你好$kr</b>";
}
?>
```