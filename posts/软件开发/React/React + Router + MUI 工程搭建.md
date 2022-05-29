---
categories:
- 软件开发
date: 2022-05-29 17:54:51.029764
id: 'react'
tags:
- react
- 软件开发
- react router
- material ui
- axios
- 跨域
title: React + Router + MUI 工程搭建
---

# React + Router + MUI 工程搭建

## 初始化

### create-react-app

```shell
npx create-react-app my-app
```

<!-- more -->

### 安装 MUI

在工程路径下执行：

```shell
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/material @mui/styled-engine-sc styled-components
npm install @mui/icons-material
```

在 `public/index.html` 中引入：

```html
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
/>
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/icon?family=Material+Icons"
/>
```

引入一个按钮。修改 `src/App.js` 如下：

```js
import './App.css';
import {Button} from "@mui/material";

function App() {
    return (
        <>
            <Button variant="contained">你好，世界</Button>
        </>
    );
}

export default App;
```

修改 `src/App.css` 如下：

```css
body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
```

### 启动

```shell
npm start
```

如此打开 <http://localhost:3000> 可看到简单页面：

![image-20220529170509431](https://static.vksir.zone/img/image-20220529170509431.png)

## 跨域请求

### 配置跨域

```shell
npm install http-proxy-middleware
```

创建文件 `src/setupProxy.js` 如下：

```js
const { createProxyMiddleware } = require("http-proxy-middleware");
module.exports = function (app) {
    app.use(
        createProxyMiddleware("/neutron_star_api", {
            target: "https://api.vksir.zone",
            changeOrigin: true,
            pathRewrite: {
                "^/neutron_star_api": ""
            }
        })
    )
}
```

### 配置 axios 实例

```shell
npm install axios
```

创建文件 `src/common/requests.js` 如下：

```js
import axios from "axios";

const neutronStarAPI = axios.create({});

const baseRequest = [
    (config) => {
        config.baseURL = '/neutron_star_api/';
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
]

const baseResponse = [
    (response) => {
        return response;
    },
    (error) => {
        return Promise.reject(error);
    }
]

neutronStarAPI.interceptors.request.use(...baseRequest);
neutronStarAPI.interceptors.response.use(...baseResponse);

export {neutronStarAPI};
```

### 请求

新增一个组件 `Ipv4`，并增加请求函数。修改 `src/App.js` 如下：

```js
import './App.css';
import {Button, TextField} from "@mui/material";
import {useState} from "react";
import {neutronStarAPI} from "./common/requests";

function App() {
    return (
        <>
            <Ipv4/>
        </>
    );
}

export default App;

function Ipv4() {
    const [ip, setIp] = useState('');

    function calc() {
        const params = new URLSearchParams();
        params.append('ip_addr', ip);
        neutronStarAPI({
            url: '/calculator/ipv4',
            params: params,
            method: 'get',
        }).then((resp) => {
            console.log(resp.data);
        });
    }

    return (
        <>
            <div>
                <TextField
                    label="IPAddress"
                    variant="outlined"
                    value={ip}
                    placeholder="192.168.10.1/24"
                    onChange={(e) => setIp(e.target.value)}/>
                <br/><br/>
                <Button variant="contained" onClick={calc}>Parse</Button>
            </div>
        </>
    );
}
```

效果如下：

![image-20220529173049275](https://static.vksir.zone/img/image-20220529173049275.png)

## 路由

```shell
npm install react-router-dom@6
```

再新增一个组件 `Ipv6`，编辑路由路径配置。修改 `src/App.js` 如下：

```js
import './App.css';
import {Button, TextField} from "@mui/material";
import {useState} from "react";
import {neutronStarAPI} from "./common/requests";
import {BrowserRouter, Routes, Route, Navigate, Link} from "react-router-dom";

function App() {
    return (
        <>
            <BrowserRouter>
                <Link to="/calculator/ipv4">IPv4</Link>
                <span> | </span>
                <Link to="/calculator/ipv6">IPv6</Link>
                <br/><br/>
                <Routes>
                    <Route path="/" element={<Navigate to="/calculator" replace />}/>
                    <Route path="/calculator" element={<Navigate to="/calculator/ipv4" replace />}/>
                    <Route path="/calculator/ipv4" element={<Ipv4/>}/>
                    <Route path="/calculator/ipv6" element={<Ipv6/>}/>
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;

function Ipv4() {
    const [ip, setIp] = useState('');

    function calc() {
        const params = new URLSearchParams();
        params.append('ip_addr', ip);
        neutronStarAPI({
            url: '/calculator/ipv4',
            params: params,
            method: 'get',
        }).then((resp) => {
            console.log(resp.data);
        });
    }

    return (
        <>
            <div>
                <TextField
                    label="IPv4 Address"
                    variant="outlined"
                    value={ip}
                    placeholder="192.168.10.1/24"
                    onChange={(e) => setIp(e.target.value)}/>
                <br/><br/>
                <Button variant="contained" onClick={calc}>Parse</Button>
            </div>
        </>
    );
}

function Ipv6() {
    const [ip, setIp] = useState('');

    function calc() {
        const params = new URLSearchParams();
        params.append('ip_addr', ip);
        neutronStarAPI({
            url: '/calculator/ipv6',
            params: params,
            method: 'get',
        }).then((resp) => {
            console.log(resp.data);
        });
    }

    return (
        <>
            <div>
                <TextField
                    label="IPv6 Address"
                    variant="outlined"
                    value={ip}
                    placeholder="1021::/64"
                    onChange={(e) => setIp(e.target.value)}/>
                <br/><br/>
                <Button variant="contained" onClick={calc}>Parse</Button>
            </div>
        </>
    );
}
```

效果如下：

![image-20220529174750568](https://static.vksir.zone/img/image-20220529174750568.png)
