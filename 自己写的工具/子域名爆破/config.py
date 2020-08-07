#子域名爆破配置
dictpath=r"" #路径字典设置
domain="github.com" #爆破的域名
level="1-5" #等级设置，1=子域名,2=3级子域名,3=4级子域名，1-3=1到4级域名
process=500 #任务量并发设置
defaultdns="114.114.114.114" #解析ip设置
blackiplist=["0.0.0.1","127.0.0.1","0.0.0.0"] #ip黑名单（解析得到的无效ip）

#http信息获取配置
domainpath=r"" #填入要进行信息获取的文件夹路径
reg=True #是否自动提取域名
process2=500 #任务量并发设置
