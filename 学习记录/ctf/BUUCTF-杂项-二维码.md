### 杂项-二维码 ###

BUUCTF的杂项第二题：二维码
![VT676K.png](https://s2.ax1x.com/2019/06/16/VT676K.png)


下载完图片之后，发现是个二维码
![VT6qmD.png](https://s2.ax1x.com/2019/06/16/VT6qmD.png)

扫描二维码之后，给出了这个东东
![VTcCX8.md.png](https://s2.ax1x.com/2019/06/16/VTcCX8.md.png)


根据之前看过的题，这图片里面肯定有第二个文件
binwalk走一波：
![VTcVts.png](https://s2.ax1x.com/2019/06/16/VTcVts.png)

分离文件，得到压缩包
```
foremost ewm.png
```
![VTcwnO.md.png](https://s2.ax1x.com/2019/06/16/VTcwnO.md.png)


unzip解压压缩包的时候发现要密码
![VTc0BD.png](https://s2.ax1x.com/2019/06/16/VTc0BD.png)

frackzip跑压缩包密码，最后得到密码是，然后得到flag
```
frackzip -b -c '1' -l 1-7 xx.zip
7639
```
![VTcg3t.png](https://s2.ax1x.com/2019/06/16/VTcg3t.png)


参考文章：
[ctf中检测和分离隐藏的文件 - Sch01aR# - 博客园](https://www.cnblogs.com/sch01ar/p/7852329.html)
[zip加密破解 - 简书](https://www.jianshu.com/p/234abeed1421)
[CTF之隐写 - 简书](https://www.jianshu.com/p/02fdd5edd9fc)