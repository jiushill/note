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
_BOOl
_Complex
_Imaginary
char
double
```

int关键字提供C使用的基本的整数类型

(long,short,和unsigned)以及ANSI附加的signed用于提供基本类型的变种

char关键字用于表示字母以及其他字符（如#、$、%、和*）。char也可以表示小的整数

float、double和组合long double表示带有小数点的整数

_Bool类型表示布尔值（true和false）。_Complex和_Imaginary分别表示复数和虚数

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
________
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

C语言标准规定了每种类型的基本大小：
```
int和short的取值范围是: -32767到32767
long类型的取值范围是：-2147483647到2147483647
unsigned long类型最小的取值范围是：0到4294967295
long long类型是为了支持对64位的需求：取值范围是-9223372036854775807到9223372036854775807
unsigned long long的取值范围是：0到18446744073709551615
```
PS：在诸多的整数类型中，首先考虑unsigned的类型，把这种类型用于计数是十分自然的事，因为你此时不需要负数
，而且无符号类型可以比有符号类型更大的正数。int类型不能表示一个数的时候而long类型可以做到，使用long类型。但是
，在long类大于int类型的系统中，使用long类型会减慢计算。所以没有必要的时候不要使用long类型

整数溢出:
PS:如果整数太大，超出了整数类型的范围会怎么样？下面分别将有符号类型和无符号类型整数设置为最大允许值
加较大的一些值，看看结果是什么？(printf()函数使用%u说明符显示unsigned int类型的值)
```c
#include <stdio.h>
int main(){
    int i=2147483647;
    unsigned int j=4294967295;

    printf("%d %d %d \n",i,i+1,i+2);
    printf("%u %u %u\n",j,j+1,j+2);
    return 0;
}
```
输出结果：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
2147483647 -2147483648 -2147483647 
4294967295 0 1
```
无符号类型j，当达到最大值时，它将溢出到起始点。整数i也是一样。
PS：系统并不会给出你数值溢出的报错，得让你自己去注意

在程序代码中使用2345这样的数字时，它可以int类型存储。当使用1000000这样的数字int类型不能表示时，
编译器会视其为long int类型（假定这种类型可以表达数字）。如果数字大于long类型的最大值，C会将其视
为unsigend long类型。如果仍然不够，C会视其为long long类型或者unsigend long long类型

打印short、long、long long和unsigned类型整数
要打印unsigned数字，可以使用%u符号。打印long数值，可以使用%ld格式说明符。short类型的前缀为h，如果
是十进制的话就是%hd,十六进制表现的话%hx unsigned short的话就是%hu.

PS：在前缀中无论大小写都可以，但是格式说明符必须要小写。
例子：使用不正确的说明符造成的下场
```C
#include <stdio.h>
int main(){
    unsigned int un=3000000;
    short end=200;
    printf("un=%u un=%d \n",un,un); //%d int格式化话字符，%u unsigned类型
    printf("end=%hd and end=%d \n",end,end); //%hd short int类型
    printf("big=%ld and %hd \n",end,end); //%ld long int类型
    printf("verybig=%lld and not %ld \n",end,end); //%lld long long int类型
    printf("This is short hex demo:end=%hx",end); //%x 十六进制输出
    return 0;
}
```
输出结果:
```
jiushideMacBook-Air:C jiushi$ ./a.out 
un=3000000 un=3000000 
end=200 and end=200 
big=200 and 200 
verybig=200 and not 200 
```

PS：一些常用的格式字符比如:long long -> %ll,short int -> %hd,unsigned int -> %u,int -> %d
hex->%x,八进制->%o,unsigned long long int -> %ulld

PS:short int类型在使用的时候会自动转换成int类型。所以说即可以使用%hd或%d

PS:使用printf()语句时，切记每个要显示的值都必须对应自己的格式化说明符，并将其显示值的类型要与说明符
相匹配

