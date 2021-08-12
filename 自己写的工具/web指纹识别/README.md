## web指纹识别 ##
之前想过弄这个，后面发现这规则全是全。但是有些不按规范写的导致难处理，今天写了一下午的容错处理。
![正确的规范](img/规范.png)

指纹库来源:https://github.com/webanalyzer/rules   
(长期使用请自行更新)

(一些错误规范的规则)  
![](img/error1.png)

![](img/error2.png)

![](img/error3.png)

## 运行测试 ##
所有规则进行搜索    
![](img/testrun.png)

![](img/testrun2.png)

指定规则(需要指定绝对路径)  
![](img/testrun3.png)

![](img/testrun4.png)

指定txt  
![](img/testrun5.png)

```text
python webinfo.py -u <url> -m all or python webinfo.py -u <url> -m <path>
python webinfo.py -f <file> -m all or python webinfo.py -f <file> -m <path>
Usage: tesst9.py [options]

Options:
  -h, --help  show this help message and exit
  -u URL      Specify URL
  -f FILE     Specify file
  -m MODEL    Mode setting
```

默认过滤设置(注释掉的代表不使用)  
```python
        self.searchconfig=[['regexp'], #ok
                           ["search","text"], #ok
                           ['search', 'regexp'], #ok
      #                     ['md5', 'url'], #ok
      #                     ['url', 'md5'], #ok
       #                    ['url', 'md5', 'model'], #ok
                           ['search', 'regexp', 'offset'], #ok
                           ['status', 'text'], #ok
                           ['name', 'regexp', 'search'], #ok
                           ['name', 'search', 'regexp', 'offset'], #ok
                           ['search', 'regexp', 'name']] #规则过滤配置
```

使用all时要排除的规则库  
```python
  self.rulesexclude=["custom","fofa"] #规则库排除
```
