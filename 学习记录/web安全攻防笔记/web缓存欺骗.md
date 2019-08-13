## WEB缓存欺骗 ##
web缓存欺骗参考资料：[Omer Gil: Web Cache Deception Attack](https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html)

攻击流程图
![Web_Cache_Manipulation.png](https://1.bp.blogspot.com/-zDck8_k-E4Y/WLP6c7VCu-I/AAAAAAAAGcI/lHhHh8SgO5cEVQ3iRBCAVPvdd3Fe-YB8ACLcB/s640/Web_Cache_Manipulation.png)

## 攻击方法 ##
在某些脚本加入如下静态脚本
`aif, aiff, au, avi, bin, bmp, cab, carb, cct, cdf, class, css, doc, dcr, dtd, gcf, gff, gif, grv, hdml, hqx, ico, ini, jpeg, jpg, js, mov, mp3, nc, pct, ppc, pws, swa, swf, txt, vbs, w32, wav, wbmp, wml, wmlc, wmls, wmlsc, xsd, zip

例如一个站点是这样的：
```
https://test.com/login.php
```

将其修改为
```
https://test.com/login.php/demo.css
```

站点返回正常，就代表存在缓存
参考YouTube视频

[![Watch the video](https://s2.ax1x.com/2019/08/13/mPMc34.md.png)](https://youtu.be/zMOVRPEhjtI)

判断利用是否成功的方法：
比如访问如下链接成功登录跳转到：
```
https://test.com/login.php
```

跳转到：
```
http://test.com/user.php
```

当访问如下：
```
https://test.com/login.php/<静态后缀>
如:https://test.com/login.php/demo.css
```
返回的内容和user.php的内容一样则代表的确存在web缓存漏洞
如果返回的不一样或404，301等等，则代表不存在漏洞

某猎人之前挖掘Google play出现的web缓存漏洞
[![Watch the video](https://s2.ax1x.com/2019/08/13/mPQkKs.md.png)](https://youtu.be/e_jYtALsqFs))
