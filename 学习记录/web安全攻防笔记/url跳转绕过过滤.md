## URL跳转过滤 ##
---
<b>0x0URL跳转出现的原因</b>
常见方式：
META标签的refresh
javascript
header

meta
```html
<meta http-equiv="refresh" content="0;url=url">
```

javascript
```
location.href="url"
```

header
```
<?php
header("Location:url");
?>
```

当上述例子中的url为限制时就产生了URL重定向/跳转漏洞

---
<b>绕过方法</b>
*.xip.ior绕过 xip.io是DNS解析

例如：
```
http://demo.com/dd/search.php?url=https://www.baidu.com #被拦截
http://demo.com/dd/search.php?url=https://www.baidu.com.8.8.8.8.xip.io #不拦截
```

使用@绕过
PS：要是@后面的域名不在白名单里也无法跳转
```
http://demo.com/dd/search.php?url=https://www.baidu.com@http://www.baidu.com
```

使用/@或\@
```
http://demo.com/dd/search.php?url=https://www.baidu.com/@http://www.baidu.com
http://demo.com/dd/search.php?url=https://www.baidu.com\@http://www.baidu.com
```

采用http://\的样式尝试绕过
```
http://demo.com/dd/search.php?url=https://www.baidu.com\http://www.baidu.com
```

总结：多试，多加一些特殊字符看看能不能修改，一般某个参数后面跟着url的话可能存在url跳转漏洞可以试试，有些是加密的要自己解码看