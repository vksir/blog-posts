---
title: 搭建 Chevereto 个人图床
comments: false
categories:
  - 玩转服务器
tags:
  - 服务器
  - 图床
date: 2020-03-11 14:53:50
id: chevereto
---

> 平时写写文什么的，图床还是要一个的，分享啊、插入图片啊，都挺方便的。（为什么要叫「图床」啊，叫「图库」多好听呢，或者「画廊」？）
>
> Chevereto 是一款常用的图床服务，这里使用的是「免费版」，个人使用也足够了。
>
> 环境：CentOS 7
>
> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)，[PHP 7.0-7.2](https://www.vksir.zone/posts/php/)（PHP 7.3 是不支持的，为此我特地把 PHP 换成了 7.2 版），[MySQL](https://www.vksir.zone/posts/mysql/)

<!-- more -->

## 下载

前往 [GitHub](https://github.com/Chevereto/Chevereto-Free/releases)，下载最新发布。

```bash
# 创建安装目录
mkdir -p /var/www/chevereto && cd /var/www/chevereto

# 下载
wget -O chevereto.zip https://github.com/Chevereto/Chevereto-Free/releases
# 解压
x chevereto.zip
```

- x：来自 [Oh My Zsh 的 extract 插件](https://www.vksir.zone/posts/onmyzsh/)，任何压缩包一个 `x` 搞定。

## 配置 Nginx

需要 `伪静态` + `php-fpm`。

- 伪静态配置文件如下
- 如何导入 `php-fpm`，参考 [搭建 FileRun 个人网盘](https://www.vksir.zone/posts/filerun/)

```nginx
server {
    server_name  www.vksir.zone;
    root         /var/www/chevereto;
    client_max_body_size 20m;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
        if (-f $request_filename/index.html){
            rewrite (.*) $1/index.html break;
        }
        if (-f $request_filename/index.php){
            rewrite (.*) $1/index.php;
        }
        if (!-f $request_filename){
            rewrite (.*) /index.php;
        }
        try_files $uri $uri/ /api.php;
    }

    location /admin {
        try_files $uri /admin/index.php?$args;
    }
}
```

## 配置 MySQL

为 Chevereto 新建一个数据库 `chevereto `，并为该数据库创建一个用户名为 `chevereto` 并设置密码，参考：[MySQL 的安装与配置](https://www.vksir.zone/posts/mysql/)。

## 完成安装

打开浏览器，输入 `http://IP` 根据指示完成安装。