# 目录
| 课时 | 主题 | 时长 | 核心产出 |
| --- | --- | --- | --- |
| **第 1 课时** | 网络分层模型与 HTTP 诞生 | 60 min | 能画出 TCP/IP 分层 + 三次握手 |
| **第 2 课时** | HTTP 报文深度剖析 | 60 min | 能徒手写出一个完整的 HTTP 请求/响应 |
| **第 3 课时** | HTTPS 与 Web 安全基础 | 60 min | 能讲清楚 TLS 握手的全过程 |
| **第 4 课时** | 渗透视角下的 HTTP 实战 | 60 min | 能用 Burp 独立完成抓包/改包/重放 |


---

# 第 1 课时：网络分层模型与 HTTP 诞生
## 1.1 从一个朴素的问题说起
> **"我在浏览器输入 **`www.baidu.com`**，按下回车，到看到页面，中间发生了什么？"**
>

这是面试经典题，也是理解 HTTP 的入口。我们一步一步拆。

### 1.1.1 两台电脑怎么通信？
```plain
┌─────────────┐                      ┌─────────────┐
│   电脑 A    │  ──────网线──────►   │   电脑 B    │
│ "hello"     │                      │             │
└─────────────┘                      └─────────────┘
```

最简单：用一根网线连起来，A 发高低电平，B 解码。

**问题来了**：

+ 100 台电脑怎么办？→ 需要**交换机/路由器**
+ 数据怎么知道发给谁？→ 需要**地址**（MAC / IP）
+ 100 个程序同时收发怎么区分？→ 需要**端口**
+ 数据太长断了怎么办？→ 需要**分包/重组**
+ 传输错了怎么办？→ 需要**校验/重传**
+ 网页/邮件/视频都用同一条路？→ 需要**协议分层**

### 1.1.2 分层思想：搭积木式通信
> 每一层只做一件事，下层为上层提供服务，上层不需要知道下层细节。
>

打个比方——你寄快递：

| 你做的事 | 类比网络层 |
| --- | --- |
| 把信装进信封、写内容 | 应用层（HTTP / 邮件） |
| 写收件人地址、贴邮票 | 传输层（TCP 加端口） |
| 邮局分拣、按城市装车 | 网络层（IP 路由） |
| 卡车走高速、过收费站 | 数据链路层（MAC / 以太网） |
| 物理公路、信号灯 | 物理层（电缆 / 光纤） |


每一层只关心自己的事，上层根本不用管信是飞机送还是卡车送。

---

