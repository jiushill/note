### 为什么要使用多进程+协程  ###
引用某DN的说法：
>
```
举个例子：给你200W条url，需要你把每个url对应的页面抓取保存起来，这种时候，单单使用多进程，效果肯定是很差的。为什么呢？

例如每次请求的等待时间是2秒，那么如下（忽略cpu计算时间）：

1、单进程+单线程：需要2秒*200W=400W秒==1111.11个小时==46.3天，这个速度明显是不能接受的

2、单进程+多线程：例如我们在这个进程中开了10个多线程，比1中能够提升10倍速度，也就是大约4.63天能够完成200W条抓取，请注意，这里的实际执行是：线程1遇见了阻塞，CPU切换到线程2去执行，遇见阻塞又切换到线程3等等，10个线程都阻塞后，这个进程就阻塞了，而直到某个线程阻塞完成后，这个进程才能继续执行，所以速度上提升大约能到10倍（这里忽略了线程切换带来的开销，实际上的提升应该是不能达到10倍的），但是需要考虑的是线程的切换也是有开销的，所以不能无限的启动多线程（开200W个线程肯定是不靠谱的）

3、多进程+多线程：这里就厉害了，一般来说也有很多人用这个方法，多进程下，每个进程都能占一个cpu，而多线程从一定程度上绕过了阻塞的等待，所以比单进程下的多线程又更好使了，例如我们开10个进程，每个进程里开20W个线程，执行的速度理论上是比单进程开200W个线程快10倍以上的（为什么是10倍以上而不是10倍，主要是cpu切换200W个线程的消耗肯定比切换20W个进程大得多，考虑到这部分开销，所以是10倍以上）。

还有更好的方法吗？答案是肯定的，它就是：

4、协程，使用它之前我们先讲讲what/why/how（它是什么/为什么用它/怎么使用它）

what：

协程是一种用户级的轻量级线程。协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈。因此：

协程能保留上一次调用时的状态（即所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态，换种说法：进入上一次离开时所处逻辑流的位置。

在并发编程中，协程与线程类似，每个协程表示一个执行单元，有自己的本地数据，与其它协程共享全局数据和其它资源。

why：

目前主流语言基本上都选择了多线程作为并发设施，与线程相关的概念是抢占式多任务（Preemptive multitasking），而与协程相关的是协作式多任务。

不管是进程还是线程，每次阻塞、切换都需要陷入系统调用(system call)，先让CPU跑操作系统的调度程序，然后再由调度程序决定该跑哪一个进程(线程)。
而且由于抢占式调度执行顺序无法确定的特点，使用线程时需要非常小心地处理同步问题，而协程完全不存在这个问题（事件驱动和异步程序也有同样的优点）。

因为协程是用户自己来编写调度逻辑的，对CPU来说，协程其实是单线程，所以CPU不用去考虑怎么调度、切换上下文，这就省去了CPU的切换开销，所以协程在一定程度上又好于多线程。

how:

python里面怎么使用协程？答案是使用gevent，使用方法：看这里

使用协程，可以不受线程开销的限制，我尝试过一次把20W条url放在单进程的协程里执行，完全没问题。

所以最推荐的方法，是多进程+协程（可以看作是每个进程里都是单线程，而这个单线程是协程化的）

多进程+协程下，避开了CPU切换的开销，又能把多个CPU充分利用起来，这种方式对于数据量较大的爬虫还有文件读写之类的效率提升是巨大的
```

一个比较捞的例子：
```python
#author:九世

import gevent
from gevent import monkey;monkey.patch_all() #猴子补丁，替换掉python原来掉函数或模块，patch.all()是执行所有可用补丁,必须提前打补丁不然会出现不可预料打错误
import requests
from multiprocessing import Process

class demo:
    def f(self,urls):
        rqt=requests.get(url=urls)
        print(rqt.url)

    def task(self,url):
        tk=[]
        tk.append(gevent.spawn(self.f,url))
        gevent.joinall(tk)

    def zx(self):
        p=Process(target=self.task,args=('https://www.baidu.com',))
        p.start()


if __name__ == '__main__':
    obj=demo()
    obj.zx()
```

一个比较牛b的例子
```python
#author:九世

import gevent
from gevent import monkey;monkey.patch_all()
import requests
from multiprocessing import Process

class Demo:
    def __init__(self,headers):
        self.headers=headers

    def demos(self,urls):
        urlx='http://{}.baidu.com'.format(urls)
        try:
            rqt=requests.get(url=urlx,headers=self.headers,timeout=2)
            if not '不存在' in rqt.text and rqt.status_code==200:
                print(rqt.url)
        except:
            print('[-] fa {}'.format(urlx))
            pass

    def xc(self,ub):
        xs=[]
        for u in ub:
            xs.append(gevent.spawn(self.demos,u)) #创建协程事件

        gevent.joinall(xs) #协程运行

    def djc(self,flag=2): #flag等于2就创建一个进程
        lt = []
        with open('cs.txt','r') as r:
            i = 0 #计算器
            for s in r.readlines():
                qc="".join(s.split('\n'))
                lt.append(qc)
                i+=1
                if i==flag: #i等于2执行多进程
                    p=Process(target=self.xc,args=(lt,))
                    p.start()
                    lt.clear() #清空列表
                    i=0 #重置计算器

        if len(lt)!=0: #如果上面出了意外没有完全执行完进程，判断列表数量是否为0如果不为0则创建一个进程，并执行
            p = Process(target=self.xc, args=(lt,))
            p.start()

if __name__ == '__main__':
    headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    obj=Demo(headers=headers)
    obj.djc()
```

牛逼的思路解释
```
有3个函数:demos(),xc(),djc()
一个函数用来执行程序demos()，一个用来协程执行xc()，一个用来多进程执行djc()

djc()函数最为关键，他首先读取字典，函数里有个flag=2，i=0，列表lt=[]
每次字典逐行读取的时候i都会+1，把逐行读取的数据加入到列表，当i等于flag的时候就会
创建一个进程，进程会调用协程到函数，也就是xc()，把列表传入到协程的函数。然后重置
i，清空列表，然后xc()函数就会遍历djc()函数传进来的列表，然后执行一个协程事件添加到新列表，然后协程在执行整个列表里面的事件，也就是说执行demos()函数,然后在回到djc()函数，如果发生了意外，循环那里没有成功执行多进程，退出文件读取的循环后，会判断列表数量是否为0如果不是则执行多进程
```
