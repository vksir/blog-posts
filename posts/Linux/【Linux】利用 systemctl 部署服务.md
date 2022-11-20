---
categories:
- Linux
date: 2022-09-01 00:09:58.293528
id: systemctl
tags:
- fastapi
- linux
- systemctl
title: 【Linux】利用 systemctl 部署服务
---

## 部署简单进程

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

## 部署 FastAPI

```
[Unit]
Description=DST Run
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=steam
Group=steam
WorkingDirectory=/etc/dst_run
ExecStart=gunicorn dst_run.app.app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:5800
Restart=on-failure
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
