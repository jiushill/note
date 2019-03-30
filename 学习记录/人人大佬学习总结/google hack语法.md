## google hack语法 ##
---
<b>简介</b>
在日站的时候google搜索能让我们获得意想不到的信息，可以找到目标站点的敏感信息。后台等等

---
<b>google hack语法列表</b>
初级语法表
```C#
模糊搜索-例如：卢本伟
精确搜索-例如："卢本伟"
通配符*-例如：何安圻*
通配符.-例如：大岭山中学.   PS:.的通配符用于匹配字符
布尔逻辑-例如：大岭山中学 and 何安圻
逻辑或|-例如：绿盟 (郑州)
逻辑非-例如：何安圻 -博客园
约束条件-例如：黎颖希 +获奖
数字范围-例如：绿盟+2009年 2015年
```

高级语法表
```C++
访问基本信息-例如：info:baidu.com
标题搜索-例如：intitle:后台登录
正文搜索-例如：intext:身份证大全
url搜索-例如：inurl:google.com
锚链链接搜索-例如：inanchor:google
文档类型限定搜索-例如：intext:身份证大全 filetype:xls
缓存搜索-l例如：cache:secqun.org
相关网址搜索-例如：related:google hacking
相关连接搜索-例如：link:baidu.com
与指定域名相关的搜索：site:baidu.com
```

高级利用
```C
inurl:robots.txt
intitle:登录 intext:username inurl:login.jsp
inurl:8080 inurl:jsp
filetype:sql site:com and "insert into admin 2014"
inurl:jsp/demo.jsp
inurl:update set inurl:where
```