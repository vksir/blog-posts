---
title: Linux | 安装 Nodejs
comments: false
id: nodejs
categories:
  - Linux 小记
tags:
  - Linux
  - Nodejs
date: 2020-03-05 18:48:04
---

## 安装 nvm

### 下载安装脚本 | 运行

```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash
```

### 添加暂时的环境变量

这将在登出 shell 后失效

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

<!-- more -->

### 添加永久的环境变量

这意味着每次登录 shell 后，会自动加载这些环境变量

```bash
echo export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")" >> /etc/profile
echo "[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"" >> /etc/profile
```

## 安装 nodejs

```bash
# 列出所有版本
nvm list-remote
# 安装最新长期支持版
nvm install v12.16.1
# 切换版本
nvm use v12.16.1
# 设置默认版本
nvm alias default v12.16.1

# 查看版本
node -v
npm -v
```

## 更改镜像源

默认镜像源太慢，改用淘宝镜像源

```bash
# 查看镜像源
npm config get registry
# 使用淘宝镜像源
npm config set registry https://registry.npm.taobao.org
npm config set sass_binary_site=https://npm.taobao.org/mirrors/node-sass/
npm config set phantomjs_cdnurl=https://npm.taobao.org/mirrors/phantomjs/
npm config set electron_mirror=https://npm.taobao.org/mirrors/electron/
```

> 2020/3/13 更新
>
> 淘宝源的 electron 镜像有坑：
>
> ```nodejs
> (node:11316) UnhandledPromiseRejectionWarning: HTTPError: Response code 404 (Not Found) for https://npm.taobao.org/mirrors/electron/v8.1.1/electron-v8.1.1-win32-x64.zip
> ```
>
> 去淘宝镜像源网站看了一下，地址是这个：
>
> ```nodejs
> https://npm.taobao.org/mirrors/electron/8.1.1/electron-v8.1.1-win32-x64.zip
> ```
>
> 就少了一个 `v` ！
>
> 需要单独设置 electron 路径了：
>
> ```nodejs
> npm config set electron_custom_dir "8.1.1"
> ```
>
> > 参考：<u>https://www.cnblogs.com/ygjzs/p/12457945.html</u>

淘宝镜像源 electron 

### npm 配置文件

- [ ] 配置文件中有镜像源设置，可以自行更改


```bash
nano ~/.npmrc
```
