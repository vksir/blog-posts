---
categories:
- 软件开发
date: 2022-05-30 02:06:27.709834
draft: false
id: go_log
tags:
- go
- log
- 软件开发
title: 【Go】实现分级日志
url: posts/go_log
---

话不多说直接上代码：

```go
package log

import (
	"errors"
	"fmt"
	"log"
	"os"
)

const (
	LevelDebug = (1 + iota) * 10
	LevelInfo
	LevelWaring
	LevelError
	LevelCritical
)

var debugLogger *log.Logger
var debugFileLogger *log.Logger
var infoLogger *log.Logger
var infoFileLogger *log.Logger
var warningLogger *log.Logger
var warningFileLogger *log.Logger
var errorLogger *log.Logger
var errorFileLogger *log.Logger
var criticalLogger *log.Logger
var criticalFileLogger *log.Logger
var flag = log.Ldate | log.Ltime | log.Lshortfile | log.Lmsgprefix
var logLevel = LevelInfo

func SetLevel(level int) error {
	if level != LevelDebug && level != LevelInfo && level != LevelWaring && level != LevelError && level != LevelCritical {
		return errors.New(fmt.Sprintf("invalid level: %d", level))
	} else {
		logLevel = level
		return nil
	}
}

func AddFileOutput(filePath string) error {
	logWriter, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0655)
	if err != nil {
		return err
	} else {
		debugFileLogger = log.New(logWriter, "[DEBUG] ", flag)
		infoFileLogger = log.New(logWriter, "[INFO] ", flag)
		warningFileLogger = log.New(logWriter, "[WARNING] ", flag)
		errorFileLogger = log.New(logWriter, "[ERROR] ", flag)
		criticalFileLogger = log.New(logWriter, "[CRITICAL] ", flag)
		return nil
	}
}

func Debug(format string, v ...any) {
	logWithLevel(debugLogger, LevelDebug, format, v)
	logWithLevel(debugFileLogger, LevelDebug, format, v)
}

func Info(format string, v ...any) {
	logWithLevel(infoLogger, LevelDebug, format, v)
	logWithLevel(infoFileLogger, LevelDebug, format, v)
}

func Waring(format string, v ...any) {
	logWithLevel(warningLogger, LevelDebug, format, v)
	logWithLevel(warningFileLogger, LevelDebug, format, v)
}

func Error(format string, v ...any) {
	logWithLevel(errorLogger, LevelDebug, format, v)
	logWithLevel(errorFileLogger, LevelDebug, format, v)
}

func Critical(format string, v ...any) {
	logWithLevel(criticalLogger, LevelDebug, format, v)
	logWithLevel(criticalFileLogger, LevelDebug, format, v)
}

func init() {
	debugLogger = log.New(os.Stderr, "[DEBUG] ", flag)
	infoLogger = log.New(os.Stderr, "[INFO] ", flag)
	warningLogger = log.New(os.Stderr, "[WARNING] ", flag)
	errorLogger = log.New(os.Stderr, "[ERROR] ", flag)
	criticalLogger = log.New(os.Stderr, "[CRITICAL] ", flag)
}

func logWithLevel(logger *log.Logger, level int, format string, v []any) {
	if logger != nil && logLevel >= level {
		logger.Printf(format, v...)
	}
}
```

<!-- more -->

简单使用如下：

```go
package main

import (
	"GoCode/log"
)

func main() {
	log.AddFileOutput("./log.txt")
	log.Info("Hello, %s", "log")
}
```

```
2022/05/30 02:04:01 log.go:89: [INFO] Hello, log
```
