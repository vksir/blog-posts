---
title: 搭建 FileRun 个人网盘
comments: false
id: filerun
categories:
  - 玩转服务器
tags:
  - 服务器
  - 网盘
date: 2020-03-06 22:26:10
---

> FileRun——一款简洁、漂亮且功能强大的个人网盘。
>
> 优点：
>
> - 美
> - 可直接访问本地目录
> - 传输文件速度快（原因不明，但是比 NextCloud 快）
>
> 缺点：
>
> - 没有手机端客户端
>
> 环境：CentOS 7
>
> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)，[PHP 7.1-7.3](https://www.vksir.zone/posts/php/)，[MySQL](https://www.vksir.zone/posts/mysql/)

<!-- more -->

## 安装 FileRun

```bash
# 创建安装目录
mkdir -p /var/www/filerun && cd /var/www/filerun
# 下载并解压安装包
wget -O FileRun.zip http://www.filerun.com/download-latest && unzip FileRun.zip
# 更改安装目录权限
chmod -Rf 777 /var/www/filerun
```

## 配置 Nginx

修改 `/etc/nginx/nginx.conf` 中的 `server` 段。

```nginx
# /etc/nginx/nginx.conf -> server{ }
server {
    listen       80;
    server_name  _;
    root         /var/www/filerun;
	# 修改上传文件大小上限
    client_max_body_size 10240m;


    # Load configuration files for the default server block.
    # 此处表示导入组件
    include /etc/nginx/default.d/*.conf;

    location / {
        index index.php index.html index.htm;
        try_files $uri $uri/ /index.php index.php;
    }
}
```

### 导入 php-fpm 组件

上方配置文件中已存在「导入额外组件」的代码，现在我们只要在目录中添加「组件文件」即可。

```nginx
# 新建组件文件
vim /etc/nginx/default.d/php-fpm.conf
# 写入以下内容
# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
location ~ .php$ {
    fastcgi_pass   127.0.0.1:9000;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
    include        fastcgi_params;
}
```

## 配置 MySQL

为 FileRun 新建一个数据库 `filerun`，并为该数据库创建一个用户名为 `filerun` 并设置密码，参考：[MySQL 的安装与配置](https://www.vksir.zone/posts/mysql/)。

## 完成安装

打开浏览器，输入 `http://IP` 根据指示完成安装。

> 参考文档：<u>http://blog.filerun.com/how-to-install-filerun-on-centos-7/</u>

## 重置密码

2020/3/16 更新

忘了密码了……

```sh
# 重置密码为 passwd
cd /var/www/filerun/cron
php reset_superuser_pass.php www.vksir.zone passwd
```

后又显示：

```
Your account has been deactivated!
```

登录 MySQL 数据库，输入：

```mysql
use filerun;
UPDATE `df_users` SET `activated` = '1' WHERE `id` = 1;
```

再登录就可以，进去改一下密码。

***Over***