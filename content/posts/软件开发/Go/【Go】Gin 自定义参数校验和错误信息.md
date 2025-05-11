---
categories:
- 软件开发
date: 2023-02-08 02:29:21.430264
draft: false
id: go_gin_validate
tags:
- go
- 软件开发
title: 【Go】Gin 自定义参数校验和错误信息
url: posts/go_gin_validate
---

Gin 使用 validator 库做数据校验，如下可以实现自定义校验、及自定义校验错误信息。

其中，自定义错误信息无法用于多层嵌套结构体，可能可以通过反射做到，但感觉在性能上很捉急。

## 代码

```go
package main

import (
	"errors"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/validator/v10"
	"net/http"
	"reflect"
	"strings"
)

type Body struct {
	Name string `json:"name" binding:"oneof=vk vksir" err:"one of vk,vksir"`
	Age  int    `json:"age" binding:"BodyAgeValidate" err:"only 18"`
}

func BodyAgeValidate(f validator.FieldLevel) bool {
	value := f.Field().Int()
	if value != 18 {
		return false
	}
	return true
}

func GetValidateErr(obj any, rawErr error) error {
	validationErrs, ok := rawErr.(validator.ValidationErrors)
	if !ok {
		return rawErr
	}
	var errString []string
	for _, validationErr := range validationErrs {
		field, ok := reflect.TypeOf(obj).FieldByName(validationErr.Field())
		if ok {
			if e := field.Tag.Get("err"); e != "" {
				errString = append(errString, fmt.Sprintf("%s: %s", validationErr.Namespace(), e))
				continue
			}
		}
		errString = append(errString, validationErr.Error())
	}
	return errors.New(strings.Join(errString, "\n"))
}

func ping(c *gin.Context) {
	b := Body{}
	if err := c.ShouldBindJSON(&b); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": GetValidateErr(b, err).Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{})
}

func main() {
	e := gin.Default()
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		v.RegisterValidation("BodyAgeValidate", BodyAgeValidate)
	}
	e.GET("/ping", ping)
	e.Run("127.0.0.1:8080")
}
```

<!-- more -->

## 运行

```
curl --location --request GET 'http://127.0.0.1:8080/ping' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "v",
    "age": 19
}'
```

```
{
    "detail": "Body.Name: one of vk,vksir\nBody.Age: only 18"
}
```

---

参考文档：

- [validator package - github.com/go-playground/validator/v10 - Go Packages](https://pkg.go.dev/github.com/go-playground/validator/v10#pkg-overview)
- [自定义验证器 | Gin Web Framework (gin-gonic.com)](https://gin-gonic.com/zh-cn/docs/examples/custom-validators/)
