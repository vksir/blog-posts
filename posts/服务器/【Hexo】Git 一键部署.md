---
categories:
- 服务器
date: 2020-03-06 23:10:28
id: hexo-2
tags:
- hexo
- 博客
- 服务器
title: 【Hexo】Git 一键部署
---

> 这里要说的是部署到自己的服务器哦~其实呢，主要是有关 Git 的使用吧。
>
> 主要内容：
>
> - Hexo 一键部署
> - 使用自己的远程 Git 库
> - 快捷登录 SSH
>
> 环境：CentOS 7

<!-- more -->

## 创建Git用户 && SSH快捷登录

### 创建Git用户

```bash
# 创建无法使用ssh登录，但可以使用git功能的用户
useradd git -s /bin/git-shell
# 设置密码
passwd git
# 添加用户到nginx用户组
usermod -G nginx git
```

- 为什么需要将 `git`添加到 `nginx`用户组后面再聊~

### SSH快捷登录

将密钥推送到服务器

```bash
ssh-copy-id git@IP
```

## 建立远端Git库

### 创建库

```bash
# 创建库
cd /home/git
git init --bare hexo_html.git
```

- --bare：创建一个裸仓库（也就是不包含文件的仓库）

如果这里不加 `--bare`，待会儿推送的时候就会报错 `receive.denyCurrentBranch = false`。如果定不想加的话，就在 `.git/config`中添加：

```
[receive]
        denyCurrentBranch = ignore
```

这样就可以正常推送了。

### 使用库

直接在本地打开终端：

```bash
# 克隆库
git clone git:/home/git/hexo_html.git

# 测试
cd hexo_html
touch testfile
# 提交到本地库
git add .
git commit -m "第一次提交"
# 推送到远端库
git push

# 换个文件夹
git clone git:/home/git/hexo_html.git
ls
# 文件存在，表示搭建成功
```

虽然是 `push`到远端库了，但是在远端库里，是看不到任何文件的。推送的文件已另一种形式存储在了 `hexo_html.git`中。

但想要把Hexo的网页文件放在服务器上，当然是需要能在服务器上直接查看文件的，这样肯定是不行的。为此，有两种方案。

## Hexo一键部署

### 方案一：Git Push

没错，就是直接 `push`~

当然，仅 `push`肯定是不行的，`push`之后，需要 `checkout`。

```bash
git --work-tree=/var/www/hexo --git-dir=/home/git/hexo_html.git checkout -f
```

- -f：强制执行

这样所有内容就会被签出到 `/var/www/hexo` 中，再使用Nginx代理该目录即可。

注意修改`.ignore`文件，默认其中是包含`public`目录的，也就是不会推送该目录，而该目录正是保存网页文件的目录，所以需要在 `.ignore`中删除 `pulic`字样。

#### 自动checkout

但每次 `push`后，都要手动 `checkout`多麻烦啊，这不行。所以需要配置：每次 `push`后自动执行 `checkout`。

```bash
# 写入命令
echo "git --work-tree=/var/www/hexo --git-dir=/home/git/hexo_html.git checkout -f" >> /home/git/hexo_html.git/hooks/post-update
# 修改权限
chmod 755 /home/git/hexo_html.git/.git/hooks/post-update
```

这样一键 `push`，这个脚本就会自动执行 `checkout`了，实现一键部署！

### 方案二：Hexo-deployer-git

这是个插件，专为Hexo开发的，用来部署网页文件，也就是 `hexo deploy`这个命令。不装插件前这个命令貌似是无用的。

```bash
# 安装
npm install hexo-deployer-git
```

修改 `_config.yml`文件，没有则添加

```yml
deploy:
  type: git
  repo: git:/home/git/hexo_html.git
```

使用 `hexo deploy`，这个插件会帮你把 `public`中的文件推送到远端库中。

自然，也是需要 `checkout`的，自动 `checkout`方法和方案一相同。
