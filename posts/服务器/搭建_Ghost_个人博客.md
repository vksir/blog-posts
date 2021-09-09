---
title: 搭建 Ghost 个人博客
comments: false
id: ghost
categories:
  - 玩转服务器
tags:
  - 服务器
  - 博客系统
date: 2020-03-06 22:14:19
---

## 安装必要的环境

- [安装 Nginx](https://www.vksir.zone/posts/nginx/)

- [安装 MySQL](https://www.vksir.zone/posts/mysql/)

- [安装 Nodejs](https://www.vksir.zone/posts/nodejs/)

- [创建非 root 用户](https://www.vksir.zone/posts/linux_user/)，以下默认该用户名为 `ghostuser`

## 安装 Ghost

`Ghost-cli` 是专为 Ghost 开发的一款安装工具，它使得安装 Ghost 变得非常容易。

```bash
# 全局安装 Ghost-cli
npm install ghost-cli@latest -g
```

选择一个目录作为 Ghost 的安装目录，个人建议将其放在 `/var/www` 中。

```bash
# 创建目录
mkdir /var/www/ghost -p && cd /var/www/ghost
# 修改权限
chown ghostuser:ghostuser /var/www/ghost
# 切换用户
su ghostuser
# 安装 Ghost
ghost install local
# 登出
exit
```

<!-- more -->

**特别注意：`/var/www/ghost` 及其下所有文件的所属为 `ghostuser:ghostuser`，请勿随意修改！**

Ghost 的所有操作必须由 `非 root 用户` 进行，若使用 `root 用户` 执行上述操作将会报错：

```bash
gyp ERR! stack Error: EACCES: permission denied, mkdir 'xxx'
```

好心点的话，会给你一点提示：

```bash
Switch to your regular user, or create a new user with regular account privileges and use this user to run 'ghost install'.
For more information, see https://ghost.org/docs/install/ubuntu/#create-a-new-user-.
```
若仍出现其他问题，可尝试在安装时查看错误日志

```bash
ghost install local --verbose flag
```

> 参考文档：https://ghost.org/docs/install/local/>

## 安装成功

```bash
✔ Checking system Node.js version
✔ Checking current folder permissions
✔ Checking memory availability
✔ Checking for latest Ghost version
✔ Setting up install directory
✔ Downloading and installing Ghost v3.8.0
✔ Finishing install process
✔ Configuring Ghost
✔ Setting up instance
✔ Starting Ghost

Ghost uses direct mail by default. To set up an alternative email method read our docs at https://ghost.org/docs/concepts/config/#mail

------------------------------------------------------------------------------

Ghost was installed successfully! To complete setup of your publication, visit:

    http://localhost:2368/ghost/

```

这里注意，Ghost 监听的端口为 `localhost:2368`，如果在 `远程服务器` 上部署 Ghost 的话，在本地访问 `http://localhost:2368/` 或者 `http://ip:2368/` 是打不开的。因此，我们需要配置 Nginx 反向代理。

## 配置 Nginx 反向代理

```nginx
# 打开配置文件
nano /etc/nginx/nginx.conf
# 修改 Server
# /etc/nginx/nginx.conf
server {
listen 80;
server_name _; # 在这里填写自己的域名。没有域名的话以 _ 代替，通过服务器 IP 访问。

location / {
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   Host  $http_host;
    proxy_pass http://127.0.0.1:2368;
}
```

在默认配置文件的基础上，仅仅修改 `server` 段就行。修改后的完整配置文件如下：

```nginx
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
    listen 80;
    server_name _;

    location / {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host  $http_host;
        proxy_pass http://127.0.0.1:2368;
    }
}

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers HIGH:!aNULL:!MD5;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```

到了这里，打开浏览器访问 `http://IP` 就可以看到 Ghost 页面了。现在我们进行进一步的配置。

## 配置 MySQL

Ghost 默认使用 SQLite3 数据库，数据存储在 `Ghost目录/content/data` 中，这里，我们为它部署 MySQL 数据库。

```bash
# 登录 MySQL
mysql -u root -p
# 新建数据库
create database ghost;
# 为 ghost 数据库创建用户 ghost, 密码 passwd
grant all on ghost.* to 'ghost'@'localhost' identified by 'passwd';
# 刷新权限相关表
flush privileges;
# 登出
exit;
```

修改 Ghost 为产品模式

```bash
# /var/www/ghost
ls
config.development.json content  current  versions
# 新建产品模式配置文件
cp config.development.json config.production.json
# 修改配置文件
nano config.production.json
# 只修改 database 段即可
# /var/www/ghost/config.production.json
  "database": {
    "client": "mysql",
    "connection": {
      "host": "localhost",
      "user": "ghost",
      "password": "passwd",
      "database": "ghost"
    }
# 重启 ghost
su ghost
ghost restart
exit
```

## Ghost 基本操作

```bash
# 启动
ghost start
# 停止
ghost stop
# 重启
ghost restart
```

Ghost 控制面板位于 `http://IP/ghost/`。

> ***Enjoy it !***