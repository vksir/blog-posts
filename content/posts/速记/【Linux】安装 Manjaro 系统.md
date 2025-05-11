---
categories:
- 速记
comments: false
date: 2022-04-23 18:18:50.281708
draft: false
id: manjaro
tags:
- linux
- manjaro
- 速记
title: 【Linux】安装 Manjaro 系统
url: posts/manjaro
---

> Manjaro 还是好啊（或者说，Arch linux 还是好）。
>
> - 系统环境全部准备的好好的，想编译安装什么的，直接 `make && make install` 就行。换了 CentOS 7，那就是各种报错，缺这缺那，麻烦的很。
> - 强大的包管理系统。又说 CentOS，想装个麻烦的很，参照 [PHP](https://www.vksir.zone/posts/php/)，想装个软件还得去找 `源`，或者你想编译安装？行，一大堆报错等着你呢！而 Manjaro，直接 `yay -S php`，真的不要太简单。
>
> 就这……这不就够了吗？要不是服务器不好装 Manjaro，我都不想在服务器上用 CentOS 了，装个软件着实麻烦（强迫症……不想用 docker）。
>
> 还是在 PC 上用用吧。
>
> 环境：？

<!-- more -->

## 制作启动盘

使用官方推荐的刻录工具 [Rufus](https://rufus.ie/) 进行刻录。

据说是要使用 `dd` 模式进行刻录，但是目前的 Rufus v3.9 并没有 `dd` 模式，或许要使用低版本的 Rufus，或许不需要（距离上次安装有点久，有点忘了，下次安装系统再修改）。

## 安装

### 从 U 盘启动

如我的电脑——Acer Swift 5，其 bios 系统中存在 `UEFI 安全模式`，将其关掉。

### 安装

#### 1.

- lang=zh_CN
- driver=nonfree

然后 `Boot` 即可。

![安装1](https://static.vksir.zone/img/Snipaste_2020-03-11_15-53-19.png)

## 配置

### 安装源

自动寻找最快源

```sh
sudo pacman-mirrors -i -c China -m rank
```

添加 archlinuxcn 清华源

```sh
echo "[archlinuxcn]" >> /etc/pacman.conf && echo "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch" >> /etc/pacman.conf && sudo pacman -S archlinuxcn-keyring
```

更新源

```sh
# 更新源
sudo pacman -Sy

# 升级系统
sudo pacman -Syu
```

安装 AUR 助手——yay

```
sudo pacman -S yay
```

---

若出现无法锁定 database 的错误时，删除锁定即可

```sh
sudo rm /var/lib/pacman/db.lck
```

### Pacman 基本用法

> 转载自：<u>https://www.cnblogs.com/elinuxboy/p/10123877.html#_label1</u>

```sh
# 安装或者升级单个软件包，或者一列软件包（包含依赖包），使用如下命令：
sudo pacman -S pkg_name1 pkg_name2 ...
# 安装一个本地包(不从源里下载）：
sudo pacman -U /path/to/package/package_name-version.pkg.tar.xz
# 安装一个远程包（不在 pacman 配置的源里面）：
sudo pacman -U http://www.example.com/repo/example.pkg.tar.xz
# 下载包而不安装它：
sudo pacman -Sw pkg_name

# 删除指定安装包，但是保留其全部已安装的依赖关系
sudo pacman -R pkg_name 
# 删除指定软件包，以及没有被其他已安装软件包使用的依赖关系。 
5sudo pacman -Rs pkg_name 
# 删除软件包和所有依赖这个软件包的程序:
# 警告: 此操作是递归的，请小心检查，可能会一次删除大量的软件包。
sudo pacman -Rsc pkg_name
# 删除软件包，但是不删除依赖这个软件包的其他程序：
sudo pacman -Rdd pkg_name

# 清除未安装软件包的缓存 
sudo pacman -Sc 

# 在包数据库中查询软件包，查询位置包含了软件包的名字和描述(不指定string，则列出所有已安装的包)：
pacman -Ss string1 string2 ...
# 查询包含某个文件的包名     
pacman -Fs pkg_name
# 查询远程库中软件包包含的文件：
pacman -Fl pkg_name
# 获取已安装软件包所包含文件的列表：
pacman -Ql pkg_name
# 查询已安装的软件包(不指定string，则列出所有已安装的包)：
pacman -Qs string1 string2 ...
# 显示软件包的详尽的信息：
sudo pacman -Si pkg_name
# 查询本地安装包的详细信息：
sudo pacman -Qi pkg_name
```

### 安装必要软件

#### 输入法

#### 字体

先安装一大堆字体

```sh
sudo pacman -S wqy-microhei adobe-source-han-sans-cn-fonts wqy-zenhei adobe-source-han-serif-cn-fonts adobe-source-sans-pro-fonts adobe-source-serif-pro-fonts
```

再手动安装 `Consolas` 和 `Jetbrains Mono`。

#### 终端

安装 [Oh My Zsh](https://www.vksir.zone/posts/onmyzsh)

#### 常用软件

```sh
# 浏览器
sudo pacman -S google-chrome
# 下载工具
sudo pacman -S uget
# 编辑器（or IDE？）
sudo pacman -S visual-studio-code-bin
```

> ***Enjoy it !***
