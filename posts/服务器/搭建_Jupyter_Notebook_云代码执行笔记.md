---
title: 搭建 Jupyter Notebook 云代码执行笔记
comments: false
categories:
  - 玩转服务器
tags:
  - 服务器
  - 云笔记
  - Jupyter
date: 2020-04-16 17:04:16
id: jupyter-notebook
---

> Jupyter Notebook——我实在想不好该用什么来形容它，百科的介绍是「交互式笔记」，或许交互式确是它的特点，但我感觉最大的特点还是它是个 Web 应用，能「云」，且能「执行代码」，支持 40+ 语言。
>
> 为什么需要它：因最近想学习一下与服务器进行远程通信，而本人 `vim` 的熟练度又着实一般，想在服务器上运行代码非常麻烦，因此搭建这么一个玩意儿方便运行代码。另外，它还能当做云笔记来用，曾想搭建一个云笔记，可印象笔记另需数据库，没那么内存给它，其它云笔记又没什么好的，因此搁置，这不 jupyter 来了，正好。
>
> 优点：远程执行代码，远端保存笔记
>
> 环境：CentOS 7
>
> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)，Python

<!-- more -->

## 安装

非常简单，这里我是基于 python 3 安装的，当然 python 2 也可以。

```sh
# 安装
pip3 install jupyter

# 启动
jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --port=8888
```

- --ip=0.0.0.0：指定 IP 为本机 IP
- --no-browser：启动后会默认打开浏览器，这里我在远端服务器上使用，选择不打开浏览器
- --allow-root：允许使用 root 用户运行
- --port=8888：默认监听 8888 端口，可修改

现在可以打开浏览器进入 `http://IP:8888` 就可以看到 Jupyter NoteBook 的登录界面了。

它会提示你设置密码，`token` 在启动程序的时候会打印出来，输入此 `token` 和自己的密码设置即可。

初次登录需要设置密码，下次就不需要了。

## Nginx 反向代理

### 配置 Nginx

> 不使用反向代理直接使用也是可以的，但无法域名访问，且无法使用 SSL 证书，信息明文传输，安全得不到保证。

哈哈，虽然没那么多机密，但是用一个也好啊。

创建文件：

```sh
vim /etc/nginx/conf.d
```

写入：

```nginx
server {
   listen 80;
   server_name www.vksir.zone;
   location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header host    "127.0.0.1:8888";
        proxy_set_header origin  "http://127.0.0.1:8888";
        proxy_set_header X-Real-IP "127.0.0.1";

        # WebSocket proxying
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

加载配置文件：

**这里 `域名`，`Jupyter Notebook 监听端口` 都需要自己设置。**

因我们使用 Nginx 进行反向代理，Jupyter Notebook 监听的 IP 就可以设置为本地 IP 了，也就是 `127.0.0.1`，这样除本机外就无法访问了。——Nginx 可访问，我们再访问 Nginx。

> 参考：<u>https://blog.csdn.net/qq_41861526/article/details/100181211</u>

### 配置 Jupyter Notebook 后台运行。

> 有两种思路，一是使用 `nohub` 命令，比较简单，但封装不够完美。
>
> 我们使用比较专业的 `systemctl`。

#### 准备工作

1. 新建一个用户 `jupyter`，并将其添加到用户组 `nginx`，参考：[Linux 用户管理](https://www.vksir.zone/posts/linux_user/)。
2. 创建工作目录 `/var/www/jupyter`，并修改其权限为 `jupyter:nginx`。

#### 创建 service

创建文件：

```sh
vim /etc/systemd/system/jupyter.service
```

写入：

```service
[Unit]
Description=Jupyter NoteBook

[Service]
WorkingDirectory=/var/www/jupyter
User=jupyter
Group=jupyter
Restart=on-failure
ExecStart=/usr/local/bin/jupyter notebook --ip=127.0.0.1 --no-browser

[Install]
WantedBy=multi-user.target
```

运行：

```sh
# 启动
systemctl start jupyter

# 开机自启
systemctl enable jupyter
```

到这里，浏览器输入域名已经可以访问到 Jupyter Notebook 了，下面我们再设置 SSL 证书。

### 安装 SSL 证书

参考：[安装 SSL 证书](https://www.vksir.zone/posts/ssl/)。