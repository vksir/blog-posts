---
title: 安装 SSL 证书
comments: false
id: ssl
categories:
  - 玩转服务器
tags:
  - Linux
  - 服务器
  - SSL
date: 2020-03-11 00:04:21
---

> 现在这个时代，SSL 已成了常态，没有 SSL 的网页浏览器都不让看，这里我们使用`let’s encrypt` 来获取「免费 SSL 证书」。
>
> 环境：CentOS 7
>
> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)

<!-- more -->

## 安装

使用 Nginx + SSL 的组合，以 Certbot 为工具安装 SSL 证书。

```bash
# 安装 EPEL repo -> Only For CentOS 7
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rp

# 安装 Certbot
yum -y install yum-utils
yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
yum install certbot python2-certbot-nginx

# 安装 SSL
certbot --nginx
```

- 建议不要一次性给所有域名授权 SSL 证书，这样大家将会使用同一个证书，有的网站就会显示「证书与域名身份不对」。别着急，一个个授权。
- 提示「是否 Redirect」建议选 `是`，这样 Certbot 将会帮你设置 Nginx，把「通往 `http / 80 端口` 的请求」重定向到「通往 `https / 443` 端口的请求」，还是非常有必要的。

就是这么简单，这就搞定了~

Certbot 会帮你把 Nginx 的所有 `server` 段重写，让其使用 SSL 证书。虽然重写后的格式非常丑陋，但是不用大家自己去配置了，还是非常方便的。

> 当然对于我这种强迫症来说，我把所有的配置文件又都重写了一遍，以漂亮的格式~

## 一点问题

### 1.

```bash
# Problem
ImportError: cannot import name UnrewindableBodyError
# Solve
pip uninstall urllib3
pip install urllib3
```

### 2.

```bash
# Problem
AttributeError: 'module' object has no attribute 'pyopenssl'
# Solve
pip install requests==2.6.0
easy_install --upgrade pip
```

### 3.

```bash
# Problem
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 2: ordinal not in range(128)
```

这是因为 `Nginx 配置文件` 中的字符编码不对劲造成的，于我，是因为配置文件中含有中文字符。

```bash
# 打印这些不对劲的字符
grep -r -P '[^\x00-\x7f]' /etc/letsencrypt /etc/nginx
```

接下来，把打印出来的「编码错误的字符」删掉即可。

> 2020/4/16 更新
>
> 遇到一个新问题：
>
> ```sh
> # Problem
> ImportError: 'pyOpenSSL' module missing required functionality. Try upgrading to v0.14 or newer.
> # Solve
> yum install http://cbs.centos.org/kojifiles/packages/pyOpenSSL/16.2.0/3.el7/noarch/python2-pyOpenSSL-16.2.0-3.el7.noarch.rpm
> ```
>
> 参考：<u>https://blog.csdn.net/mxw2552261/article/details/79730757</u>

## Nginx 配置文件示例

```nginx
server {
        listen 443 ssl http2; # managed by Certbot
        server_name www.vksir.zone;
        root /var/www/hexo;
        ssl_certificate /etc/letsencrypt/live/www.vksir.zone/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/www.vksir.zone/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        location / {
            index index.html index.htm;
        }

}

server {
        if ($host = www.vksir.zone) {
            return 301 https://$host$request_uri;
        } # managed by Certbot

        listen       80;
        server_name  www.vksir.zone;
        return 404; # managed by Certbot
}
```

### HTTP/2

如上文件 `Line:2` `listen 443 ssl http2; # managed by Certbot`，表示监听 443端口，使用 SSL 证书，同时启用 HTTP/2。

### 禁用 80 端口

第二个 `server` 段表示，以 `http` 访问网站的请求，将其全部转化为 `https` 访问，也就是访问 80 端口的请求全部被代理到 443 端口。

同时，若是强行访问 80 端口，则会返回 404。

## 调整防火墙

常用端口由 80 换到了 443，这也意味着我们需要为此调整防火墙端口。

- 禁用 80（其实无所谓，不禁用为好）
- 开放443（这很必要，否则将会无法访问）

具体指令参照：[Firewall 防火墙管理](https://www.vksir.zone/posts/ck7lsywxw0006z4jvcdpj1tag/)

## 证书管理

```sh
# 查看所有证书
certbot certificates
# 删除证书
certbot delete
```

> 参考文档：<u>https://certbot.eff.org/docs/using.html#id21</u>