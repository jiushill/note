## RPO漏洞学习 ##
<b>目录</b>
<ul>
<li><a href="#yuanli">漏洞原理</a></li>
<li><a href="#shiyan">实验测试</a></li>
<li><a href="#fangfan">漏洞防范</a></li>
<li><a href="#referer">参考文章</a></li>
</ul>

<h3 id="yuanli">漏洞原理</h3>
RPO漏洞又名相对路径覆盖漏洞，最早由Gareth Heyes在2014年期间其发表的文章中提出。由于此漏洞的新颖，暂时没有什么人会做防范。而且大部分开发习惯了以相对路径来引用静态文件，并不会做改变以至于这方面的漏洞并不“惹人注意”。

原理：由于web容器的特殊，与浏览器的加载致这个漏洞可以形成

web容器的对比：
Apache下访问http://xxx.com/oub%2fxxx.php ----- apache并不会将%2f解码，所以apache将%2fxxx.php当做一个文件来看
![](https://s2.ax1x.com/2019/06/01/V10kYF.png)

Nginx下访问http://xxx.com/oub%2f/xxx.php ------ nginx会自动解码%2f，所以nginx是没有问题的
![](https://s2.ax1x.com/2019/06/01/V101YD.png)

<h3 id="shiyan">实验测试</h3>
环境：
```
Phpstudy选择Nginx+5.5.4版本
```

rpo目录如下：
![](https://s2.ax1x.com/2019/06/01/V102mq.md.png)

test文件夹里有个a.js
```javascript
alert("Read file successfully");
```

当前目录下有个rpo.php
```php
 <html>
<head></head>
<body>
<script src=a.js></script>
</body>
</html>

<?php
	header("Content-type: text/html;charset=utf-8");
	echo "这是个测试页面";
?>
```
读取本地目录下的a.js，如何使得rpo.php读取test文件夹下的a.js呢？
访问：
```
http://127.0.0.1/rpo/test/..%2frpo.php
```

解释URL如下：
```
在Nginx眼里：http://127.0.0.1/rpo/test/..%2frpo.php -> http://127.0.0.1/rpo/test/../rpo.php -> http://127.0.0.1/rpo/rpo.php
在浏览器眼里：http://127.0.0.1/rpo/test/..%2frpo.php -> %2frpo.php当做一个目录会直接删除掉 -> 然后加载test里的a.js 
```
![](https://s2.ax1x.com/2019/06/01/V1Dzyd.png)

一句话总结这个漏洞：
```
比如当前php的文件在/pub里
http://127.0.0.1/pub/index.php
test.js的文件在pub/test里
你想要加载test文件夹下的test.js要做到两部分
1.使得index.php能访问
2.加载test文件夹下的test.js
 ../代表往上一级跳，使用../跳到index.php所在的文件路径下也就是pub，最终payload
http://127.0.0.1/pub/test..%2findex.php
最终nginx得到的url是：http://127.0.0.1/pub/index.php，而浏览器会加载：http://127.0.0.1/pub/test/test.js

在通俗一点就是：
访问的脚本是在：http://127.0.0.1/pub/index.php
要加载的js是在：http://127.0.0.1/pub/test/test.js
首先构造：http://127.0.0.1/pub/test/index.php，数要跳几个路径才能到脚本所在的路径（有几个路径就有几个../），从test跳到pub要跳一个路径，所以构造payload:http://127.0.0.1/pub/test/..%2findex.php
```

在某个站找来的一个例子
![](https://s2.ax1x.com/2019/06/01/V1IU2R.png)
一般在路径和路径之间将/改为%2f如果存在RPO的话，静态文件和图片都加载不出来
总的来说这个漏洞必须配合利用才能有高危，单用是没什么用的
```
常见的操作：RPO+CSRF+XSS、RPO+XSS、RPO+XSS+钓鱼
前提：js里的变量可控
```

![](https://s2.ax1x.com/2019/06/01/V1T3h4.md.png)

<h3 id="fangfan">漏洞防范</h3>
引用css和js的时候不要用相对路径

<h3 id="referer">参考文章</h3>
[RPO漏洞学习](http://39.106.59.19/2018/03/11-rpo%E6%BC%8F%E6%B4%9E%E5%AD%A6%E4%B9%A0.html)
[【技术分析】RPO攻击技术浅析 \| 绿盟科技博客](http://blog.nsfocus.net/rpo-attack/)
[RPO攻击方式的探究 - FreeBuf互联网安全新媒体平台](https://www.freebuf.com/articles/web/166731.html)