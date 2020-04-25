## fuzz_waf ##
"草" WAF

**config.py**  
English版
```python
path="I:\\jb\\fuzz_waf\\fuzz\\sqlDict\\sql.txt" #fuzz dict path or fuzz dir
whitelist=["txt"] #suffix list
blacklist={"code":0,"word":["网站防火墙"]} #Detect the keyword or keyword of WAF
fileenc=False #Automatic identification of file code, not on by default, UTF-8 by default
process=500 #Concurrent tasks to a certain extent
url="http://192.168.1.108/sql.php?id=1%20FUZZ" #URL requiring fuzzy
```

**config.py**  
中文版
```python
path="I:\\jb\\fuzz_waf\\fuzz\\sqlDict\\sql.txt" #字典txt或文件夹
whitelist=["txt"] #配合从文件夹里选出需要的后缀文件
blacklist={"code":0,"word":["网站防火墙"]} #匹配waf的关键点，状态码、关键字
fileenc=False #当path为文件夹时，读取文件需不需要编码识别，默认不开启（编码默认为utf-8）
process=500 #任务数量达到多少进行一次并发
url="http://192.168.1.108/sql.php?id=1%20FUZZ" #需要fuzz的url，并在需要fuzz的地方加上FUZZ
```

文件说明:
```text
config.py - 配置文件
fuzz.py - fuzz
result - fuzz结果
    blacklist.txt #失败的payload
    fuzz.txt #waf没拦截的payload
```

![](https://s1.ax1x.com/2020/04/25/Js4j4f.png)

