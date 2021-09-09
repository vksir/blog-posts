---
title: 搭建 Aria2 离线下载
comments: false
id: aria2
categories:
  - 玩转服务器
tags:
  - 服务器
  - aria2
date: 2020-03-06 22:50:48
---

> 环境：CentOS 7

## 安装 Aria2

```bash
# 安装
yum install aria2

# 查看版本
aria2c --version
# 添加配置文件
mkdir -p /root/.aria2
touch /root/.aria2/aria2.session
nano /root/.aria2/aria2.conf
```
<!-- more -->

`/root/.aria2/aria2.conf` 完整文件如下：

```aria2
# /root/.aria2/aria2.conf
# 需要修改-------------------------
# 文件的保存路径
dir=/data/download
# 设置的RPC授权令牌
rpc-secret=vksir97634

# 可选修改--------------------------
# 当下载的是一个种子(以.torrent结尾)时, 自动开始BT任务
#follow-torrent=true
# 断点续传
continue=true
# 最大同时下载任务数, 运行时可修改
max-concurrent-downloads=5
# 禁用IPv6
disable-ipv6=true
# 从会话文件中读取下载任务
input-file=/root/.aria2/aria2.session
# 退出时保存`错误/未完成`的下载任务到会话文件
save-session=/root/.aria2/aria2.session
# RPC监听端口, 端口被占用时可以修改
rpc-listen-port=6800

# 不推荐修改-----------------------
# 启用磁盘缓存, 0为禁用缓存
#disk-cache=32M
# 文件预分配方式, 能有效降低磁盘碎片
file-allocation=none
# 同一服务器连接数, 添加时可指定
max-connection-per-server=5
# 最小文件分片大小, 添加时可指定
min-split-size=20M
# 单个任务最大线程数, 添加时可指定
split=5
# 整体下载速度限制, 运行时可修改
#max-overall-download-limit=0
# 单个任务下载速度限制
#max-download-limit=0
# 整体上传速度限制, 运行时可修改
#max-overall-upload-limit=0
# 单个任务上传速度限制
#max-upload-limit=0
# 定时保存会话, 0为退出时才保存
#save-session-interval=60
# 启用RPC
enable-rpc=true
# 允许所有来源
rpc-allow-origin-all=true
# 允许非外部访问
rpc-listen-all=true
# 事件轮询方式, 取值:[epoll, kqueue, port, poll, select]
#event-poll=select
# BT监听端口, 当端口被屏蔽时使用
listen-port=6881-6999
# 单个种子最大连接数
#bt-max-peers=55
# 打开DHT功能, PT需要禁用
enable-dht=false
# 打开IPv6 DHT功能, PT需要禁用
#enable-dht6=false
# DHT网络监听端口
#dht-listen-port=6881-6999
# 本地节点查找, PT需要禁用
#bt-enable-lpd=false
# 种子交换, PT需要禁用
enable-peer-exchange=false
# 每个种子限速
#bt-request-peer-speed-limit=50K
# 客户端伪装, PT需要
peer-id-prefix=-TR2770-
user-agent=Transmission/2.77
# 当种子的分享率达到这个数时, 自动停止做种, 0为一直做种
seed-ratio=1.0
# 强制保存会话, 即使任务已经完成
#force-save=false
# BT校验相关, 默认:true
#bt-hash-check-seed=true
# 继续之前的BT任务时, 无需再次校验
bt-seed-unverified=true
# 保存磁力链接元数据为 .torrent 文件
bt-save-metadata=true
```

```bash
# 启动 Aria2
aria2c –conf-path=/root/.aria2/aria2.conf -D
# 查看 Aria2 监听的端口
netstat -ntlp
```

- -D：表示在后台启动 Aria2

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:6800            0.0.0.0:*               LISTEN      9398/aria2c
```

默认监听的端口为 `6800`，注意为此端口 [打开防火墙](https://www.vksir.zone/posts/firefall/)。

```bash
# 设置开机自启
echo "aria2c –conf-path=/root/.aria2/aria2.conf -D" >> /etc/rc.local
```

## 安装 AriaNG

> 需求：[Nginx](https://www.vksir.zone/posts/nginx/)

命令形式的 Aria2 工具如果不方便使用的话，可以为它安装这一款 WebUI。

AriaNG 仅使用 `html` 和 `JavaScript` 编写，其安装仅需要 Nginx。

```bash
# 创建安装目录
mkdir -p /var/www/ariaNG && cd /var/www/ariaNG
# 下载并解压安装包
wget -O AriaNG.zip https://github.com/mayswind/AriaNg/releases/download/1.1.4/AriaNg-1.1.4.zip && unzip AriaNG.zip
```

Nginx 配置文件。

```nginx
# /etc/nginx/nginx.conf -> server{ }
server {
    listen       80;			   # 监听端口
    server_name  _;				   # 此处填写域名，没有域名则以 _ 替代，使用 IP 访问
    root         /var/www/ariaNG;	# 网站根目录

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
        index index.html index.htm;
    }
}
```