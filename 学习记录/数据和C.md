## 数据和C ##
本章研究数据类型里的两大系列：整数类型和浮点数类型
例子：
```c++
#include <stdio.h>
int main(){
    float weight; //定义浮点类型
    float value;
    printf("Are you worth your weight in rhodium?\n");
    printf("Let's check it out.\n");
    printf("Please enter your weight in pounds:");
    scanf("%f",&weight); /*用户输入*/
    value=770*weight*14.5833; //计算公式
    printf("Your weight is rhodium is worth $%.2f.\n",value);
    printf("You are easily worth that! if rhodium pricess drop.\n");
    printf("eat more to maintain your value. \n");
    return 0;
}
```
注意：到了让用户输入的时候，输入完值按一下Enter或return键。不要等在哪里
程序输出如下：
```txt
Are you worth your weight in rhodium?
Let's check it out.
Please enter your weight in pounds:13.5
Your weight is rhodium is worth $151593.41.
You are easily worth that! if rhodium pricess drop.
eat more to maintain your value. 
```
float为浮点类型 （可以使用用有小数点的数了）

int为整数类型

printf()里的%f占位符用于处理浮点数值

使用scanf()函数为程序供键盘输入。%f指示从函数中取一个浮点数类型。对%f占位符使用.2修饰词可以精确的控制输出格式
使浮点数显示到小数点后两位

## 变量与常量数据 ##
变量与常量的区别是：

变量的值可以变而常量的值不可以变

说的在简单点的就是

变量可以被重新赋值，如：
```
int a=10;
int a=100;
```

常量第一次赋值后就不能在变，如：
```
const int a=10;
```
后面说到常量的时候会详细说明

## 数据类型关键字 ##
除了变量和常量的区别，各种数据类型也有不同，一些数据类型是数字。而另一些是字母，更广泛的说是字符
计算机需要一种方法来区分和使用这些不同的类型：11是整数类型（int）,11.0是浮点数类型（float）......

C语言的基本变量类型：
```
int
float
long
short
unsigned
signed
void
__BOOl
__Complex
__Imaginary
char
double
```

int关键字提供C使用的基本的整数类型

(long,short,和unsigned)以及ANSI附加的signed用于提供基本类型的变种

char关键字用于表示字母以及其他字符（如#、$、%、和*）。char也可以表示小的整数

float、double和组合long double表示带有小数点的整数

__Bool类型表示布尔值（true和false）。__Complex和__Imaginary分别表示复数和虚数

这些类型可以按其在计算机中的存储方式被划分为两个系列，即整数类型和浮点数类型

### 位、字节和字 ###
```
术语位、字节和字用于描述计算机数据单位或计算机存储单位。这里主要指存储单位
最小的存储单位称为位（bit）,它可以容纳两个值（0或1）之一（或者可以称该位被置为”关“或”开“）。
不能在一个位中存储更多的信息，但是计算机中包含数量极其众多的位。位是计算机存储的基本单位
    字节（byte）是常用的计算机存储单位。几乎对于所有的机器，1个字节均为8位。这是字节的标准定义，至少在衡量存储单位时是这样的。由于每个位或者是0或者是1，所以一个8位的字节包含256（2的8次方）种可能的0、1组合。这些组合可用于表示0到255的整数或者一组字符。这种表示可以通过二进制编码来实现。
    对于一种给定的计算机设计，字（word）是自然的存储单位。对于8位微机，比如原始的Apple机，一个字正好有8位。使用80826处理器的早期IBM兼容机是16位，这意味着一个字的大小为16位。基于Pentium的PC机和Macintosh PowerPC机中的字是32位。更强大的计算机可以有64位，甚至更长的数字。
```

## 整数类型与浮点数类型 ##
整数就是没有小数部分的数。在C中，小数点永远不会出现在整数的书写中。例如2、-23和2456都是整数。数3.14、0.22和2.000都不是整数。整数以二进制数字存储。例如整数7的二进制表示为111，在8位的字节中存储它需要将前5位置0，将后三位置1
```
—————————-———————
|0|0|0|0|0|1|1|1|
—————————————————
```

浮点数差不多可以和数学中的实数概念想对应。实数包含了整数之间的那些数。2.75、3.16E7、7.00和2E~8都是浮点数。
注意：加了小数点就是浮点型值，所以7是整数类型，7.00是浮点类型。后面讲述E记数法，这里简单的说：3.16E7表示3.16
乘10的7次方（即1后面带有7个0），7称为10的指数

这里最总要的一点是浮点数与整数的存储方案不同。浮点数表示将一个数分为小数部分和指数部分，并分别存储
```
_______________
|+|.31415926|1| //+是符号，.31415926是小数部分，1是指数部分
---------------
```

这两种类型的区别：
+ 整数没有小数部分：浮点数可以有小数部分
+ 浮点数可以表示比整数范围大得多的数
+ 因为对于任何区间内（比如1.0到2.0之间）都存在无穷多个实数，所以计算浮点数不能表示区域内所有的值。
浮点数往往只是实际值相似
+ 浮点数运算通常比整数运算慢。不过，已经开发出专门处理浮点运算的微处理器，它可以缩小速度上的差别


## C和数据类型 ##
int类型
```c++
#include <stdio.h>
int main(){
    int ten=10;
    int two=2;
    printf("Doing it right");
    printf("%d minus %d \n",ten,ten-two);
    printf("Doing it wrong");
    printf("%d minus %d is %d \n",ten,two,ten-two);
    return 0;
}
```

输出结果是：
```
Doing it right10 minus 8 
Doing it wrong10 minus 2 is 8 
```

PS:printf里面的占位符要与显示的数量对应

显示八进制数和十六进制数
C即允许使用3种数制书写数字，也允许这3种树显示数字。要用八进制而不是十进制显示整数，用%0代替%d。要显示十六进制整数，请使用%x。如果显示C语言前缀，可以使用说明符%#o,%#x和%#X分别生成0、0x和0X前缀。
```c++
#include <stdio.h>
int main(){
    int x=100;
    printf("十进制和八进制与十六进制: dec=%d dec=%o dec=%x \n",x,x,x);
    printf("C语言前缀: dec=%d dec=%#o dec=%#x",x,x,x);
    getchar(); //执行程序之后，使窗口不会立即关闭
    return 0;
}
```
显示结果：
```
十进制和八进制与十六进制: dec=100 dec=144 dec=64 
C语言前缀: dec=100 dec=0144 dec=0x64
```

## 其他整数类型 ##
+ short int类型（简写为short类型）可能占用比int类型更少的存储空间，用于小数值的场合，可以节省空间
+ long int类型（简写为long类型）可能占用比int类型要更多的存储空间，用于大数值的场合
+ long long int类型（简写为long lont类型），可能占用比long类型要更多的存储空间，用于更大数值的场合
+ unsinged int类型 （简写为unsinged类型）用于只适应非负值的场合。这种类型同有符号类型的表示范围不同，后面会详细说到
+ 关键字sigent可以和任何有符号类型一起使用，它使用数据的类型更加明确，例如：short、short int、signed short以及signed short int代表了同一类型

其他类型的声明方式和int类型相同