## chr类型 ##
chr类型用于存储字符和标点符号之类的字符。但在技术实现上char却是整数类型，这是因为char类型实际存储的是整数而不是
字符。为了处理字符，计算机使用了一种数字编码，用特定的整数来表示特定的字符。就是ASCII码，标准的ASCII码范围
从0到127，只需7位即可表示。而char类型通常定义为使用8位内存单元，该大小容纳ASCII码绰绰有余。更普遍来说C确保
char类型足够大，以存储基于系统上的字符集。

声明一个char类型：
```
char demo;
char response;
```

字符常量以及其初始化：
假设要把一个字符常量初始化为字母A
```
char edge='A'
```
单引号中的一个字符是C的一个字符常量，编译器遇到'A'时会将其转换为相应的编码值。其中单引号是必不可缺少的，一个错误
的char例子：
```
char broiled; //声明一个char变量
broiled='T'; //可以
broiled="T" //不可以，把“T”看做一个字符串
broiled=T //不可以，把T看做一个变量
```
PS:char只能使用字符转换，不能使用字符串

例子：
```C
#include <stdio.h>
int main(){
    char respone='A';
    printf("demo %d ",respone);
    return 0;
}
```

输出结果：转换成了ASCII码,'A'->65
```
jiushideMacBook-Air:C jiushi$ ./a.out
demo 65 jiushideMacBook-Air:C jiushi$ 
```
PS:char的说明符也是用%d输出，因为char类型被视为int类型

下面的语句中，65是int类型，但是它在char类型大小范围之内，所以这样的赋值完全允许。由于65是字母A的ASCII码
此语句将字符A给予变量grade。但是要注意，这个结果的假设是系统使用ASCII码，而使用'A'代替65进行赋值则可以
在任意系统中正常工作。因此，推荐使用字符常量，而不是使用数值编码。

PS:当输出char类型的字符的时候，当以%d格式化字符串输出的时候，会将字符转换为ASCII,而以%c格式化字符串输出的时候将不会转换为ASCII码。原因是，以%d整数类型显示的时候，会自动将字符类型转换为整数类型。转换过程就是ASCII编码,由于char是字符型所以输出不会被转换

例子：
```c
#include <stdio.h>
int main(){
    char ch;
    printf("Whos is your ASCII:");
    scanf("%c",&ch);
    printf("\n%c=>%d\n",ch,ch);
    return 0;
}
```
输出结果
```
jiushideMacBook-Air:C jiushi$ ./a.out 
Whos is your ASCII:a

a=>97
```

## 转义序列 ##

非打印字符：
单引号技术适用于字符、数字和标点符号，但是如果有些ASCII字符是打印不出来的，例如一些动作描述：退格、换行或者让
终端响铃。怎么样表示这些字符？
    第一种方法是使用ASCII码，例如：蜂鸣字符的ASCII值为7，所以可以这样写：
    char beep=7;
    第二种方法是使用特殊的符号序列，即转义序列

转义序列表
```
\a 警报
\b 退格
\f 走纸
\n 换行
\r 回车
\t 水平制表格
\v 垂直制表格
\\ 反斜杆(\)
\' 单引号(')
\" 双引号(")
\? 问号(?)
\0oo 八进制值，（o表示一个八进制数字）
\xhh 十六进制值，(h表示一个十六进制数字)
```
给一个字符变量进行赋值时，转义序列必须用单引号括起来，例如：
```
char berf='\n';
```
这样nef在屏幕上表示为换行

PS:\a是一个警报字符，产生一个能听到或者能看到的警报，这取决于计算机的硬件
就是说在显示设备（屏幕、电传打字机、打印机等等）中下一个字符将出现的位置。也就是
说，如果在程序中把警报字符输出到屏幕上，将只发出一声蜂鸣，而不移动鼠标光标

例子：
```c
#include <stab.h>
int main(){
    while (1)
    {
        printf("%c",'\a');
    }
    return 0;
}

```

%c代表字符型格式字符
%s代表字符串格式字符

