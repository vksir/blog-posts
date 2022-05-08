---
categories:
- 软件开发
date: 2022-05-08 14:23:55.238289
id: logging
tags:
- logging
- python
- 软件开发
title: 【Python】日志 logging
---

记录 logging 简单用法。

***constants.py***

```python
#!/usr/bin/env python
# coding=utf-8

import os
import platform

class FilePath:
    HOME = os.environ['HOME'] if platform.system() == 'Linux' else os.environ['USERPROFILE']
    CFG_DIR = f'{HOME}/.cfg'
    LOG_PATH = f'{CFG_DIR}/log.txt'
```

***log.py***

```python
#!/usr/bin/env python
# coding=utf-8

import os
import logging
from common.constants import FilePath

log = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [%(threadName)s] %(message)s')
log.setLevel(logging.DEBUG)

def init_path():
    for path_name, path in FilePath.__dict__.items():
        if not path_name.endswith('DIR') or os.path.exists(path):
            continue
        os.system(f'mkdir -p {path}')

def init_log():
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(FilePath.LOG_PATH, 'w', encoding='utf-8')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.addHandler(fh)

init_path()
init_log()
```
