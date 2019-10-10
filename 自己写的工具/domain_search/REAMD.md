## domain_search ##
环境：python3  
用的框架：scrapy  

**说明**
采用scrapy来探测域名是否存活，scrapy在请求之前会先用DNS探测域名是否存活，并判断是否能连接成功  

![](https://s2.ax1x.com/2019/10/10/u78mlQ.png)

## 配置 ##
scrapy默认只返回状态码为200的url，如果要返回其他状态码的URL的话，在settings.py设置
```python
HTTPERROR_ALLOWED_CODES = [200,403]
```

* 从dict文件夹里面获取字典，需要更多的字典请扔进dict文件夹
* 域名保存在save文件夹下

## 使用方式 ##
在路径:domain_search/domain_search/spiders执行
```
scrapy crawl domain -s LOG_FILE=all.log
```

或者运行start.bat

![](https://s2.ax1x.com/2019/10/10/u7JlGT.png)