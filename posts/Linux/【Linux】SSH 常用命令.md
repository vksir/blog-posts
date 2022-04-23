---
categories:
- Linux
date: 2021-07-12 22:55:46
id: ssh
tags:
- linux
- ssh
title: 【Linux】SSH 常用命令
---

## 常用命令

```bash
# 登录
ssh <USER>:<PASSWORD>@<IP>

# 创建密钥
ssh-keygen
# 上传公钥
ssh-copy-id <UESR>@<IP>

# 端口映射
ssh -L <LOCAL_IP>:<LOCAL_PORT>:<REMOTE_IP>:<REMOTE_> <UESR>@<IP>
```

## 使用昵称登录

<!-- more -->

可以为服务器起一个「昵称」，然后用它来登录。

打开 ssh 配置文件。

```sh
vim ~/.ssh/config
```

输入以下内容。

```sh
Host mine
    Hostname IP
    Port 22
    User root
```

以后登录就输入昵称就行了。

```ssh
ssh mine
```

## 免断连

ssh 连上后几分钟不操作就会断开连接，这样的安全性确实好，但是却给我们造成了一定的困扰。

### 客户端

在客户端上，打开配置文件。

```sh
vim ~/.ssh/config
```

添加 `ServerAliveInterval 60`，just like this。

```config
Host mine
    Hostname IP
    Port 22
    User root
    ServerAliveInterval 60
```

客户端每隔 60 s 就会向服务端发送确认连接的消息，这样就可以避免断连了。

### 服务端

设置 60 分钟内不操作则断开连接。

```sh
echo "ClientAliveCountMax 60" > /etc/ssh/sshd_config
```
