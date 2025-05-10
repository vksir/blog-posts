---
categories:
- 软件开发
date: 2022-08-30 00:14:05.817968
id: electron-vue-antd-python
tags:
- antd
- electron
- python
- vue
- 软件开发
title: 【Electron】使用 Electron + Vue + Antd + Python 构建桌面程序
url: posts/electron-vue-antd-python
---

## 写在前面

也算是个记录吧，以免以后想写桌面程序又要走一遍弯路。这玩意不难，只是也有些坑，会耗些时间。

前端真没什么好说的，搞框架、搞设计的人很强，但调包这件事，人人都会干。

## 搭建前端

### 创建 vue 项目

<!-- more -->

```shell
yarn global add @vue/cli
vue create electron-vue
```

> 参考：https://cli.vuejs.org/zh/guide/installation.html。

### 引入 electron

有现成的不用是……

```shell
cd electron-vue
vue add electron-builder
```

> 参考：https://nklayman.github.io/vue-cli-plugin-electron-builder/guide/#installation。

没事儿不要自己瞎折腾，有时候遇上一些奇怪的报错，作为后端开发党，很难解决。

### 试一试

```shell
yarn electron:serve
```

![image-20220829223528809](https://static.vksir.zone/img/image-20220829223528809.png)

### 引入 Antd Vue

```shell
yarn add ant-design-vue
```

> 参考：https://www.antdv.com/docs/vue/getting-started-cn。

这里如果使用 npm 进行安装 `npm i --save ant-design-vue`，就会报错。——咱也不懂，咱也懒得看。

修改 `src/main.js` 如下：

```js
import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

createApp(App).use(Antd).mount('#app')
```

修改 `src/components/HelloWorld.vue` 如下：

```vue
<script setup>
import {ref} from "vue";

const content = ref('hello electron')

function click() {
  content.value = 'hello vue'
}
</script>

<template>
  <a-button type="primary" @click="click">click me</a-button>
  <a-typography-paragraph>{{ content }}</a-typography-paragraph>
</template>
```

## 搭建后端

后端用什么都行，go、python 都可以。

### 创建 fastapi server

server 代码不细说，详情看文末 Git 库。

### 引入 axios

```shell
 yarn add axios
```

修改 `src/componets/HelloWorld.vue` 如下：

```vue
<script setup>
import {ref} from "vue";
import axios from "axios";

const content = ref('hello electron')

function click() {
  axios({
    url: '/',
    method: 'get'
  }).then((resp) => {
    content.value = resp.data['detail']
  })
}
</script>

<template>
  <a-button type="primary" @click="click">click me</a-button>
  <a-typography-paragraph>{{ content }}</a-typography-paragraph>
</template>
```

修改 `src/main.js` 如下：

```js
import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import axios from "axios";

// 跨域请求
axios.defaults.baseURL = 'http://127.0.0.1:8081'
createApp(App).use(Antd).mount('#app')
```

这里使用了最简单粗暴的跨域请求方式，别忘了在后端放开跨域访问限制。fastapi 放开方式如下：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 试一试

同时启动后端 server 和 electron，点击 click me 按钮，可以看到有新信息出现：

![image-20220829232525584](https://static.vksir.zone/img/image-20220829232525584.png)

## 打包

### 打包 python 程序

```shell
# 安装 pyinstaller
pip install pyinstaller

# 初次打包，并生成 spec 文件
cd server
pyinstaller -F server.py
```

修改 `package.json` 中的 `scripts` 字段，新增两条脚本如下：

```json
{
	"scripts": {
		"server:build": "cd server && pyinstaller server.spec",
		"server:serve": "cd server && python server.py"
	}
}
```

再次打包，并尝试启动 server：

```shell
$ yarn run server:build
$ ./server/dist/server.exe
ERROR:    Error loading ASGI app. Could not import module "route".
```

有报错，找不到包，需要修改 spec 文件中的 hidenimports 字段：

```spec
hiddenimports=['route']
```

再次打包，并尝试启动 server 成功。

编辑 `backgroud.js`，使用如下方式启动后端：

```js
import child_process from 'child_process'
import path from 'path'
const server_path = path.join(path.dirname(__dirname), 'server', 'dist', 'server.exe')

// 启动
server = child_process.spawn(server_path)
// 退出
server.kill()
```

尝试运行 `yarn run electron:serve`，已经可以正常启动后端了。

### 打包 electron 程序

```shell
yarn run electron:build
```

打包时会从 Github 上下载一些东西，若网络较差可能会打包失败。这样打包，并不会打包后端 server，还需要做一些额外配置。

编辑 `vue.config.js` 如下：

```javascript
module.exports = {
    pluginOptions: {
        electronBuilder: {
            builderOptions: {
                'extraResources': [
                    {
                        'from': './server/dist',
                        'to': './server/dist'
                    }
                ]
            }
        }
    }
}
```

> 参考：https://nklayman.github.io/vue-cli-plugin-electron-builder/guide/configuration.html#configuring-electron-builder。

再次打包后运行，可正常运行，并且 server 后端亦正常运行。打包后的可执行文件位于 `dist_electron/win-unpacked/electron-vue.exe`。

此处获取后端程序路径的方式 `const server_path = path.join(path.dirname(__dirname), 'server', 'dist', 'server.exe')` 在打包前后皆可使用，若打包前后路径有所差异，则需额外做特殊处理。

## 后记

> Git 链接：https://github.com/vksir/electron-vue-example

我想，偶尔还是会写一写桌面程序，遇到什么想要的工具，就自己写一个。使用这个库，能节约一些时间。毕竟，时间长了，忘得超快。
