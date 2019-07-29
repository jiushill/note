## 起因 ##
今天出发去度假，来到酒店后。连上个wifi，看见网关地址就觉得想搞= =
![](https://s2.ax1x.com/2019/07/29/e80VNn.jpg)

## 经过 ##
打开登录页面查看了一下源代码，发现是js认证
![](https://s2.ax1x.com/2019/07/29/e80GNR.png)

表单的action居然是null...
![](https://s2.ax1x.com/2019/07/29/e80ajO.png)

看了一下加载的js，有个login.js
![](https://s2.ax1x.com/2019/07/29/e80BHH.png)

查看login.js
![](https://s2.ax1x.com/2019/07/29/e80y4I.png)

仔细读了一下js后发现过程大概是这样的
```
1.先将username和password进行MD5加密
2.判断是否异步，然后请求判断得到返回的状态码
状态码有：status，superuser，session。
3.如果请求过程中不出问题则只需sucess的判断，到最后将状态码返回给login.html，login.html通过login.js返回的状态码决定是否登录成功
```
![](https://s2.ax1x.com/2019/07/29/e8BwR0.png)

将这三个状态码全部改为0，然后输入任意用户名和任意密码即可登录成功（因为login.html判断如果返回的状态码为0的话视为登录成功）
![](https://s2.ax1x.com/2019/07/29/e8BWJ1.png)

修改后
![](https://s2.ax1x.com/2019/07/29/e8Bhz6.png)

登录成功
![](https://s2.ax1x.com/2019/07/29/e8B7ee.png)



总结：
```
像这种js验证，找到关键的判断位置，和关键的返回值。将其修改就能达到意想不到的结果
```
