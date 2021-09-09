---
title: Linux | 安装 Nginx
comments: false
id: nginx
categories:
  - 玩转服务器
tags:
  - Linux
  - 服务器
  - Nginx
date: 2020-03-06 22:36:00
---

> 主要内容：安装 & 配置文件介绍 & 静态网页 & 伪静态 & 加载 php-fpm
>
> 环境：CentOS 7
>
> Nginx 版本：1.16

## 安装 Nginx

```bash
# 安装
yum install nginx
# 查看版本
nginx -v

# 启动
nginx
# 设置开机自启
systemctl enable nginx
```

这时访问 `http://IP` 就可以看到 Nginx 初始网页了。

如果不能访问，一般是因为防火墙未开放端口，或者未设置安全组规则，如阿里、腾讯等国内 VPS 厂商，想访问其服务器端口，需在其控制台设置 `安全组规则`。请参照 [Firewall 防火墙管理](https://www.vksir.zone/posts/firewall/)。

<!-- more -->

## Nginx 配置文件

每次修改配置文件后，都需要重载配置文件才能使其生效。

```bash
nginx -s reload
```

### 配置文件

`/etc/nginx/nginx.conf`

### 配置目录

`/etc/nginx/conf.d`

在配置文件中，有这样一条：

```nginx
# /etc/nginx/nginx.conf
include /etc/nginx/conf.d/*.conf;
```

表示每次 Nginx 加载配置文件时，都会加载 `配置目录` 中的配置文件。

如果我们想在 Nginx 上部署很多 `server`，就可以写成一个个后缀为 `.conf` 的文件放入配置目录中。当然，直接在配置文件中间添加 `server` 段也可以，只是后期不那么容易管理。

### 组件目录

`/etc/nginx/default.d `

在有的 `server` 段中，有这样一条：

```nginx
# /etc/nginx/nginx.conf -> server{ }
include /etc/nginx/default.d/*.conf;
```

表示每次 Nginx 加载该 `server` 时，会为它加载组件中间夹中的组件。

这里面可以放置一些组件，例如 `php-fpm`，待到某个 `server` 需要用到这些组件时，在其中添上如上语句调用即可。

## 常用配置

### 基本网页配置

可访问仅使用 `html` 和 `JavaScript` 编写的静态网页。

```nginx
server {
    listen       80;			   # 监听端口
    server_name  _;				   # 此处填写域名，没有域名则以 _ 替代，使用 IP 访问
    root         /var/www/html;		# 网站根目录

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
        index index.html index.htm;
    }
}
```

### 反向代理

用来代理监听本地其它端口，如 [搭建 Ghost 个人博客](https://www.vksir.zone/posts/ghost/) 就要使用反向代理。

```nginx
    server {
    listen 80;
    server_name _;

    location / {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host  $http_host;
        proxy_pass http://127.0.0.1:2368;		# 代理本地 2368 端口
    }
```

### php-fpm 组件

此组件能使 Nginx 支持使用了 `php` 语言的网页。

```nginx
# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
location ~ .php$ {
    fastcgi_pass   127.0.0.1:9000;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
    include        fastcgi_params;
}
```

配置支持 `php` 的 `server`，例子可参考：[搭建 FileRun 个人网盘](https://www.vksir.zone/posts/filerun/)。

## 高级配置

### 修改传输文件大小上限

Nginx 默认允许上传的文件最大仅有 `1M`，若需要修改，则需向 `server` 中添加如下代码：

```nginx
# 修改允许上传的文件大小上限为 10G
client_max_body_size 10240m;
```

### 为网页配置密码

总有些网页我们不想让其他人访问，这时我们就需要为网页「上锁」。

```bash
# 安装 htpasswd
yum install httpd-tools
# 创建密码文件 passwd, 按指示输入用户名、密码
htpasswd -c /etc/nginx/ passwd
```

为需要上锁的 `server` 添加如下代码

```nginx
# /etc/nginx/nginx.conf -> server{ }
auth_basic "Please input password";
auth_basic_user_file /etc/nginx/passwd;
```

重载配置文件

```bash
nginx -s reload
```

这时再访问该 `server` 代理的网页，就会弹出一个窗口，提示你输入用户名及密码了。

如果无论怎么输入，访问页面都会出现 `500 Internal Server Error`，则是 Nginx 没有权限访问 `passwd` 文件，修改其权限即可。

```bash
chmod 644 /etc/nginx/passwd
```

请勿将 `passwd` 文件放在 Nginx 无法访问的目录中，这样无论怎么改变其文件属性，Nginx 都无法访问。

### 查看错误日志

```bash
tail -f /var/log/nginx/error.log
```

- -f：按流形式输出

### 权限管理

遇事不决，`chmod 777 -Rf /var/www/html` 。

这固然简单直接，但是这等于说为所有用户开放该目录的所有权限，`user`、`group` 还好，但开放了 `other` 的 `rwx` 权限就非常不妙了。在个人服务器上这么做倒无伤大雅，如果是多人共用的服务器，其他人也能登录服务器，这么做会使这个目录在其他人面前毫不设防，别人随随便便就能将其删除、修改，或者……添加病毒？

所以轻易不要这么做。Nginx 所代理的服务，其目录权限仅仅授予给 Nginx 自己就行了。

Nginx 默认使用的用户 为 `nginx:nginx`，前为用户，后为用户组。其组件 `php-fpm` 默认使用的用户为 `apache:apache`。

想修改 Nginx 用户直接修改其配置文件即可。

```bash
# Nginx 用户修改
nano /etc/nginx/nginx.conf
```

```nginx
# /etc/nginx/nginx.conf -> Line:5
user nginx;
```

```bash
# 重载配置文件
nginx -s reload
```

PHP 配置文件的存放位置各不一，随着版本、安装源的不同而变化。

```bash
# 寻找配置文件
find / -name php-fpm.d
/etc/opt/remi/php72/php-fpm.d
ls /etc/opt/remi/php72/php-fpm.d
www.conf

# php-fpm 用户修改
nano /etc/opt/remi/php72/php-fpm.d/www.conf
# /etc/opt/remi/php72/php-fpm.d/www.conf
# 默认
; RPM: apache user chosen to provide access to the same directories as httpd
user = apache
; RPM: Keep a group allowed to write in log dir.
group = apache
# 修改为
; RPM: apache user chosen to provide access to the same directories as httpd
user = nginx
; RPM: Keep a group allowed to write in log dir.
group = nginx

# 重启 php-fpm
systemctl restart php72-php-fpm
```

这样 Nginx 和 PHP 运行的就都是 `nginx:nginx` 用户了。

修改 PHP 用户后，可能会出现这种错误：

```
Sessions are not working on this server (session_start)
```

因此我们还得修改 `session` 权限。

```bash
# 这是个固定位置
chown nginx:nginx -Rf /var/lib/php/session/*
chown root:nginx /var/lib/php/session/*

# （或许）还有不定位置，由 php 版本决定
# 查看位置
cat /etc/opt/remi/php72/php-fpm.d/www.conf
php_value[session.save_handler] = files
php_value[session.save_path]    = /var/opt/remi/php72/lib/php/session
php_value[soap.wsdl_cache_dir]  = /var/opt/remi/php72/lib/php/wsdlcache
;php_value[opcache.file_cache]  = /var/opt/remi/php72/lib/php/opcache

# 修改权限（
chown nginx:nginx -Rf /var/opt/remi/php72/lib/php/*
chown root:nginx /var/opt/remi/php72/lib/php/*
```

这表示将 `session`、`wsdlcache`、`opcache` 内的文件权限改为 `nginx:nginx`，而把这三个目录本身的权限改为 `root:nginx`。

至此，Nginx、PHP 用户修改完成！

现在可以为 Nginx 代理的目录修改权限了。

```bash
# 修改目录权限
chown nginx:nginx -Rf /var/www/html
```

这样就不用担心其它用户随意修改了。

## 小贴士

1. 87 端口受到浏览器限制,是无法访问的。