参考地址：
https://zhidao.baidu.com/question/568315333.html
```
\a是 转义字符 007，响铃符 BEL。
printf("%d ",'\a'); 输出 7
printf("%c ",'\a'); 发出一声“嘀”
printf("\a"); 发出一声“嘀”
printf("\007"); 发出一声“嘀”
```
转义序列\b、\f、\n、\r、\t、\v是常用的输出设备控制字符。说明它们最后的方法是描述
它们对活动位置的影响。退格符\b使活动位置在当行退回一个空格。走纸符\f将活动位置移动
到下一页的开始处。换行符\n将活动位置移动到下一行的开始处。回车符\r将活动位置移动到
当前行的开始处。水平制表符\t将活动位置移动到下一个水平制表点（通常字符位置是1、9、17、25，等等）
垂直制表符\v将活动位置移动到下一个垂直制表点。
    这些转义符不一定适用所有设备，例如\f和\v在PC屏幕上产生奇怪的符号，而不会产生
    任何光标移动，它们只有在输出打印机上时才会像前面描述的那样工作
    例子：
    ```c
    #include <stdio.h>
    int main(){
        char c='\f';
        char v='\v';
        printf("c=%c v=%c",c,v);
        return 0;
    }
    ```
    输出结果：
    ```
    jiushideMacBook-Air:C jiushi$ ./a.out 
    c=
        v=
        jiushideMacBook-Air:C jiushi$ 

    ```
如果要在输出上打印'或“，也要用到转义
```
\"
\'
```

例子：
```c
#include <stdio.h>
int main(){
    printf("This is demo:\'");
    return 0;
}
```

输出结果：
```
deMacBook-Air:C jiushi$ ./a.out 
This is demo:'jiushideMacBook-Air:C jiushi$ 
```

最后两个转义符\0和\x是ASCII码的专用表示方法。如果想得到一个字符的八进制ASCII码代表它，可以在编码前
加个反斜杠(\)并用单引号括起来,例如：如果编辑器不识别警报字符(\a),则可以用ASCII码代表
```
beep='\007';
```
可以省去前面的0，就是说'\07'和'\7'都可以。即使前缀没有0，这种写法仍会被数值解释为八进制
例子：
```c
#include <stdio.h>
int main(){
    char a='\065'; //字符的65数值ASCII编码
    char b='\x65';
    printf("This is demo:\' %d\n",a);
    printf("This is demo_hex:%d",b);
    return 0;
}
```
输出：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
This is demo:' 53
This is demo_hex:101
```

PS:使用ASCII码时要注意数字和数字字符的区别，例如，字符4的ASCII码值为52，写法'4'表示符号4而不是数值4

## 打印字符 ##
```c
#include <stdio.h>
int main(){
    char ch;
    printf("Whos is your ASCII:");
    scanf("%c",&ch);
    printf("\n%c=>%d\n",ch,ch);
    return 0;
}
```
 ## 有符号与符号类型 ##

一些C实现把char当做有符号类型。这意味着char类型的典型范围为-128到127。另一些C实现把char
当做无符号类型，其取值为0-255
例如：使用无符号类型的时候需要定义unsigned,而有符号类型则不需要定义。
```c
#include <stdio.h>
int main(){
    unsigned demo_A=-10;
    int demo_b=-1;
    printf("signed类型和unsigned类型测试\n");
    printf("unsigned=%u signed=%d",demo_A+1,demo_b);
    return 0;
}
```

输出结果如下：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
signed类型和unsigned类型测试
unsigned=4294967287 signed=-1jiushideMacBook-Air:C jiushi$ //可以看见无符号类型确实溢出了，代表无负值
```

PS:依靠C90标准，C允许关键字char前使用signed和unsigned这样，无论默认的char类型是什么
signed char是有符号类型，而unsigned char则是无符号类型，这对于使用字符类型处理小整数十分
有用，如果处理字符。则使用不带修饰词的标准char类型

