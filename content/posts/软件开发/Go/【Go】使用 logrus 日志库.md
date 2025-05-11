---
categories:
- 软件开发
date: 2024-03-13 21:02:16.066699
draft: false
id: logrus
tags:
- go
- 软件开发
title: 【Go】使用 logrus 日志库
url: posts/logrus
---

相比起 zap 日志库，logrus 性能会低一些，但在很多场景，并不需要太高性能，而 logrus 库的自定义能力较为强大，可以任意定义日志格式，较为方便。

```go
package main

import (
    "context"
    "fmt"
    "github.com/sirupsen/logrus"
    "io"
    "os"
    "path/filepath"
    "runtime"
    "strings"
)

const logPath = "./log.txt"

var log = New()

func New() *Logger {
    return &Logger{logger: logrus.New()}
}

type Logger struct {
    ctx    context.Context
    logger *logrus.Logger
}

func (l *Logger) SetFormatter(formatter logrus.Formatter) {
    l.logger.SetFormatter(formatter)
}

func (l *Logger) SetOutput(output io.Writer) {
    l.logger.SetOutput(output)
}

func (l *Logger) SetLevel(level logrus.Level) {
    l.logger.SetLevel(level)
}

func (l *Logger) WithContext(ctx context.Context) *Logger {
    return &Logger{ctx: ctx, logger: l.logger}
}

func (l *Logger) Debug(format string, args ...any) {
    l.log(logrus.DebugLevel, format, args...)
}

func (l *Logger) Info(format string, args ...any) {
    l.log(logrus.InfoLevel, format, args...)
}

func (l *Logger) Warn(format string, args ...any) {
    l.log(logrus.WarnLevel, format, args...)
}

func (l *Logger) Error(format string, args ...any) {
    l.log(logrus.ErrorLevel, format, args...)
}

func (l *Logger) Fatal(format string, args ...any) {
    l.log(logrus.FatalLevel, format, args...)
}

func (l *Logger) log(level logrus.Level, format string, args ...any) {
    format = fmt.Sprintf("[%s] %s", GetCallerShort(3), format)
    l.logger.WithContext(l.ctx).Logf(level, format, args...)
}

type Formatter struct{}

func (f *Formatter) Format(entry *logrus.Entry) ([]byte, error) {
    pid := os.Getpid()
    time := entry.Time.Format("2006-01-02T15:04:05.000000")
    level := strings.ToUpper(entry.Level.String())
    traceId := GetTraceIdFromCtx(entry.Context)

    content := fmt.Sprintf("%s %s %d %s %s\n", time, level, pid, traceId, entry.Message)
    return []byte(content), nil
}

// GetCallerShort 获取调用点文件名 + 行号
func GetCallerShort(skip int) string {
    _, file, line, ok := runtime.Caller(skip + 1)
    if !ok {
       return ""
    }
    _, file = filepath.Split(file)
    return fmt.Sprintf("%s:%d", file, line)
}

// CtxSetTraceId 在 ctx 中设置 trace id
func CtxSetTraceId(ctx context.Context) context.Context {
    return context.WithValue(ctx, "trace_id", "id1")
}

// GetTraceIdFromCtx 打印日志时，从 ctx 中获取 trace id 打印
func GetTraceIdFromCtx(ctx context.Context) string {
    if ctx == nil {
       return "-"
    }

    val := ctx.Value("trace_id")
    if traceId, ok := val.(string); ok {
       return fmt.Sprintf("trace-%s", traceId)
    } else {
       return "-"
    }
}

func init() {
    f, err := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o640)
    if err != nil {
       panic(err)
    }

    log.SetFormatter(&Formatter{})
    log.SetOutput(io.MultiWriter(os.Stdout, f))
    log.SetLevel(logrus.DebugLevel)
}

func main() {
    ctx := context.Background()
    ctx = CtxSetTraceId(ctx)
    log.WithContext(ctx).Info("main failed: %s", "detail")
}
```
