---
categories:
- 软件开发
date: 2022-05-08 14:11:01.243103
id: argparse
tags:
- argparse
- python
- 软件开发
title: 【Python】命令行解析器 argparse
---

```python
#!/usr/bin/env python
# coding=utf-8


import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', metavar='<NAME>', required=True)
parser.add_argument('-a', '--age', metavar='<AGE>', required=True, type=int)
args = parser.parse_args()


if __name__ == '__main__':
    print(args)
```

<!-- more -->

```
$ ./script.py -n vksir -a 18
Namespace(age=18, name='vksir')
```
