停止日志记录的几个方法：
https://github.com/hlldz/Invoke-Phant0m

之后导入脚本
Import-Mode Inove-Phant0m.ps1
Inove-Phant0m

删除日志：
wevtutil cl Application
wevtutil cl Security
wevtutil cl System
wevtutil cl Setup
wevtutil cl ForwardedEvents


参考链接：
https://3gstudent.github.io/%E6%B8%97%E9%80%8F%E6%8A%80%E5%B7%A7-Windows%E6%97%A5%E5%BF%97%E7%9A%84%E5%88%A0%E9%99%A4%E4%B8%8E%E7%BB%95%E8%BF%87/
