---
title: float 运算精度
comments: false
id: float
categories:
  - 编程语言
tags:
  - python
  - float
date: 2021-08-07 15:10:04
---

如果有一天，有人告诉你三个 0.1 加起来不等于 0.3 你会不会觉得很惊讶？但事实如此：

```python
>>> 0.1 + 0.1 + 0.1 == 0.3
False
```

这是为什么呢？这就涉及到了**浮点运算的精度问题**。

<!-- more -->

## Why

计算机一般以二进制存储数据。在十进制里，0.1 是个精确值，但在二进制里，0.1 是一个无限循环小数：

```python
a = 0.1
print('0.', end='')
for _ in range(50):
    a *= 2
    print(int(a // 1), end='')
    a -= a // 1
```

```
0.00011001100110011001100110011001100110011001100110
```

所以从存入的那一刻，其数值就已经从精确值变为了不定值。

在某些需要精确计算的场合，这非常致命。

## How

如何解决？

其一是使用 decimal 模块，这里也仅介绍 decimal 模块，在我看来，它几乎满足所有要求。

## decimal

> Decimal is based on a floating-point model which was designed with people in mind.

它模仿人类十进制计算方法进行计算：

- 绝对精确：0.1 + 0.1 + 0.1 = 0.3
- 有效位保留：0.30 * 0.200 = 0.06000
- 四舍五入

### Decimal

```python
class decimal.Decimal(value="0", context=None)
```

**value**

可以是整数、字符串、浮点数等。

```python
>>> Decimal(1)	# 一般用于表示大数字
Decimal(1)
>>> Decimal('0.1')	# 用于精确表示浮点数
Decimal('0.1')
>>> Decimal(0.1)	# 一般无用
Decimal('0.1000000000000000055511151231257827021181583404541015625')

>>> Decimal('inf')
>>> Decimal('-inf')
```

**context**

context 翻译为上下文对象，详见 [wiki](https://docs.python.org/zh-cn/3/library/decimal.html#module-decimal)。

### getContext()

```python
# 设置运算精度
getContext().prec = 1024

# 设置四舍五入(默认是舍入到最接近的数，同样接近则舍入到最接近的偶数。)
getContext().rounding = decimal.ROUND_HALF_UP
```

> 目前来说一般用于算法题中……有的需要进行大数字计算，或者是高精度比较相等之类的，就可以用到 decimal。