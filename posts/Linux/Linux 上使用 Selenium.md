---
title: Linux 上使用 Selenium
comments: false
id: selenium
categories:
  - Linux 小记
tags:
  - Linux
  - 爬虫
date: 2021-07-12 23:04:47
---

> 环境：CentOS 7，无界面

## 安装 Chrome

```sh
# 直接从网络安装 rpm 包
yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# 查看版本
google-chrome -version
```

```sh
Google Chrome 83.0.4103.97
```

<!-- more -->

## 安装 chromedriver

[chromedriver 淘宝镜像网站](http://npm.taobao.org/mirrors/chromedriver/)

```sh
# 下载对应的版本
wget http://npm.taobao.org/mirrors/chromedriver/83.0.4103.39/chromedriver_linux64.zip

# 解压并移动到默认应用目录
x chromedriver_linux64.zip
mv ./chromedriver_linux64/chromedriver /usr/local/bin
```

## 安装虚拟桌面

因为是无界面系统，所以直接运行 selenium 是会报错的，需要先开启虚拟桌面。

```sh
pip install pyvirtualdisplay
yum install xorg-x11-server-Xvfb
```

尝试运行，会出现警告：

```python
# python3
from pyvirtualdisplay import Display
display = Display()
```

```sh
xdpyinfo was not found, X start can not be checked! Please install xdpyinfo!
```

忽略警告也能正常运行，为了消除警告：

```sh
yum install xdpyinfo
```

## 测试

```python
# python3

from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1280, 720))
display.start()

options = webdriver.ChromeOptions()

# 允许 root 运行
options.add_argument('--no-sandbox')

# 不加载图片
prefs = {"profile.managed_default_content_settings.images":2}
options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=options)

# 设置窗口大小（有的网站，小窗口会显示手机版网页）
driver.set_window_size(1280, 720)

driver.get('https://www.baidu.com')
print(driver.page_source)

# 关闭虚拟桌面和 selenium
selenium.quit()
display.stop()
```

## 封装成类

如上操作，每次都需要关闭一系列资源的，可以使用 Python 的 `with` 进行封装。

```python
from selenium import webdriver
from pyvirtualdisplay import Display
import os

class WebDriver(object):
    def __init__(self):		# 创建时运行
        self.__os_name = os.name

    def __enter__(self):	# 创建后时运行
        if self.__os_name == 'nt':	# Windows 系统
            option = webdriver.ChromeOptions()
            # option.add_experimental_option('excludeSwitches', ['enable-automation'])
            # option.set_headless()
            self.__driver = webdriver.Chrome(executable_path='chromedriver', options=option)
        elif self.__os_name == 'posix':	# Linux 系统
            self.__display = Display(visible=0, size=(1280, 720))
            self.__display.start()
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(options=options)
            self.__driver.set_window_size(1280, 720)
        return self.__driver

    def __exit__(self, exc_type, exc_val, exc_tb):	# 脱离 with 后运行
        self.__driver.quit()
        if self.__os_name == 'posix':
            self.__display.stop()

if __name__ == '__main__':
    from time import sleep
    with WebDriver() as d:
        d.get('https://www.baidu.com/s?wd=ip')
        sleep(5)
    sleep(5000)
```

