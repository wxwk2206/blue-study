# RouteVulScan —— 递归式被动路径探测的 Burp 插件

> 项目地址：[https://github.com/F6JO/RouteVulScan/](https://github.com/F6JO/RouteVulScan/)
> 语言：Java（基于 Burp Suite API），2026-07-10 已重构为 Maven 工程
> 作者：F6JO（合作者 @deep0，规则贡献 @r0fus0d，参考项目 HaE）

---

## 一、它是什么（概括 → 比喻 → 细节）

**概括**
RouteVulScan 是一个基于 Burp Suite API 用 Java 写的**被动扫描插件（passive scanner extension）**，核心能力是**递归式探测"脆弱路径"**——那些不固定在某一层、藏得很深的低危/易漏接口（Spring Actuator、Swagger、`.git` 泄露等）。

**比喻**
想象你拿到一栋楼（目标站点）的访客记录。普通路径爆破像挨家挨户砸每一扇门；RouteVulScan 聪明在——它顺着你已经走过的"楼层结构"（流量里的 URL 路径层级），在每一层都顺手敲一遍那几个"危险房间"的门。既不多发请求，又能覆盖任意楼层。

**细节（工作原理）**
- 基于 `IScannerCheck` 接口做**被动扫描**：流量首次经过 Burp 时才扫，重复流量不扫（省带宽、不惊动 WAF）。
- **递归路径拼接**：对请求 `/aaa/bbb`，以 `/`、`/aaa/`、`/aaa/bbb/` 为基址，分别拼上规则里的探测路径去发请求。例如规则 `/actuator/env`，实际可能打 `/aaa/actuator/env`——这就是"脆弱端点可能在任意层"痛点的解法。
- 对响应用**正则匹配**关键字，命中后在 `VulDisplay` 面板展示。带点后缀的静态资源路径会跳过。
- 用**线程池**提速（默认 10 线程，最多等于规则数）。

---

## 二、与 HaE 的区别（重点：会不会多发包）

**结论：HaE 一个包都不发（纯被动）；RouteVulScan 会多发数据包（主动探测）。** 两者名字都带"被动"，但含义不同。

> 关键误区：Burp 里的"被动扫描（passive scanning）"指通过 `IScannerCheck` 接口注册、随流量自动**触发**的扫描方式。被动扫描器**照样可以发请求**——RouteVulScan 就是典型。HaE 连发请求那步都不干，只在已有响应上跑正则。

| 维度 | HaE | RouteVulScan |
|------|-----|--------------|
| 是否发新包 | ❌ 不发（纯被动） | ✅ 发（主动探测） |
| "被动"含义 | 不触发任何新请求 | 流量触发 + 基于 host/path 发新请求 |
| 发现能力 | 只能"看到"已存在的响应 | 能"探出"未公开暴露的端点 |
| 典型用途 | 提取手机号/身份证/JWT/API Key | 找 Actuator / Swagger / `.git` 泄露 |
| 流量代价 | 0 | 规则数 × 路径层数（默认 10 线程） |

**RouteVulScan 多发多少包**
拿到请求 `https://x.com/aaa/bbb` 后：
1. 拆基址层：`/`、`/aaa/`、`/aaa/bbb/`
2. 每条规则（如 `/actuator/env`、`/swagger-ui.html`）拼到每层基址发 GET
3. 响应用正则匹配，命中进 `VulDisplay`

多发包量 ≈ **（启用的规则数）×（路径层数）**。

---

## 三、关键能力

| 能力 | 说明 |
|------|------|
| Start / Head 开关 | 主开关（默认关）；Head 决定是否带原始请求头（默认开，绕过部分鉴权） |
| Filter_Host 白名单 | 多行 host 白名单，`*.baidu.com` 通配，只扫目标站 |
| 模板标记（template tags） | 规则里可用 `{{request.head.cookie}}`、`{{request.head.host.main}}` 等动态取请求/响应字段当路径或正则 |
| 状态码范围 | 如 `200-299,500-599,302`，逗号分隔多段 |
| 主动扫描 | 右键请求 → 发送到插件，把站点地图里同 host 的历史路径全扫一遍 |
| 规则可分类/可选 | 每条规则可开关、可按 type 分类 |

**模板标记速查**
```
请求：{{request.head.*}}  {{request.head.cookie}}  {{request.head.host.main}}  {{request.head.host.name}}
      {{request.method}}  {{request.path}}  {{request.url}}  {{request.protocol}}  {{request.port}}
响应：{{response.head.*}}  {{response.head.server}}  {{response.status}}
```

---

## 四、内置规则覆盖的漏洞类型（节选）

| 类别 | 例子 |
|------|------|
| Spring 风险 | `/actuator/env`（Env RCE）、Jolokia RCE、Spring Actuator |
| API 文档泄露 | Swagger / `api-docs` / `doc.html` / SOAP / Web API Help |
| 信息泄露 | `.git`、`.svn`、`.DS_Store`、`.idea`、`robots.txt`、`README.md` |
| 未授权后台 | Druid Monitor、Nacos、XXL-JOB、Kibana、Jenkins、Solr、Elasticsearch |
| 编辑器 | UEditor / CKFinder 各类 controller 端点 |
| 中间件 CVE | Weblogic CVE-2019-2618 / 2020-14882、Kibana CVE-2019-7609 等（默认关） |

> 配置文件：`~/.config/RouteVulScan/Config_yaml.yaml`（macOS/Linux），默认规则已内置，首次运行自动初始化。

---

## 五、适用场景 & 局限

- ✅ 适合用 Burp 测站时"顺手"发现易忽略的暴露面，尤其 Java/Spring 栈。
- ⚠️ 本质是**指纹/暴露面发现**，不是漏洞利用；命中后需手动验证（如 Actuator 到底能否 RCE）。
- ⚠️ 依赖先有目标流量（被动触发），需先逛一圈站点，再右键发到插件全量扫。

---

## 六、⚠️ 安全测试风险提示

多发包意味着：① 目标访问日志留痕；② 可能触发 WAF/封 IP；③ 对生产环境有额外负载。建议：
1. 用 `Filter_Host` 白名单只锁目标站（`*.目标.com`）
2. `Start` 主开关默认关，确认要扫再开
3. 必要时调低线程，或只启用"高危优先"规则

---

## 七、与现有环境的配合

Burp 已接 MCP（端口 9876）。RouteVulScan 跑出的可疑点，可用 `get_proxy_http_history` / `get_scanner_issues` 拉到 WorkBuddy 做二次分析与复现，形成闭环。

---

*参考笔记：`HaE使用教程.md`（同目录，纯被动提取工具，与本文互补）*
