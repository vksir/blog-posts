---
categories:
- 速记
date: 2020-03-06 21:33:38
draft: false
id: linux_user
tags:
- linux
- 速记
title: 【Linux】用户 & 权限
url: posts/linux_user
---

## 用户管理

新建用户

```bash
# 新建用户
useradd username -s /bin/bash -d /home/username -m /home/username
# 新建一个无法登录的用户
useradd username -s /usr/sbin/nologin
```

<!-- more -->

- -s：指定 shell
- -d：指定 home 目录
- -m：创建 home 目录

删除用户

```bash
userdel username
```

修改用户密码

```bash
passwd username
```

切换用户

```bash
# 切换用户
su username
# 退回原用户
exit
```

## 用户组管理

查看用户组及其用户

```bash
cat /etc/group
```

将用户添加到用户组

```bash
# 修改用户所属的群组
usermod -g groupname username
# 修改用户所属的附加群组
usermod -G groupname username
```

删除组

```bash
groupdel groupname
```

## 权限修改

```bash
# 为文件/目录指定 用户:用户组
chown -Rf nginx:nginx /var/www/nginx

# 修改文件/目录权限
chmod -Rf 777 /var/www/nginx
```

- -R：使用递归方式逐个修改
- -f：不显示提示信息，静默执行
- 777：三个数字分别代表`User`、`Group`、`Other`。7 即最高权限 rwx——读、写、执行。
    - r = 4，w = 2，x = 1
    - 一般来说最好不要设置 777 权限，这样多用户使用时，将会使得管理变得非常麻烦。尽量多使用`用户组`管理权限，文件(夹)权限设置 774 就够了。

## 允许用户使用 Sudo

增加用户权限

```bash
chmod u+w /etc/sudoers
```

- u：表示是该文件的拥有者
- +：表示增加权限
- w：表示写权限

编辑文件

```bash
nano /etc/sudoers
```

添加以下代码

```bash
username ALL=(ALL) ALL		//添加用户
%groupname ALL=(ALL) ALL	//添加用户组(内所有用户)
```

- 建议添加在 `root ALL=(ALL) ALL`后面

删除用户权限

```bash
chmod u-w /etc/sudoers
```
