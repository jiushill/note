## X段探测

准备
```text
pip -r install requirements.txt
```

根据IP和子网掩码来生成IP来进行探测，例如:
```text
python C_search.py 192.168.6.0/24 #生成C段的IP
请注意必须是x.x.x.0/子网掩码
```

config.py
```python
PORT_LIST=[80,443,8080] #要进行探测的端口
TIMEOUT=3 #超时设置
```

测试
![](https://s2.ax1x.com/2019/10/20/KuiOfK.png)

结果将保存为save.txt
