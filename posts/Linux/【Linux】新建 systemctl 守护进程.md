---
categories:
- Linux
date: 2022-09-01 00:09:58.293528
id: systemctl
tags:
- linux
- systemctl
title: 【Linux】新建 systemctl 守护进程
---

编辑文件 `/etc/systemd/system/supernode.service` 如下：

```ini
[Unit]
Description=Supernode
After=network-online.target syslog.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/sbin/supernode /etc/n2n/supernode.conf -f
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

<!-- more -->

```shell
# 启动服务
systemctl start supernode
# 开启自启
systemctl enable supernode
```

> 参考文档：https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html
