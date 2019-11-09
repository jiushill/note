# Google关键信息收集
- [x] Google关键信息主程序启动之前，先获取指定的代理
- [x] 随机UA头
- [x] 随机代理
- [x] 读取配置文件的关键搜索语法
- [x] 批量检测
- [x] 随机延时
- [x] 随机google域名

Tips:这并不是Url采集器
# 所需模块
```text
requests
gevent
asyncio
multiprocessing
bs4
```

# 关键点说明
files文件夹
```text
files/domain.txt --- Google子域名的字典
files/ip.txt --- 代理存放
files/UA.txt --- UA头大全
files/file.txt --- 要检测的域名
```

jg文件夹
```text
jg/save.txt --- 保存搜到的url
```

google_search.py
```python
 self.search=['site:{domain} inurl:upload','site:{domain} inurl:admin'] #搜索语法定义，24行，这里的domain后面是对应file.txt里的域
 data['sleep']=random.choice([x for x in range(1,30)]) #延时随机设置范围1-30秒
 url='https://'+random.choice(self.gdomain)+self.url.format(search=str(y).format(domain=z['domain'])) #构造最后请求的url
```

流程
```text
1.读取所需的文件
2.构造随机UA头、随机代理、随机google域
3.创建URL请求
```

测试
![](https://s2.ax1x.com/2019/11/09/MmaJZ6.png)

![](https://s2.ax1x.com/2019/11/09/MmayeP.png)