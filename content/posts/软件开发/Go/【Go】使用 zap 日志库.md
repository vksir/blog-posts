---
categories:
- 软件开发
date: 2023-02-08 02:29:21.432264
id: go_zap
tags:
- go
- 软件开发
title: 【Go】使用 zap 日志库
---

## 代码

**loging\logging.go**

```go
package logging

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"os"
)

const logPath = "./log.txt"

func SugaredLogger() *zap.SugaredLogger {
	return zap.S()
}

func init() {
	encoder := getEncoder()
	writeSyncer := getWriteSyncer()
	core := zapcore.NewCore(encoder, writeSyncer, zap.DebugLevel)
	logger := zap.New(core, zap.AddCaller(), zap.AddStacktrace(zap.ErrorLevel))
	zap.ReplaceGlobals(logger)
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	return zapcore.NewConsoleEncoder(encoderConfig)
}

func getWriteSyncer() zapcore.WriteSyncer {
	f, err := os.OpenFile(logPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		panic(err)
	}
	return zapcore.NewMultiWriteSyncer(zapcore.AddSync(f), zapcore.AddSync(os.Stdout))
}
```

<!-- more -->

## 使用

**main.go**

```go
package main

import (
	"GoCode/logging"
)

var log = logging.SugaredLogger()

func main() {
	log.Info("Hello zap")
}

```

```
2023-02-06T01:26:29.514+0800	INFO	GoCode/main.go:11	Hello zap
```
