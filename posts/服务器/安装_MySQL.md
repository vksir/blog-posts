---
title: Linux | 安装 MySQL
comments: false
id: mysql
categories:
  - 玩转服务器
tags:
  - Linux
  - 服务器
  - MySQL
date: 2020-03-06 21:38:10
---

> 主要内容：安装 & 基本操作 & 用户管理
>
> 环境：CentOS 7
>
> MySQL 版本：5.7

## 安装 MySQL

```sh
# 下载 rpm 包
wget http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
# 安装 rpm 包
rpm -Uvh mysql57-community-release-el7-9.noarch.rpm
# 安装 mysql
yum install mysql
# 检查版本
mysql --version

# 启动 mysql
systemctl start mysqld
# 设置开机启动
systemctl enable mysqld
```

<!-- more -->

## 配置 root 用户

```mysql
# 获取临时密码
grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}'
# 登录
mysql -uroot -p
# 修改密码安全要求（可选）
set global validate_password_policy=LOW;
# 修改密码为 passwd
alter user 'root'@'localhost' identified by 'passwd';
# 登出
exit;
```

## MySQL 基本操作

```mysql
# 查看数据库
show databases;
# 创建数据库 database_name
create database database_name;
# 删除数据库
drop database NAME;
```

## 用户管理

### 创建用户

#### 本地用户

```mysql
# 赋予该用户所有权限
grant all on DATABASE_NAME.* to 'username'@'localhost' identified by 'passwd';
# 创建只读用户
grant SELECT on DATABASE_NAME.* to 'username'@'localhost' identified by 'passwd';
```

- 可操作的数据库：`database_name`
- 用户名：`username`
- 密码：`passwd`

进行过权限操作后需要刷新权限。

```mysql
flush privileges;
```

#### 远程登录

创建能远程登录的用户，即将 `localhost` 改为 `%`。

```mysql
grant all on DATABASE_NAME.* to 'username'@'%' identified by 'passwd';
```

再 [打开防火墙](https://www.vksir.zone/posts/firewall/) `3306` 端口即可。

### 删除用户

```mysql
# 删除用户（仅删除远程用户）
drop user 'username';
# 删除本地用户
drop user 'username'@'localhost';
```

