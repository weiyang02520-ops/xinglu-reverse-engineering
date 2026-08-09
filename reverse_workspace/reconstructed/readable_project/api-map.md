# API 总览

> 完整端点/方法/认证见 `../reports/08_API_MAP.md`。

## 官方 API (api.xushilu.cn)

Base URL: `https://api.xushilu.cn`(备用 `https://119.45.39.251`)
认证: `Authorization: Bearer <token>`(登录后)

| 端点 | 用途 |
|---|---|
| `/v1/accounts/login` / `register` / `login-or-create` | 账号 |
| `/v1/accounts/redeem` | 激活码 |
| `/v1/orders` / `/v1/plans` | 订单/套餐 |
| `/v1/app/startup-notice` / `legal-agreements` / `official-website` / `creative-tools` / `project-writing-presets` / `update` | 应用配置 |
| `/v1/official-models/catalog` / `usage` | 官方模型 |
| `/v1/support/chat/{thread,messages,read,session,status}` | 客服 |

## 第三方

| 服务 | 端点 | 认证 |
|---|---|---|
| LLM 中转 a6api | api.a6api.com/v1 | Bearer |
| LLM 中转 vectorengine | api.vectorengine.ai/cn/v1 | Bearer |
| 搜索 Serper | /search | X-API-KEY |
| 搜索智谱 | /v1/search | Bearer |
| 搜索博查 | /v1/ai-search | Bearer |
| 图像生成 | /images/generations, /images/edits | Bearer |
| Suno 音乐 | 任务创建 + /fetch 轮询 | Bearer |
| 可灵视频 | 任务创建 + 轮询 | Bearer |

## 本地 Mobile Bridge

| 端点 | 方法 | 功能 |
|---|---|---|
| /mobile/health | GET | 健康检查 |
| /mobile/connect | GET | 配对信息 |
| /bridge/events | GET | SSE 事件流 |
| /bridge/media | GET | 媒体读取 |
| /mobile/android.apk | GET | APK 分发 |
| /bridge | POST | 命令(JSON-RPC) |

认证: `x-novelforge-key` / `Authorization: Bearer <pairingKey>` / `?key=`
端口: 8787, 18789, 8891-8999
