## 指针总结 ##
指针是一个特殊的变量，它里面存储的数值被解释成为内存里的一个地址。要搞清一个指针需要搞清指针的四方面的内容：指针的类型、指针所指向的类型、指针的值或者叫指针所指向的内存区、指针本身所占据的内存区

指针的创建：
```C
int *a; //创建一个int类型的指针
//a是指的物理地址
//*a是指针的值
int b=10;
a=&b; //将b的地址赋给a,此时a是b的地址，*a放的是b的值
```

一个简单的例子：
```C
#include <stdio.h>

void test(int *a,int *b);
int main(){
    int username=25,password=15;
    printf("The username=%d and password=%d \n",username,password);
    test(&username,&password);
    printf("The username=%d and password=%d \n",username,password);
    return 0;
}

void test(int *a,int *b){
    int test=*a;
    *a=*b; //指针A的值被重新赋值为指针b的值
    *b=test; //指针b的值被重新赋值为指针A的值
}
```

&是取地址符

>指针的值是指针本身存储的数值，这个值将被编译器当作一个地址，而不是一个一般的数值。在32 位程序里，所有类型的指针的值都是一个32 位整数，因为32 位程序里内存地址全都是32 位长。指针所指向的内存区就是从指针的值所代表的那个内存地址开始，长度为si zeof(指针所指向的类型)的一片内存区。以后，我们说一个指针的值是XX，就相当于说该指针指向了以XX 为首地址的一片内存区域；我们说一个指针指向了某块内存区域，就相当于说该指针的值是这块内存区域的首地址。指针所指向的内存区和指针所指向的类型是两个完全不同的概念。在例一中，指针所指向的类型已经有了，但由于指针还未初始化，所以它所指向的内存区是不存在的，或者说是无意义的。
————————————————
原文链接：https://blog.csdn.net/constantin_/article/details/79575638


指针本身所占据的内存区 :使用sizeof函数就可以知道

## 数组与指针 ##
数组的创建：
```C
int test[70]; //声明一个有70个元素位的数组，元素范围为0-69
```

详细的数组总结看自己Google文档上的文章

数组创建的时候头部就带有地址，所以指针指向数组的时候。数组不需要使用取址符
```C
#include <stdio.h>
#define DATE 70

int main(){
    int size[DATE]={1,2,3,4,5,6,7,8,9,10};
    int *test;
    test=size; //指针指向数组
    printf("size number 0:%d\n",*test); //将输出1，数组的首地址的值是1
    return 0;
}
```

指针对数组的一些操作
*指针表达式*
```
*test+1 //将地址移动数组的第二个地址，也可以这样写*(test+1)
*++test+1 //将数组的第二个地址的值递增一次，也可以这样写++*test;
```

比如对数组里面的首地址的值加10
```C
#include <stdio.h>
#define DATE 70

int main(){
    int size[DATE]={1,2,3,4,5,6,7,8,9,10};
    int *test;
    test=size; //指针指向数组
    printf("size number 0:%d\n",10+*test);
    return 0;
}
```

多维数组本身可以当做一个指针来操作
二维数组示例：
```C
#include <stdio.h>
#define DATE 70

int main(){
    int size[DATE][2]={{60,3}};
    printf("The value is %d\n",*size[0]); //这将输出60
    return 0;
}
```

三维数组示例：
```C
#include <stdio.h>
#define DATE 70

int main(){
    int size[DATE][2][2]={{60,3,{10,20}}};
    printf("The value is %d\n",*size[0][1]); //将输出10
    return 0;
}
```

错误的示例：
```C
#include <stdio.h>
#define DATE 70

int main(){
    int size[DATE][2][2]={{60,3,{10,20}}};
    printf("The value is %d\n",**size[0]);
    return 0;
}
```

## 指针与函数的操作 ##
可以将指针作为参数用来传递值或数组
```C
#include <stdio.h>

void test(int *a);
int main(){
    int tv[3]={1,2,3};
    test(tv);
    return 0;
}

void test(int *a){
    int calc=0;
    for(calc=0;calc<3;calc++){
        printf("The value %d\n",a[calc]);
    }
}
```

顺便记一下多维数组的遍历
```C
#include <stdio.h>
#define SIZE 4
#define SIZES 3

void tests(int test[][SIZES]);
int main(){
    int number[SIZE][SIZES]={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
    tests(number);
    return 0;
}

void tests(int test[][SIZES]){
    for(int calc=0;calc<SIZE;calc++){
        for(int calc2=0;calc2<SIZES;calc2++){
            printf("The key[%d][%d]=%d\n",calc,calc2,test[calc][calc2]);
        }
    }
}
```

指针方式的多维数组遍历
```C
#include<stdio.h>

void printMatirx(int *pArray,int rows,int cols);
int main()
{
    int array[2][3] ={{1,2,3},{4,5,6}};
    int *pArray = NULL;
    pArray = array;
    printf("array[0][0] = %d\n", *pArray);
    printf("array[1][2] = %d\n", *(pArray + 1 * 3 + 2));//访问1行2列的二维数组
    printMatirx(array,2,3);//打印2行3列的数组
    return 0;
}
void printMatirx(int *pArray,int rows,int cols)
{
    int i;
    int j;
    for(i=0;i<rows;i++)
    {
        for(j=0;j< cols;j++)
        {
            printf("%d\t",*(pArray+i*cols+j));//访问i行j列的二维数组元素
        }
        printf("\n");
    }
}
```

## 指针类型 ##
```C
int *calc; //int类型的数组
float *calc; //float类型的数组
char *calc; //char类的指针
```

不同类型的指针对应不同类型的变量
int类型的指针只能指向int类型的变量或其他


错误的示例：
```C
#include<stdio.h>

int main(){
    int *test;
    float sb=10.0;
    //printf("%f\n",sb);
    test=&sb;
    printf("The value:%d\n",*test);
}
```

## 指针运算 ##
```C
#include<stdio.h>

int main(){
    int *test;
    int  a=10;
    test=&a;
    printf("The value is %d\n",10+*test);
}
```

## 指针注意事项 ##
避免野指针的发生

````
野指针：

不是NULL指针，是指向“垃圾”内存的指针。

出现“野指针”主要有以下原因：

 

指针变量没有被初始化。
指针p被free或者delete之后，没有置为NULL，让人误以为p是个合法的指针。
指针操作超越了变量的作用范围。
````

1.未初始化的指针
```C
#include<stdio.h>

int main(){
    int *test;
}
```
应该改为：
```C
int *test=NULL;
```

2.指针被删除后没有被设置为NULL
```C
#include<stdio.h>
#include <stdlib.h>

int main(){
    int a=10;
    int *test=&a;
    free(test);
}
```

3.指针操作超出作用范围
```C
#include<stdio.h>
#include <stdlib.h>

int main(){
    int numbr[2]={1,2};
    int *test=numbr;
    printf("%d\n",test[2]);
    return 0;
}
```

>正确的做法：
a.正确的声明指针，让指针指向合法的内存区或者NULL
b.释放指针内存时，一定要先让指针执行空，再释放内存
c.指针如果访问超过作用范围，我没有想到什么好的办法避免这种情况下的野指针

## 参考链接 ##
[【 C语言指针详解 】(七）野指针 - 799 - 博客园](https://www.cnblogs.com/sxy-798013203/p/7790376.html)
[C 野指针](https://blog.csdn.net/qq_39540247/article/details/81353599)