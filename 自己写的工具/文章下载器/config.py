from plugin import xianzhidemo
MODE={"1":"从指定文件里读取txt下载页面","2":"从网页里搜集url下载"} #2是预留函数
RESERVE=xianzhidemo.geturl #预留函数定义

REQUEST_CONF={
    "REQUEST_HEADER":{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},
    "TIMEOUT":5,
} #请求配置 (COOKIE也请设置在REQUEST_HEADER里)

#download module配置 (main函数线程池不受DOWNLOAD_MODULE设置所影响)
DOWNLOAD_MODULE=1 #0为单线程,1为多进程
PROCESS=5 #进程限制大小 （要求DOWNLOAD_MODULE为1）