---
categories:
- Linux
date: 2022-09-01 00:09:58.292528
id: swap
tags:
- linux
title: 【Linux】新建 swap 交换分区
---

最近开我的世界服，发生了好几次内存占满服务器卡死、导致不得不重启服务器的事情，遂而想新建一个交换分区，以免内存占满服务器直接卡死。

```shell
# 新建交换分区文件
dd if=/dev/zero of=/var/swap bs=1M count=4096
# 格式化交换分区
mkswap /var/swap
# 设置为交换分区
swapon /var/swap
# 设置开机自动挂载交换分区
echo "/var/swap swap swap defaults 0 0" >> /etc/fstab

# 查看交换分区是否生效
free -m
```
