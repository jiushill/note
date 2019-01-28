## 正文 ##
date()为php的时间函数，返回一个保护日期时间的字符串，所以可以自行设置
具体时间格式自己百度
例子为：,

主要使用date()之前要设置好地区先，默认是美国

date_default_timezone_set('地区)

date(format_string,timestamp)
````
format_string:带有格式参数的字符串
timestamp:要显示日期时间的时间戳
y为年，m为月，d为日，h为时，i为分，s为秒，a为am
````

```
<?php
date_default_timezone_set('Asia/Shanghai'); /*设置时间地区*/
echo date('Y-m-d h:i:s a'); /*输出时间*/
echo date("y-m-D-d-a");
?>
```

time()
````
获取当前时间戳，time()会返回1970/01/01 00:00:00:00到现在的相差秒数
````
date+time函数获取几个小时后或指定的时间
```
<?php
header("Content-type: text/html;charset=utf-8");
date_default_timezone_set('Asia/Shanghai'); /*设置时间地区*/
echo date('Y-m-d h:i:s a'); /*输出时间*/
echo "<br>";
echo "Demo时间：".date('Y-m-d',time()+2*60*60); /*使用time计算出2个小时后的日期时间*/
?>
```

mktime(hour,minute,second,minth,day,year)
```
mktime()可以获取指定的时间戳，配合date()可以获取指定的时间
hour:时
minute:分
second:秒
minth:月
day:日
year:年
```
````
<?php
header("Content-type: text/html;charset=utf-8");
date_default_timezone_set('Asia/Shanghai'); /*设置时间地区*/
echo date('Y-m-d h:i:s a'); /*输出时间*/
echo "<br>";
echo "Demo时间：".date('Y-m-d',time()+2*60*60); /*使用time计算出2个小时后的日期时间*/
echo "<br>";
echo date('Y-m-d h:i:s a',mktime(0,1,0,1,1,2020)); /*对应：2020-01-01 12:01:00 am，y为年，m为月，d为日，h为时，i为分，s为秒，所以对应mktime，Y对2020....*/
?>
````