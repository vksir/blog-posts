---
categories:
- 优质工具
date: 2020-03-06 22:58:30
draft: false
id: ffmpeg
tags:
- 优质工具
- 视频处理
title: 优质工具 / FFmpeg 音视频处理
url: posts/ffmpeg
---

> FFmpeg——一款极其优秀的视频处理工具
>
> 优点：
>
> - 全平台支持：Linux、Windows、Mac
> - 参数众多，符合你对于视频处理的各种要求。如常用的 **视频压缩**、**格式转化**、**音视频提取**，都是手到擒来。
> - 性能强悍
>
> 缺点：
>
> - 纯命令行工具，受众注定不会大
> - 参数实在太多，五花八门，有点摸不着头脑
>
> 环境：CentOS 7
>
> 需求：None

## 常用参数

```bash
-i 设定输出流
-f 设定输出格式

-b:v 设定平均码率
-r 设定帧数
-S 设定分辨率

-crf 设定视频质量（18-28为佳，0无损，51最低）
-preset 设定转换速度 （ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo(不建议))

-vn 不处理视频
-an 不处理音频
-c:v 设定视频解码器（libx264, libx265(H265虽然好，但是很多地方不支持)）
-c:a 设定音频解码器（copy——直接复制原音频）

-maxrate 设定最大码率
-minrate 设定最小码率
-bufsize 设定缓冲
```

是不是感觉很麻烦呢？这才是其中一点点参数呢，`ffmpeg -h` 查看所有参数！

不过没关系，日常使用根本不用了解那么多~

## 视频处理

### 视频压缩

```bash
# 网站投稿 -> 快速压缩
ffmpeg -i name.mp4 -s 1920x1080 -preset veryfast -crf 28 -c:v libx264 -c:a copy -f mp4 output.mp4 -y
# 视频存放 -> 压缩体积
ffmpeg -i name.mp4 -s 1280x720 -b:v 1024k -preset veryslow -c:v libx265 -f mp4 output.mp4 -y
```

- -y：表示不用确认，直接覆盖视频

### 格式转换

```bash
# mp4 转 flv
ffmpeg -i name.mp4 output.flv -y
```

### 编码格式转换

```shell
# 查看支持的编码格式
ffmpeg -codecs

# av1 转 h264
ffmpeg -c:v av1_cuvid -i input.mp4 -crf 18 -c:v libx264 output.mp4 -y
```

其中，解码器用的 N 卡的解码器 `av1_cuvid`，编码器用 CPU 编码 `libx264`。
### 视频截取

```shell
# 从 20:40 开始，截取 15s
ffmpeg -ss 20:40 -t 15 -i input.mp4 -c:v copy output.mp4 -y
```

### 音视频提取

```bash
# 提取音频
ffmpeg -i name.mp4 -c:a copy -vn output.aac
# 提取视频
ffmpeg -i name.mp4 -c:v copy -an output.mp4
```

## 音频处理

### flac 转 mp3

```
ffmpeg -i "1.flac" -ab 320k -map_metadata 0 -id3v2_version 3 "1.mp3"
```
