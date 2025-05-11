---
categories:
- 速记
date: 2025-05-12 01:12:41.113627
draft: false
id: wsl_root
tags:
- 速记
title: WSL / 默认使用 root 用户
url: posts/wsl_root
---

打开 PowerShell，以 root 用户进入 wsl，

```
wsl -u root
```

再修改 root 密码，

```
passwd
```

修改 `/etc/wsl.conf` 文件，添加，

```
[user]
default=root
```

保存退出。

再退出到 PowerShell，重启 wsl，

```
wsl -t ubuntu
```

重新进入 wsl，即发现默认用户即 root。
