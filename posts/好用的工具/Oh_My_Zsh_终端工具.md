---
title: Oh My Zsh 终端工具
comments: false
id: onmyzsh
categories:
  - 良工尽用
tags:
  - 终端
  - 工具
date: 2020-03-06 23:02:54
---

![ys](https://gallery.vksir.zone/images/2020/03/05/-ys.png)

> 一款极其好用的终端工具，简单易上手。
>
> 环境：CentOS 7

<!-- more -->

## 安装

```bash
# 使用 zsh
chsh -s /bin/zsh
# 重启生效
reboot

# 安装 Oh My Zsh
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

有什么好处呢？用了就知道了！

## 主题

第一个好处就是漂亮！

有多少种主题？

```bash
ls ~/.oh-my-zsh/themes
```

太多了，我选 `ys`。

![ys](https://gallery.vksir.zone/images/2020/03/05/-ys.png)

```bash
vim ~/.zshrc
# 修改
ZSH_THEME="ys"
# 重载配置
source ~/.zshrc
```

[pure](https://github.com/sindresorhus/pure) 其实也不错，但是它没有被集成到 `Oh My Zsh` 中，需要额外安装。

![pure](https://gallery.vksir.zone/images/2020/03/05/-pure.png)

```bash
# 下载
mkdir -p "$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"

# 配置
vim ~/.zshrc
# 修改
#ZSH_THEME="ys"		# Em 没错~ 注意把原主题注释掉
fpath+=$HOME/.zsh/pure
autoload -U promptinit; promptinit
prompt pure

#重载配置
source ~/.zshrc
```

## 插件

必装插件：`highlighting` && `autosuggestions`。直接 `CV` 就完事！

```sh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
echo "source $ZSH_CUSTOM/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc
echo "source $ZSH_CUSTOM/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc
source .zshrc
```

选装插件：

- extract：再也不用 `tar -zxvf` 了，直接 `x` 搞定所有！
- autojump：
	- `cd /var/www/hexo`（x）
	- `j hexo`（√）
- themes：快速切换主题

如何装？Just：

```bash
vim ~/.zshrc
# 修改
plugins=(git extract autojump themes)
```

如果要安装 `autojump` 则还需要：

```bash
yum install autojump-zsh
```

然后重载配置：

```bash
source ~/.zshrc
```

> ***Enjoy it !***

> 2020/3/14 更新
>
> 解决安装 autosuggestions 后往终端里粘贴文字变慢的问题：
>
> ```sh
> vim ～.zshrc
> 
> # 添加以下内容
> # This speeds up pasting w/ autosuggest
> # https://github.com/zsh-users/zsh-autosuggestions/issues/238
> pasteinit() {
>   OLD_SELF_INSERT=${${(s.:.)widgets[self-insert]}[2,3]}
>   zle -N self-insert url-quote-magic # I wonder if you'd need `.url-quote-magic`?
> }
>  
> pastefinish() {
>   zle -N self-insert $OLD_SELF_INSERT
> }
> zstyle :bracketed-paste-magic paste-init pasteinit
> zstyle :bracketed-paste-magic paste-finish pastefinish
> 
> # 使其生效
> source .zshrc
> ```