---
title: 简明的 SSH 登录法
comments: false
id: ssh
categories:
  - 玩转服务器
tags:
  - 服务器
  - Linux
date: 2021-07-12 22:55:46
---

> 刚买了个服务器，第一步做什么？当然是 ssh 登录啦~

## 直接登录

当然也可以输入密码直接登录啊。

```sh
ssh root@IP
```

之后服务器会向你询问密码，输入然后 `Enter` 即可（Linux 特性：输入的密码是看不见的~）。

##  使用密钥登录

每次登录都要输密码，岂不是太过麻烦？使用密钥，就可以免密登录了。

<!-- more -->

### 创建密钥对

```sh
ssh-keygen
```

### 上传公钥

```sh
ssh-copy-id root@IP
```

这一步也是需要的密码的。

### 尝试登录

上传成功后，就可以免密登录了。

```sh
ssh root@IP
```

不需要密码就直接登录进去了。

## 使用昵称登录

免密登录还不够简单，还需要输入 `IP` 呢！`IP` 也是很难记的啊。

当然，我们可以为服务器起一个「昵称」，然后用它来登录。

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

## 客户端

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

## Shell for Windows

Linux 系统当然好说，各种各样强大的终端。Windows 可选择的终端就不多了。

### Windows Terminal

[下载地址](https://www.microsoft.com/zh-cn/p/windows-terminal-preview/9n0dx20hk701?activetab=pivot:overviewtab)

微软自家的增强型终端，你值得有用。

但是这终端本身是没有 ssh 功能，你需要下载一个。

[OpenSSH](https://www.openssh.com/)

下载完成后，你会发现里面就是一些 exe 程序，诸如我们所熟悉的 `ssh.exe`，`ssh-copy-id.exe`。那么显而易见，把它们加入环境变量，就可以直接在 `Windows Terminal`，`Powershell`，`cmd` 等任意终端使用 ssh 功能了。

### WSL-Ubuntu

微软应用商店下载一个 Ubuntu 子系统，然后利用它的终端来进行 ssh 登录。（有点麻烦）

### MobaXterm

功能繁多——主要也就是馋它的 fstp。但有个缺点，不太好看——这很致命。

当然你也可以选择 XShell，我感觉那个更……哈哈，也是个选择。