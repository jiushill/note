# Injection
* 采用异步+多进程+协程

# 关键点说明
需要设置的
```text
url.txt --- 要测试的url
black.txt --- 黑名单设置
payload.txt --- payload设置
```

保存文件
```text
成功注入的保存为 --- sql_inject_ok.txt
Error问题 --- sql_inject_error.log
```

判断是否注入的地方（方便你们自己改）
```python
   def reqt(self,url):
        for p in self.payloads:
            urls1=url+p[0]
            urls2=url+p[1]
            try:
                rqt=requests.get(url=urls1,headers=self.headers,timeout=3)
                rqt2=requests.get(url=urls2,headers=self.headers,timeout=3)
                for y in self.blacks:
                    if y in rqt.text or y in rqt2.text:
                        print(Fore.YELLOW+'[X] '+Fore.WHITE+'发现黑名单关键字 url:{}'.format(url))
                        self.on_black.append(url)
                        break

                if rqt.text != rqt2.text and len(rqt.text)!=len(rqt2.text) and url not in self.on_black:
                    print(Fore.BLUE+'[+] '+Fore.WHITE+'Sql injection URL:{}'.format(url))
                    print('Sql injection URL:{}'.format(url),file=open('sql_inject_ok.txt','a',encoding='utf-8'))
                    break
                elif url in self.on_black:
                    break
                else:
                    print(Fore.RED+'[-] '+Fore.WHITE+'Not Sql injection URL:{} http_status_code:{}'.format(rqt.url,rqt.status_code))
            except Exception as r:
                print(Fore.RED+'[-] '+Fore.WHITE+'Error {} url:{}'.format(r,url))
                print('Error {} url:{}'.format(r, url),file=open('sql_inject_error.log','a',encoding='utf-8'))
```

## 测试结果
![](https://s2.ax1x.com/2019/11/01/KHejyD.png)