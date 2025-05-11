---
categories:
- 个人项目
date: 2021-09-29 04:14:04
draft: false
id: stella_dst
tags:
- qq 机器人
- 个人项目
- 饥荒
title: 智能助理——Stella
url: posts/stella_dst
---

> 最近为饥荒群安排了 QQ 机器人 Stella ，并为其搭载了饥荒服务器管理模块，只要 @Stella 发送指令就可以快捷地对服务器进行操作。旨在使饥荒服务器更易于管理，降低操作门槛，让每个人都能参与使用，同时减轻服务器管理者的负担。
>
> 以下，是服务器管理命令的简明文档。

# 须知

- Stella 是 Q 群机器人，发送指令必须先 @Stella，然后输入指令。
- 输入指令必须以 `#` 开头。
- 服务器名见公告，当前只有 **极光** 和 **矮星** 两台服务器搭载了此功能。

<!-- more -->

如：

![image-20210929030359399](https://static.vksir.zone/img/image-20210929030359399.png)

# 通用 API

```
#服务器名 player-list	显示当前在线玩家
#服务器名 mod-list		显示服务器安装的 Mod
```

# 管理员 API

## 基本管理

```
#服务器名 start			启动服务器
#服务器名 stop			关闭服务器
#服务器名 restart		重启服务器（并更新 Mod）
#服务器名 update		更新服务器（指更新服务器版本）
```

## Mod 管理

### 添加 Mod

```
#服务器名 mod-add 参数
```

有两种参数，一种是 ModID，一种是 `modoverrides.lua` 文件内容。

#### ModID

一个或多个 ModID，中间以空格隔开，如下：

![image-20210929032555674](https://static.vksir.zone/img/image-20210929032555674.png)

**ModID 怎么看？**

以全球定位为例，如下图红框中内容。

![image-20210929035033205](https://static.vksir.zone/img/image-20210929035033205.png)

#### `modoverrides.lua` 文件内容

`modoverrides.lua` 文件位于 `Cluster_1/Master/modoverrides.lua`，每个存档都有各自的 Mod 文件。

一只加了 `Show me` 的 Mod 文件，内容如下：

```
return {
-- Show Me
  ["workshop-666155465"]={
    ["configuration_options"]={
      ["chestB"]=-1,
      ["chestG"]=-1,
      ["chestR"]=-1,
      ["food_estimation"]=-1,
      ["food_order"]=0,
      ["food_style"]=0,
      ["lang"]="auto",
      ["show_food_units"]=-1,
      ["show_uses"]=-1 
    },
    ["enabled"]=true 
  }
}
```

![image-20210929034541688](https://static.vksir.zone/img/image-20210929034541688.png)

### 删除 Mod

```
#服务器名 mod-del 参数
```

这里参数只支持 ModID，如下：

![image-20210929035458699](https://static.vksir.zone/img/image-20210929035458699.png)

## 创建新存档

```
#服务器名 create-cluster
```

创建新存档后，原存档会自动备份，不用担心存档丢失。

创建新存档后，一般会查询下 Mod 列表，然后按需增删 Mod。

![image-20210929040103459](https://static.vksir.zone/img/image-20210929040103459.png)

# 关于项目

本项目主要由机器人 Web Server 和饥荒服务器管理器两部分组成，基于 Python Web 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) QQ 机器人框架开发，所以源码以上传至我的 Github。
