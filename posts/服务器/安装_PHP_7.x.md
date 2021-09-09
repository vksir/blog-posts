---
title: Linux | 安装 PHP 7.x
comments: false
id: php
categories:
  - 玩转服务器
tags:
  - Linux
  - 服务器
  - PHP
date: 2020-03-06 22:41:08
---

> 环境：CentOS 7
>
> PHP版本：7.1 | 7.2 | 7.3 | 7.4

## 卸载其它版本

如果实现安装了其他版本的 PHP，需先将其卸载，避免冲突。

```bash
# 查看当前版本
php -v

# 列出已安装的 php 包
yum list installed | grep php
# 删除所有 php 包
yum remove *php*
```

<!-- more -->

## 安装 PHP

```bash
# 安装源
yum install epel-release
# CentOS 7
yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
# CentOS 6
yum install http://rpms.remirepo.net/enterprise/remi-release-6.rpm

# 查找库中的 php 包
yum search php

# 安装 php 7.2
yum install -y php72-php-fpm php72-php-cli php72-php-xmll php72-php-mcrypt php72-php-mysqlnd php72-php-pdo
```

php 有非常多组件，一开始并不需要装那么多，待到需要的时候再选择性安装就行了。

这里以安装 zip 组件为例。

```bash
# 查找相关 php 包
yum search php72 zip
# 复制其包名，安装
yum install php72-php-zip
```

安装完成后，启动 php。

```bash
# 查看版本
php -v
# 启动
systemctl start php72-php-fpm
# 设置开机自启
systemctl enable php72-php-fpm
```