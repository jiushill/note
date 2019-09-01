## 目录扫描器 ##

```
              ___.       ___________             __    
__  _  __ ____\_ |__     \_   _____/_ __   ____ |  | __
\ \/ \/ // __ \| __ \     |    __)|  |  \_/ ___\|  |/ /
 \     /\  ___/| \_\ \    |     \ |  |  /\  \___|    < 
  \/\_/  \___  >___  /____\___  / |____/  \___  >__|_ \
             \/    \/_____/   \/              \/     \/
```



支持的操作：

- [x] 黑名单设置
- [x] 数量到达一定程度启动一个进程
- [x] 超时设置
- [x] 单线程或多进程+协程
- [x] 代理设置
- [x] 延时设置



文件夹说明：

```
dict---存放收集来的字典
start---将要使用的字典放入到该文件夹
url.txt---扫描的URL
```

配置说明：

```python
self.black=['黑名单','拦截','WAF','360防火墙','防火墙','502','Not Found','拒绝访问','403','安全狗','云锁','找不到','不存在','404'] #black list
self.process=100 #process
self.time=False #When this condition is true, a single thread is executed
self.sleep=5 #delays
self.timeout=10 #request time out
self.proxies='' #For proxy settings, use the following formats: {http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
```



## Run Demo ##

![](https://s2.ax1x.com/2019/09/02/n9WJyt.png)



save->

![](https://s2.ax1x.com/2019/09/02/n9WNef.png)