## _Bool类型 ##

_Bool类型由C99引入，用于表示布尔值，即逻辑值True(真)和False(假)。C用1表示True用0表示False,所以_Bool也是一种
整数类型。只是原则上它仅仅需要1位来进行存储

## _inttypes类型 ##
_可移植的类型inttypes.h
该类型使用typedef工具创建了新的类的工具，比如该文件会使用uint32_t作为一个系统中则可能是unsigned long。编译器会提供所在系统相一致的头文件，这些新的名称叫做“确切长度类型”（exact width long）。注意，与int不同，uint32_t不是关键字。所以必须在程序中包含inttypes.h头文件，编译器才能认识他

PS：使用确切长度类型的一个潜在问题是某个系统可能不支持的一些的选择。比如，不能保证某个系统上存在一种int8_t类型(8位有符号整数)。int_least8_t是可以容纳8位有符号数的那些类型中长度最小的一个别名，一个有符类型可以容纳-127-127

int_fast8_t定义为系统中对8位有符号类型而言计算最快的整数类型的别名


最后，对于某些程序员来说有时会需要系统最大的整数，那么可以使用intmax_t定义为最大有符号类型，相似的把uintmax_t定义为最大的无符号类型。顺便说一句，这些类型可能会大于long long和unsigned long类型，因为除了要实现的类型之外，C实现还可以定义其他类型

C99不仅提供这些新的、可移植的类型名，还提供了对这些类型数据进行输入输出的方法。例如,printf()打印某类型值要求之相应的说明符。如果打印int32_t类型值在一种宏定义中应该使用%d说明符，说白了就是定义的类型有int关键字的都用%d说明符

类似于更多的这种类型得百度

altnames.c
```c
#include <stdio.h>
#include <inttypes.h>
int main(){

    int16_t me16;

    me16=4593;
    printf("First ,ssume int16_t is short:");
    printf("me16=%hd \n",me16);
    printf("Next,iet's not make any assumptions.\n");
    printf("Instead, use a \"macro\" from intypes.h\n");
    printf("me16=%"PRId16"\n",me16);
    return 0;
}
```

输出结果：
```
First ,ssume int16_t is short:me16=4593 
Next,iet's not make any assumptions.
Instead, use a "macro" from intypes.h
me16=4593
```

在最后的pinrtf()语句中，参数PRId16被它在inttypes.h里的定义hd所代替，因而这行语句等价于：
```
printf("me16=%hd "\n",me16)
```

## 浮点类型 ##
float、double和long double类型
C语言中，浮点方法能够表示包括小数在内的更大范围的数。浮点数表示类似于科学计数法
C标准规定，float类型至少能表示有6位有效数字
C还提供一种double类型（意为双精度）的浮点类型。double类型和float类型具有相同的最小取值范围要求。但他
至少能表示10位有效数字。一般double使用64位而不是32位长度。一些系统将多出的32位全部用于尾数部分这增加
了数值的精度并减小了舍入的误差。C提供了第三种浮点类型long double类型，以满足比double类型更高的精度
要求。不过C只保证long duble类型至少同double类型一样精确

声明浮点变量
```
float noah,jonah
double trouble
float planck=6.63e-34
long double gnp
```

浮点常量
例子：
```
-1.56E+12
2.87E-3
-1
0.97
3.1415926
```

PS：在浮点常量中不要使用空格 错误 1.56 E+12、3 .14
默认情况下，编辑器将浮点数常量当做double类型。

double eum=0.6*0.8 这种就是double类型。计算结果将被截为正常的float类型
C使用您可以通过f或F后缀使编译器把浮点常量当做float类型，比如2.3F和9.11E9F。l或L后缀使
一个数字成为long double类型。比如54.31和4.32e4L。建议使用L后缀，因为字符l和1容易混淆

c99为表示浮点常量添加了一种十六进制格式。这种格式使用前缀0x或0X，接着是十六进制数字，然后是P或P


