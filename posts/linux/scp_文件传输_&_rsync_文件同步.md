---
title: Linux | scp 文件传输 & rsync 文件同步
comments: false
id: rsync
categories:
  - Linux 小记
tags:
  - Linux
  - 文件传输
date: 2020-03-06 23:04:47
---

> 环境：CentOS 7

## scp 文件传输

```bash
# 上传到服务器
scp -r ~./hexo root@IP:/var/www
# 从服务器上下载
scp -r root@IP:/var/www ~./hexo
```

- -r：传输目录，不加即「传输文件」

<!-- more -->

scp 文件传输采用 `SSH` 手段加密，安全有保障，但是相对应的，传输速度会稍微慢一点。

## rsync 文件同步

rsync 文件同步同样会采用 `SSH` 手段加密，但是它会事先校验哪些文件相同，相同的则不进行传输。且 rsync 功能更加强大，参数更多，适合真正意义上的「同步」。

```bash
# 由本地同步到服务器
rsync -vau --progress ~./hexo root@IP:/var/www
# 服务器同步到本地
rsync -vau --progress root@IP:/var/www ~./hexo
```

- -v，--verbose：详细模式输出
- -q，--quiet：精简输出模式
- -a，--archive：归档模式，表示以递归方式传输文件，并保持所有文件属性，等于 `-rlptgoD`
- -u，--update：仅仅进行更新，也就是跳过所有已经存在于DST，并且文件时间晚于要备份的文件，不覆盖更新的文件
- -z, --compress：对备份的文件在传输时进行压缩处理（减少流量，其实用处不大）
- --progress：显示备份过程