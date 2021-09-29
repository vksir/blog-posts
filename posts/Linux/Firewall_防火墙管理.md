---
title: Linux | Firewall 防火墙管理
comments: false
id: firewall
categories:
  - Linux 小记
tags:
  - Linux
  - Firewall
date: 2020-03-06 21:43:39
---

> 个人电脑倒没什么，如国内，很少有个人电脑有公网 IP 的。但服务器不同，24 小时运行 + 公网 IP + 诸多网站、数据库等信息，防火墙还是要开一个的。
>
> 主要内容：基本操作，端口开启关闭，安全组
>
> 环境：CentOS 7

<!-- more -->

常见的 Linux 防火墙有两种：iptables 和 firewall，不过呢，虽然他们是一种东西，但是 firewall 其实是通过调用 iptables 来实现功能的，firewall 对比起 iptables 多提供了一些桌面程序接口，实质上两者是一样的。

这里我们禁用 iptables

```bash
systemctl stop iptables
systemctl disable iptables
```

## 基本操作

```bash
# 启动
systemctl start firewalld
# 关闭
systemctl stop firewalld
# 查看状态
systemctl status firewalld
# 重启
systemctl restart firewalld

# 开机自启
systemctl enable firewalld
# 禁用开机自启
systemctl disable firewalld
```

## 端口开启 & 关闭

```bash
# 查看端口监听
netstat -ntlp

# 查看 Firewall 已经开放的端口
firewall-cmd --list-ports
# 开启端口
firewall-cmd --zone=public --add-port=19999/tcp --permanent
# 关闭端口
firewall-cmd --zone=public --remove-port=19999/tcp --permanent
# 使设置生效
systemctl restart firewalld
```

## 关于安全组

开了防火墙端口还是无法访问？八成是添加安全组规则。

这玩意儿只有诸如腾讯云、阿里云厂商的服务器有，国外的 VPS 大多没有。配置方法见 [教我设置](https://help.aliyun.com/document_detail/25475.html?spm=5176.2020520101.121.1.6b144df5saKTIG)。

其实不用看，直接「快速创建规则」按着来就行了。

![安全组](https://gallery.vksir.zone/images/2020/03/05/QQ20200305005754.jpg)