打印浮点值
printf()函数使用%f格式说明符打印十进制计数法的float和double数字,用%e打印指数记数法的数字
如果系统支持C99的十六进制格式浮点数，您可以使用a或A代替e或E。打印long double类型需要%LF、%Le
和%La说明符。注意float和double类型的输出都用%f和%e或%a说明符

%a或%e->十六进制浮点数
%Lf->long double
例子：
```c
#include <stdio.h>
int main(){
    float aboat=3200.0;
    double abet=2.14e9;
    long double dip=5.32e-5;
    printf("%f can be written %e\n",aboat,aboat);
    printf("%f can be written %a\n",abet,abet);
    printf("%Lf can be written %Lf",dip,dip);
    return 0;
}
```
输出结果：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
3200.000000 can be written 3.200000e+03
2140000000.000000 can be written 0x1.fe373cp+30
0.000053 can be written 0.000053
```

浮点值的上溢和下溢，
当计算一个结果大的不能表达的时候就会出现上溢，当除以一个十分小的数的时候，情况更复杂一些。回忆一下float数字被划分为指数和尾数部分进行存储。有这样一个数，它具有最小的指数，并且仍具有可以由全部可用位进行表示的最小尾数值。这将是能用
对浮点数值可用的全部精度进行表示的最小数字。现在可以把此数除2，通常这个操作将使指数部分减小，但是指数已经达到了最小值
所以计算机只好将尾数部分进行右移，空出首位二进制位，并丢弃最后一位二进制值。这就是下溢，C将损失了类型的精度的浮点值
称为低于正常的


浮点数舍入误差
将一个数加上1再减去1结果为1，但是如果是使用浮点数急速那的话，可能有所不同
```c
#include <stdio.h>
int main(){
    float a,b;
    b=2.0e20+1.0;
    a=b-2.0e20;
    printf("B:%f A:%f C:%e\n",a,b,b);
    return 0;
}
```

输出结果：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
B:4008175468544.000000 A:200000004008175468544.000000 C:2.000000e+20
```


复数和虚数类型：
```
三种复数类型
float_Complex、double_Complex和long duble_Complex
三种虚数类型
float_Imaginary、double_Imaginary、long double_Imaginary
```

使用虚数和复数可以用到complex.h
用complex.h里的Complex代替 _Complex,Imageinary代替_Imageinary
```c
#include <stdio.h>
#include <complex.h>
int main(){
    complex float a=182.33;
    printf("%f",a);
    return 0;
}
```

## 其他类型 ##
数组
指针
结构
联合等

## 总结：基本数据类型 ##
关键字：
    基本数据类型使用11关键字：int、long、short、unsigned、char、float、double、signed、_Bool、_Comple和_Imaginary

