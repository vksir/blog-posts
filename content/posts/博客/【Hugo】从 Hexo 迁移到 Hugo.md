---
categories:
- 博客
date: 2025-05-11 15:21:29.682602
draft: true
id: hexo_to_hugo
tags:
- 博客
title: Hugo / 从 Hexo 迁移到 Hugo
url: posts/hexo_to_hugo
---

## 写在前面

很早之前就有换个博客系统的想法了，核心原因是我在 Hexo Next 的这个主题上做了太多侵入式修改，导致其很难再更新了。其目前也有一些问题，比如在手机上适配不太好。我也不想再大动它了，不如重接重新开始，换个博客系统。

但这不足以推动我去换，因为还能用。博客，写才是关键，博客系统能用就行。

但现在契机它来了——我租的阿里云 1H2G 服务器到期了，续租一年近 1500。有点过于离谱了。

我只好重新弄一个新服务器，需要搬迁。那就顺手把博客系统换一下吧。

Hugo 是个好博客系统，我一开始其实没意识到它为什么好，只是见其 Star 多便选用它。

## 流程

### Hugo 初始化

Hugo + PaperMod，官方指导很清晰，直接用。

### 基本配置

配置站名、网址、网站图标等等，参考 PaperMod 文档配置。

### 搜索功能

PaperMod 文档有指导。

### 备案信息

放在页脚，修改配置文件中 `copyright` 即可。

### 友链和关于

这两个页面是以前自定义的页面，直接拷过来，放 `content` 目录下。并在 Hugo 配置中配置即可。

```
content/
├── about.md
└── friends.md
```

```yaml
menu:
  main:
    - name: "友链"
      url: friends/
      weight: 5
      pre: <i class="fa fa-users fa-fw"></i>
    - name: "关于"
      url: about/
      weight: 6
      pre: <i class="fa fa-user fa-fw"></i>
```

需注意，在 Metadata 中添加 `layout = "single"`，让其使用 `single.html` 模板，否则后续的评论系统无法加载。

### 修复文章软链、图片软链和 FontAwesome 图标

#### 文章软链

形如 `https://www.vksir.zone/posts/onmyzsh` 的软链，在 Hugo 中无法直接使用，因 Hugo 生成文章的 URL 和 Hexo 不同。

对于这一点，在 Hexo 中，定义 Metadata：

```yaml
title: 【优质工具】Oh My Zsh 终端
id: onmyzsh
```

在 Hugo 中，定义如下即可：

```yaml
title: 【优质工具】Oh My Zsh 终端
url: posts/onmyzsh
```

保持向前兼容。该变更使用 Python 脚本完成。

#### 图片软链

大批量图片放在阿里 OSS 中，链接不用动。如果要更新博客域名，需要放开白名单，参考[阿里 OSS 访问图片 403](https://www.vksir.zone/posts/oss/)。不过我不打算换网址，也就不用了。

少批量图片放在曾经的 Gallery 图床中，图床服务因几次搬迁服务器停用了，图片没法访问了。均手动上传到 OSS 中，更新链接。量比较少，还不算痛苦。

#### FontAwesome 图标

Hexo 中大量使用 [Font Awesome](https://fontawesome.com/) 图标，挺漂亮的，一些文章里我也加了图标。换了 PaperMod，也加了图标。一方面为了让以前文章中的图标能显示，一方面也在 PaperMod 一些地方加上了图标。

### 不蒜子计数

![image-20250511051143285](https://static.vksir.zone/img/image-20250511051143285.png)

虽然只有 3w 访客、4w 访问量。但是无法舍弃。

参考大好人的配置[不蒜子 | 不如](http://ibruce.info/2015/04/04/busuanzi/)。

### CI/CD

现在貌似都不太需要手写了，Github Marketplace 里找找。核心需求就是 Hugo Build 及 Rclone Deploy。很快就找到两个比较优秀的项目。

稍作修改调整就可以用了。

#### Hugo Build

非常直接，直接用。

```yaml
  - name: Setup Hugo
    uses: peaceiris/actions-hugo@v3
    with:
      hugo-version: '0.147.2'
      extended: true

  - name: Build
    run: |
      cd ${{ github.workspace }}/hugo
      hugo --minify
```

#### Rclone Deploy

Rclone 也是个非常优秀的项目，以前还不知道。

```yaml
  - name: Setup Rclone
    uses: AnimMouse/setup-rclone@v1
    with:
      rclone_config: ${{ secrets.RCLONE_CONFIG }}   # From base64 -w 0 rclone.conf
  - name: Deploy
    run: |
      cd ${{ github.workspace }}
      rclone sync ./hugo/public/ vksir_zone:/opt/www/
```

Github Action 配置文件没什么特别的，但 `secrets.RCLONE_CONFIG` 的生成踩了些坑。

```
rclone config
```

按照 Rclone 的交互式命令一步步生成，因为我是用 root 用户生成的，所以默认使用 root 用户进行 sftp。可能是用户相同，Rclone 配置文件中的 `user` 字段被省略了。

到了 Github 的编包机中，用户不再是 root，就会使用其它用户进行 sftp，就登不上了。

注意在 Rclone 配置文件中添加 `user`，形如：

```
[vksir_zone]
type = sftp
host = vksir.zone
key_pem = 
shell_type = unix
md5sum_command = md5sum
sha1sum_command = sha1sum
user = root
```

后续再 base64 加密放到 Github Repo 的 `secret` 中就行。

### 代理静态文件

#### 域名解析

先进行域名解析：

- `www.vksir.zone` 解析 A 记录到新服务器 IP。
- `vksir.zone` 解析 CNAME 记录到 `www.vksir.zone`。

#### 配置 Caddy

这次不打算使用 Nginx 了，没必要。

```
apt install caddy
```

清空原配置文件 `/etc/caddy/Caddyfile`，添加以下内容：

```
import /etc/caddy/conf.d/*
```

创建配置，

```
mkdir -p /etc/caddy/conf.d/
echo "https://www.vksir.zone {
        root * /opt/www/
        file_server
}
https://vksir.zone {
        redir https://www.vksir.zone{uri} permanent
}" > /etc/caddy/conf.d/www
```

将 `vksir.zone` 永久重定向到 `www.vksir.zone`，而 Caddy 会自动帮我们申请证书，并且将 HTTP 重定向到 HTTPS。

非常省心。

重启生效，

```
systemctl restart caddy
```

检查是否生效，

```
curl https://www.vksir.zone -v
```

至此，大功告成。

## 再见 Hexo

![image-20250511051103644](https://static.vksir.zone/img/image-20250511051103644.png)

左上角灰色是非常漂亮的一张图，可惜定义在 Next 主题中，不好修复

![image-bei_ying.md.jpg](https://static.vksir.zone/img/bei_ying.md.jpg)
