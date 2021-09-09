---
title: Subprocess——Python 标准子进程管理模块
comments: true
id: subprocess
categories:
  - 编程语言
tags:
  - python
  - shell
date: 2021-08-7 12:56:59
---

> 非常强大的子进程管理模块，你想要的它都有。
>
> 环境：Windows 10

上一篇文章讲的 Pexpect，功能是不错，但它有的 Subprocess 都能做到，且更加完美。

一个好的子进程管理需要满足什么功能需求？

- 无阻塞 / 阻塞
- 标准输入 / 输出
- 信号发送 / kill

其实也不多。

## 开始

```python
import subprocess
proc = subprocess.Popen('ping 127.0.0.1', shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        stdin=subprocess.PIPE)
print(proc.stdout.read().decode('gbk'))	# 因为是 windows 系统，默认编码是 ‘gbk’
```

```
正在 Ping 127.0.0.1 具有 32 字节的数据:
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
127.0.0.1 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 0ms，最长 = 0ms，平均 = 0ms
```

<!-- more -->

subprocess 主要有两个运行命令的方法：

- subprocess.run：阻塞，运行时传入输入，运行结束返回输出；
- `subprocess.Popen`：无阻塞，是 `subprocess.run` 的底层实现，拥有一切功能。

## Popen()

```python
class subprocess.Popen(args, bufsize=-1, executable=None, 
                       stdin=None, stdout=None, stderr=None, 
                       preexec_fn=None, close_fds=True, shell=False, 
                       cwd=None, env=None, universal_newlines=None, 
                       startupinfo=None, creationflags=0, restore_signals=True, 
                       start_new_session=False, pass_fds=(), *, group=None, 
                       extra_groups=None, user=None, umask=-1, encoding=None, 
                       errors=None, text=None)
```

可以看到，参数非常之多，但我们一般关注其中几个足矣。

**args & shell**

args 为子进程命令，默认只能是字符串列表。shell 默认 False，为 True 代表着使用环境变量中默认 shell 来执行 args，这种情况下，可以传入字符串 args。

```python
Popen(['git', 'commit', '-m', 'Fixes a bug.'])
Popen('git commit -m Fixs a bug.', shell=True)
```

