---
categories:
- Linux
date: 2022-11-20 21:20:59.860989
id: autocomplete
tags:
- linux
title: 【Linux】Ubuntu 历史命令补全
---

## 前言

RetHat 系列 Linux 发行版，如 Centos 7，自带历史命令补全。

如之前敲过一条命令：

```shell
ps -ef | grep sshd
```

<!-- more -->

下次再敲只需要按敲 `ps` 再按 `PageUp` 键即可自动补全，非常方便。

而 Debian 系列如 Ubuntu 20.04 默认没开启这项功能。

## 开启历史命令补全

```
vim /etc/inputrc
```

下两条设置取消注释：

```
# alternate mappings for "page up" and "page down" to search the history
# "\e[5~": history-search-backward
# "\e[6~": history-search-forward
```

改为：

```
# alternate mappings for "page up" and "page down" to search the history
"\e[5~": history-search-backward
"\e[6~": history-search-forward
```

然后执行 `exec bash` 即可。
