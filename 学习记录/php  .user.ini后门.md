# .user.ini后门
参考链接：
[.user.ini文件构成的PHP后门 – phith0n \| 漏洞人生](http://www.vuln.cn/6001)


今天早上看到一个链接，.user.ini后门。下班回家马上就试了试，这特么真的牛逼，比啥.htaccess牛逼多了。

根据上面链接给出的介绍：
```
在 .user.ini 风格的 INI 文件中只有具有 PHP_INI_PERDIR 和 PHP_INI_USER 模式的 INI 设置可被识别。
这里就很清楚了，.user.ini实际上就是一个可以由用户“自定义”的php.ini，我们能够自定义的设置是模式为“PHP_INI_PERDIR 、 PHP_INI_USER”的设置。（上面表格中没有提到的PHP_INI_PERDIR也可以在.user.ini中设置）
```

具体更详细的话可以看上面的链接，这操作可以在黑名单上传的时候直接秒shell= =

## 实验
创建一个.user.ini，写入
```
auto_prepend_file=01.gif
```
>01.gif是要包含的文件。
所以，我们可以借助.user.ini轻松让所有php文件都“自动”包含某个文件，而这个文件可以是一个正常php文件，也可以是一个包含一句话的webshell

![KoG3wD.png](https://s2.ax1x.com/2019/10/31/KoG3wD.png)

![Ko8sR1.png](https://s2.ax1x.com/2019/10/31/Ko8sR1.png)

然后随便访问web目录下的任意一个php即是后门
![KoGW60.md.png](https://s2.ax1x.com/2019/10/31/KoGW60.md.png)

![KoJ3j0.png](https://s2.ax1x.com/2019/10/31/KoJ3j0.png)

可用的容器环境：IIS/Apache/nginx

补充了upload-master上的一点
![KoJR4H.png](https://s2.ax1x.com/2019/10/31/KoJR4H.png)