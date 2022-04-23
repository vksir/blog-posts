---
categories:
- 软件开发
date: 2022-04-23 18:05:32.294698
id: go_requests
tags:
- 软件开发
- go
title: 【Go】实现 requests 库
---

粗略实现了一下 requests 库。但后来想想，也必要自己造轮子，还是 [resty](https://github.com/go-resty/resty) 香！

```go
package requests

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"reflect"
	"strings"
)

type Client struct {
	Url     string
	Headers map[string][]string
	Params  map[string][]string
	Content string
	Data    interface{}
	Json    interface{}
}

type Response struct {
	Status     string
	StatusCode int
	Body       string
}

func (c Client) newRequest(method string) (req *http.Request, err error) {
	// url
	if reflect.ValueOf(c.Url).IsZero() {
		err = errors.New(fmt.Sprintf("url is needed: client=%+v", c))
		return
	}
	u, err := url.ParseRequestURI(c.Url)
	if err != nil {
		return
	}

	// params
	if !reflect.ValueOf(c.Params).IsNil() {
		var params url.Values = c.Params
		u.RawQuery = params.Encode()
	}

	// body, headers
	body := ""
	if reflect.ValueOf(c.Headers).IsNil() {
		c.Headers = make(map[string][]string)
	}
	if !reflect.ValueOf(c.Content).IsZero() {
		body = c.Content
	} else if !reflect.ValueOf(c.Data).IsValid() {
		c.Headers["Content-Type"] = []string{"application/x-www-form-urlencoded"}
		var bodyBytes []byte
		bodyBytes, err = json.Marshal(c.Json)
		if err != nil {
			return
		}
		body = string(bodyBytes)
	} else if !reflect.ValueOf(c.Json).IsValid() {
		c.Headers["Content-Type"] = []string{"application/json"}
		var bodyBytes []byte
		bodyBytes, err = json.Marshal(c.Json)
		if err != nil {
			return
		}
		body = string(bodyBytes)
	}

	req, err = http.NewRequest(method, u.String(), strings.NewReader(body))
	if err != nil {
		return
	}
	req.Header = c.Headers
	return
}

func (c Client) parseResponse(resp *http.Response) (response *Response, err error) {
	defer func(Body io.ReadCloser) {
		err := Body.Close()
		if err != nil {
			log.Printf("close response body failed: err=%s", err)
		}
	}(resp.Body)
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return
	}
	return &Response{
		resp.Status,
		resp.StatusCode,
		string(body),
	}, nil
}

func (c Client) Request(method string) (response *Response, err error) {
	req, err := c.newRequest(method)
	if err != nil {
		return
	}
	client := http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return
	}
	return c.parseResponse(resp)
}

func (c Client) Get() (response *Response, err error) {
	return c.Request("GET")
}

func (c Client) Post() (response *Response, err error) {
	return c.Request("POST")
}
```
