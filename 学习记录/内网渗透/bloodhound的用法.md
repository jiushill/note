## bloodhound的用法 ##
今天在雷神众测公众号见到一个篇叫：bloodhound技术讲解的文章，自己捞了康康，捎带总结
文章链接：[bloodhound技术讲解](https://mp.weixin.qq.com/s?__biz=MzI0NzEwOTM0MA==&mid=2652471925&idx=1&sn=09d691c85d9bf83122557546fbd31374&chksm=f25821c6c52fa8d00e44f24533fc5ab30ac343b71d9862a6be74d0df4b8fc904a12831901c9f&mpshare=1&scene=23&srcid=&sharer_sharetime=1571130787590&sharer_shareid=64458b89777349122de4fc747d336e14#rd)


## 参考链接 ##
https://www.cnblogs.com/backlion/p/10643132.html
https://github.com/C0axx/AggressorScripts
[BloodHoundAD · GitHub](https://github.com/BloodHoundAD)

## bloodhound介绍 ##
>BloodHound是一个单页Javascript Web应用程序，基于Linkurious构建，该应用程序由Electron编译，具有由C＃数据收集器提供的Neo4j数据库。
BloodHound使用图论来揭示Active Directory环境中隐藏的，通常是意外的关系。攻击者可以使用BloodHound轻松识别高度复杂的攻击路径，否则这些攻击路径将无法快速识别。防御者可以使用BloodHound来识别和消除那些相同的攻击路径。蓝队和红队均可使用BloodHound轻松获得对Active Directory环境中特权关系的更深入了解


## 环境 ##
```
VM:kali
```
PS:懒得的搭域这里就借别人的图来用用

## 安装与初始化 ##
```
安装bloodhound
apt-get install bloodhound

启动Neo4和bloodhound
neo4j console
bloodhound
```
之后进入http://127.0.0.1:7474,可以看到如下界面
![1049983-20190402155722502-1719968636.png](https://img2018.cnblogs.com/blog/1049983/201904/1049983-20190402155722502-1719968636.png)

输入默认username和password更改密码，默认是
```
neo4j
neo4j
```
![1049983-20190402155722976-431988692.png](https://img2018.cnblogs.com/blog/1049983/201904/1049983-20190402155722976-431988692.png)

之后会看到
![KPlHl4.png](https://s2.ax1x.com/2019/10/15/KPlHl4.png)

新开一个终端执行：`bloodHound`
![KP1iXd.png](https://s2.ax1x.com/2019/10/15/KP1iXd.png)

然后会弹出一个框框，根据上图给出的消息和你的账号进行登录
![1049983-20190402155723356-1627066939.png](https://img2018.cnblogs.com/blog/1049983/201904/1049983-20190402155723356-1627066939.png)

登录进去之后是一片空白，需要自己导入zip
![KP1U9U.png](https://s2.ax1x.com/2019/10/15/KP1U9U.png)

>可以通过sharpbound.exe和ps1单独使用（execute-assembly、powershell-import）。
导入插件，快速导出并下载bloodhound的json文件。

![KP3Zr9.md.png](https://s2.ax1x.com/2019/10/15/KP3Zr9.md.png)

>导入zip后就可以通过各种关系寻找路线攻击域管或者某台特定机器
寻找攻击域管的最短路径

![KP312D.png](https://s2.ax1x.com/2019/10/15/KP312D.png)

![KP3NVI.png](https://s2.ax1x.com/2019/10/15/KP3NVI.png)

使用技巧

如果你不想过多了解bloodhound对运行机制，不需要自己编写语法查询，只用bloodhound提供的默认ui显示。那么只需要认识几个图形所代表的意义及一些使用技巧

* 绿色用户头像：用户
* 三个黄色头像：用户组
* 红色小电脑：计算机
* 绿色小地球：域

自带的查询功能：
```
Find all Domain Admins 查找所有域管理员 

Find Shortest Paths to Domain Admins  查找域管理员的最短路径 

Find Principals with DCSync Rights查找具有DCSync权限的主体 

Users with Foreign Domain Group Membership 具有外域组成员身份的用户 

Groups with Foreign Domain Group Membership  具有外域组成员身份的组 

Map Domain Trusts域信任映射图 

Shortest Paths to Unconstrained Delegation Systems  不受约束的委派系统的最短路径 

Shortest Paths from Kerberoastable Users 来自Kerberoastable用户的最短路径 

Shortest Paths to Domain Admins from Kerberoastable Users  可通过Kerberoastable用户访问域管理员的最短路径

 Shortest Path from Owned Principals  已拥有权限最短路径 

Shortest Paths to Domain Admins from Owned Principals 已拥有权限到域管理员的最短路径 

Shortest Paths to High Value Targets高价值目标的最短路径
```

![KP8EJf.png](https://s2.ax1x.com/2019/10/15/KP8EJf.png)

![KP8Mes.png](https://s2.ax1x.com/2019/10/15/KP8Mes.png)

>当选择高价值目标的最短路径UI进行分析（选择其他UI使用方式一样），可以重点关注用户（绿色头像）、计算机（红色小电脑）。当用鼠标指向这两个单位时，会以高亮显示体现出具体的攻击路径。简而言之：
1.对高亮攻击路径中的所有用户分析
2.对高亮攻击路径中的所有计算机进行分析

![KP8GWT.png](https://s2.ax1x.com/2019/10/15/KP8GWT.png)

![KP8UOJ.png](https://s2.ax1x.com/2019/10/15/KP8UOJ.png)