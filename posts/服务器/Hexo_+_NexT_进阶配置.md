---
title: Hexo + NexT 进阶配置
comments: false
id: hexo-1
categories:
  - 玩转服务器
tags:
  - 服务器
  - 博客系统
  - Hexo
date: 2020-03-06 23:07:57
---

> Hexo——一款纯静态、基于 Nodejs 的博客系统。
>
> NexT——Hexo 下的强大的主题，该博客发展到了现在，倒是算是 Hexo 还是 NexT，真的很难说清。
>
> 优点：
>
> - 万能！什么功能都有！相比起 Ghost 博客系统，Hexo + NexT 完善太多
> - 支持所有 Markdown 语法，类似于嵌套列表（Now），而 Ghost 和 WordPress 都是不支持的。强迫症如我，表示没有嵌套列表日子不能过！
>
> 缺点：
>
> - 相比起 Ghost 的主题配置语言 HandBar，NexT 主题的这个 swig 语言系统着实难懂。且 NexT 的文档不是非常完善，自定义主题较为困难。
> - 没有 Web 后台（有一个，但是太丑……），只能在命令行下发布文章，没有一种家的感觉
>
> 环境：[Nodejs v12.14.1](https://www.vksir.zone/posts/nodejs/)
>
> 版本：Hexo v4.2.0，NexT  v7.7.2

<!-- more -->

## 访问量统计


```html
<!-- 添加脚本 -->
<!-- next/layout/_partials/head/head-unique.swig -> END -->
<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>


<!-- 这一段是页脚 由Hexo强力驱动 等字样，删了也罢 -->
<!-- next/layout/_partials/footer.swig -> FIND -->
{%- if theme.footer.powered.enable %}
  <div class="powered-by">
    {{- __('footer.powered', next_url('https://hexo.io', 'Hexo', {class: 'theme-link'})) }}
    {%- if theme.footer.powered.version %} v{{ hexo_version }}{%- endif %}
  </div>
{%- endif %}

{%- if theme.footer.powered.enable and theme.footer.theme.enable %}
  <span class="post-meta-divider">|</span>
{%- endif %}

{%- if theme.footer.theme.enable %}
  <div class="theme-info">
    {%- set next_site = 'https://theme-next.org' %}
    {%- if theme.scheme !== 'Gemini' %}
      {%- set next_site = 'https://' + theme.scheme | lower + '.theme-next.org' %}
    {%- endif %}
    {{- __('footer.theme') }} – {{ next_url(next_site, 'NexT.' + theme.scheme, {class: 'theme-link'}) }}
    {%- if theme.footer.theme.version %} v{{ next_version }}{%- endif %}
  </div>
{%- endif %}

{%- if theme.add_this_id %}
  <div class="addthis_inline_share_toolbox">
    <script src="//s7.addthis.com/js/300/addthis_widget.js#pubid={{ theme.add_this_id }}" async="async"></script>
  </div>
{%- endif %}

<!-- 替换为本站总访客数 -->
<!-- next/layout/_partials/footer.swig -->
<div class="powered-by">
  <span class="post-meta-item-icon">
    <i class="fa fa-eye"></i>
  </span>
  <span id="busuanzi_container_site_uv">总访客数: <span id="busuanzi_value_site_uv"></span></span>
</div>

<!-- 这一段前 -->
<!-- next/layout/_macro/post.swig -> FIND -->
{%- endif %}

{#################}
{### POST BODY ###}
{#################}

<!-- 添加本文阅读量 -->
<!-- next/layout/_macro/post.swig -->
<span class="post-meta-item" id="busuanzi_container_page_pv">
  <span class="post-meta-item-icon">
    <i class="fa fa-eye"></i>
  </span>
  阅读量: <span id="busuanzi_value_page_pv"></span>
</span>
```

来自：

> 不蒜子极简访问计数：<u>http://busuanzi.ibruce.info/</u>

## 字数统计 & 搜索功能

### 安装

```bash
# 删除所有依赖
cd hexo && rm -rf node_modules
# 重新安装
npm install hexo hexo-wordcount hexo-generator-searchdb
```

### 配置

#### 字数统计

```html
<!-- 本文字数 -->
   <span class="post-count">{{ wordcount(post.content) }}</span>
<!-- 阅读时长 -->
   <span class="post-count">{{ min2read(post.content) }}</span>
<!-- 全站字数统计 -->
   <span class="post-count">{{ totalcount(site) }}</span>
```

添加到想要添加的位置即可。

这里我同样选择，页脚和文章页面标题下。

```html
<!-- 在页脚添加全站字数 -->
<!-- next/layout/_partials/footer.swig -->
<div class="powered-by">
  <span class="post-meta-divider">|</span>
  <span class="post-meta-item-icon">
    <i class="fa fa-file-text-o"></i>
  </span>
  全站字数: <span class="post-count">{{ totalcount(site) }}</span>
</div>

<!-- 在文章页面标题下方，添加本文字数 -->
<!-- next/layout/_macro/post.swig -->
<span class="post-meta-item">
  <span class="post-meta-item-icon">
    <i class="fa fa-file-text"></i>
  </span>
  本文字数: <span class="post-count">{{ wordcount(post.content) }}</span>
</span>
```

#### 搜索功能

```yml
# 添加配置以覆盖原配置
# hexo/_config.yml -> END
theme_config:
    search:
        path: search.xml
        field: post
        content: true
        format: html

    # Local Search
    # Dependencies: https://github.com/theme-next/hexo-generator-searchdb
    local_search:
        enable: true
        # If auto, trigger search by changing input.
        # If manual, trigger search by pressing enter key or search button.
        trigger: auto
        # Show top n results per article, show all results by setting to -1
        top_n_per_article: 1
        # Unescape html strings to the readable one.
        unescape: false
        # Preload the search data when the page loads.
        preload: false
```

来自：

> 搜索功能：<u>https://github.com/theme-next/hexo-generator-searchdb</u>
>
> 字数统计：<u>https://github.com/willin/hexo-wordcount</u>