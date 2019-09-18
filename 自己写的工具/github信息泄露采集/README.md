## Found_Github

![](https://s2.ax1x.com/2019/09/18/n7DqJS.png)

一切配置皆在config.py

```python
#COOKIE
COOKIES='<YOUR_GITHUB_COOKIE>'
#UA头设置
HEADERS={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
#需要搜的关键词
'''
注意事项:搜索关键词如果是中文的话请自行在51行中获取页数中的self.guanjianzi进行url编码，否则获取不到页数。不要问我为什么不写，我懒~
'''
MATH=['freebuf.com']
#协程判断条件
THREADS=100
#延迟设置
SLEEP=0.3
#当页数到达设置的数值后将不在继续,倘若设置为False则爬全部页数
PAGE=3
#搜索结果保存至的文件
FILE='save.txt'
```



使用demo

![](https://s2.ax1x.com/2019/09/18/n7rZLR.md.png)