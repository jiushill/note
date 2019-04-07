### django显示不出js和css的问题 ###

由于django默认设置不会显示js和css，需要自己修改settings.py
修改位于STATIC位置
![](https://s2.ax1x.com/2019/04/07/AfDHAJ.png)

在STATIC下面添加图中几句
```python
HERE = os.path.join(HERE, '../')
STATICFILES_DIRS = (
    os.path.join(HERE, 'static/'),
)
```

然后创建一个static文件夹里面创放js和css
![](https://s2.ax1x.com/2019/04/07/AfDX1x.png)

然后在修改一个html加载css和js的路径就完事了