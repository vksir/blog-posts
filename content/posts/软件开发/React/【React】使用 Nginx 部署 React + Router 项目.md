---
categories:
- 软件开发
date: 2022-06-05 01:45:06.278889
draft: false
id: react_deploy
tags:
- http-proxy-middleware
- nginx
- react
- react router
- 软件开发
title: 【React】使用 Nginx 部署 React + Router 项目
url: posts/react_deploy
---

# 【React】使用 Nginx 部署 React + Router 项目

## 项目编译 & 打包

```sh
npm run build
```

编译好的静态文件会在 `build` 目录下。

<!-- more -->

## React 项目 Nginx 配置

```nginx
server {
    server_name web.vksir.zone;

    location / {
        root         /var/www/ns-web;
        index  index.html;
    }
}
```

## React + Router 项目 Nginx 配置

如果使用了 `react-router`，则 Nginx 配置会多出一项：

```nginx
server {
    server_name web.vksir.zone;

    location / {
        root         /var/www/ns-web;
        index  index.html;
        try_files $uri /index.html;
    }
}
```

## 配置代理

如果开发时使用了 `http-proxy-middleware`，打包成静态文件后，这个包将会失去作用，需要使用 Nginx 代替其提供代理功能。

如果 `src/setupProxy.js` 文件内容如下：

```js
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use('/ns_server', createProxyMiddleware({
        target: 'http://server.vksir.zone',
        changeOrigin: true,
        pathRewrite: {
            '^/ns_server': ''
        }
    }));
};
```

那么 Nginx 配置应当如下：

```nginx
server {
    server_name web.vksir.zone;

    location / {
        root         /var/www/ns-web;
        index  index.html;
        try_files $uri /index.html;
    }

    location /ns_server/ {
        proxy_pass http://server.vksir.zone/;
    }
}
```

## 安装 SSL 证书后 Post 请求变为 Get 请求的问题

使用 Certbot 安装 SSL 证书后，再访问发现网页登不上了，获取 token 的 post 请求经 301 重定向之后全部变成了 get请求：

![image-20220605011824875](https://static.vksir.zone/img/image-20220605011824875.png)

![image-20220605011850302](https://static.vksir.zone/img/image-20220605011850302.png)

Nginx 配置如下：

```nginx
server {
    server_name web.vksir.zone;

    location / {
        root         /var/www/ns-web;
        index  index.html;
        try_files $uri /index.html;
    }

    location /ns_server/ {
        proxy_pass http://server.vksir.zone/;
    }
    
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/api.vksir.zone/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/api.vksir.zone/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = web.vksir.zone) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

server_name web.vksir.zone;
    listen 80;
    return 404; # managed by Certbot
}
```

简单规避即是不让它去重定向，那么只要将 `http://server.vksir.zone/` 改为 `https://server.vksir.zone/` 即可。

修改完毕如下：

```nginx
server {
    server_name web.vksir.zone;

    location / {
        root         /var/www/ns-web;
        index  index.html;
        try_files $uri /index.html;
    }

    location /ns_server/ {
        proxy_pass http://server.vksir.zone/;
    }
    
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/api.vksir.zone/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/api.vksir.zone/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = web.vksir.zone) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

server_name web.vksir.zone;
    listen 80;
    return 404; # managed by Certbot
}
```
