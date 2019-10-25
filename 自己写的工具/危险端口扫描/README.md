# Port_scanner

采用:异步+多进程+协程

用法
```
python port_scanner.py [IP/子网掩码] [port_range]
```

看图
![](https://s2.ax1x.com/2019/10/24/KauV2R.md.png)

自动保存为save.txt


## 生成饼图
修改jiance.py的函数调用
```python
    obj=Tonji(['1433','3306','80','554','139'],['MSSQL','MYSQL','Web','Video source','shared']) #第一个列表为要生成数据的对象，第二个为对应的端口名称，记得两者数量得相等
```
![](https://s2.ax1x.com/2019/10/25/KdPV4P.png)