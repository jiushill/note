从ssh里把文件拖回去
base64 xxx.zip
把得到的base64编码在本地解码
echo "<base64>" | base64 -d > test.zip

拿到ssh的私钥先用
ssh2john转换格式，在用john爆破
python ssh2john id_rsa > cack
john cack

ssh用私钥连接先把id_rsa赋权限为600
chmod 600 id_rsa
ssh -i id_rsa 对应的用户@IP
私钥的密码