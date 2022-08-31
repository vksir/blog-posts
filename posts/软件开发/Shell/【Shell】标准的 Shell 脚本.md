---
categories:
- 软件开发
date: 2022-09-01 00:14:50.095011
id: shell
tags:
- shell
- 软件开发
title: 【Shell】标准的 Shell 脚本
---

记录一下 shell 脚本模板。

```shell
#!/usr/bin/bash

args_num=$#
action="${1}"
allowed_action_args=("set" "unset" "test")


function print_ok() {
    local msg="${1}"
    echo "${msg}"
}

function print_err() {
    local msg="${1}"
    echo "${msg}" > /dev/stderr
}

function contain() {
    local list="${1}"
    local ele="${2}"
    for i in ${list[*]};
    do
        if [ "${ele}" == "${i}" ]; then
            return 0
        fi
    done
    return 1
}

function check_args_num() {
    if [ ${args_num} != 1 ]; then
        print_err "Wrong args num"
        return 1
    fi
}

function check_action_arg() {
    if ! contain "${allowed_action_args[*]}" "${action}"; then
        echo "Action arg must be [ set || unset || test ]"
        return 1
    fi
}

function set_proxy () {
    export ALL_PROXY=http://www.vksir.zone
    print_ok "Set proxy success"
}

function unset_proxy() {
    unset ALL_PROXY
    print_ok "Unset proxy success"
}

function test_proxy() {
    if curl -k https://www.google.com --connect-timeout 3 >/dev/null 2>&1; then
        print_ok "Proxy is available"
    else
        print_err "Proxy is not available"
    fi
}


if ! check_args_num; then
    return 1
fi
if ! check_action_arg; then
    return 1
fi

if [ "${action}" == "set" ]; then
    set_proxy
elif [ "${action}" == "unset" ]; then
    unset_proxy
elif [ "${action}" == "test" ]; then
    test_proxy
fi
```

<!-- more -->

```
source proxy set
source proxy unset
source proxy test
```

注意，这里如果想写 source 脚本，那就不能使用 exit，否则会使 ssh 会话退出。