## 1.2 网络分层模型
### 1.2.1 OSI 七层 vs TCP/IP 四层
![](https://cdn.nlark.com/yuque/__mermaid_v3/0d2d193d3ac761c050684d44562c7e4e.svg)

| OSI 层 | TCP/IP 层 | 典型协议 | 数据单元 | 类比 |
| --- | --- | --- | --- | --- |
| 7 应用 | 应用 | HTTP, DNS, SMTP, FTP | Message | 信件内容 |
| 6 表示 | 应用 | SSL/TLS, JPEG | Message | 信件加密 |
| 5 会话 | 应用 | NetBIUS, RPC | Message | 通信约定 |
| 4 传输 | 传输 | TCP, UDP | Segment / Datagram | 信封+收件人 |
| 3 网络 | 网际 | IP, ICMP | Packet | 邮政分拣 |
| 2 链路 | 接口 | Ethernet, ARP | Frame | 卡车 |
| 1 物理 | 接口 | 电缆, 光纤 | Bit | 公路 |


> 💡 **记住一句话**：HTTP 工作在**应用层**，它**站在 TCP/IP 的肩膀上**。
>

### 1.2.2 数据是怎么一层层"打包"的？
```plain
应用层数据 (HTTP 报文)
   ▼  加 TCP 头 (源端口/目的端口/序号...)
TCP 段 (Segment)
   ▼  加 IP 头 (源 IP/目的 IP)
IP 数据报 (Packet)
   ▼  加 MAC 头 (源 MAC/目的 MAC)
以太网帧 (Frame)
   ▼  变成电信号/光信号
Bit 流
```

**封装图**（重点）：

```plain
┌──────────────────────────────────────────────────┐
│ [MAC头 14B][IP头 20B][TCP头 20B][ HTTP 报文 data ] │
└──────────────────────────────────────────────────┘
                                     ▲
                                     └── 真正的应用数据
```

**抓包验证**：用 Wireshark 抓一个 HTTP 请求，会看到清晰的分层结构。

---

## 1.3 IP、端口、DNS 速通
### 1.3.1 IP 地址
+ **IPv4**：32 位，4 字节，例如 `192.168.1.1`，约 43 亿个（已耗尽）
+ **IPv6**：128 位，例如 `2001:0db8:85a3::8a2e:0370:7334`
+ **特殊 IP**：

| 范围 | 含义 |
| --- | --- |
| `127.0.0.0/8` | 本机回环 (loopback) |
| `10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16` | 私有 IP（内网） |
| `169.254.0.0/16` | 链路本地（云元数据接口！SSRF 关键） |
| `0.0.0.0` | 所有网卡 |


> 🎯 **渗透视角**：`169.254.169.254` 是 AWS / 阿里云的**元数据接口**，SSRF 漏洞的"圣杯"。
>

### 1.3.2 端口
+ 范围：`0 - 65535`（2^16）
+ 分类：

| 范围 | 类型 | 例子 |
| --- | --- | --- |
| 0 - 1023 | 公认端口 | 80 (HTTP), 443 (HTTPS), 22 (SSH), 21 (FTP) |
| 1024 - 49151 | 注册端口 | 3306 (MySQL), 6379 (Redis), 8080 |
| 49152 - 65535 | 动态端口 | 客户端临时用 |


> **一台服务器最多能开 65535 个端口吗？** 是的，但通常受文件描述符限制。
>

### 1.3.3 DNS（Domain Name System）
> IP 难记，域名好记。DNS 就是**域名 → IP** 的电话簿。
>

**解析流程**：

```mermaid
sequenceDiagram
    participant U as 用户浏览器
    participant L as 本地 DNS 缓存
    participant R as "递归 DNS 服务器<br/>(运营商/8.8.8.8)"
    participant T as 根 DNS
    participant A as ".com 顶级 DNS"
    participant B as "example.com 权威 DNS"

    U->>L: 查 www.example.com
    L-->>U: 没有
    U->>R: 查 www.example.com
    R->>T: 问根
    T-->>R: 去 .com 问
    R->>A: 问 .com
    A-->>R: 去 example.com 问
    R->>B: 问 example.com
    B-->>R: IP = 1.2.3.4
    R-->>U: "返回 1.2.3.4 (并缓存)"
```

**实操**：观察 DNS 解析

```bash
# Linux/Mac
dig www.baidu.com
nslookup www.baidu.com

# Windows
nslookup www.baidu.com
```

> 🎯 **渗透视角**：DNS 也能成为攻击通道 —— DNS Rebinding（重绑定）、DNSLog（带外数据外带）、子域爆破。
>

---

## 1.4 TCP 三次握手与四次挥手（重点！）
HTTP 是基于 TCP 的，**每次 HTTP 通信前都要先建立 TCP 连接**。

### 1.4.1 三次握手（建立连接）
```plain
客户端                                       服务端
  │                                            │
  │ ───── SYN (seq=x) ─────────────────────►   │  ① 我想连
  │                                            │
  │   ◄───────── SYN+ACK (seq=y, ack=x+1) ───  │  ② 我同意，也想连
  │                                            │
  │ ───── ACK (ack=y+1) ─────────────────►    │  ③ 好的，开始吧
  │                                            │
  │ ═════════ 可以传输数据了 ═══════════════════ │
```

**为什么是 3 次不是 2 次？**

> 如果只有 2 次：客户端发 SYN → 服务端回 ACK 就建立。  
但如果客户端的 SYN 在网络里堵了，**迟到了很久**才到，服务端会误以为是新请求，建立一个**死连接**，浪费资源。  
3 次握手让客户端**最后确认一次**，避免这种"历史报文"问题。
>

### 1.4.2 四次挥手（断开连接）
```plain
客户端                                       服务端
  │                                            │
  │ ───── FIN ────────────────────────────►    │  ① 我说完了
  │   ◄───────── ACK ──────────────────────    │  ② 我知道了
  │                                            │
  │            (服务端可能还有数据要发...)        │
  │   ◄───────── 数据 ─────────────────────    │
  │   ◄───────── FIN ─────────────────────    │  ③ 我也说完了
  │ ───── ACK ────────────────────────────►    │  ④ 收到，再见
  │                                            │
  │ (TIME_WAIT 2MSL)                           │ (CLOSED)
  │                                            │
```

**为什么挥手要 4 次？**

> TCP 是**全双工**的——两边都能独立关闭。一方说"我不发了"，另一方还能继续发，等也说"我不发了"才算完。
>

### 1.4.3 抓包验证
```bash
# 启动监听
sudo tcpdump -i any -n 'port 80' -S

# 另一个终端
curl http://example.com/

# 观察输出：能看到 SYN / SYN-ACK / ACK / ... / FIN / ACK
```

**Wireshark 过滤**：`tcp.port == 80` ，右键 → 跟踪流 → TCP Stream。

---

## 1.5 HTTP 诞生记
### 1.5.1 一个英国人在 CERN 的发明
**人物**：Tim Berners-Lee（蒂姆·伯纳斯-李）  
**时间**：1989 年提案，1991 年首个版本上线  
**地点**：欧洲核子研究中心 CERN  
**目的**：让科学家之间能方便地**共享文档**

### 1.5.2 三大支柱
```mermaid
graph TB
    W["万维网 WWW"] --> URL["URL<br/>统一资源定位符<br/>「地址」"]
    W --> HTTP["HTTP<br/>超文本传输协议<br/>「语言」"]
    W --> HTML["HTML<br/>超文本标记语言<br/>「格式」"]
```

> **重要区分**：很多人混淆"互联网"和"万维网"。
>
> + **互联网 (Internet)**：全球的计算机网络（1970s 开始）
> + **万维网 (Web)**：跑在互联网上的一种应用（HTTP/HTML，1989 年才出现）
>

### 1.5.3 HTTP 版本演进
| 版本 | 年份 | 关键变化 | 性能 |
| --- | --- | --- | --- |
| HTTP/0.9 | 1991 | 只有 GET，纯文本 HTML | 单次 |
| HTTP/1.0 | 1996 | 加 Header、状态码、POST、Content-Type | 每 request 新建 TCP |
| HTTP/1.1 | 1997 | Keep-Alive、Host、分块传输、管线化 | 默认长连接 |
| HTTP/2 | 2015 | 二进制分帧、多路复用、Header 压缩 | 并发 |
| HTTP/3 | 2022 | 基于 QUIC (UDP)，无队头阻塞 | 弱网更优 |


```mermaid
graph LR
    H1["HTTP/1.1<br/>一问一答<br/>文本协议"] --> H2["HTTP/2<br/>多路复用<br/>二进制"]
    H2 --> H3["HTTP/3<br/>QUIC/UDP<br/>抗弱网"]
```

> 🎯 **渗透视角**：99% 的 Web 漏洞仍集中在 **HTTP/1.1**，因为它是事实标准，也是工具最支持的协议。HTTP/2 带来了**请求走私**的新变种。
>

---

## 1.6 URL、URI、URN 区别
```plain
URI  = 统一资源标识符 (Uniform Resource Identifier)
       ├── URL  = 定位符 (Uniform Resource Locator)   ← "地址"：在哪里
       └── URN  = 命名 (Uniform Resource Name)         ← "名字"：叫什么
```

### URL 八段结构
```plain
            userinfo       host      port
            ┌──┴──┐ ┌───┴───┐ ┌─┴─┐
https://username:password@www.example.com:8443/path/to/file.html?key=value#fragment
└─┬─┘                          └───────┬───────┘ └──────┬───────┘ └──┬──┘
scheme                               path               query      fragment
```

| 段 | 说明 | 示例 |
| --- | --- | --- |
| scheme | 协议 | http, https, ftp, file, javascript, data |
| userinfo | 用户信息（基本已弃用） | user:pass@ |
| host | 主机名 / IP | example.com / 1.1.1.1 |
| port | 端口 | 80, 443, 8080 |
| path | 路径 | /admin/login.php |
| query | 查询字符串 | ?id=1&type=2 |
| fragment | 锚点（**不发给服务器**） | #section1 |


> 🎯 **渗透视角**：
>
> + `?id=1` 这种 query 是 SQL 注入/XSS 的主要入口
> + `javascript:` scheme 是 XSS 跳板的常客
> + `file://` / `gopher://` / `dict://` 是 SSRF 利用协议
>

### URL 编码（百分号编码）
为什么需要？URL 里不能出现空格、中文、`&` `?` `#` 等保留字符。

| 字符 | 编码 |
| --- | --- |
| 空格 | `%20` 或 `+` |
| 中文"中" | `%E4%B8%AD` (UTF-8 三字节) |
| `&` | `%26` |
| `#` | `%23` |
| `'` | `%27` |
| `<` | `%3C` |


**实操**：

```bash
curl "https://www.baidu.com/s?wd=渗透测试" -G --data-urlencode "q=hello world"
```

> 🎯 **渗透视角**：**双重 URL 编码**是绕过 WAF 的经典技巧 —— `%253c` 解码一次是 `%3c`，再解码是 `<`。
>

---

## 1.7 课时 1 小结
| 关键词 | 一句话 |
| --- | --- |
| 分层 | OSI 7 层 / TCP/IP 4 层，HTTP 在最上层 |
| 寻址 | IP 找机器，端口找进程，DNS 把名字翻译成 IP |
| TCP | 3 次握手建立，4 次挥手断开 |
| HTTP 历史 | 1991 → 2022 五代演进，1.1 是事实标准 |
| URL | 8 段结构 + 百分号编码 |


### 课间思考题（10 min）
1. 浏览器输入 URL 到看到页面，列出**至少 8 步**。
2. 为什么 TCP 握手是 3 次而不是 2 次？
3. `http://localhost` 和 `http://127.0.0.1` 走的网络栈一样吗？
4. URL 编码 `%2527` 解码两次分别是什么？

---

# 第 2 课时：HTTP 报文深度剖析
## 2.1 HTTP 报文总览
HTTP 报文是**纯文本**（HTTP/1.x）或**二进制帧**（HTTP/2+），由两部分组成：

```plain
┌─────────────────────────────┐
│       起始行 / 状态行        │  ← 一行
├─────────────────────────────┤
│           Header            │  ← 多行，每行 name: value
│           Header            │
│           ...               │
├─────────────────────────────┤
│      空行 (\r\n)            │  ← 关键！Header 结束标志
├─────────────────────────────┤
│           Body              │  ← 可选
│           Body              │
└─────────────────────────────┘
```

> 💡 **重点**：**Header 和 Body 之间的空行（CRLF）是 HTTP 解析的关键**，请求走私漏洞就来自这里。
>

---

## 2.2 请求报文详解
### 2.2.1 完整示例
```http
POST /login.php HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,*/*
Accept-Language: zh-CN,zh;q=0.9
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Cookie: PHPSESSID=abc123; role=user
Connection: keep-alive
Referer: https://www.example.com/

username=admin&password=123456
```

**逐行解释**：

| 行号 | 内容 | 含义 |
| --- | --- | --- |
| 1 | `POST /login.php HTTP/1.1` | **请求行**：方法 + 路径 + 版本 |
| 2 | `Host: ...` | 目标主机（HTTP/1.1 必填，支持虚拟主机） |
| 3 | `User-Agent` | 客户端身份 |
| 4-6 | `Accept*` | 客户端想要什么 |
| 7 | `Content-Type` | Body 的格式 |
| 8 | `Content-Length` | Body 长度（字节） |
| 9 | `Cookie` | 客户端状态 |
| 10 | `Connection` | 是否复用连接 |
| 11 | `Referer` | 从哪个页面跳来的 |
| (空行) |  | 分隔 Header 和 Body |
| Body | `username=admin&password=123456` | 提交的数据 |


### 2.2.2 用 curl 看到原始请求
```bash
curl -v http://example.com/ 2>&1 | head -20
```

输出会有 `>` 开头的行（请求）和 `<` 开头的行（响应）：

```plain
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/7.88.1
> Accept: */*
>
< HTTP/1.1 200 OK
< ...
```

### 2.2.3 用 telnet 手写 HTTP 请求（神技！）
```bash
telnet example.com 80
# 连上后手动输入：
GET / HTTP/1.1
Host: example.com

# 注意：最后必须按两次回车（空行结束 Header）
```

> 💡 **重要练习**：学会用 telnet / nc 手写 HTTP 请求，可以绕过所有浏览器/curl 的"美化"，直击协议本质。
>

---

## 2.3 响应报文详解
```http
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Wed, 24 Jul 2026 10:00:00 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1256
Set-Cookie: PHPSESSID=xyz789; path=/; HttpOnly
Connection: keep-alive

<!DOCTYPE html>
<html>...</html>

```

**组成**：

1. 状态行：`HTTP/1.1 200 OK`（版本 + 状态码 + 短语）
2. 响应头
3. 空行
4. 响应体

---

## 2.4 HTTP 方法详解
| 方法 | 含义 | 幂等 | 安全 | 有 Body | 典型用途 |
| --- | --- | :---: | :---: | :---: | --- |
| **GET** | 获取资源 | ✅ | ✅ | ❌ | 看网页、搜索 |
| **POST** | 提交数据，创建 | ❌ | ❌ | ✅ | 表单提交、登录、上传 |
| **PUT** | 整体更新/创建 | ✅ | ❌ | ✅ | RESTful 更新 |
| **PATCH** | 部分更新 | ❌ | ❌ | ✅ | 修改单个字段 |
| **DELETE** | 删除 | ✅ | ❌ | 可选 | 删资源 |
| **HEAD** | 只拿 Header | ✅ | ✅ | ❌ | 探测大小 |
| **OPTIONS** | 查询支持的方法 | ✅ | ✅ | ❌ | CORS 预检 |
| **TRACE** | 回显请求 | ✅ | ❌ | ❌ | 调试（**应禁用！XST 攻击**） |
| **CONNECT** | 建立隧道 | - | - | - | HTTPS 代理 |


### 概念解析：幂等 & 安全
+ **安全 (Safe)**：不修改服务器数据（GET/HEAD/OPTIONS）
+ **幂等 (Idempotent)**：执行 N 次和 1 次效果相同（GET/PUT/DELETE）

> 🎯 **渗透视角**：
>
> + **GET 不应该改数据**——但有些开发者把删除接口写成 `GET /delete?id=1`，会被 `<img>` 偷偷触发 → 升级为 CSRF
> + **PUT/DELETE 经常被管理员接口忘记鉴权** → 越权
> + **OPTIONS 暴露** CORS 配置 → 探测内网 API
>

### 实操：测试服务器支持哪些方法
```bash
curl -X OPTIONS http://example.com/ -i
curl -X TRACE http://example.com/
curl -X PUT http://example.com/test.txt -d "hello"
curl -X DELETE http://example.com/test.txt
```

---

## 2.5 状态码全表（必须背）
```plain
1xx ── 信息
2xx ── 成功
3xx ── 重定向
4xx ── 客户端错误
5xx ── 服务端错误
```

| 码 | 短语 | 含义 | 渗透关注 |
| --- | --- | --- | --- |
| **200** | OK | 正常成功 | - |
| **201** | Created | 资源创建成功 | - |
| **204** | No Content | 成功但无内容 | - |
| **301** | Moved Permanently | 永久重定向 | 钓鱼利用 |
| **302** | Found | 临时重定向 | 登录跳转常见 |
| **304** | Not Modified | 缓存仍有效 | - |
| **307** | Temporary Redirect | 不改方法的重定向 | - |
| **308** | Permanent Redirect | 永久且不改方法 | - |
| **400** | Bad Request | 语法错误 | 请求走私探测点 |
| **401** | Unauthorized | 未认证 | **要看 WWW-Authenticate 头** |
| **403** | Forbidden | 拒绝（认证了但没权限） | 暴露目录/文件存在 |
| **404** | Not Found | 资源不存在 | 目录爆破判断 |
| **405** | Method Not Allowed | 方法不允许 | 换方法试试 |
| **413** | Payload Too Large | 数据太大 | DoS 测试点 |
| **429** | Too Many Requests | 限流 | WAF/风控信号 |
| **500** | Internal Server Error | 服务端异常 | **报错信息泄露** |
| **502** | Bad Gateway | 网关错误 | 反代后端挂了 |
| **503** | Service Unavailable | 服务不可用 | 被限流/维护 |
| **504** | Gateway Timeout | 网关超时 | 后端慢 |


> 🎯 **渗透口诀**：
>
> + **200 vs 403 vs 404**：判断资源是否存在 → 目录爆破依据
> + **500**：报错里常泄露**绝对路径 / SQL 语句 / 框架版本**
> + **302 跳转**：未登录跳登录页 → 鉴权逻辑分析
>

### 实操：触发各种状态码
```bash
curl -i http://httpbin.org/status/200
curl -i http://httpbin.org/status/403
curl -i http://httpbin.org/status/500
curl -i http://example.com/non-existent-page   # 404
```

---

## 2.6 Header 大全
### 2.6.1 通用头（请求响应都有）
| Header | 含义 | 示例 |
| --- | --- | --- |
| `Cache-Control` | 缓存策略 | `no-cache, no-store, must-revalidate` |
| `Connection` | 连接管理 | `keep-alive` / `close` |
| `Date` | 时间 | `Wed, 24 Jul 2026 10:00:00 GMT` |
| `Transfer-Encoding` | 传输编码 | `chunked` |
| `Upgrade` | 升级协议 | `h2c`, `websocket` |


### 2.6.2 请求头（重点关注！）
| Header | 含义 | 渗透关注 |
| --- | --- | --- |
| `Host` | 目标主机（虚拟主机判断） | **Host 头攻击、内网访问、缓存投毒** |
| `User-Agent` | 客户端身份 | UA 注入（写入数据库/日志 → XSS/SQLi） |
| `Referer` | 来源页面 | CSRF 防御、广告追踪 |
| `Cookie` | 客户端状态 | **会话劫持的核心** |
| `Authorization` | 凭证 | Basic/JWT 窃取 |
| `X-Forwarded-For` | 代理 IP 链 | **IP 伪造绕过** |
| `X-Real-IP` | 真实 IP | 同上 |
| `Origin` | CORS 来源 | 跨域判断 |
| `Accept` | 接受类型 | - |
| `Accept-Language` | 语言 | - |
| `Accept-Encoding` | 编码 | - |
| `If-None-Match` | 缓存校验 | - |
| `If-Modified-Since` | 缓存校验 | - |
| `Range` | 断点续传 | 服务器不一致 → 信息泄露 |


#### 重点：X-Forwarded-For 伪造
```bash
# 服务端可能记录"用户 IP"
curl -H "X-Forwarded-For: 127.0.0.1" http://target.com/admin
curl -H "X-Real-IP: 127.0.0.1" http://target.com/
curl -H "X-Original-URL: /admin" http://target.com/
```

> 🎯 很多后端直接信任 `X-Forwarded-For`，可借此**伪造 IP** 绕过频率限制或访问控制。
>

### 2.6.3 响应头（重点关注！）
| Header | 含义 | 渗透关注 |
| --- | --- | --- |
| `Server` | 服务器类型/版本 | **指纹识别** |
| `X-Powered-By` | 后端语言/框架 | **指纹识别** |
| `Set-Cookie` | 设置 Cookie | 看 `HttpOnly` / `Secure` / `SameSite` |
| `Location` | 重定向地址 | 开放重定向 |
| `WWW-Authenticate` | 认证方式 | Basic/Digest |
| `Access-Control-Allow-Origin` | CORS | **跨域敏感信息泄露** |
| `Content-Disposition` | 下载文件名 | 文件名注入 |
| `ETag` | 资源指纹 | - |
| `Vary` | 缓存键 | 缓存投毒 |


### 2.6.4 安全响应头（必考）
| Header | 防什么 | 推荐值 |
| --- | --- | --- |
| `Content-Security-Policy` | XSS / 数据注入 | `default-src 'self'` |
| `Strict-Transport-Security` | 协议降级（HSTS） | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | 点击劫持 | `DENY` |
| `X-Content-Type-Options` | MIME 嗅探 | `nosniff` |
| `Referrer-Policy` | Referer 泄露 | `no-referrer` |
| `Permissions-Policy` | 浏览器特性 | `camera=(), microphone=()` |


---

## 2.7 Cookie、Session、Token（重点中的重点）
### 2.7.1 为什么需要它们？
HTTP 是**无状态协议**——服务器不记得你上次干了什么。但登录、购物车都需要"记住"，所以需要**会话管理**。

### 2.7.2 Cookie 详解
```plain
服务器 ──Set-Cookie──► 浏览器（保存到磁盘）
浏览器 ──Cookie────► 服务器（每次请求自动带上）
```

**Set-Cookie 完整语法**：

```plain
Set-Cookie: name=value; Domain=example.com; Path=/;
            Expires=Wed, 24 Jul 2026 12:00:00 GMT;
            Max-Age=3600; Secure; HttpOnly; SameSite=Strict
```

| 属性 | 含义 | 渗透关注 |
| --- | --- | --- |
| `Domain` | 生效域名 | 范围太宽 → 子域 Cookie 互窜 |
| `Path` | 生效路径 | - |
| `Expires` / `Max-Age` | 过期时间 | 持久 Cookie |
| `Secure` | 仅 HTTPS 传输 | 缺失 → 中间人可窃 |
| `HttpOnly` | JS 不能读 | **防 XSS 偷 Cookie** |
| `SameSite` | 跨站发送策略 | **防 CSRF**：Strict / Lax / None |


**SameSite 三档**：

| 值 | 行为 | CSRF 防护 |
| --- | --- | --- |
| `Strict` | 完全不带 | 强 |
| `Lax`（默认） | 顶层 GET 导航带 | 中 |
| `None` | 都带（必须 Secure） | 弱 |


### 2.7.3 Session 机制
```plain
1. 用户登录：username=admin&password=xxx
2. 服务端验证通过 → 生成 sessionId
3. 通过 Set-Cookie: PHPSESSID=xxx 返回
4. 后续请求浏览器自动带 Cookie: PHPSESSID=xxx
5. 服务端按 sessionId 查内存/Redis 找到对应用户
```

> 🎯 **渗透视角**：
>
> + **会话劫持**：偷到 sessionId = 偷到登录态
> + **会话固定**：登录前后 sessionId 不变 → 攻击者预先植入自己的 sessionId
> + **会话预测**：sessionId 是自增/弱随机 → 可猜测
> + **Session 过期不当**：注销后服务端没删 sessionId → 旧 Cookie 仍可用
>

### 2.7.4 Token（特别是 JWT）
**JWT 结构**（3 段，用 `.` 分隔）：

```plain
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9      ← Header (Base64)
.
eyJzdWIiOiIxMjM0IiwibmFtZSI6IkFsaWNlIn0   ← Payload (Base64)
.
SflKxwRJSMeKKF2QT4fwpX...                  ← Signature
```

**Header**：

```json
{"alg": "HS256", "typ": "JWT"}
```

**Payload**：

```json
{"sub": "1234", "name": "Alice", "role": "admin", "exp": 1735689600}
```

**Signature**：

```plain
HMAC-SHA256(base64(header) + "." + base64(payload), secret_key)
```

> 🎯 **JWT 常见漏洞**：
>
> + `alg: none` 攻击：删除签名，服务器不验证
> + 弱密钥爆破：`hashcat -m 16500 jwt.txt rockyou.txt`
> + 算法混淆：RS256 → HS256，用公钥当 HMAC 密钥
> + `kid` 注入：路径遍历 / SQL 注入
>

### 2.7.5 Cookie vs Session vs Token 对比
| 维度 | Cookie | Session | Token (JWT) |
| --- | --- | --- | --- |
| 存储位置 | 浏览器 | 服务端 | 客户端 |
| 状态 | 无状态 | **有状态** | **无状态** |
| 扩展性 | 好 | 差（要共享） | 好 |
| 撤销 | 删 Cookie 即可 | 服务端删 sessionId | 难（需黑名单） |
| 安全 | 中 | 较高 | 取决于实现 |


---

## 2.8 HTTP Body 与 Content-Type
### 2.8.1 常见 Content-Type
| 类型 | 用途 | 示例 |
| --- | --- | --- |
| `application/x-www-form-urlencoded` | 普通表单 | `a=1&b=2` |
| `multipart/form-data` | 文件上传 | 带边界 |
| `application/json` | API | `{"a":1,"b":2}` |
| `application/xml` | SOAP / XXE | `<xml>...` |
| `text/plain` | 纯文本 | - |
| `text/html` | 网页 | - |


### 2.8.2 三种 Body 示例
**表单**：

```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

username=admin&password=123
```

**JSON**：

```http
POST /api/login HTTP/1.1
Content-Type: application/json
Content-Length: 38

{"username":"admin","password":"123"}
```

**文件上传**：

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: application/octet-stream

<?php system($_GET['cmd']); ?>
------WebKitFormBoundary--
```

> 🎯 **渗透视角**：
>
> + 同一接口支持多种 Content-Type → WAF 可能只检查一种 → **Content-Type 绕过**
> + 服务器按 `Content-Type` 选解析器 → JSON 转 form 转换可能绕过过滤
>

### 2.8.3 Transfer-Encoding: chunked（分块传输）
当不知道 Body 多长时，可以分块发送：

```http
POST /api HTTP/1.1
Transfer-Encoding: chunked

4
Wiki
5
pedia
0

```

每段是 `[字节数十六进制]\r\n[数据]\r\n`，最后 `0\r\n\r\n` 结束。

> 🎯 **渗透视角**：**请求走私 (Request Smuggling)** 的核心 —— 当前后端代理对 `Content-Length` vs `Transfer-Encoding` 的处理不一致时，可以"偷偷夹带"一个请求。
>

---

## 2.9 课时 2 小结
| 模块 | 要点 |
| --- | --- |
| 报文结构 | 起始行 + Header + 空行 + Body |
| 方法 | 9 种，重点 GET/POST/PUT/DELETE/OPTIONS |
| 状态码 | 5 大类，记住 200/301/302/400/401/403/404/500 |
| Header | Host/Cookie/X-Forwarded-For 是渗透重灾区 |
| 安全头 | CSP / HSTS / X-Frame-Options / HttpOnly / SameSite |
| 会话 | Cookie → Session → JWT 演进 |


### 课间实操题（15 min）
1. 用 `telnet` 手写一个 GET 请求，拿到 baidu.com 首页。
2. 用 `curl -v` 观察访问 `https://example.com` 的完整请求/响应。
3. 触发一个 `405` 和一个 `500`。
4. 用 `curl -H "X-Forwarded-For: 1.1.1.1"` 访问 [httpbin.org/ip](https://httpbin.org/ip)，观察返回。

---



# 第 3 课时：HTTPS 与 Web 安全基础
## 3.1 为什么 HTTP 不安全？
### 3.1.1 HTTP 的三大原罪
```plain
明文传输      ──►  被窃听
无完整性校验   ──►  被篡改
无身份验证     ──►  被冒充
```

### 3.1.2 经典场景：咖啡厅里的攻击者
```plain
┌────────┐         ┌──────────────┐         ┌──────────┐
│  你    │ ──明文─► │  攻击者(咖啡厅)│ ──明文─► │ 银行服务器 │
└────────┘         └──────────────┘         └──────────┘
                      │
                      ▼
                  偷密码、改页面、
                  假装是银行（中间人）
```

> 攻击者可以：
>
> + **窃听**：拿到你的账号密码
> + **篡改**：把"转账给张三 100 元"改成"转账给李四 10000 元"
> + **冒充**：假装是银行服务器，骗你输入密码
>

---

## 3.2 密码学三大基石（零基础也要懂）
### 3.2.1 哈希 (Hash)
**特点**：单向、定长、雪崩、抗碰撞

```plain
任意长度输入 ──哈希函数──► 固定长度输出（指纹）

MD5("hello")   = 5d41402abc4b2a76b9719d911017c592
SHA256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

| 算法 | 输出长度 | 状态 |
| --- | --- | --- |
| MD5 | 128 bit | **已破，不可用于安全场景** |
| SHA-1 | 160 bit | **已破** |
| SHA-256 | 256 bit | 安全 |
| SHA-512 | 512 bit | 安全 |


> 🎯 **用途**：密码存储（+salt）、文件完整性、数字签名。  
**彩虹表破解**：md5(`123456`) = `e10adc...`，预先算好的表能秒查。
>

### 3.2.2 对称加密
```plain
密钥 K（同一把）── 加密 ──►  密文 ── 解密（同一把 K） ──►  原文

[AES_密钥]                        [AES_密钥]
   │ 密文 ╳═══════════════════════════╳ │
   ▼                                  ▼
 加密方                              解密方
```

| 算法 | 类型 | 速度 |
| --- | --- | --- |
| AES-128/256 | 分组 | 快，标准 |
| ChaCha20 | 流 | 快，移动端 |
| DES / 3DES | 分组 | **已淘汰** |
| RC4 | 流 | **已破** |


> **优点**：快。**缺点**：双方都得有密钥，**怎么把密钥安全送给对方？**
>

### 3.2.3 非对称加密
```plain
公钥 (Public Key) ──► 公开给所有人
私钥 (Private Key) ──► 只自己留着

公钥加密 ──► 私钥才能解密      （加密场景）
私钥签名 ──► 公钥才能验证      （签名场景）
```

| 算法 | 类型 | 用途 |
| --- | --- | --- |
| RSA | 大数分解 | 加密 + 签名 |
| ECC | 椭圆曲线 | 同等安全更短的密钥 |
| DSA | 离散对数 | 仅签名 |


> **优点**：解决密钥分发问题。**缺点**：慢，比对称慢 100~1000 倍。
>

### 3.2.4 三种加密怎么配合？
**混合加密**（HTTPS 就是这么做的）：

```plain
1. 非对称加密协商出"对称密钥"   ← 慢，但只需一次
2. 对称密钥加密后续数据          ← 快，大量数据
3. 哈希 + 签名验证身份           ← 防伪
```

---

## 3.3 数字证书与 CA
### 3.3.1 中间人攻击的威胁
```plain
你 ──公钥──► 攻击者替换成自己的公钥 ──► 银行
                    ▲
              "我怎么知道这公钥真的是银行的？"
```

### 3.3.2 解决方案：CA（证书颁发机构）
> CA 是受信任的第三方，**用它的私钥给银行签名**，证明"这个公钥确实是银行的"。
>

**证书内容**：

+ 持有者域名（CN / SAN）
+ 持有者公钥
+ 有效期
+ 颁发者（CA）
+ CA 的数字签名

### 3.3.3 信任链
```plain
根 CA (Root) ── 自签名，预装在操作系统/浏览器
  │
  └─ 中级 CA ── 由根 CA 签发
       │
       └─ 终端证书 (你的网站)
```

**验证过程**：

1. 服务器发来终端证书 + 中级证书
2. 浏览器用中级 CA 公钥验终端证书签名
3. 用根 CA 公钥验中级证书签名
4. 根 CA 在系统信任列表 → 信任

> 🎯 **渗透视角**：
>
> + **自签名证书**：浏览器红警告，但内部系统常在用
> + **弱签名算法**：MD5 / SHA-1 签名证书可伪造
> + **Heartbleed**：直接偷服务器私钥
> + **证书透明度 (CT)**：CT Log 可查某域名所有历史证书
>

### 3.3.4 实操：查看证书
```bash
# 命令行看证书
openssl s_client -connect www.baidu.com:443 -servername www.baidu.com </dev/null

# 详细看
echo | openssl s_client -connect www.baidu.com:443 -showcerts 2>/dev/null | openssl x509 -noout -text
```

浏览器：点地址栏小锁 → 证书。

---

## 3.4 TLS 握手详解（TLS 1.2）
```plain
客户端                                     服务端
  │                                          │
  │ ──── ClientHello ────────────────────►   │  ① 我支持这些加密套件 + 随机数 A
  │                                          │
  │   ◄──────── ServerHello ────────────     │  ② 选这个套件 + 随机数 B
  │   ◄──────── Certificate ────────────     │     发证书
  │   ◄──────── ServerHelloDone ─────────    │
  │                                          │
  │ ──── ClientKeyExchange ──────────────►   │  ③ 用公钥加密"预主密钥"
  │ ──── ChangeCipherSpec ───────────────►   │     切换到加密
  │ ──── Finished (加密) ────────────────►   │
  │                                          │
  │   ◄──────── ChangeCipherSpec ───────     │  ④ 我也切换
  │   ◄──────── Finished (加密) ─────────    │
  │                                          │
  │ ════════ 双向加密通信开始 ════════════════│
```

**密钥生成**：

```plain
master_secret = PRF(pre_master_secret, "master secret",
                    ClientHello.random + ServerHello.random)
```

> 三份随机数确保每次会话密钥都不同。
>

### TLS 1.3 的进化
+ 握手从 2 个 RTT 缩短到 1 个 RTT（甚至 0-RTT 恢复）
+ 强制使用**前向加密** (Forward Secrecy)：会话密钥不依赖服务器私钥
+ 删除了不安全算法（RSA 密钥交换、SHA-1、MD5、RC4、3DES）

> **前向加密的好处**：即使攻击者今天录下所有密文，**明天拿到服务器私钥也解不开**——因为会话密钥是用临时 DH/ECDH 协商的，不在传输里。
>

---

## 3.5 HTTPS 抓包原理（中间人代理）
### 3.5.1 为什么 Burp 能抓 HTTPS？
```plain
浏览器 ──HTTPS──► Burp ──HTTPS──► 真服务器
   ▲                              │
   │                              │
   └─ Burp 用自签证书冒充服务器 ◄─┘
       (你要信任 Burp 的根证书)
```

### 3.5.2 配置步骤
1. **Burp Suite → Proxy → Options**：默认监听 `127.0.0.1:8080`
2. **浏览器代理设置**：HTTP 代理 → `127.0.0.1:8080`
3. **导入 Burp 证书**：
    - 浏览器访问 `http://burp`
    - 下载 `cacert.der`
    - 导入到浏览器的"受信任根证书颁发机构"
4. 浏览 HTTPS 站点，Burp 既能看明文也能改

> ⚠️ **证书安全警告**：培训结束后**务必删除** Burp 根证书，否则同咖啡厅黑客能拦截你所有 HTTPS！
>

### 3.5.3 移动端抓包
```mermaid
graph LR
    APP[手机 App] --> Burp[Burp<br/>同 WiFi 电脑]
    Burp --> Server[服务器]
```

1. 电脑与手机同一 WiFi
2. Burp 设置监听 `0.0.0.0:8080`
3. 手机 WiFi 代理 → 电脑 IP:8080
4. 手机浏览器访问 `http://电脑IP:8080/cert` 下载证书
5. 安装为系统证书（Android 7+ 需 root，否则只能装用户证书）

> 🎯 **渗透视角**：
>
> + **SSL Pinning**：App 写死了证书指纹，不信任系统证书 → 抓包失败 → 需 Frida / objection 绕过
> + **双向 TLS (mTLS)**：服务器也校验客户端证书 → 需从 App 提取客户端证书
>

---

## 3.6 安全响应头实战
### 3.6.1 HSTS（HTTP Strict Transport Security）
```plain
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**作用**：告诉浏览器"以后只准用 HTTPS 访问我"，**抵御第一次的重定向劫持**。

### 3.6.2 CSP（Content Security Policy）
```plain
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.jsdelivr.net;
  style-src 'self' 'unsafe-inline';
  img-src *;
  connect-src 'self' https://api.example.com;
```

**作用**：白名单限制各类资源加载来源，**核心防 XSS**。

> 🎯 **绕过 CSP 的思路**：
>
> + `'unsafe-inline'` → 直接执行内联 JS
> + 上传 JS 文件到白名单域 → 利用 angular/moustache 模板注入
> + `dns-prefetch` 带外数据外带
>

### 3.6.3 其他安全头一览
```plain
X-Frame-Options: DENY                    ← 防点击劫持
X-Content-Type-Options: nosniff          ← 防 MIME 嗅探
Referrer-Policy: no-referrer             ← 防 Referer 泄露
Permissions-Policy: geolocation=()       ← 禁用浏览器特性
Cross-Origin-Opener-Policy: same-origin  ← 防 Spectre 类
```

### 3.6.4 实操：观察安全头
```bash
# 一键看所有响应头
curl -I https://www.github.com/

# 专业工具：securityheaders.com
```

---

## 3.7 课时 3 小结
| 模块 | 要点 |
| --- | --- |
| HTTP 三大原罪 | 明文、无完整性、无身份 |
| 加密三件套 | 哈希、对称、非对称 |
| 信任机制 | CA + 证书 + 信任链 |
| TLS 握手 | 4 步交换随机数 + 协商密钥 |
| 抓包原理 | 中间人 + 自签根证书 |
| 安全头 | HSTS / CSP / X-Frame-Options 等 |


### 课间思考题（10 min）
1. 为什么 TLS 握手需要"3 个随机数"？
2. 前向加密是什么意思？为什么 RSA 密钥交换没有前向加密？
3. 为什么 Burp 抓 HTTPS 不报警告？
4. 一个网站只配 HSTS 没配 CSP，能防住反射型 XSS 吗？

---

# 第 4 课时：渗透视角下的 HTTP 实战
## 4.1 Burp Suite 入门（核心工具）
### 4.1.1 界面与核心模块
```mermaid
graph TB
    Burp[Burp Suite] --> Proxy[Proxy 代理<br/>抓包/改包]
    Burp --> Repeater[Repeater 重放<br/>反复试 payload]
    Burp --> Intruder[Intruder 暴力枚举<br/>批量 fuzz]
    Burp --> Decoder[Decoder 编解码]
    Burp --> Comparer[Comparer 差异对比]
    Burp --> Scanner[Scanner 漏洞扫描<br/>社区版受限]
```

### 4.1.2 第一次抓包流程
1. 启动 Burp → Proxy → Intercept is on
2. 浏览器配代理 `127.0.0.1:8080`
3. 浏览器访问 [http://ginwan.com](http://ginwan.com)（任意靶场）
4. Burp 拦截到请求 → 右键 → **Send to Repeater**
5. Repeater 里点 **Send** 看响应

### 4.1.3 实操：修改请求
```http
# 原始
GET /profile?id=1001 HTTP/1.1
Cookie: session=user_1001

# 改成
GET /profile?id=1002 HTTP/1.1       ← 改 ID（测试越权！）
Cookie: session=user_1001
```

> 🎯 **这就是越权 (IDOR) 漏洞测试的本质**：用合法登录的 Cookie + 别人的 ID。
>

---

## 4.2 HTTP 请求走私 (Request Smuggling)
### 4.2.1 漏洞原理
```plain
浏览器 ──► 前端代理 (Nginx/CDN) ──► 后端服务器 (Tomcat/Node)

前端代理按 Content-Length 解析
后端服务器按 Transfer-Encoding 解析
                 ▼
        两者对"Body 边界"判断不一致
                 ▼
        攻击者可以"偷偷夹带"下一个请求
```

### 4.2.2 经典 CL-TE 漏洞
```http
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

+ 前端代理看 `Content-Length: 13`，把整段（包括 `SMUGGLED`）发给后端
+ 后端看 `Transfer-Encoding: chunked`，遇到 `0\r\n\r\n` 就结束
+ `SMUGGLED` 被**当成下一个请求的开头**！

### 4.2.3 危害
+ **绕过前端安全控制**：前端 WAF 只检查第一个请求，第二个请求直接穿透
+ **窃取其他用户请求**：注入的请求头会污染下一个用户的请求
+ **缓存投毒**：把恶意响应写进共享缓存

> 🎯 **真实案例**：2019 年 James Kettle 在顶级厂商中发现大量此漏洞（[HTTP Desync Attack](https://portswigger.net/research/http-desync-attacks)）。
>

---

## 4.3 HTTP/2 速览
### 4.3.1 关键变化
```plain
HTTP/1.1：文本协议，串行请求
   GET /a
   GET /b   （要等 /a 完成，或开多个 TCP 连接）

HTTP/2：二进制分帧，多路复用
   一个 TCP 连接里，多个请求并发
```

| 特性 | HTTP/1.1 | HTTP/2 |
| --- | --- | --- |
| 格式 | 文本 | 二进制 |
| 多路复用 | ❌ | ✅ |
| Header 压缩 (HPACK) | ❌ | ✅ |
| 服务端推送 | ❌ | ✅ |
| 请求优先级 | ❌ | ✅ |


### 4.3.2 HTTP/2 的新攻击面
+ **H2C 走私**：HTTP/1.1 → HTTP/2 升级时的走私
+ **HPACK 状态机滥用**：DoS
+ **协议降级攻击**：HTTP/3 → HTTP/2 → HTTP/1.1 降级链

---

## 4.4 综合 Lab：4 小时通关项目
### Lab 4.1：手工 HTTP 请求大师
```bash
# 用 telnet/nc 手写请求
nc example.com 80
GET / HTTP/1.1
Host: example.com
[空行]
```

**任务**：

- [ ] 不带 `Host` 头会怎样？
- [ ] 发个超大 Header 会怎样？
- [ ] 用 `TRACE` 方法会怎样？
- [ ] 故意发个错误的 HTTP 版本号？

### Lab 4.2：Burp 抓包改包
**靶场**：DVWA（参考前序课件）

```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```

**任务**：

- [ ] 用 Burp 拦截 DVWA 登录请求，分析每个 Header
- [ ] 把 `User-Agent` 改成 `<script>alert(1)</script>`，观察日志
- [ ] 改 Cookie 中的 `security` 字段：`high` → `low`（绕过安全等级）
- [ ] 把 GET 改成 POST，看服务器反应

### Lab 4.3：状态码与指纹
```bash
# 1. 指纹识别
curl -I https://www.taobao.com/
# 关注：Server / X-Powered-By / Set-Cookie / X-Tengine

# 2. 目录爆破
# (需要授权环境！)
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302,401,403
```

**任务**：

- [ ] 列出淘宝用的 Web 服务器、负载均衡、CDN
- [ ] 解释每个安全响应头的含义
- [ ] 比较不同网站（银行 / 政府 / 招聘）的安全头完整度

### Lab 4.4：HTTPS 证书分析
```bash
# 一键检查
openssl s_client -connect www.github.com:443 -servername www.github.com < /dev/null 2>&1 | openssl x509 -noout -text | head -50
```

**任务**：

- [ ] GitHub 用的 CA 是哪家？
- [ ] 证书有效期多长？为什么？
- [ ] 找一个用 SHA-1 签名的旧证书（提示：搜国内某些政府站）
- [ ] 解释为什么证书最大有效期从 5 年缩到 1 年（398 天）

### Lab 4.5：综合报告（毕业作业）
任选一个公开 SRC 授权范围（如补天平台的教育公益漏洞），完整产出：

1. **HTTP 请求分析**：用 Burp 抓 5 个不同功能点的请求，标注每个 Header 的作用
2. **指纹识别**：服务器、框架、CMS、CDN 各是什么
3. **安全头评估**：列出缺失的安全响应头，给出补全建议
4. **证书体检**：算法、有效期、链是否完整
5. **攻击面初探**：未授权接口 / 目录爆破 / 越权点候选

**报告模板**：

```markdown
# HTTP 分析报告

## 1. 目标信息
- URL: ...
- IP: ...
- 服务器: nginx 1.18

## 2. 关键请求
### 2.1 登录
[贴抓包]

## 3. 安全头评估
| Header | 存在 | 建议值 |
|--------|------|-------|
| CSP | ❌ | ... |

## 4. 证书
...

## 5. 攻击面
- /admin (403) → 越权候选
- /api/v1/users (401) → 认证绕过候选
```

---

## 4.5 课时 4 小结
| 模块 | 要点 |
| --- | --- |
| Burp | Proxy → Repeater → Intruder 三件套 |
| 走私 | CL-TE / TE-CL / H2C |
| HTTP/2 | 二进制多路复用，新走私变种 |
| 实战 | 抓包 → 改包 → 重放 → 推理 |


---

# 附录 A：必背 Header 速查表
## 请求头（10 个高频）
```plain
Host                    目标主机
User-Agent              客户端身份
Cookie                  会话凭证
Authorization           认证凭证（Basic/Bearer）
Referer                 来源页面
Origin                  CORS 来源
X-Forwarded-For         代理 IP 链
X-Requested-With        是否 AJAX
Content-Type            Body 类型
Content-Length          Body 长度
```

## 响应头（10 个高频）
```plain
Server                  服务器指纹
Set-Cookie              设置 Cookie
Location                重定向地址
WWW-Authenticate        认证要求
Content-Type            响应类型
Content-Length          响应长度
ETag                    资源指纹
Cache-Control           缓存策略
Access-Control-Allow-Origin  CORS 策略
Strict-Transport-Security    HSTS
```

---

# 附录 B：命令速查
```bash
# 抓包
curl -v https://example.com/
curl -i https://example.com/        # 只看响应头
curl -X POST -d "a=1&b=2" https://example.com/
curl -H "X-Forwarded-For: 1.1.1.1" https://example.com/
curl --cookie "session=abc" https://example.com/
curl -k https://self-signed.example.com/   # 忽略证书

# 端口/连接
nc -vz example.com 80
telnet example.com 80
tcpdump -i any -n port 80

# DNS
dig example.com
dig +trace example.com
nslookup example.com 8.8.8.8

# TLS
openssl s_client -connect example.com:443
nmap --script ssl-cert -p 443 example.com
testssl.sh example.com

# 编解码
echo "hello" | base64                # 编码
echo "aGVsbG8=" | base64 -d          # 解码
python3 -c "import urllib.parse; print(urllib.parse.quote('hello world'))"
```

---

# 附录 C：推荐资源
| 类型 | 资源 | 用途 |
| --- | --- | --- |
| 官方规范 | RFC 7230-7235 (HTTP/1.1) | 查最权威定义 |
| RFC 7540 | HTTP/2 | 同上 |
| 在线练习 | [PortSwigger Web Academy](https://portswigger.net/web-security) | 免费、官方、体系完整 |
| 工具 | Burp Suite / Wireshark / curl / tcpdump | 必装 |
| 书 | 《HTTP 权威指南》 | 厚但全 |
| 书 | 《图解 HTTP》 | 入门首选 |
| 网站 | [Mozilla MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP) | 查 Header 用 |


---

# 课后作业（提交截止：下次课前）
1. **基础题**：默写 HTTP 请求报文结构，每个部分举例说明。
2. **状态码题**：列出 5 个你能在真实网站中触发的非 2xx 状态码，写出触发 URL 和原因。
3. **实操题**：用 telnet 手写一个 GET 请求，贴出完整请求 + 响应。
4. **分析题**：选一个真实网站（如学校教务系统），完成附录 B Lab 4.5 的报告。
5. **思考题**：HTTP/2 多路复用解决了队头阻塞吗？为什么又有 HTTP/3？

---

# 课程回顾（必背 30 条）
1. OSI 7 层 / TCP/IP 4 层 / HTTP 在应用层
2. TCP 三次握手：SYN, SYN+ACK, ACK
3. TCP 四次挥手：FIN, ACK, FIN, ACK
4. URL = scheme://userinfo@host:port/path?query#fragment
5. 百分号编码：空格 = `%20`，`'` = `%27`
6. HTTP 报文 = 起始行 + Header + 空行 + Body
7. GET 安全且幂等，POST 不幂等
8. 状态码 5 类：1xx 信息/2xx 成功/3xx 重定向/4xx 客户端错/5xx 服务端错
9. 401 是未认证，403 是无权限
10. Host 头是 HTTP/1.1 强制要求
11. X-Forwarded-For 可伪造，需谨慎使用
12. Cookie 三大安全属性：Secure / HttpOnly / SameSite
13. Session 是有状态，JWT 是无状态
14. JWT 三段：Header.Payload.Signature
15. JWT `alg:none` 是经典攻击
16. HTTP 三大原罪：明文、无完整性、无身份
17. 哈希单向、对称快但密钥分发难、非对称慢但解决分发
18. HTTPS = HTTP + TLS，混合加密
19. CA 颁发证书，根 CA 预装在系统/浏览器
20. TLS 1.2 握手 4 步，TLS 1.3 只要 1 RTT
21. 前向加密：私钥泄露不影响历史会话
22. Burp 抓 HTTPS = 中间人 + 自签证书
23. CSP 防 XSS，HSTS 防降级
24. X-Frame-Options 防点击劫持
25. Burp 三件套：Proxy / Repeater / Intruder
26. 越权 (IDOR) 测试：合法 Cookie + 别人 ID
27. 请求走私源于前后端 Body 边界判断不一致
28. HTTP/2 二进制 + 多路复用 + HPACK
29. 双重 URL 编码可绕 WAF
30. **授权是底线，靶场是家园**
