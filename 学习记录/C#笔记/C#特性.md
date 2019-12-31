# C#特性
>特性（Attribute）是用于在运行时传递程序中各种元素（比如类、方法、结构、枚举、组件等）的行为信息的声明性标签。您可以通过使用特性向程序添加声明性信息。一个声明性标签是通过放置在它所应用的元素前面的方括号（[ ]）来描述的。
特性（Attribute）用于添加元数据，如编译器指令和注释、描述、方法、类等其他信息。.Net 框架提供了两种类型的特性：预定义特性和自定义特性。


## Conditional
这个预定义特性标记了一个条件方法，其执行依赖于指定的预处理标识符。

它会引起方法调用的条件编译，取决于指定的值，比如 Debug 或 Trace。例如，当调试代码时显示变量的值。

规定该特性的语法如下：
```
[Conditional(
   conditionalSymbol
)]
```
这种特性用和不用没啥区别....就是标记一下...为了好康一点？我也不知道，除了标记在指定类或函数上方没见起到啥作用。处理过程还是靠函数
(网上大部分都说用来标识当做异常处理函数)
```C#
#define DEBUG
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Diagnostics;

public class Mycalss {
    [Conditional("DEBUG")]
    public static void Message(string msg) {
        Console.WriteLine(msg);
    }
}

class Test {
    static void function1()
    {
        Mycalss.Message("This is function 1");
        function2();
    }

    static void function2() {
        Mycalss.Message("This is function 2");
    }

    public static void Main() {
        Mycalss.Message("In Main function");
        function1();
        Console.ReadKey();
    }
}
```

输出结果：
![QdGMBF.png](https://s2.ax1x.com/2019/12/08/QdGMBF.png)

## Obsolete
这个预定义特性标记了不应被使用的程序实体。它可以让您通知编译器丢弃某个特定的目标元素。例如，当一个新方法被用在一个类中，但是您仍然想要保持类中的旧方法，您可以通过显示一个应该使用新方法，而不是旧方法的消息，来把它标记为 obsolete（过时的）。

规定该特性的语法如下：
```
[Obsolete(
   message
)]
[Obsolete(
   message,
   iserror
)]
```
例子：
```C#
#define DEBUG
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Diagnostics;

namespace Tests {
    class Rpcs {
        [Obsolete("This is remove function",true)]
        public void Netwtrd() {
            Console.WriteLine("You are Test1");
        }

        public void Nvt() {
            Console.WriteLine("You are Test2");
        }

        static void Main(string[] args) {
            Rpcs r = new Rpcs();
            r.Netwtrd();
            r.Nvt();
        }
    }
}
```
在函数上用了特性Obsolete，在调用这个函数可以发现Vs已经标红
![QdYPij.png](https://s2.ax1x.com/2019/12/08/QdYPij.png)

被标记位True的函数已经作废，调用哪个函数运行会得到一个错误
![QdYkzq.png](https://s2.ax1x.com/2019/12/08/QdYkzq.png)

## AttributeUsage
预定义特性 AttributeUsage 描述了如何使用一个自定义特性类。它规定了特性可应用到的项目的类型。

规定该特性的语法如下：
```C#
[AttributeUsage(
   validon,
   AllowMultiple=allowmultiple,
   Inherited=inherited
)]
```
AttributeUsage可选参数很多，参考MSDN文档
[编写自定义特性 \| Microsoft Docs](https://docs.microsoft.com/zh-cn/dotnet/standard/attributes/writing-custom-attributes)

一般定义是这样使用的
```
[AttributeUsage(AttributeTargets.All, Inherited = false, AllowMultiple = true)]
```
AttributeTargets.All代表定义所有，AllowMultiple = true表示允许定义多个属性指明元素能否包含属性的多个实例。 如果设置为 true，则允许多个实例；如果设置为 false（默认值），则只允许一个实例。

例子
```C#
#define DEBUG
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Diagnostics;

[AttributeUsage(AttributeTargets.All, Inherited = false, AllowMultiple = true)]
public class Someingattr:Attribute {
    private string name;
    private string data;
    public string Name {
        get { return name; } //通过Name来返回name的值
        set { name = value; } //name等于传递过来的值
    }

    public string Data {
        get { return data; }
        set { data = value; }
    }

    public Someingattr(string name,string data) { //定义处理函数
        this.name = name;
        this.data = data;
    }

}


namespace One_test {
    [Someingattr("jiushi", "2019/12/9")] //调用自定义特性
    class Trcp {
        static void Main(string[] args) {
            Console.WriteLine("This is Main function");
            Type t = typeof(Trcp);
            var something = t.GetCustomAttributes(typeof(Someingattr), true); //获取自定义特性的值
            foreach (Someingattr each in something) {  //遍历所得的值
                Console.WriteLine("Name:{0} Value:{1}", each.Name, each.Data); //输出定义的值，必须是定义值的那个函数，比如Data。因为通过Data给data赋值的
            }
            Console.ReadKey();
        }
    }
}
```

get和set的使用参考：https://blog.csdn.net/Jeffxu_lib/article/details/89203503

使用反射（Reflection）可以查看特性（attribute）信息
参考链接：[C# 反射（Reflection） \| 菜鸟教程](https://www.runoob.com/csharp/csharp-reflection.html)
```C#
Type t = typeof(Trcp);
            var something = t.GetCustomAttributes(typeof(Someingattr), true); //获取自定义特性的值
            foreach (Someingattr each in something) {  //遍历所得的值
                Console.WriteLine("Name:{0} Value:{1}", each.Name, each.Data); //输出定义的值，必须是定义值的那个函数，比如Data。因为通过Data给data赋值的
```

注意：自定义特性（AttributeUsage）只能在class上使用，对函数使用无效
![Qd03NT.png](https://s2.ax1x.com/2019/12/09/Qd03NT.png)

下面是一个对函数使用的，可以发现并没有起到特性的效果

![Qd0dD1.png](https://s2.ax1x.com/2019/12/09/Qd0dD1.png)

自定义特性给我的感觉和py的装饰器一样