有符号整数
    * int:系统的基本整数类型，C保证int类型至少有16位长
    * short或short int:最大的short整数不大于最大的int整数值。C保证short类型至少有16位长
    *long或long int:这种类型的整数不小于最大的int整数值。C保证long至少有32位长
    *long long或long long int:这种类型不小于long最大的整数值。C保证long long至少有64位长
    
    一般地，long类型长于short类型，int类型和它们其中的一个长度相同。例如PC机上基于DOS的系统提供16位长的
    short和int类型，以及32位长的long类型；而基于windows 95的系统提供16位长的short以及32位长的int类型和long类型
        如果喜欢可以使用signed关键字任何一种有符号类型以明确表示这一属性，signed可以不写，因为默认声明为有符号类型，写了只不过更突出这个属性
    
    无符号整数：
        无符号整数只有0和正值，这使得无符号数可以表达比有符号数更大的正值。使用unsigned关键字表示无符号数，例如：unsigned、unsigned long和unsigned short。单独的unsigned等价于unsigned int

    字符：
        字符包括印刷字符，如A、&和+。在定义中，char类型使用一个字节的存储空间表示一个字符。出于历史原因，字符字节
        通常为8位，但出于表示基本字符集的需要，它可以为16位或更长

        char:字符类型的关键字。一些实现使用有符号的char，另外一些则使用无符号char，C允许使用signed和unsigned
        关键字标志char符号属性

    布尔值：
        布尔值表示ture和false；C使用1代表true，0代表false
        _Bool:此类型的关键字，布尔值是一个无符号整数，其存储只需能够表示0和1的空间
    
    实浮点数：
        浮点数可以有正值和负值
        float:系统的基本浮点数类型，至少能精确表示6位有效数字
        double:范围更大的浮点类型。能表示比float类型更多的有效数字（至少10位，通常会更多）以及更多的浮点数
        long double:范围可能再大的浮点类型。能表示比double类型更多的有效数字以及更大的指数
    
    复数和浮点数：
        虚数类型是可选类型，实部和虚部基于如下相应的实数类型：
        *float _Complex
        *double _Complex
        *long double _Complex
        *float _Imaginary
        *double _Imaginary
        *long double _Imaginary

    总结：如何声明简单变量
        1.所虚类型
        2.选用合法的字符为变量起一个名字
        3.使用下面的声明语句格式
        ```
        type-specifier variable-name
        ```
        type-specifier由一个或多个类型关键字组成，下面是一些声明例子
        ```
        int erest;
        unisgned short ocale;
        ```
        可以在同一类型后声明多个变量，这些变量名之间用逗号分隔，如下所示：
        ```
        char ch,init,ans;
        ```
        可以在声明语句中初始化变量，如下所示：
        ```
        float mass=6.0E24
        ```
    
        参考文章：https://zhidao.baidu.com/question/138203513697880125.html
        可以导入complex.h模块来将_Complex和_Imaginary替换成Cimplex和Imaginary来使用


典型系统的整数类型大小：
```
类型 Macintosh Metrpwerks CW(默认) PC机上的Linux系统 IBMPC机上的Windows XP和Windows NT系统  ASCII规定最小值
char 8 8 8 8
int 32 32 32 16
short 16 16 16 16
long 32 32 32 32
long long 64 64 64 64
```
以上所说的是有效数字位数

典型系统浮点数的情况：
```
类型 acintosh Metrpwerks CW(默认) PC机上的Linux系统 IBMPC机上的Windows XP和Windows NT系统  ASCII规定最小值
float 6 6 6 6
-37到38 -37到38 -37到38 -37到38
double 18 15 15 10
-4931到4932 -307到308 -307到308 -37到37
18 18 18 10
-4931到4932 -4931到4932 -4931到4932 -37到38
```
float上行的代表有效数字位，下行代表指数的范围


sizeof()以字节为单位给出类型的大小：
```C
#include <stdio.h>
int main(){
    printf("Type int a size of %u bytes.\n",sizeof(int));
    printf("Type int a size of %u bytes.\n",sizeof(float));
    printf("Type int a size of %u bytes.\n",sizeof(double));
    printf("Type int a size of %u bytes.\n",sizeof(signed));
    printf("Type int a size of %u bytes.\n",sizeof(long));
    printf("Type int a size of %u bytes.\n",sizeof(long long));
    printf("Type int a size of %u bytes.\n",sizeof(char));
    printf("Type int a size of %u bytes.\n",sizeof(short));
    return 0;
}
```

输出结果：
```
jiushideMacBook-Air:C jiushi$ ./a.out 
demo+demos=63.650002jiushideMacBook-Air:C jiushi$ ./a.out 
Type int a size of 4 bytes.
Type int a size of 4 bytes.
Type int a size of 8 bytes.
Type int a size of 4 bytes.
Type int a size of 8 bytes.
Type int a size of 8 bytes.
Type int a size of 1 bytes.
Type int a size of 2 bytes.
```

## 使用数据类型 ##
开发程序时，应当注意所需的变量以及类型的选择。一般的使用int或float类型表示数字，使用char类型表示字符。
在使用变量的函数开始处声明该变量，并为它选择有意义的名字。初始化变量使用的常量应当同变量类型相匹配
```
int a=30
float b=30.0
```

