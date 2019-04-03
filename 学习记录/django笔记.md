### Django学习笔记 ###


#### 简介 ####
>Python下有许多款不同的 Web 框架。Django是重量级选手中最有代表性的一位。许多成功的网站和APP都基于Django。
Django是一个开放源代码的Web应用框架，由Python写成。
Django遵守BSD版权，初次发布于2005年7月, 并于2008年9月发布了第一个正式版本1.0 。
Django采用了MVC的软件设计模式，即模型M，视图V和控制器C。

#### 安装 ####
在cmd执行
```
pip install Django
```
安装完成后在cmd输入Django-admin，如果有回显。就代表安装成功
![](https://s2.ax1x.com/2019/03/31/ADbsDf.png)

#### 创建一个项目 ####
django创建项目的命令如下：
```
django-admin startproject 项目名称
例：django-admin startject 信息收集_web版
```
创建完成后tree一下可以看到以下路径
![](https://s2.ax1x.com/2019/03/31/ADb25Q.png)

根据菜鸟教程的目录说明
![](https://s2.ax1x.com/2019/03/31/ADborV.md.png)

```
mange.py 命令行工具，与Django项目进行交互
__init__.py 一个空文件
settings.py Django项目的配置
urls.py Django项目的URL目录配置
wsgi.py 一个WSGI兼容的web服务器入口
```

测试运行
```
python mange.py runserver 0.0.0.0:8080
```
访问127.0.0.1:8080看到如下图
![](https://s2.ax1x.com/2019/03/31/ADqYMq.md.png)

cmd也会出现Request记录
![](https://s2.ax1x.com/2019/03/31/ADqts0.png)


<b>视图和URL配置</b>

在信息收集_web版创建一个view.py,代码如下
```python
from django.http import HttpResponse

def demo(request):
     return HttpResponse("测试")
```

HttpResponse是返回响应数据

设置urls.py
```python
from django.conf.urls import url #导入配置url的参数
from . import view

urlpatterns = [
    url(r'^$',view.demo) #设置主页
]
``` 
之后整个目录结构如下
![](https://s2.ax1x.com/2019/03/31/ADOVDP.png)

测试运行
![](https://s2.ax1x.com/2019/03/31/ADOnUS.png)


<b>path函数</b>
path函数用来设置路径和URL函数是一样的
path() 函数
Django path() 可以接收四个参数，分别是两个必选参数：route、view 和两个可选参数：kwargs、name。

>语法格式：
path(route, view, kwargs=None, name=None)
route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
view: 用于执行与正则表达式匹配的 URL 请求。
kwargs: 视图使用的字典类型的参数。

修改上面的代码
```python
from django.urls import path
from . import view

urlpatterns = [
    path(r'demo/',view.demo)
]

```

访问http://127.0.0.1/demo就会出现以下
![](https://s2.ax1x.com/2019/03/31/ADXcyn.png)

Django2. 0中可以使用 re_path() 方法来兼容 1.x 版本中的 url() 方法，一些正则表达式的规则也可以通过 re_path() 来实现 
引用菜鸟教程里的代码
```python
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]
```

查看自己的django版本
```
django-admin version
```
![](https://s2.ax1x.com/2019/03/31/ADX4FU.png)

### 模板 ###
>在上一章节中我们使用 django.http.HttpResponse() 来输出 "Hello World！"。该方式将数据与视图混合在一起，不符合 Django 的 MVC 思想。
本章节我们将为大家详细介绍 Django 模板的应用，模板是一个文本，用于分离文档的表现形式和内容。

创建一个templates文件夹，目录结构如下
![](https://s2.ax1x.com/2019/03/31/ADvzMd.png)

创建一个demo.html,内容如下
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
</head>
<body>
<h1>{{demo}}</h1>
</body>
</html>
```

修改settings.py里的TEMPLATES
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates"], #修改位置
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

修改view.py
```python
from django.shortcuts import render

def demo(request):
    content={}
    content['demo']='demo'
    return render(request,'demo.html',content) #指定html，指定标签
```

可以看到，我们这里使用 render 来替代之前使用的 HttpResponse。render 还使用了一个字典 context 作为参数
![](https://s2.ax1x.com/2019/03/31/ADzGAP.png)

标准的标签开头和结尾
```html
{% if %}
代码
{% endif %}
```

一个for标签的例子,反正django的标签和python的有参数函数一样，传入参数然后他那边就是个什么样
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
</head>
<body>
<h1>{{demo}}</h1>
<ul>
    <ui>
        {% for i in lb %}
        <b>{{ i }}{{ gg }}</br></b>
        {% endfor %}
    </ui>
</ul>
</body>
</html>
```

修改view.py
```python
from django.shortcuts import render

def demo(request):
    content={}
    content['demo']='demo'
    content['lb']=[1,2,3,4,5,6,7,8,9,10]
    content['gg']='何安圻'
    return render(request,'demo.html',content)
```
测试结果
![](https://s2.ax1x.com/2019/03/31/ArSpUP.png)

django的一些标签

if/else标签
```html
{% if condition %}
     ... display
{% endif %}
```
或者
```html
{% if condition %}
     ... display
{% elif condition %}
	... display
{% else condition %}
	... display
{% endif %}
```
根据条件判断是否输出。if/else 支持嵌套。

{% if %} 标签接受 and ， or 或者 not 关键字来对多个变量做判断 ，或者对变量取反（ not )，例如：
```html
{% if athlete_list and coach_list %}
     athletes 和 coaches 变量都是可用的。
{% endif %}

```

for标签
{% for %} 允许我们在一个序列上迭代。

与Python的 for 语句的情形类似，循环语法是 for X in Y ，Y是要迭代的序列而X是在每一个特定的循环中使用的变量名称。

每一次循环中，模板系统会渲染在 {% for %} 和 {% endfor %} 之间的所有内容。

例如，给定一个运动员列表 athlete_list 变量，我们可以使用下面的代码来显示这个列表：
```html
ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

ifequal/ifnotequal 标签
{% ifequal %} 标签比较两个值，当他们相等时，显示在 {% ifequal %} 和 {% endifequal %} 之中所有的值。
下面的例子比较两个模板变量 user 和 currentuser :
```html
{% ifequal user currentuser %}
    <h1>Welcome!</h1>
{% endifequal %}
```

注释标签
Django 注释使用 {# #}。
```html
{# 这是一个注释 #}
```

过滤器
模板过滤器可以在变量被显示前修改它，过滤器使用管道字符，如下所示：
```html
{{ name|lower }}
```
{{ name }} 变量被过滤器 lower 处理后，文档大写转换文本为小写。
过滤管道可以被* 套接* ，既是说，一个过滤器管道的输出又可以作为下一个管道的输入：

include 标签
{% include %} 标签允许在模板中包含其它的模板的内容。
下面这个例子都包含了 nav.html 模板：
```html
{% include "nav.html" %}
```

if标签的例子：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
</head>
<body>
<h1>{{ demos }}问答</h1>
<b>阎魔刀是谁用的？</b>
{% if wj %}
<p>{{ wj }}用的</p>
{% elif not wj %}
<p>没有维吉尔</p>
{% endif %}
</body>
</html>
```

测试运行：
![](https://s2.ax1x.com/2019/04/02/A6EW3d.png)

![](https://s2.ax1x.com/2019/04/02/A6Exuq.png)

![](https://s2.ax1x.com/2019/04/02/A6Exuq.png)

![](https://s2.ax1x.com/2019/04/02/A6VUVf.png)


更全面的django标签介绍：http://www.liujiangblog.com/course/django/146
更全面的django过滤器介绍：http://www.liujiangblog.com/course/django/147

过滤器例子：
修改demo.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
</head>
<body>
<h1>{{demo}}</h1>
<ul>
    <ui>
        {% for i in lb %}
        <b>{{ i }}{{ gg }},长度：{{ gg|length }}</br></b>
        {% endfor %}
    </ui>
</ul>
</body>
</html>
```

结果
![](https://s2.ax1x.com/2019/03/31/ArpVzD.png)


过滤器第二个例子：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
</head>
<body>
<h1>{{ demos }}问答</h1>
<b>阎魔刀是谁用的？</b>
{% if wj %}
<p>{{ wj|lower }}用的</p>
{% elif not wj %}
<p>没有维吉尔</p>
{% endif %}
</body>
</html>
```

结果：
![](https://s2.ax1x.com/2019/04/02/A6Z9sI.png)

模板继承
模板可以用继承的方式来实现复用。
接下来我们先创建之前项目的 templates 目录中添加 base.html 文件，代码如下：

base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>模板继承</title>
</head>
<body>
{% extends "index.html" %}
{% block demo %}
<p>继承了index.html</p>
{% endblock %}
</body>
</html>
```
extends标签用于继承指定的模板
block定义一个子模板可以覆盖的块，要引用了一个模板才能使用的标签
![](https://s2.ax1x.com/2019/04/02/A6Nw2n.md.png)

#### Django操作数MYSQL据库 ####
首先得安装mysqlclient模块
```
pip install mysqlclient
```

修改settings.py里的DATABASES
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tests', #数据库名称
        'USER':'root', #数据库用户名
        'PASSWORD':'haq5201314', #数据库密码
        'HOST':'localhost', #数据库地址
        'PORT':'3306', #数据库端口
    }
}
```

<b>创建模型</b>
Django规定，如果要使用模型，必须要创建一个app
```
django-admin startapp TestModel
```
目录结构如下：
PS:去学校了，重新弄了一下
![](https://s2.ax1x.com/2019/04/02/A6096s.png)

修改TestsModel里的models.py
```python
from django.db import models

class Test(models.Model):
    name=models.CharField(max_length=20)
```
>以上的类名代表了数据库表名，且继承了models.Model，
类里面的字段代表数据表中的字段(name)，数据类型则由CharField（相当于varchar）、
DateField（相当于datetime）， max_length 参数限定长度。

接下来在settings.py中找到INSTALLED_APPS这一项
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Testsmode', #你创建的模型名称
]
```
在命令行运行
```
python mange.py migrate #创建表结构
python manage.py makemigrations TestModel  # 更新模型
python manage.py migrate TestModel   # 创建表结构
```

注意：DJango2.x版本开始不支持mysql5.x版本，如果mysql版本是5.x版本请修改

mysql版本是5.x执行python mange.py migrate报错如下
```
django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table ((1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(6) NOT NULL)' at line 1"))
```
解决方法
```
找到python目录下的Lib\site-packages\django\db\backends\mysql\base.py，找到 'DateTimeField': 'datetime(6)', 把datetime(6)改成datetime,问题解决。
```

最后测试结果
![](https://s2.ax1x.com/2019/04/02/A6BQ2Q.png)

![](https://s2.ax1x.com/2019/04/02/A6BdGF.png)

mysql里的tests数据库
![](https://s2.ax1x.com/2019/04/02/A6Bca6.png)

成功创建了表名


<b>添加数据</b>
添加数据需要先创建对象，然后在执行save函数，想党羽SQL中的ISERT
```python
from django.shortcuts import render
from django.http import HttpResponse
from Testsmode.models import Test

def demo(request):
    context={}
    context['demos']='阎魔刀'
    context['wj']='Virgil'
    return render(request,'base.html',context)

def testdb(request):
    test1=Test(name='demo')
    test1.save()
    return HttpResponse("<p>添加数据成功</p>")
```
修改urls.py
```python
from django.urls import path
from . import view

urlpatterns = [
    path(r'hello/',view.demo),
    path(r'testsdb/',view.testdb)
]
```

访问http://127.0.0.1/testdb 
![](https://s2.ax1x.com/2019/04/02/A67WYF.png)


<b>获取数据</b>
```
objects.all() 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
objects.filter(id=1) filter相当于SQL中的WHERE，可设置条件过滤结果
objects.get(id=1) 获取单个对象
objects.order_by('name')[0:2] 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
objects.order_by("id") 数据排序
objects.filter(name="runoob").order_by("id") 上面的方法可以连锁使用
```

输出数据,例子
```python
from django.shortcuts import render
from django.http import HttpResponse
from Testsmode.models import Test

def demo(request):
    context={}
    context['demos']='阎魔刀'
    context['wj']='Virgil'
    return render(request,'base.html',context)

def testdb(request):
    test1=Test(name='demo')
    test1.save()
    return HttpResponse("<p>添加数据成功</p>")

def hc(request):
    test2=Test.objects.all()
    response=Test.objects.order_by('name')[0:2]
    for r in response:
        return HttpResponse(r.name)
```

结果：
![](https://s2.ax1x.com/2019/04/02/A6bQKA.png)

<b>删除数据</b>
删除数据库的对象调用delete()方法即可
现在数据库拥有的数据
![](https://s2.ax1x.com/2019/04/02/A6bwKs.png)

修改view.py和urls.py
```python
from django.shortcuts import render
from django.http import HttpResponse
from Testsmode.models import Test

def demo(request):
    context={}
    context['demos']='阎魔刀'
    context['wj']='Virgil'
    return render(request,'base.html',context)

def testdb(request):
    test1=Test(name='haq')
    test1.save()
    return HttpResponse("<p>添加数据成功</p>")

def hc(request):
    test2=Test.objects.all()
    response=Test.objects.order_by('name')[0:2]
    for r in response:
        return HttpResponse(r.name)

def dels(request):
    rbt=Test.objects.get(id=2)
    rbt.delete()
    return HttpResponse('<p>删除数据成功</p>')
```

urls.py
```python
from django.urls import path
from . import view

urlpatterns = [
    path(r'hello/',view.demo),
    path(r'testsdb/',view.testdb),
    path(r'db/',view.hc),
    path(r'del/',view.dels)
]
```

访问http://127.0.0.1:8080/del/ 
结果：
![](https://s2.ax1x.com/2019/04/02/A6bHPO.md.png)

数据库现有数据
![](https://s2.ax1x.com/2019/04/02/A6bLxH.png).

#### Django表单 ####
<b>GET方法</b>
例子：
```python
from django.shortcuts import render
from django.http import HttpResponse
from Testsmode.models import Test
from django.shortcuts import render_to_response

def demo(request):
    context={}
    context['demos']='阎魔刀'
    context['wj']='Virgil'
    return render(request,'base.html',context)

def testdb(request):
    test1=Test(name='haq')
    test1.save()
    return HttpResponse("<p>添加数据成功</p>")

def hc(request):
    test2=Test.objects.all()
    response=Test.objects.order_by('name')[0:2]
    for r in response:
        return HttpResponse(r.name)

def dels(request):
    rbt=Test.objects.get(id=2)
    rbt.delete()
    return HttpResponse('<p>删除数据成功</p>')

def search(request):
    return render_to_response('search.html') #返回整个html
def search_form(request):
    bd={}
    if 'q' in request.GET:
        message='你搜索的内容为:{}'.format(request.GET['q'])
    else:
        message='你没有搜索任何东西'
    bd['jg']=message
    return render(request,'search.html',bd)
```
request的一些函数记录
```
request.GET GET请求方法
request.POST POST请求方法
```

html表单
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>表单测试</title>
</head>
<body>
<form action="/search_s" method="get">
    搜索：<input type="text" name="q">
    <input type="submit" value="搜索">
</form>
<h3>{{ jg }}</h3>
</body>
</html>
```

修改url.py
```python
from django.urls import path
from . import view

urlpatterns = [
    path(r'hello/',view.demo),
    path(r'testsdb/',view.testdb),
    path(r'db/',view.hc),
    path(r'del/',view.dels),
    path(r'search/',view.search), 访问表单URL
    path(r'search_s/',view.search_form) 处理表单URL
]
```
注意：访问表单的URL和处理表单的URL要分为两个函数来处理
测试结果：
![](https://s2.ax1x.com/2019/04/02/A6v2RK.md.png)

<b>Django POST请求</b>
在模板目录添加一下login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>POST请求测试</title>
</head>
<body>
<form action="/login/" method="post" >
    {% csrf_token %}
    用户名:<input type="text" name="user"><br>
    密码:<input   type="password" name="pwd"><br>
    <input type="submit" value="登陆">
</form>
<p>{{ status }}</p>
<p>{{ username }}</p>
<p>{{ password }}</p>
</body>
</html>
```

修改view.py
注意：POST请求不用区分两个URL来处理，一个URL处理即可
```python
from django.shortcuts import render
from django.http import HttpResponse
from Testsmode.models import Test
from django.shortcuts import render_to_response

def demo(request):
    context={}
    context['demos']='阎魔刀'
    context['wj']='Virgil'
    return render(request,'base.html',context)

def testdb(request):
    test1=Test(name='haq')
    test1.save()
    return HttpResponse("<p>添加数据成功</p>")

def hc(request):
    test2=Test.objects.all()
    response=Test.objects.order_by('name')[0:2]
    for r in response:
        return HttpResponse(r.name)

def dels(request):
    rbt=Test.objects.get(id=2)
    rbt.delete()
    return HttpResponse('<p>删除数据成功</p>')

def search(request):
    return render_to_response('search.html')
def search_form(request):
    bd={}
    if 'q' in request.GET:
        message='你搜索的内容为:{}'.format(request.GET['q'])
    else:
        message='你没有搜索任何东西'
    bd['jg']=message
    return render(request,'search.html',bd)

def cllogin(request):
    cls={}
    if request.POST:
        if request.POST['user']!='' and request.POST['pwd']!='':
            cls['username']=request.POST['user']
            cls['password']=request.POST['pwd']
        else:
            cls['status']='用户名或密码输入为空'

    return render(request,'login-post.html',cls)
```

访问http://127.0.0.1:8080/login
结果：
![](https://s2.ax1x.com/2019/04/03/AcG4de.png)

#### Request对象 ####
上面的每个view函数都调用了Request对象，例如：
```python
forn django.http import HttpResponse
def dg(request):
	return HttpResponse("何安圻")
```

HttpRequest对象包含了当前请求URL的信息
```
path     请求页面的全路径,不包括域名—例如, "/hello/"
method   例子1
GET		 包含所有HTTP GET参数的类字典对象。参见QueryDict 文档。
POST	 包含所有HTTP POST参数的类字典对象。参见QueryDict 文档服务器收到空的POST请求的情况也是有可能发生的。也就是说，表单form通过HTTP POST方法提交请求，但是表单中可以没有数据。因此，不能使用语句if request.POST来判断是否使用HTTP POST方法；应该使用if request.method == "POST" (参见本表的method属性)。注意: POST不包括file-upload信息。参见FILES属性。
REQUEST	 为了方便，该属性是POST和GET属性的集合体，但是有特殊性，先查找POST属性，然后再查找GET属性。借鉴PHP's $_REQUEST。例如，如果GET = {"name": "john"} 和POST = {"age": '34'},则 REQUEST["name"] 的值是"john", REQUEST["age"]的值是"34".强烈建议使用GET and POST,因为这两个属性更加显式化，写出的代码也更易理解。
COOKIES	 包含所有cookies的标准Python字典对象。Keys和values都是字符串。
FILES	 包含所有上传文件的类字典对象。FILES中的每个Key都是<input type="file" name="" />标签中name属性的值. FILES中的每个value 同时也是一个标准Python字典对象，包含下面三个Keys:filename: 上传文件名,用Python字符串表示content-type: 上传文件的Content typecontent: 上传文件的原始内容注意：只有在请求方法是POST，并且请求页面中<form>有enctype="multipart/form-data"属性时FILES才拥有数据。否则，FILES 是一个空字典。
META	 说明1
user	 例子2
session  唯一可读写的属性，代表当前会话的字典对象。只有激活Django中的session支持时该属性才可用。
raw_post_data	原始HTTP POST数据，未解析过。 高级处理时会有用处
__getitem__		和标准字典的处理有一点不同，就是，如果Key对应多个Value，__getitem__()返回最后一个value。
__setitem__		设置参数指定key的value列表(一个Python list)。注意：它只能在一个mutable QueryDict 对象上被调用(就是通过copy()产生的一个QueryDict对象的拷贝).
get()	如果key对应多个value，get()返回最后一个value。
update()	例子3
items()		例子4
valuse()	和标准字典的values()方法有一点不同,该方法使用单值逻辑的__getitem__()
```

例子1：
```python
请求中使用的HTTP方法的字符串表示。全大写表示。例如:

if request.method == 'GET':
    do_something()
elif request.method == 'POST':
    do_something_else()
````

说明1
```
包含所有可用HTTP头部信息的字典。 例如:

CONTENT_LENGTH
CONTENT_TYPE
QUERY_STRING: 未解析的原始查询字符串
REMOTE_ADDR: 客户端IP地址
REMOTE_HOST: 客户端主机名
SERVER_NAME: 服务器主机名
SERVER_PORT: 服务器端口
META 中这些头加上前缀HTTP_最为Key, 例如:

HTTP_ACCEPT_ENCODING
HTTP_ACCEPT_LANGUAGE
HTTP_HOST: 客户发送的HTTP主机头信息
HTTP_REFERER: referring页
HTTP_USER_AGENT: 客户端的user-agent字符串
HTTP_X_BENDER: X-Bender头信息
```

例子2
```python
是一个django.contrib.auth.models.User 对象，代表当前登录的用户。

如果访问用户当前没有登录，user将被初始化为django.contrib.auth.models.AnonymousUser的实例。

你可以通过user的is_authenticated()方法来辨别用户是否登录：

if request.user.is_authenticated():
    # Do something for logged-in users.
else:
    # Do something for anonymous users.
只有激活Django中的AuthenticationMiddleware时该属性才可用
```

例子3
```python
参数可以是QueryDict，也可以是标准字典。和标准字典的update方法不同，该方法添加字典 items，而不是替换它们:

>>> q = QueryDict('a=1')

>>> q = q.copy() # to make it mutable

>>> q.update({'a': '2'})

>>> q.getlist('a')

 ['1', '2']

>>> q['a'] # returns the last

['2']
```

例子4
```python
和标准字典的items()方法有一点不同,该方法使用单值逻辑的__getitem__():

>>> q = QueryDict('a=1&a=2&a=3')

>>> q.items()

[('a', '3')]
```

#### DJango admin后台管理 ####
当用django-admin创建了一个项目后，urls.py自动帮你设置了后台
直接访问admin路径即可见到后台，如果urls.py删除了admin。就手动添加一个
```python
from django.urls import path
from . import view
from django.contrib import admin

urlpatterns = [
    path(r'hello/',view.demo),
    path(r'testsdb/',view.testdb),
    path(r'db/',view.hc),
    path(r'del/',view.dels),
    path(r'search/',view.search),
    path(r'search_s/',view.search_form),
    path(r'login/',view.cllogin),
    path(r'admin/',admin.site.urls)
]
```

访问http://127.0.0.1:8080/admin 
![](https://s2.ax1x.com/2019/04/03/AcYOUg.md.png)

创建管理员账号
```
python manage.py createsuperuser
```
![](https://s2.ax1x.com/2019/04/03/AcYz2n.png)

登陆后台
![](https://s2.ax1x.com/2019/04/03/ActCrV.png)

可以见到有用户和组
![](https://s2.ax1x.com/2019/04/03/ActPbT.png)

如果想要管理我们的创建的数据库，得修改admin.py
```
from django.contrib import admin
from Testsmode.models import Test
admin.site.register(Test)
```

然后重新登陆后台
即可看见我们创建的tests数据库
![](https://s2.ax1x.com/2019/04/03/ActFVU.png)

点进去可以看到字段数据
![](https://s2.ax1x.com/2019/04/03/ActZG9.png)

![](https://s2.ax1x.com/2019/04/03/ActKr6.png)


还可以自定义后台，比如：添加搜索数据库功能，自定义表单，自定义CSS都行
详情请看：http://www.runoob.com/django/django-admin-manage-tool.html