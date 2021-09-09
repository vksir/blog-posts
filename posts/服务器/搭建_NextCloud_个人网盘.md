---
title: 搭建 NextCloud 个人网盘
comments: false
id: nextcloud
categories:
  - 玩转服务器
tags:
  - 服务器
  - 网盘
date: 2020-03-06 22:55:46
---

> NextCloud——一款优秀的，非常受欢迎的个人网盘。
>
> 优点：
>
> - 全平台支持：有 Windows、Linux、Mac、Android、IOS 客户端
> 
> - 支持文件同步（目前来看，安卓端文件同步没法使用）
> 
> 缺点：
> 
> - 无法直接访问本地目录
> 
> - 添加本地文件很麻烦
> 
> 环境：CentOS 7
> 
> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)，[PHP](https://www.vksir.zone/posts/php/)，[MySQL](https://www.vksir.zone/posts/mysql/)

<!-- more -->

## 安装 NextCloud

```bash
# 创建安装目录
mkdir -p /var/www/nextcloud && cd /var/www/nextcloud
# 下载并解压
wget -O nextcloud.zip https://download.nextcloud.com/server/releases/nextcloud-18.0.1.zip && unzip nextcloud.zip && mv nextcloud/* ./ && rm -rf nextcloud
# 更改安装目录权限
chmod -Rf 777 /var/www/nextcloud
```

## 配置 Nginx

修改 `/etc/nginx/nginx.conf`。

```nginx
# /etc/nginx/nginx.conf -> server{ }
upstream php-handler {
    server 127.0.0.1:9000;
    # server  unix:/var/run/php/php7.2-fpm.sock;
}

server {
    #listen 443 ssl http2; #若使用https，取消本行注释，同时注释下面这行
    listen 80;
    server_name _; #将cloud.example.com替换为你的域名

    # 若使用https，取消注释下面两行
    # ssl_certificate /etc/ssl/nginx/cloud.example.com.crt;
    # ssl_certificate_key /etc/ssl/nginx/cloud.example.com.key;

    # Add headers to serve security related headers
    # Before enabling Strict-Transport-Security headers please read into this
    # topic first.
    # add_header Strict-Transport-Security "max-age=15768000;
    # includeSubDomains; preload;";
    #
    # WARNING: Only add the preload option once you read about
    # the consequences in https://hstspreload.org/. This option
    # will add the domain to a hardcoded list that is shipped
    # in all major browsers and getting removed from this list
    # could take several months.
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Robots-Tag none;
    add_header X-Download-Options noopen;
    add_header X-Permitted-Cross-Domain-Policies none;

    # Path to the root of your installation
    root /var/www/nextcloud;

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    # The following 2 rules are only needed for the user_webfinger app.
    # Uncomment it if you're planning to use this app.
    #rewrite ^/.well-known/host-meta /public.php?service=host-meta last;
    #rewrite ^/.well-known/host-meta.json /public.php?service=host-meta-json
    # last;

    location = /.well-known/carddav {
    return 301 $scheme://$host/remote.php/dav;
    }
    location = /.well-known/caldav {
    return 301 $scheme://$host/remote.php/dav;
    }

    # set max upload size
    client_max_body_size 512M;
    fastcgi_buffers 64 4K;

    # Enable gzip but do not remove ETag headers
    gzip on;
    gzip_vary on;
    gzip_comp_level 4;
    gzip_min_length 256;
    gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
    gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

    # Uncomment if your server is build with the ngx_pagespeed module
    # This module is currently not supported.
    #pagespeed off;

    location / {
        rewrite ^ /index.php$uri;
    }

    location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {
        deny all;
    }
    location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
        deny all;
    }

    location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+)\.php(?:$|/) {
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        # fastcgi_param HTTPS on; # 若使用https取消这行注释
        #Avoid sending the security headers twice
        fastcgi_param modHeadersAvailable true;
        fastcgi_param front_controller_active true;
        fastcgi_pass php-handler;
        fastcgi_intercept_errors on;
        fastcgi_request_buffering off;
    }

    location ~ ^/(?:updater|ocs-provider)(?:$|/) {
        try_files $uri/ =404;
        index index.php;
    }

    # Adding the cache control header for js and css files
    # Make sure it is BELOW the PHP block
    location ~ \.(?:css|js|woff|svg|gif)$ {
        try_files $uri /index.php$uri$is_args$args;
        add_header Cache-Control "public, max-age=15778463";
        # Add headers to serve security related headers (It is intended to
        # have those duplicated to the ones above)
        # Before enabling Strict-Transport-Security headers please read into
        # this topic first.
        # add_header Strict-Transport-Security "max-age=15768000;
        #  includeSubDomains; preload;";
        #
        # WARNING: Only add the preload option once you read about
        # the consequences in https://hstspreload.org/. This option
        # will add the domain to a hardcoded list that is shipped
        # in all major browsers and getting removed from this list
        # could take several months.
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Robots-Tag none;
        add_header X-Download-Options noopen;
        add_header X-Permitted-Cross-Domain-Policies none;
        # Optional: Don't log access to assets
        access_log off;
    }

    location ~ \.(?:png|html|ttf|ico|jpg|jpeg)$ {
        try_files $uri /index.php$uri$is_args$args;
        # Optional: Don't log access to other assets
        access_log off;
    }
}
```

导入 `php-fpm` 组件，参考：[搭建 FileRun 个人网盘](https://www.vksir.zone/posts/filerun/)。

## 配置 MySQL

为 FileRun 新建一个数据库 `filerun`，并为该数据库创建一个用户 `filerun` 并设置密码，参考：[MySQL 的安装与配置](https://www.vksir.zone/posts/mysql/)。

## 完成安装

打开浏览器，输入 `http://IP` 根据指示完成安装。

## 添加本地文件

有时候我们需要往 NextCloud 中直接添加文件。将文件移入其根目录还不行，还得在其数据库中建立索引。

```bash
# 根目录 /var/www/nextcloud/data/username/files
# 建立索引
cd /var/www/nextcloud
sudo -u apache php72 occ files:scan --all
```

> 参考文档：<u>https://docs.nextcloud.com/server/18/admin_manual/installation/</u>