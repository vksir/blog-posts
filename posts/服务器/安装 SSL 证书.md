---
categories:
- 服务器
date: 2022-05-08 11:35:26.141785
id: ssl-2
tags:
- ssl
- 服务器
title: 安装 SSL 证书
---

```sh
wget -O -  https://get.acme.sh | sh
. .bashrc
# 自动更新
acme.sh --upgrade --auto-upgrade
# 测试是否能成功获取
acme.sh --issue --test -d joking.vksir.zone -w /var/www/html --keylength ec-256
# 正式获取
acme.sh --issue -d joking.vksir.zone -w /var/www/html --keylength ec-256 --force
```

<!-- more -->

```sh
# 为 Xray 安装证书
acme.sh --install-cert -d joking.vksir.zone --ecc \
        --fullchain-file /usr/local/etc/xray/xray.crt \
        --key-file /usr/local/etc/xray/xray.key
chmod +r /usr/local/etc/xray/xray.key
```
