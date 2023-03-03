---
categories:
- 软件开发
date: 2023-02-08 02:29:21.451912
id: postgresql_cmd
tags:
- 数据库
- 软件开发
title: 【Postgresql】Postgresql 常用命令
---

## 创建用户和数据库

```shell
# 进入命令行
su -u postgre
psql

# 创建用户
create user vksir with password 'passwd';

# 创建数据库并赋予用户权限
create database db owner vksir;
grant all privileges on datebase db to vksir;

# 退出
\q

# 使用新用户登录数据库
psql -U vksir -d db
```

<!-- more -->

## 命令行命令

```shell
\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
```

## SQL 语句

```sql
# 创建新表
create table t_person
(
    id serial primary key,
    name text not null,
    age int,
    alive bool
);

# 插入数据
insert into t_person(name) values ('vksir');

# 选择记录
select * from t_person;

# 更新数据
update t_person set age = '18' where name = 'vksir';

# 删除记录
delete from t_person where name = 'vksir';

# 删除表格
drop table t_person;
```

---

参考文档：

- [介绍 - 《PostgreSQL新手入门》 - 书栈网 · BookStack](https://www.bookstack.cn/read/getting_started_with_postgresql/pgsql.md)
