### gevent模块的使用 ###

gevent是协程模块
```
协程:轻量级线程，拥有自己的寄存器上下文，栈，每次切换协程的时候，会保留当前的状态，当重新来到上步的时候会以保存上次的状态来恢复
```

代码
```python
#author:九世

import gevent
from gevent import monkey;monkey.patch_all() #猴子补丁，替换掉python原来掉函数或模块，patch.all()是执行所有可用补丁,必须提前打补丁不然会出现不可预料打错误
import requests

class demo:
    def f(self,urls):
        rqt=requests.get(url=urls)
        print(rqt.url)


if __name__ == '__main__':
    obj=demo()
    g1=gevent.spawn(obj.f,'https://www.baidu.com') #注册一个greenlet事件
    g2=gevent.spawn(obj.f,'https://www.bing.com')
    g1.join()
    g2.join()

```

spwan() #注册一个greenlet事件
getcurrent() #当前栈存在这里
join() #执行协程
joinall() #执行一个列表里的协程
from gevent import monkey #导入猴子补丁
monkey.patch_all() #执行全部可用的补丁

猴子补丁的来源：
```
 猴子补丁的这个叫法起源于Zope框架，大家在修正Zope的Bug的时候经常在程序后面追加更新部分，这些被称作是“杂牌军补丁(guerillapatch)”，后来guerilla就渐渐的写成了gorllia(猩猩)，再后来就写了monkey(猴子)，所以猴子补丁的叫法是这么莫名其妙的得来的。

         后来在动态语言中，不改变源代码而对功能进行追加和变更，统称为“猴子补丁”。所以猴子补丁并不是Python中专有的。猴子补丁这种东西充分利用了动态语言的灵活性，可以对现有的语言Api进行追加，替换，修改Bug，甚至性能优化等等。

   使用猴子补丁的方式，gevent能够修改标准库里面大部分的阻塞式系统调用，包括socket、ssl、threading和 select等模块，而变为协作式运行。也就是通过猴子补丁的monkey.patch_xxx()来将python标准库中模块或函数改成gevent中的响应的具有协程的协作式对象。这样在不改变原有代码的情况下，将应用的阻塞式方法，变成协程式的。

（2）猴子补丁使用时的注意事项

   猴子补丁的功能很强大，但是也带来了很多的风险，尤其是像gevent这种直接进行API替换的补丁，整个Python进程所使用的模块都会被替换，可能自己的代码能hold住，但是其它第三方库，有时候问题并不好排查，即使排查出来也是很棘手，所以，就像松本建议的那样，如果要使用猴子补丁，那么只是做功能追加，尽量避免大规模的API覆盖。

  虽然猴子补丁仍然是邪恶的(evil)，但在这种情况下它是“有用的邪恶(useful evil)”。
```

使用猴子补丁之前先查看有什么补丁在用
我上面写的requests，猴子补丁里面并没有，哈哈哈

怎么看猴子补丁里面有没有对应的模块补丁呢？
```python
from gevent import monkey;monkey.patch_all() #这是使用所有补丁
from gevent import monkey;monkey.path_select() #这是使用select模块的补丁
也就是说如果你想的那个模块有补丁的话patch_模块名()
```
