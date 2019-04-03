### github修改项目并上传的方法 ###

---

PS：由于之前一直使用github网页端的文件上传功能，后来发现不方便就直接用git来更新了

安装git:[git下载](https://git-scm.com/downloads)

首先git clone你项目，比如我这里的项目是note
```
git clone https://422926799/note.git
```

然后配置你用户名和邮箱
```
git config --global user.email "你的邮箱"
git config --global user.user "你的用户名"
```
配置ssh_key
```
cd ~/.ssh
ssh-keygen -t rsa -C "你的邮箱"
```
会在~/.ssh生成一个id_rsa.pub，复制里面的内容在你github账号添加ssh_key

然后回到你clone的项目,进行你要的修改

然后git init
```
git init
```

上传
```
git add .
git commint "上传注释"
git push -u origin master
```