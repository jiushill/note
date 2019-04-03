### rid劫持 ###
<b>简介:</b>
当你搞下一台服务器后，怎么进行权限维持是一个
重要的问题。rid劫持就是个不错的选择

<b>正文</b>
rid劫持教程：
https://www.sohu.com/a/229960576_354899

其实就是改了注册表的两个值，从而实现管理员权限

先查看注册表路径的：
```
HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names
```
从上面的路径来看，可以看到当前计算机里的所有用户
![](https://s2.ax1x.com/2019/03/27/AaJ9KI.png)

对应用户子项里的默认键值对应users子项
![](https://s2.ax1x.com/2019/03/27/AaJka8.md.png)

进管理员的users子项查看F键值对比Guest用户键值有什么不同
![](https://s2.ax1x.com/2019/03/27/AaJmxs.png)

![](https://s2.ax1x.com/2019/03/27/AaJKrq.png)

```
Administrator子项里面的F键值里面有个是:F4 01
Guest子项里面的F键值里面有个是:F5 01
```
那么把Guest里面的F5 01改为F4 01会怎么样？
```
没错，和你想的一样。改为F4 01后他将获得Administrator
权限。并且用户Administrator的配置，比如Administrator桌面上有个连接mysql的工具，工具已经连上数据库了，能看见表名等..当RID劫持后，Guest用户的权限变为Administrator也能看到Administrator桌面上已经连接好数据库的配置
```
这里我就不截图了，具体自己试

工具地址：https://github.com/422926799/python/tree/master/RID%E5%8A%AB%E6%8C%81

测试截图：
![](https://s2.ax1x.com/2019/03/27/AaJoFS.png)

查看注册表
![](https://s2.ax1x.com/2019/03/27/AaJHzj.png)

这个工具是改进版，之前就写过一次了。但是那次是依赖导出注册表然后在修改。后面掌握了如何调用注册表后决定重写。。之前那个文章被百度收录了。上面那张图片给她本人发现得打死我(滑稽)

之前写的：
https://422926799.github.io/2018/10/27/python%E5%AE%9E%E7%8E%B0rid%E5%8A%AB%E6%8C%81/

溜了，溜了。。。不然等一下饭堂又爆满了