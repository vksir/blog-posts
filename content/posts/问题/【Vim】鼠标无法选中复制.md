---
categories:
- 问题
date: 2025-05-12 01:59:25.810375
draft: false
id: vim_mouse
tags:
- 问题
title: Vim / 鼠标无法选中复制
url: posts/vim_mouse
---

![image-20250512015149010](https://static.vksir.zone/img/image-20250512015149010.png)

问题出现在 Manjaro 上，vim 打开文件，鼠标选中后仍然是箭头形状，无法复制。

## 临时解决

按 `:`，再输入以下指令回车即可，

```
set mouse-=a
```

## 永久解决

在 `/etc/vimrc` 中配置 `set mouse-=a`，不生效。

执行 `vim -V` 打开文件，观察读取配置文件的顺序，

```
[vksir-swiftsf51451 ~]# vim -V 1.py 2>&1 | grep 继续
在 /etc/vimrc 中继续
在 /usr/share/vim/vim91/defaults.vim 中继续
在 /usr/share/vim/vim91/defaults.vim 中继续
在 /usr/share/vim/vim91/defaults.vim 中继续
在 /usr/share/vim/vim91/syntax/syncolor.vim 中继续
在 /usr/share/vim/vim91/syntax/synload.vim 中继续
在 /usr/share/vim/vim91/syntax/syntax.vim 中继续
在 /usr/share/vim/vim91/defaults.vim 中继续
请按 ENTER 或其它命令继续
```

最后读取了 `/usr/share/vim/vim91/defaults.vim`，在该文件末尾加上 `set mouse-=a` 生效。

## 写在后面

如此可知 `/etc/vimrc` 中配置不生效的原因可能是被后续配置覆盖了，在 `/usr/share/vim/vim91/defaults.vim` 中配置也不太好，可能升级 vim 该配置就丢失了。

但，我也懒得花时间研究了。
