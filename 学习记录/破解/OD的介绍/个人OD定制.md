# 定制自己的OD
需要准备的工具：
```
winhex
原本OD
ResourceHacker
```

首先原版的OD是这样的
![MaQl9I.png](https://s2.ax1x.com/2019/11/15/MaQl9I.png)

修改其标题`OllyICE`,打开Winhex搜索OllyICE，然后替换为你要的标题名
![MaQRUJ.png](https://s2.ax1x.com/2019/11/15/MaQRUJ.png)

如果要修改的标题名超过原有标题名字集长度会出现如图所示
![MaQIv6.md.png](https://s2.ax1x.com/2019/11/15/MaQIv6.md.png)

点击否即可，否则保存完之后会出现程序错误
![MaQzxP.png](https://s2.ax1x.com/2019/11/15/MaQzxP.png)

然后另存为
![Mal9r8.png](https://s2.ax1x.com/2019/11/15/Mal9r8.png)

在点开jiushi_od.exe可以发现标题已经改成了自己的
![MalEPs.png](https://s2.ax1x.com/2019/11/15/MalEPs.png)

然后在修改`帮助->关于`的官方链接为自己的博客，方法和上面一样搜索`http://www.ollydbg.de`
替换为自己的博客链接，如果超出自集符长度点否即可
![Ma1mYd.gif](https://s2.ax1x.com/2019/11/15/Ma1mYd.gif)


接下来修改控件内容，使用ResourceHacker打开另存为jiushi_od.exe
![Ma3HbT.png](https://s2.ax1x.com/2019/11/15/Ma3HbT.png)

这里有一点要注意的是，原有的控件不能被删除，但是可以隐藏，例如下操作
拉大窗口然后将图片拖动到外面在拉回来，从而实现隐藏功能
![Ma8ldS.gif](https://s2.ax1x.com/2019/11/15/Ma8ldS.gif)

这里我修改点击那个按钮控件然后打开默认浏览器跳转链接的名字，然后点击编译脚本
（汉化工具也用Resource Hacker修改内容汉化的）
![MaGL9J.png](https://s2.ax1x.com/2019/11/15/MaGL9J.png)

然后在把原来的空间给隐藏掉，添加一个新的控件写入自己的内容
![MaJOIS.png](https://s2.ax1x.com/2019/11/15/MaJOIS.png)

插入新的控件
![MaYvTK.png](https://s2.ax1x.com/2019/11/15/Mat5nI.png)

然后点击编译脚本，在保存即可
![MatzBq.png](https://s2.ax1x.com/2019/11/15/MatzBq.png)

![MaNAgJ.png](https://s2.ax1x.com/2019/11/15/MaNAgJ.png)

替换图标，还是使用Resource Hacker打开。找到图标文件的文件夹
![Maa0Xj.png](https://s2.ax1x.com/2019/11/15/Maa0Xj.png)

可以保存这张图片自己PS在替换
![MaahjJ.png](https://s2.ax1x.com/2019/11/15/MaahjJ.png)

![MaaIBR.png](https://s2.ax1x.com/2019/11/15/MaaIBR.png)

注意：图片大小要差不多，不要过大否则会造成崩溃问题

将这图片保存为bmp后缀然后替换原有的图片
![Mad0PK.png](https://s2.ax1x.com/2019/11/15/Mad0PK.png)

![MadIxg.png](https://s2.ax1x.com/2019/11/15/MadIxg.png)

然后保存即可
![MawiZR.png](https://s2.ax1x.com/2019/11/15/MawiZR.png)

(其他的图片的替换方法也一样，以此类推即可)

ResourceHacker打开后所列出来的文件夹：
```
Dialog - 控件
Icon - 软件图标
Bitmap - 图片
```