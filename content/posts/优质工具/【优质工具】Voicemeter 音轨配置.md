---
categories:
- 优质工具
date: 2025-05-12 01:12:41.078740
draft: false
id: voicemeter
tags:
- 优质工具
title: 优质工具 / Voicemeter 音轨配置
url: posts/voicemeter
---

## 基本用法

Voicemeter 功能非常强大，我仅使用其冰山一角。

![image-20250125173757-9j5a3lm](https://static.vksir.zone/img/image-20250125173757-9j5a3lm.png)

### 录制

跟着绿色箭头：

1. 点击 Stereo Input 1，选择硬件麦克风，麦克风录音从这里输入 Voicemeter
2. 点亮 B3，麦克风录音从 B3 音轨走
3. 看最右侧 B3，麦克风录音在这里调音，最终从 Voicemeeter Out B3 设备送入操作系统。

![image-20250511230926945](https://static.vksir.zone/img/image-20250511230926945.png)

### 播放

![image-20250511231136442](https://static.vksir.zone/img/image-20250511231136442.png)

跟着红色箭头：

1. 在操作系统中选择 Voicemeeter VAIO3 Input 设备，媒体声音（比如游戏声音）从该设备送入 Voicemeter
2. 点亮 A1，媒体声音从 A1音轨走
3. 点击 A1，选择硬件扬声器，放出声音

理一下：

- 录制：硬件麦克风 > B3 > 虚拟麦克风 Voicemeeter Out B3 > 操作系统录制
- 播放：操作系统播放 > 虚拟扬声器 Voicemeeter VAIO3 Input > A1 > 硬件耳机

很清晰了。

## 使用场景 1

快捷在耳机和扬声器间切换，或者想将声音在多个播放设备中同时播放

![image-20250511231826788](https://static.vksir.zone/img/image-20250511231826788.png)

1. A1 选择硬件耳机，A2 选择硬件扬声器
2. Voicemeeter VAIO3 Input 虚拟扬声器同时勾选 A1、A2 轨道

如此，媒体声音将从虚拟扬声器进入Voicemeter，复制两份，同时走 A1、A2 硬件，这时只有有选择的将其中某个扬声器禁音即可。

## 使用场景 2

边直播，边和队友连麦，

- 录制：希望直接能录入游戏声音、自己人声，但不录入队友声音
- 播放：希望同时听见游戏声音和队友声音

从需求角度翻译一下，

1. 耳机：游戏播放 + 连麦软件播放
2. 录制软件：游戏播放 + 麦克风录制
3. 连麦软件：麦克风录制

![image-20250512010306197](https://static.vksir.zone/img/image-20250512010306197.png)

理清楚了，如何配置？

**Voicemeter:**

如上图

**操作系统：**

1. 默认输入设备，选虚拟麦克风 Voicemeeter Out B3
2. 默认输出设备，选虚拟扬声器 Voicemeeter VAIO3 Input

**软件：**

1. 游戏软件，使用默认输出设备
2. 录制软件，麦克风录音选默认输入设备，桌面音频录音选默认输出设备
3. 连麦软件，录音选虚拟麦克风 Voicemeeter Out B2，播放选虚拟扬声器 Voicemeeter AUX Input
