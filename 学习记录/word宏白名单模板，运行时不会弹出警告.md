## word宏白名单模板，运行时不会弹出警告 ##
路径：C:\Users\Administrator\AppData\Roaming\Microsoft\Templates
里面的Normal模板，在里面创建宏代码保存为启用宏的word文档不会出现警告，让你按确定才能运行宏
![](https://s2.ax1x.com/2019/05/28/VeNVyj.md.png)

宏代码：
```vba
Sub AutoOpen()
    MsgBox "demo"
End Sub

```

![](https://s2.ax1x.com/2019/05/28/VeNlfU.png)

因为该路径的模板默认在信任路径：
```shell
C:\Users\Administrator\AppData\Roaming\Microsoft\Templates
```