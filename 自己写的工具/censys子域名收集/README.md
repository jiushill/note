## Censys子域名收集 ##
```text
python query.py -a <API_ID> -s <Secret> -d <domain> -m #单个收集
python query.py -a <API_ID> -s <Secret> -f <file> -m #批量收集
```


help
```text
Usage: query.py [options]

Options:
  -h, --help     show this help message and exit
  -a API         This is Censys API ID
  -s API_SECRET  This is api_secret
  -d DATA        Search content
  -f FILE        Bulk search
  -m             domain query
```

测试结果：
![](https://s2.ax1x.com/2020/01/24/1VzgHA.png)