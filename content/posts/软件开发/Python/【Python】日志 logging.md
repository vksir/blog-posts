---
categories:
- 软件开发
date: 2022-05-08 14:23:55.238289
draft: false
id: logging
tags:
- logging
- python
- 软件开发
title: 【Python】日志 logging
url: posts/logging
---

记录 logging 简单用法。

```python
#!/usr/bin/env python
# coding=utf-8

import time
import logging


LOG_PATH = f'./{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
LOG = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d][%(threadName)s][%(funcName)s] %(message)s')
LOG.setLevel(logging.DEBUG)


def init_log():
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_PATH, 'w', encoding='utf-8')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    LOG.addHandler(sh)
    LOG.addHandler(fh)


init_log()
```

<!-- more -->

更多 `Formatter` 格式配置见 [logging --- Python 的日志记录工具 — Python 3.11.1 文档](https://docs.python.org/zh-cn/3/library/logging.html?highlight=logging formatter#logging.LogRecord)。
