---
categories:
- 速记
date: 2022-09-01 00:09:58.293528
draft: false
id: systemctl
tags:
- fastapi
- linux
- systemctl
- 速记
title: Linux / 使用 systemctl 部署后台常驻服务
url: posts/systemctl
---

执行命令，添加配置内容，

```
systemctl edit --force --full xxx.service
```

```
[Unit]
Description=xxx
After=network.target

[Service]
Type=simple
# WorkingDirectory=xxx
ExecStart=xxx
Restart=on-failure
# User=root
# Group=root

[Install]
WantedBy=multi-user.target
```

启动服务，

```shell
# 启动服务
systemctl start supernode
# 开启自启
systemctl enable supernode
```

## 