很多程序员和组织都有系统化的变量名规则，其中变量的名字可以表示它的类型。例如：使用i_前缀表示int变量，使用us_开头
代表unsigned short变量。这样通过名字就可以确定变量i_smart为int类型，变量us_verymast为unsigned short类型

参数和易犯的错误
传递给函数的信息被称为参数，函数调用printf("Hello,pal")包含一个参数"Hello,pal",用双引号引起来的一串字符称为字符串"sss",不论包含多少字符和标点符号，一个字符串只是一个参数
    与之类似，函数调用scanf("%d",&weight)包含两个参数，"%d"和&weight。C用逗号来隔开函数调用中的多个参数，printf()和scanf()比较特殊，其参数数目不受限制。例如，我们曾经使用1个，2个，甚至3个参数调用printf()函数。
    程序需要知道参数的目的才能正常工作，这两个函数通过第一个参数确定后续参数的数目才能正常工作，这两个函数通过第一个
    参数确定后续的参数个数，方法是一个参数字符串的每个说明符对应了后面的一个参数。如，下面的语句包含两个格式说明符
    %d和%d
    ```
    printf("This is %d and %d",a,a);
    ```

刷新输出：
```
printf()函数什么时候真正把输出传给屏幕？首先，printf()语句输出传递一个被称为缓冲区(buffer)的中介存储区域
缓冲区的内容再不断地被传递给屏幕，标准C规定在以下几种情况下降缓冲区传递给屏幕：缓冲区满的时候，遇到换行符的时候
以及要输入的时候，将缓冲区内容传送给屏幕或文件称为刷新缓冲区，例如，上列中，两个printf()语句既没有填满缓冲区
也找不到换行符，但是后面紧跟着一个scanf()语句要求输入。迫使printf()输出内容被传递屏幕，有一个函数用于专门
刷新缓冲区ffush()函数
```

PS:C允许书写混合数据类型表达式，但它会自动进行类型转换，以实际的计算只使用一种类型，计算机内存中使用数值编码来
表示字符，美国最常用的数值编码是ASCII编码，C也支持其他编码的使用，字符常量是计算机系统所使用的数值编码的符号
表示，它表示为单引号中的一个字符（如'A'）

PS:只有int(整数型)才有，有符号类型和无符号类型，最小的整数类型是char，因实现不同可以是有符号或无符号的。可以使用
signed char和unsigned char确定该类型符号的属性，不过这些通常用于使用此类型表示小整数而非字符编码。其他的整数
类型包括short,int,long,long long类型。C要求后面的类型不能小于前面的类型，上述类型是有符号的，但可以使用unsigned
关键字来产生相应的无符号类型：unsigned short,unsigned int,unsigned long,unsigned long long类型，也可以
使用signed修饰词明确地表示一个类型为有符号类型。最后_Bool类型是一种无符号类型，它只包含两个值0和1，对应于false和
true

3种浮点类型为float、double和ANSI C新增的long double后面类型的大小至少要和前面的类型一样大。有些实现支持复数
和虚数类型，方法是把_Complex和_Imaginary关键字同浮点类型关键字结合使用，例如double _Complex和float _Imaginary类型。

整数可以表达为10进制，8进制，16进制。前缀0指示八进制数，前缀0x或0X指示16进制数。例如，32、040和0x20分别表示
十进制，八进制和十六进制相同的一个值。后缀1或L指示long类型值，后缀II或LL表示long long类型值

字符常量表示为放在单引号中的一个字符，比如'Q'、'8'和'$'。C的转义序列（例如:'\n'）用于表示一些非打印字符。可以使用
诸如'\007'这样的形式通过字符的ASCII码表示一个字符
浮点数可以书写为小数点固定的形式，比如9393.912;或者书写为指数形式，比如：7.38E10
printf()函数通过对应于各种类型的转换说明符打印相应类型的数据。形式最简单的转换说明符由一个百分号和一个指示类型的
字符组成，比如%d和%f


