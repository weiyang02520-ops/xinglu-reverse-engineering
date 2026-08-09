# 08 — API 地图报告 (API Map)

> 所有端点均为静态推断, 未访问任何服务器。

## 1. 官方 API (api.xushilu.cn)

**Base URL**: `https://api.xushilu.cn` [CONFIRMED]
**备用 IP**: `https://119.45.39.251` [CONFIRMED]
**可覆盖**: 环境变量 `NOVELFORGE_GATEWAY_URL`, `NOVELFORGE_ACCOUNT_GATEWAY_URL`, `NOVELFORGE_GATEWAY_FALLBACK_URL`

### 请求封装 (main.js)
- POST: `{method:"POST", headers:{"Content-Type":"application/json", ...(token?{Authorization:`Bearer ${token}`})}, body:JSON.stringify(...)}`
- GET: `{method:"GET", headers:{...(token?{Authorization:`Bearer ${token}`})}}`
- 响应: JSON `{ok:true/false, ...}`; 失败抛错 `ok===false`
- 错误消息解析: 从响应提取 error 文案
- 更新检查: `GET /v1/app/update` 或环境变量 `NOVELFORGE_UPDATE_CHECK_URL` / `NOVELFORGE_UPDATE_URL`

### 端点清单 [CONFIRMED, main.js 明文]

| 端点 | 方法(推断) | 用途 |
|---|---|---|
| `/v1/accounts/login` | POST | 账号登录 |
| `/v1/accounts/register` | POST | 账号注册 |
| `/v1/accounts/login-or-create` | POST | 手机端一键登录/注册(免密) |
| `/v1/accounts/redeem` | POST | 激活码兑换 |
| `/v1/orders` | POST | 创建订单(会员购买) |
| `/v1/plans` | GET | 会员套餐列表 |
| `/v1/app/startup-notice` | GET | 启动公告 |
| `/v1/app/legal-agreements` | GET | 用户协议/隐私政策 |
| `/v1/app/official-website` | GET | 官网信息 |
| `/v1/app/creative-tools` | GET | 创作工具配置 |
| `/v1/app/project-writing-presets` | GET | 项目写作预设 |
| `/v1/app/update` | GET | 版本更新检查 |
| `/v1/official-models/catalog` | GET | 官方模型目录 |
| `/v1/official-models/usage` | GET | 官方模型用量/余额 |
| `/v1/support/chat/thread` | POST/GET | 客服会话线程 |
| `/v1/support/chat/messages` | POST/GET | 客服消息 |
| `/v1/support/chat/read` | POST | 客服已读 |
| `/v1/support/chat/session` | POST | 客服会话创建 |
| `/v1/support/chat/status` | GET | 客服状态 |

**订单支付**: 创建订单后轮询 `orderWatchUrl`(由订单接口返回), 到账后回调本地发放权益。

## 2. 第三方 LLM 中转

| 提供商 | Base URL | 用途 |
|---|---|---|
| a6api.com | `https://api.a6api.com/v1` | OpenAI 兼容 LLM 中转(带 `/api/usage/token/` 用量查询) |
| vectorengine.ai | `https://api.vectorengine.ai/v1` | OpenAI 兼容 LLM 中转 |
| vectorengine.cn | `https://api.vectorengine.cn/v1` | 国内版 |

- 请求: `POST {authorization:"Bearer <apiKey>", content-type:"application/json"}`
- 401 → `refreshApiKey()` 自动刷新后重试
- 重试: 408/425/429/5xx 指数退避

## 3. LLM 提供方协议

| 能力 | 协议 | 证据 |
|---|---|---|
| 文本生成 (OpenAI 兼容) | `POST /chat/completions` (Bearer) | [CONFIRMED] |
| Anthropic | `POST /v1/messages`, headers: `anthropic-version`, `x-api-key` | [CONFIRMED] |
| Gemini | `POST /v1beta/models/{model}:generateContent` | [CONFIRMED] |
| 图像生成 | `POST /images/generations` (b64_json), `/images/edits` | [CONFIRMED] |
| 图像任务轮询 | `GET /v1/.../tasks/{id}/fetch` (SUCCESS/FAILURE 状态) | [CONFIRMED] |
| 音乐 (Suno) | 任务创建 + `GET .../fetch` 轮询, tracks 返回 | [CONFIRMED] |
| 视频 (可灵 Omni) | 任务创建 + 轮询, videoUrl/coverUrl/duration/resolution | [CONFIRMED] |

## 4. 搜索提供方

| 提供商 | 端点 | 认证 |
|---|---|---|
| Serper | `POST /search` | `X-API-KEY` |
| 智谱 | `POST {endpoint}/v1/search` | `Authorization: Bearer` |
| 博查 | `POST {endpoint}` (query/freshness/count/answer/stream) | `Authorization: Bearer` |
| 统一网关 | `POST {gateway}/v1/search` (provider:"auto") | `Authorization: Bearer {gatewayToken}` |

统一结构: `{query, maxResults, provider, recency, domains, language, country, contentSize, searchEngine?, userId?, requestId?}`

## 5. 博查请求格式 [CONFIRMED]

```json
{"query": "<查询>", "freshness": "noLimit|day|week|month|year", "count": N, "answer": false, "stream": false}
```
响应: `data.queryContext.originalQuery` + `data.webPages.value[]`

## 6. 更新服务 (download.xushilu.cn)

- `app-update.yml`: `https://download.xushilu.cn/updates/win` (electron-updater generic provider)
- APK 分发: 桌面端本地服务器 `GET /mobile/android.apk`

## 7. 本地 HTTP 服务 (Mobile Bridge) [CONFIRMED]

| 端点 | 方法 | 功能 |
|---|---|---|
| `/mobile/health` | GET | 健康检查 → `{ok, protocolVersion, desktopTime}` |
| `/mobile/connect` | GET | 配对 → `{ok, protocolVersion, urls[]}` |
| `/bridge/events` | GET | SSE 事件流 |
| `/bridge/media` | GET/HEAD | 媒体文件读取 |
| `/mobile/android.apk` | GET/HEAD | APK 下载 |
| `/bridge` | POST | 命令调用 (JSON-RPC 风格) |
| 其他 | - | 404 `{ok:false, error:{code:"NOT_FOUND"}}` |

认证: `x-novelforge-key` / `Authorization: Bearer <pairingKey>` / `?key=<pairingKey>`
端口: 配置端口 + 8787 + 18789 + 8891~8999 自动探测

### Bridge 命令全集 [CONFIRMED]

`connection.ping`, `project.list`, `project.current`, `project.select`, `project.create`, `project.settings.read`, `project.settings.write`, `chat.history`, `chat.active`, `chat.send`, `chat.stop`, `chapter.list`, `chapter.read`, `chapter.write`, `resource.list`, `resource.read`, `resource.write`, `resource.rename`, `resource.delete`, `media.list`, `attachment.add`, `debug.chat_ui_state`
