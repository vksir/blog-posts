---
categories:
- 软件开发
date: 2022-07-10 23:15:16.762119
id: go-signal-context
tags:
- go
- 软件开发
title: 【Go】利用 signal + context 实现优雅退出
---

```go
package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"sync"
	"time"
)

var wg sync.WaitGroup

func worker(name string, ctx context.Context, t time.Duration) {
	fmt.Println(name, ": enter worker")
	select {
	case <-ctx.Done():
		fmt.Println(name, ": worker context cancel, exit")
	case <-time.After(t):
		fmt.Println(name, ": worker process complete, exit")
	}
	wg.Done()
}

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	wg.Add(2)
	go worker("worker1", ctx, time.Second*2)
	go worker("worker2", ctx, time.Second*4)

	wg.Wait()
	fmt.Println("exit main")
}
```