练习题：
1.通过试验的方法观察系统如何处理整数上溢和浮点数上溢与下溢
```C
#include <stdio.h>
int main(){
	int i_shangyi=32767+8;
	float f_a=999999999;
	double f_b=-999999;
	printf("Integer type of overflow:% d, floating point type of overflow:%d\n",i_shangyi,f_a);
	printf("Floating point type of underflow:%e\n",f_b);
	return 0;
}
```
输出结果：
```
Integer type of overflow: 32775, floating point type of overflow:0
Floating point type of underflow:-9.999990e+005
```

编写一个程序，要求输入一个ASCII码值，然后输出相应的字符
```C
#include <stdio.h>
int main(){
	int i_demo;
	printf("Input number:");
	scanf("%d",&i_demo);
	printf("\nDemo:%c\n",i_demo);
	return 0;
}
```

输出结果：
```
Input number:65

Demo:A
```

PS:int类型转char类型，ASCII码变字符（默认取最左边第一个数字转换成字符）
char转int类型，字符变ASCII码（默认取最左边的第一个字母转出数字）

编写一个程序，发出警报声，并打印下列文字
```C
#include <stdio.h>
int main(){
	printf("\a Startled by the sudden sound,Sally shouted,\"By the Great Pumpkin,what was the!\"");
	return 0;
}
```

输出结果：
```
鸣叫一声，输出Startled by the sudden sound,Sally shouted,"By the Great Pumpkin,what was the!"
```

编写一个程序，读入一个浮点数，并分别以小数形式和指数形式打印
```C
#include <stdio.h>
int main(){
	float f_number;
	printf("Input float number:");
	scanf("%f",&f_number);
	printf("f_number=%f f_number=%e",f_number,f_number);
	return 0;
}
```

输出结果：
```
Input float number:3.1415
f_number=3.141500 f_number=3.141500e+000
```
一年约有3.156*10的7次方，编写一个程序，要求输入你的年龄，然后显示该年龄合多少秒
```C
#include <stdio.h>
#include <math.h>
int main(){
	int long i_gonshi=3.156*pow(10,7);
	unsigned int i_age;
	printf("Input your age:");
	scanf("%d",&i_age);
	printf("\n This is your age=%d,Seconds:%d",i_age,i_age*i_gonshi);
	return 0;
}
```
PS:pow()函数用于计算指定数值的几次方，用法pow(数值,多少次) 要引入的头部文件math.h

输出结果：
```
Input your age:17

 This is your age=17,Seconds:536520000
```

1个水分子的质量约为3.0*10的23次方，1夸脱水大约有950g，编写一个程序，要求输入的夸脱数。然后
显示多少个水分子
```C
#include <stdio.h>
#include <math.h>
int main(){
	double f_gonshi=3.0*pow(10,23);
	double f_value;
	printf("Input float number:");
	scanf("%f",&f_value);
	printf("\n %f",f_gonshi-f_value);
	return 0;
}
```

输出结果：
```
Input float number:69.6

 299999999999999970000000.000000
```

1英寸等于2.54cm，编写一个程序，要求输入您的身高（以英寸为单位），然后显示该身高值等于
多少厘米

```C
#include <stdio.h>
int main(){
	double f_yc=2.54;
	int i_yc;
	printf("This is your yinc:");
	scanf("%d",i_yc);
	printf("The number is:%f",i_yc/f_yc);
	return 0;
}
```

输出结果：
```
This is your yinc:6
The number is:3127713.385827
```

PS:在定义变量的时候先想好数值是怎么样的是，是什么类型的。如果用不到负数就声明属性unsigned用无符号类型来定义这个变量
用浮点数的时候尽量用double来代替float，因为double可以减少舍入的错误。根据想输出的内容来写说明符输出

END
