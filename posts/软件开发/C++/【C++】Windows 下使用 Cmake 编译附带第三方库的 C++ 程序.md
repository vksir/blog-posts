---
categories:
- 软件开发
date: 2022-12-17 07:06:20.994384
id: windows_cmake
tags:
- c++
- 软件开发
title: 【C++】Windows 下使用 Cmake 编译附带第三方库的 C++ 程序
---

## C++ 环境搭建

下载 [Cygwin](https://cygwin.com/) 并安装，选择 Category-Devel，勾选如下 Package：

![image-20221217060145372](https://static.vksir.zone/img/image-20221217060145372.png)

## 开发简单 C++ 项目

打开 Cygwin64 Terminal。

<!-- more -->

```shell
mkdir -p /home/dev/cpp-code && cd /home/dev/cpp-code
```

编辑文件 `/home/dev/cpp-code/main.cpp` 如下：

```c++
#include <fmt/core.h>

int main() {
    fmt::print("Hello World!\n");
}
```

编辑文件 `/home/dev/cpp-code/CMakeLists.txt` 如下：

```cmake
cmake_minimum_required(VERSION 3.23)
project(cpp_code)

set(CMAKE_CXX_STANDARD 14)

include(FetchContent)
FetchContent_Declare(
        fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt.git
        GIT_TAG 9.1.0
)
FetchContent_MakeAvailable(fmt)

add_executable(hello_world main.cpp)
target_link_libraries(hello_world PRIVATE fmt::fmt)
```

这里使用了一个第三方库 [fmt](https://github.com/fmtlib/fmt.git)。

## Cmake 编译

执行以下命令编译：

```shell
cd /home/dev/cpp-code

mkdir build && cd build
cmake ..
make
```

日志打印如下：

```shell
$ cmake ..
-- The C compiler identification is GNU 11.3.0
-- The CXX compiler identification is GNU 11.3.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Module support is disabled.
-- Version: 9.1.0
-- Build type:
-- CXX_STANDARD: 14
-- Performing Test has_std_14_flag
-- Performing Test has_std_14_flag - Success
-- Performing Test has_std_1y_flag
-- Performing Test has_std_1y_flag - Success
-- Required features: cxx_variadic_templates
-- Configuring done
-- Generating done
-- Build files have been written to: /home/dev/cpp-code/build
```

```shell
$ make
[ 20%] Building CXX object _deps/fmt-build/CMakeFiles/fmt.dir/src/format.cc.o
[ 40%] Building CXX object _deps/fmt-build/CMakeFiles/fmt.dir/src/os.cc.o
[ 60%] Linking CXX static library libfmt.a
[ 60%] Built target fmt
[ 80%] Building CXX object CMakeFiles/hello_world.dir/main.cpp.o
[100%] Linking CXX executable hello_world.exe
[100%] Built target hello_world
```

查看编译后的程序，并运行：

```shell
$ ls
_deps  cmake_install.cmake  CMakeCache.txt  CMakeFiles  hello_world.exe  Makefile
$ ./hello_world.exe
Hello World!
```
