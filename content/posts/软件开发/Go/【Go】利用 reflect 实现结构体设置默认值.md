---
categories:
- 软件开发
date: 2022-06-04 20:14:35.645296
id: go_struct_default
tags:
- go
- reflect
- struct
- 软件开发
title: 【Go】利用 reflect 实现结构体设置默认值
---

# 【Go】利用 reflect 实现结构体设置默认值

写 API 时经常会需要结构体中某个参数拥有默认值。但如 Gin 只有 `ShouldBindQuery` 这种 `form` 类型支持设置默认值，常用的 `ShouldBindJSON` 这种 `json` 类型却不支持，很奇怪。

## Gin 中 bind 结构体设置默认值

```go
package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
)

type FormData struct {
	Name string `form:"name,default=vksir"`
	Age  int    `form:"age,default=18"`
}

type JsonData struct {
	Name string `json:"name,default=vksir"`
	Age  int    `json:"age,default=18"`
}

func main() {
	e := gin.Default()
	e.GET("/", func(c *gin.Context) {
		var fd FormData
		c.ShouldBindQuery(&fd)
		var jd JsonData
		c.ShouldBindJSON(&jd)
		fmt.Printf("FormData: %+v\n", fd)
		fmt.Printf("JsonData:%+v\n", jd)
	})
	e.Run()
}
```

<!-- more -->

请求会打印如下结果：

```
FormData: {Name:vksir Age:18}
JsonData:{Name: Age:0}
```

也就是说 `JsonData` 的默认值没有生效，如果看源码也可以发现 `ShouldBindJSON` 是没有设置默认值的动作的。

## 简单实现结构体设置默认值

编辑 `structutil/struct.go`：

```go
package structutil

import (
	"reflect"
	"strconv"
)

func SetDefault(v any) error {
	typeOf := reflect.TypeOf(v).Elem()
	valueOf := reflect.ValueOf(v).Elem()
	return subSetDefault(typeOf, valueOf)
}

func subSetDefault(typeOf reflect.Type, valueOf reflect.Value) error {
	for i := 0; i < typeOf.NumField(); i++ {
		tField := typeOf.Field(i)
		vField := valueOf.Field(i)
		switch tField.Type.Kind() {
		case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
			defaultVal, ok := tField.Tag.Lookup("default")
			if !ok {
				continue
			}
			defaultValInt, err := strconv.ParseInt(defaultVal, 10, 64)
			if err != nil {
				return err
			}
			vField.SetInt(defaultValInt)
		case reflect.String:
			defaultVal, ok := tField.Tag.Lookup("default")
			if !ok {
				continue
			}
			vField.SetString(defaultVal)
		case reflect.Struct:
			err := subSetDefault(tField.Type, vField)
			if err != nil {
				return err
			}
		}
	}
	return nil
}
```

简单使用：

```go
package main

import (
	"GoCode/structutil"
	"encoding/json"
	"fmt"
)

type Person struct {
	Name string `json:"name" default:"vksir"`
	Age  int    `json:"age" default:"18"`
	Like struct {
		Name string `json:"name" default:"she"`
		Age  int    `json:"age" default:"18"`
	} `json:"like"`
}

func main() {
	var p Person
	rawData := `{"like": {}}`
	structutil.SetDefault(&p)
	json.Unmarshal([]byte(rawData), &p)
	fmt.Printf("%+v\n", p)
}
```

```
{Name:vksir Age:18 Like:{Name:she Age:18}}
```

如期设置了默认值。

---

经常会发现 Go 利用 tag 完成了大量工作。

这点其实很奇怪，tag 本来就是类似注释一样的东西，但给了它太多意义。包括很多时候，注释也都利用起来了（像 `embed`）。

个人感觉这是属于语言内容太少的原因，关键字少，内置函数少。

怪怪的。
