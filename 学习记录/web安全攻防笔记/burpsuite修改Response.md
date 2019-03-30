### burpsuite修改Response ###
0x00简介
0x001配置
0x002实例测试
#### 简介 ####
通过设置burp可以修改Response，然后在放包

#### 配置 ####
在burp的proxy->options->Intercept Server Responses
勾选Intercept responses based on the following rules
然后添加规则如下图所示
![ADZVde.png](https://s2.ax1x.com/2019/03/30/ADZVde.png)

![ADZmid.png](https://s2.ax1x.com/2019/03/30/ADZmid.png)

#### 实例测试 ####
根据secqun某文章发现修改返回包的值可以登录后台，本人测试的时候已经被修复
测试地址：[星火系统 - 登录](http://ss.800best.com/user/login)

先抓Request包
![ADZazq.md.png](https://s2.ax1x.com/2019/03/30/ADZazq.md.png)

右键Dont't intercept requests->Response to this is request,然后放包完成这次请求
![ADZreU.md.png](https://s2.ax1x.com/2019/03/30/ADZreU.md.png)

成功拦截到Response包
![ADZ4OK.png](https://s2.ax1x.com/2019/03/30/ADZ4OK.png)

修改数据
![ADZj6P.png](https://s2.ax1x.com/2019/03/30/ADZj6P.png)

结果并没有成功登录后台，不过可以解释清楚为什么有些人burp可以修改Response包
