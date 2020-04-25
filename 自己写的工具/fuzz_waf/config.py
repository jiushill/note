path="I:\\jb\\fuzz_waf\\fuzz\\sqlDict\\sql.txt" #fuzz dict path
whitelist=["txt"] #suffix list
blacklist={"code":0,"word":["网站防火墙"]} #Detect the keyword or keyword of WAF
fileenc=False #Automatic identification of file code, not on by default, UTF-8 by default
process=500 #Concurrent tasks to a certain extent
url="http://192.168.1.108/sql.php?id=1%20FUZZ" #URL requiring fuzzy
