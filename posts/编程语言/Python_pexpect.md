---
title: Pexpect——Python 自动化程序交互模块
comments: false
id: pexpect
categories:
  - 编程语言
tags:
  - python
  - shell
date: 2021-07-27 1:25:04
---

> 相对有名的可用于自动化应用程序交互的模块，可用于 ssh、ftp 等程序。
>
> 环境：Ubuntu 20.04 LTS

最近想做一个游戏服务器管理器，以 Python 为主语言，对 Linux 上的常驻程序进行管理。需要满足：

- 无阻塞启动程序
- 实时读取程序输出
- 实时进行程序输入
- 定时进行程序重启

等功能要求。

要求不是很多，也不是很复杂，但 Pexpect 完成得不是很好。

## 开始

```python
child = pexpect.spawn('ssh uesr@IP')	# 执行命令
child.expect('password:')	# 期待程序输出 'password:'
child.sendline(my_password)	# 向程序输入 my_password
```

<!-- more -->

## spawn()

```python
pexpect.spawn(command, args=[], timeout=30, maxread=2000,
              searchwindowsize=None, logfile=None, cwd=None, env=None,
              ignore_sighup=False, echo=True, preexec_fn=None, encoding=None,
              codec_errors='strict', dimensions=None, use_poll=False)
```

**command**

```python
# 推荐直接使用命令字符串
child = pexpect.spawn('ls -latr /tmp')

# pexpect 不解释 shell 元字符，如重定向、管道或通配符（>，|，*），因此需要如下使用
child = pexpect.spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
```

**timeout**

默认 30s，超时则报错。

**logfile**


> [wiki](https://pexpect.readthedocs.io/en/stable/api/pexpect.html)：
>
> 日志文件成员打开或关闭日志记录。所有输入和输出都将复制到给定的文件对象。将 logfile 设置为 None 以停止记录。这是默认设置。将日志文件设置为 sys.stdout 以将所有内容回显到标准输出。每次写入后都会刷新日志文件。

```python
>>> child = pexpect.spawn('ping 127.0.0.1', logfile=sys.stdout, encoding='utf-8')
# 但是很遗憾，没有任何输出

>>> child.sendline('hello')
hello
6
```

只能打印输入，无法打印输出，显然，wiki 有误。

**cwd**

程序运行环境。需要注意的是，`command` 寻址仍然是从当前路径开始寻址的，并非 `cwd` 所指代的路径。

### expect()

```python
expect(pattern, timeout=-1, searchwindowsize=-1, async_=False, **kw)
```

**pattern**

正则表达式，但并不是非常正则，个人认为该模块最大的坑。

- `$` 行尾匹配的模式是无用的
- 始终进行非贪婪匹配

```python
# 以下将始终只返回一个字符
child.expect('.+')

# 始终不返回任何字符
child.expect('.*')
```

以上是 [wiki](https://pexpect.readthedocs.io/en/stable/overview.html) 里说的，但实际上 `'.+'` 并不是只返回一个字符：

```python
>>> child = pexpect.spawn('ping 127.0.0.1', encoding='utf-8')
>>> child.expect('.+')
0
>>> print(child.after)
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.059 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.053 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.062 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.070 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.074 ms
64 bytes from 127.0.0.1: icmp_seq=6 ttl=64 time=0.057 ms
64 bytes from 127.0.0.1: icmp_seq=7 ttl=64 time=0.057 ms
```

如上，`'.+'` 直接匹配到了行尾，显然，[wiki](https://pexpect.readthedocs.io/en/stable/overview.html) 有误。

但，这样岂不是更好？NO！ 

```python
...
childs[i].expect(r'.+')
stdout = childs[i].before
test = childs[i].readline()
print('stdout: ' + stdout)
print('test: ' + test)
...
```

```
on 0: stdout: 
on 0: test:  breakpad minidump AppID = 322330
```

如上，是我个人开发中一段代码。readline 有输出，表示子程序其实是正常输出了内容的，但 `'.+'` 什么都没有匹配到。但这同样表明 wiki 有误，因为 wiki 可是说会匹配一个字符的。

Github 上有个 [issue](https://github.com/pexpect/pexpect/issues/692)，那位仁兄的测试代码是这样的。

```python
import pexpect
import sys

p = pexpect.spawn("ping 10.192.225.199", encoding="utf-8")
while True:
    try:
        index = p.expect([".+", pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        if index == 0:	
            print("===")
            print(p.after)
            print("===")
    except Exception as e:
        print(e)
```

```
$ python3 test.py
===
PING 10.192.225.199 (10.192.225.199) 56(84) bytes of data.

===
===
64 bytes from 10.192.225.199: icmp_seq=1 ttl=63 time=0.607 ms

===
===
64 bytes from 10.192.225.199: icmp_seq=2 ttl=63 time=0.587 ms

===
...

```

他的结论是「`'.+'` 会匹配到行尾」，显然，他的结论是错的。只是因为 ping 输出是一行行的，而 expect 又太快，所以导致每次匹配的都是刚好一行。但无论他的结论如何，`'.+'` 都有问题，只需静候作者处理 issue 即可。

但，距离该模块上次更新已经 15 个月了。

**timeout**

- `timeout=-1`：默认超时时间
- `timeout=None`：无限期阻塞

#### before & after

### send(s)

发送字符串 `s` 到子程序。用的不是很多。

### sendline(s)

发送字符串 `s + '\n'` 到子程序。一般用这个。

**sendcontrol(s)**

发送控制字符到子程序，如 Ctrl + C、Ctrl + D。

```python
child.sendcontrol('c')	# 一般用于让子程序自动退出
```

### read(size=-1)

读取 size 大小的字节，如果 `size=-1` 则读取直到达到 EOF。如果子程序运行结束，那么当然可以 read 成功，非常完美；但如果子程序会一直运行，一直输出，那么 read 会导致无限期阻塞。

### readline()

读取一行，如果遇到 EOF 则返回空字符串。同样，子程序运行，但不输出，则 readline 也会导致阻塞。

### interact()

进入用户交互模式，效果同直接运行子程序，能够持续看到程序输出，进行手动输入。按 `Ctrl + ]` 退出该模式。

### isalive()

子进程运行则返回 True，否则返回 False。

### wait()

阻塞，等待子进程运行结束。

## 问题

对于开头说的开发的四个需求，并不知道怎么实现「实时读取程序输出」。expect 太怪了，read、readline 都是阻塞的，stdout=file 也不太行，压根儿就不写文件。

> 模块做得不错，但可惜貌似没在更新了。如果在下能读懂其源码，亲自更新修复，那也是相当不错的，可惜尝试过了，并不是很能读懂。
>
> 但后又仔细研究了一番 Python 官方提供的 subprocess，惊然发现它其实能满足我所有需求，不过太晚了，还是明天再写吧。
>
> 记于 2021年7月27日 1:16，工作后第三周周一。
