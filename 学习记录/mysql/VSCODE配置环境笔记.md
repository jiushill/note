## vscode配置使用笔记 ##
配置中文环境：
```
command+shift+p
```
搜索：configure display language，选择第二个安装其他语言
![](https://s2.ax1x.com/2019/07/05/Zd6vAe.png)

配置C/C++环境
去搜索插件:C/++，安装
![](https://s2.ax1x.com/2019/07/05/ZdckB8.png)
安装完之后，打开一个文件夹，打开个文件，点击的设置键

![](https://s2.ax1x.com/2019/07/05/ZdcGEF.png)

此时会创建一个launch.json然后配置任务，将externalConsole设置为true
![](https://s2.ax1x.com/2019/07/05/ZdcU3R.png)
这里的externalConsole是开启代码补全的意思，然后在
![](https://s2.ax1x.com/2019/07/05/ZdcBDK.png)

在根据对应的配置配置编译环境即可
```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "gcc编译", //任务名称
            "type": "shell", //使用shell来执行
            "command": "gcc", //使用命令gcc
            "args": [ //参数控制
                "demo.c"
            ],
            "group": {
                "kind": "build", //所属组
                "isDefault": true
            },
            "presentation": {
                "echo": true, //是否输出按任意键结束该终端
                "reveal": "always",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": true,
                "clear": false
            }
        }
    ]
}
```

在vscode上显示md：

安装Markdown Preview Enhanced插件即可


Vscode上配置python环境：
安装python扩展：
安装Python扩展，如果前面安装的anaconda的路径已经加入到path环境变量中，这里跟着提示操作就可以，vscode会自动找到系统python的位置，调试时如果发现提示pylint没有安装，可以通过pip或者conda安装，参看Linting Python in Visual Studio Code
安装Jupyter、Path Intellisense、vscode-python-docstring等扩展，直接参看扩展说明以及Working with Jupyter Notebooks in Visual Studio Code即可，都很直观

然后设置python解析器
![](https://s2.ax1x.com/2019/07/06/Zw9mex.png)

然后配置一下settings.json即可
```json
{
    "python.pythonPath": "/usr/local/opt/python/bin/python3.7", //这里选择了解析器后自动设置的
    "python.jediEnabled": true, //用VS code写python，标准模块自动补全都没有问题，在用自定义的module，import后怎么都没有补全提示。最后采用替换掉Microsoft python analysis engine，采用了Jedi as intellisense engine。设置如下：在settings.json中搜索python.jediEnabled修改为true
    "python.autoComplete.addBrackets": true //自动补全函数的时候有括号
}
```
参考文章:
https://www.jianshu.com/p/504d66800968
https://www.cnblogs.com/shine-lee/p/10234378.html
https://blog.csdn.net/loovelj/article/details/78969872

配置tasks.json参考链接：

https://go.microsoft.com/fwlink/?LinkId=733558

Referer：

https://www.jianshu.com/p/7e5fc8f032a4
https://www.cnblogs.com/lianshuiwuyi/p/8094388.html
https://blog.csdn.net/double_debug/article/details/84636703

几个快捷键：

command+shift+p --- 命令行模式

command+shift+b --- 运行指定任务

command+p --- 查看最近打开的文件

command+o --- 打开指定文件

command+n --- 打开一个新的文件

command+s --- 保存指定的文件