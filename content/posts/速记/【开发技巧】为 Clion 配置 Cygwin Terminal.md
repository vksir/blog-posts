---
categories:
- 速记
date: 2022-12-17 07:06:20.959438
draft: false
id: clion_cygwin
tags:
- 优质工具
- 速记
title: 【开发技巧】为 Clion 配置 Cygwin Terminal
url: posts/clion_cygwin
---

习惯了使用 Unix 风格的终端，过去在 Windows 上，一直给 Clion 配置 Git Bash 作为终端：

```
"D:\Program Files\Git\bin\sh.exe"
```

但近来发现，在 Git Bash 中运行编译好的 C++ 程序时，有时候会没有回显。Cygwin Terminal 就没这问题，Clion 中配置 Cygwin Terminal 如下：

```
"D:\Dependencies\cygwin64\bin\sh.exe" -lic "cd ${OLDPWD-.}; bash"
```

<!-- more -->

![image-20221217065536808](https://static.vksir.zone/img/image-20221217065536808.png)
