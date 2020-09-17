usage: check_inject.py [-h] [-f FILE] [-c]  

optional arguments:  
  -h, --help            show this help message and exit  
  -f FILE, --file FILE  批量检测  
  -c, --command         批量执行指定的命令  
cmd.txt是放要执行的命令  
Example:python check_inject.py -f file.txt #批量检测是否存在SQL注入  
Example:python check_inject.py -f file.txt -c #批量执行命令  
