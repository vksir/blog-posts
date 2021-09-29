---
title: FFmpeg 视频处理工具
comments: false
id: ffmpeg
categories:
  - 良工尽用
tags:
  - 视频处理
  - 工具
date: 2020-03-06 22:58:30
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

<!-- more -->

## 安装

使用第三方源安装比较简单，但是安装的版本非常低，不推荐。

```bash
# 使用第三方源安装
yum install epel-release
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
yum install ffmpeg -y

# 安装官方静态构建
# 创建安装目录
mkdir /usr/local/ffmpeg -p && cd /usr/local/ffmpeg
# 下载
wget -O ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
# tar.xz 文件解压
xz -d ffmpeg.tar.xz
tar -xvf ffmpeg.tar
# 让目录更美观
mv ffmpeg-4.2.2-amd64-static/* ./ && rm -r ffmpeg-4.2.2-amd64-static
# 建立软链接
ln -s /usr/local/ffmpeg/ffmpeg /usr/local/bin
ln -s /usr/local/ffmpeg/ffprobe /usr/local/bin

# 查看版本
ffmpeg -version
```

在解压命令中：

- -d：解压
- -x：extract——解压
- -v：verbose——显示指令执行过程
- -f：file——指定文件

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

## 常用场景

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

### 音视频提取

```bash
# 提取音频
ffmpeg -i name.mp4 -c:a copy -vn output.aac
# 提取视频
ffmpeg -i name.mp4 -c:v copy -an output.mp4
```

## 进阶使用

视频处理可是个耗时的活儿，轻轻松松 CPU 飙升 100%，还要运行好几个小时。我们不可能一直 ssh 连接着服务器，这时候就需要后台运行了。

```bash
# 后台运行
nohup <command> &
# 以较低优先级后台运行
nice nohup <command> &
# 查看输出流
tail -f nohup.out
# 停止后台运行
ps -aux | grep ffmpeg
kill -9 <PID>
```