`shell=True` 其实是有较大安全隐患的，容易导致命令注入，参考 [安全考量](https://docs.python.org/zh-cn/3/library/subprocess.html?highlight=subprocess#security-considerations)。作为替代，可以使用 shlex：

```python
from shlex import split
cmd = 'git commit -m Fixs a bug.'
Popen(split(cmd), shell=False)
```

> 并且，如果 shell=True，那么后续是无法使用 `proc.kill()` 或者是 `proc.send_signal(2)` 去主动结束子进程，目前并不清楚为什么，wiki 上也并没有提到这一点，但 kill 子进程无效。

**stdin & stdout & stderr**

标准输入 \ 输出 \ 错误。合法的值有 `None`（默认）， `subprocess.PIPE`，`subprocess.DEVNULL`，`subprocess.STDOUT`，[文件对象](https://docs.python.org/zh-cn/3/glossary.html#term-file-object)。

- `None`：子进程直接输出到终端，且可直接输入命令到子进程，但 Popen 仍然是无阻塞的；
- `PIPE`：数据传入管道，可读写；
- `DEVNULL`：数据丢弃；
- `STDOUT`：一般 `stderr=STDOUT`，用来将标准错误重定向到标准输出。

默认 I/O 流为字节流，需要进行编码、解码。

```python
proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

# 同向子进程输入 msg
proc.stdin.write(msg.encode())
# 读取子进程输出
msg = proc.stdout.readline().decode()
msg = proc.stdout.read().decoude()
```

需要注意的是，不管是 `stdout.readline` 还是 `stdout.read` 都是阻塞的。详细及无阻塞见下文。

**bufsize & encoding**

如果设置 `encoding='utf-8'`，则 I/O 字节流以 utf-8 编码形式打开，变为字符流。

```python
proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
proc.stdin.write(msg)
msg = proc.stdout.read()
```

bufsize 参数有四类：

- 0：表示不使用缓冲区；
- 1：表示行缓冲（只有字符流形式打开的情况下才有用）；
- 任何其他正值：表示使用一个约为对应大小的缓冲区；
- -1（默认）：表示使用系统默认的缓冲区大小。

如果发现输入或输出没反应，可以检查一下是否是缓冲区的问题。

```python
# 即时读取缓冲区
proc.stdin.flush()
proc.stdout.flush()
```

> 但经测试，如果是使用管道 PIPE，那么无论如何，stdout 的内容总能第一时间被读取，而 stdin 的内容并不会即时被写入，需要设置缓冲区，或者是 `stdin.write(msg)` 之后就执行 `stdin.flush()`。

**cwd**

子进程执行时的工作目录。

```python
# 寻址还是从当前目录寻址，并不会从工作目录寻址。如下，是找不到 bash 的。
proc = Popen('bash', cwd='/usr/bin/bash')
```

## Popen 对象

Popen 对象有挺多方法的，可以直接参照 [wiki](https://docs.python.org/zh-cn/3/library/subprocess.html?highlight=subprocess#popen-objects)。

需要注意的是，`Popen.communicate()` 只能执行一次，若要多次执行还得直接操作 `stdin & stdout`。

## 标准输入 / 输出

### Demo

一个 Demo，无阻塞调用子进程，读取其输出，向其输入，再次读取其输出。

编辑两个文件，并执行。

```python
# main.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT


proc = Popen('py ./sub.py', shell=True, encoding='utf-8',
             stdin=PIPE, stdout=PIPE, stderr=STDOUT)

for _ in range(5):
    print(proc.stdout.readline(), end='')

proc.stdin.write('Hello Sub.\n')	# 需要 \n，不然输出无法上屏
proc.stdin.flush()	# 上屏后其实存储在缓冲区，需要刷新
print(proc.stdout.readline(), end='')
```

```python
# sub.py
from time import sleep


def log(s: str):
    print('[Sub] ' + s)


for i in range(5):
    log('Msg ' + str(i))
    sleep(0.5)

user_in = input()
log('I received: ' + user_in)
```

```
[Sub] Msg 0
[Sub] Msg 1
[Sub] Msg 2
[Sub] Msg 3
[Sub] Msg 4
[Sub] I received: Hello Sub.
```

上文是使用了 flush，还可以设置 bufsize 为行缓冲，这样无需主动刷新。

```python
# main2.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT


proc = Popen('py ./sub.py', shell=True, encoding='utf-8', bufsize=1,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT)

for _ in range(5):
    print(proc.stdout.readline(), end='')

proc.stdin.write('Hello Sub.\n')
print(proc.stdout.readline(), end='')
```

### 无阻塞读取

上面的例子运行时就可以看出，readline 是阻塞的，只有读取到了 \n 才会输出，否则就会阻塞。而 read 更绝，只有待到子进程执行完毕，才会输出，否则阻塞。在大多数情况下，这是没什么问题的，但有的子进程——比如游戏服务器，并不会执行完毕，一旦开启会持续打印日志，这时候就需要无阻塞读取了。

大约有四类思路：

#### 线程 & 异步

大可开一个线程专门对 PIPE 进行阻塞读取，内容存储到 Queue 中，主进程再从 Queue 中获取信息。而从队列中获取信息可以是无阻塞的。异步同理。

```python
# main3.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from queue import Queue, Empty
from threading import Thread


def func(proc: Popen, que: Queue):
    while True:
        msg = proc.stdout.readline()
        que.put(msg)


proc = Popen('py ./sub2.py', shell=True, encoding='utf-8', bufsize=1,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT)

msg_que = Queue()
th1 = Thread(target=func, args=(proc, msg_que), daemon=True)
th1.start()

while proc.poll() is None:
    sleep(0.2)

    try:
        print(msg_que.get(block=False), end='')
    except Empty:
        print('[Main] Noting get.')
```

这里创建一个新的 sub 文件，简化一点。

```python
# sub2.py
from time import sleep


def log(s: str):
    print('[Sub] ' + s)


for i in range(5):
    log('Msg ' + str(i))
    sleep(0.5)
```

```
[Sub] Msg 0
[Main] Noting get.
[Main] Noting get.
[Sub] Msg 1
[Main] Noting get.
[Sub] Msg 2
[Main] Noting get.
[Main] Noting get.
[Sub] Msg 3
[Main] Noting get.
[Sub] Msg 4
[Main] Noting get.
[Main] Noting get.
```

#### 文件对象

```python
with open(path, 'r') as fd:
    ...
```

如上，fd 是个文件对象，且是以文本形式打开文件，是个文本 I/O，也即是 `io.TextIOBase`，详见 [wiki](https://docs.python.org/zh-cn/3/library/io.html?highlight=read#io.TextIOBase)。其有两个读取方法，wiki 中如下写到：

- read(*size=-1*)

	从流中读取至多 *size* 个字符并以单个 str 的形式返回。 如果 size 为负值或 None，则读取至 EOF。

- readline(*size=-1*)

	读取至换行符或 EOF 并返回单个 str。 如果流已经到达 EOF，则将返回一个空字符串。如果指定了 *size* ，最多将读取 *size* 个字符。

从介绍上看，它们也是阻塞的，但是实际上……

```python
# main4.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT

fd_w = open('./sub2.log', 'w')
fd_r = open('./sub2.log', 'r')

proc = Popen('py ./sub2.py', shell=True, encoding='utf-8', bufsize=1,
             stdin=PIPE, stdout=fd_w, stderr=STDOUT)

while proc.poll() is None:
    sleep(0.2)

    msg = fd_r.readline()
    if msg:
        print(msg, end='')
    else:
        print('[Main] Noting get.')

fd_w.close()
fd_r.close()
```

```
[Sub] Msg 0
[Main] Noting get.
[Main] Noting get.
[Sub] Msg 1
[Main] Noting get.
[Sub] Msg 2
[Main] Noting get.
[Main] Noting get.
[Sub] Msg 3
[Main] Noting get.
[Sub] Msg 4
[Main] Noting get.
[Main] Noting get.
[Main] Noting get.
```

readline 和 read 表示出来的都是无阻塞的。这里可以大胆猜测，每次 read 时候，读到了文件结尾，遇上了 EOF 所以直接返回了空字符串。虽然子进程没有结束，但是它的输出被定向到文件中，文件末尾永远是 EOF，所以我们每次能都 read 到内容，至少能读到 EOF。——这也造就了它们的无阻塞。

如果是直接 PIPE 中 read，因为子进程没有结束，PIPE 末尾是不会有 EOF 的，所以阻塞了。

利用文件这个特性，就可以实现无阻塞读取了。

还有个反例：

```python
# main5.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT


proc = Popen('py ./sub2.py', shell=True, encoding='utf-8', bufsize=1,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT)

with open(proc.stdout.fileno(), 'r') as fd:
    while proc.poll() is None:
        sleep(0.2)

        msg = fd.readline()
        if msg:
            print(msg, end='')
        else:
            print('[Main] Noting get.')
```

```
[Sub] Msg 0
[Sub] Msg 1
[Sub] Msg 2
[Sub] Msg 3
[Sub] Msg 4
[Main] Noting get.
[Main] Noting get.
```

如上，同样是 `io.TextIOBase.readline()` ，却是阻塞的。因为它不是文件，末尾不是 EOF。

#### select

个人感觉 select 是个比较重要的东西，后面专门写一篇文吧。

#### fcntl

仅在 Unix 类系统上可用，可直接将 stdout 设置为无阻塞。暂时不太想多了解它，其功能也是非常强大的。

> 文章纯摸着石头过河，有误欢迎指正。
>
> 参考文档：
>
> [1] https://docs.python.org/zh-cn/3/library/subprocess.html?highlight=subprocess#popen-objects
>
> [2] https://www.orcode.com/question/55018_k2a152.html
