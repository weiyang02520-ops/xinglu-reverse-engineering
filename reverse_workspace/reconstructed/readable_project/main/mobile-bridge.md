# Mobile Bridge 协议

> CONFIRMED — 端点和命令名从 main.js fPt/bPt 明文提取。

## 概述

桌面端主进程内嵌一个 HTTP 服务器, 供手机 PWA 局域网访问。
手机通过该桥执行项目管理/聊天/章节读写等操作, 实时与桌面端同步。

## 启动

- 端口选择: 配置端口 → 8787 → 18789 → 8891-8999(逐端口尝试, EACCES 则换)
- 监听地址: 0.0.0.0/::(非 localhost)或配置 host
- 配对密钥: `pairingKey`(18 字节随机 → base64url), 存 `userData/mobile_bridge.json`
- 状态接口: `novelforge:mobile-bridge:get-status` / `restart`

## 端点

| 端点 | 方法 | 请求 | 响应 |
|---|---|---|---|
| /mobile/health | GET | - | `{ok, protocolVersion, desktopTime}` |
| /mobile/connect | GET | 需鉴权 | `{ok, protocolVersion, urls[]}` |
| /bridge/events | GET | 需鉴权 | SSE 事件流 |
| /bridge/media | GET/HEAD | 需鉴权 | 媒体文件(音频/图片/视频) |
| /mobile/android.apk | GET/HEAD | - | APK 文件下载 |
| /bridge | POST | JSON | JSON-RPC 响应 |
| 其他 | - | - | 404 `{ok:false, error:{code:"NOT_FOUND"}}` |

CORS: `Access-Control-Allow-Origin: *`, 允许头 `content-type, x-novelforge-key, authorization`

## 鉴权

三种方式之一, 值必须等于 `pairingKey`:
- Header: `x-novelforge-key`
- Header: `Authorization: Bearer <key>`
- Query: `?key=<key>`

失败 → 401 "Invalid mobile pairing key."

## 命令协议 (POST /bridge)

请求:
```json
{ "id": "mobile-…", "protocolVersion": 2, "command": "chat.send", "input": {…} }
```

响应:
```json
{ "id": "mobile-…", "kind": "response", "ok": true, "output": {…} }
{ "id": "mobile-…", "kind": "response", "ok": false, "error": {…} }
```

## 命令全集 (22)

```
connection.ping        → {ok, protocolVersion, desktopTime}
project.list           → {projects[], currentProjectId}
project.current        → {project}
project.select         → {project} (切换当前项目, 广播 changed)
project.create         → {project, projects[], currentProjectId} (从灵感/题材创建)
project.settings.read  → 项目设置
project.settings.write → 写入项目设置
chat.history           → 聊天历史
chat.active            → 当前聊天会话
chat.send              → 发送消息 (流式经 SSE 返回)
chat.stop              → 停止生成
chapter.list           → 章节列表
chapter.read           → 章节内容
chapter.write          → 写入章节
resource.list          → 创作资料列表
resource.read          → 资料内容
resource.write         → 写入资料
resource.rename        → 重命名
resource.delete        → 删除
media.list             → 媒体列表
attachment.add         → 添加聊天附件
debug.chat_ui_state    → 调试: 读取主编聊天 UI 状态(executeJavaScript)
```

## SSE 事件流 (/bridge/events)

- 用于聊天流式输出、状态推送(项目切换/资料变更/章节更新)
- 移动端据此实时同步("这份资料已在另一端更新" 冲突检测)

## 项目创建(手机端)

- 参数: name / inspiration(一句灵感) / genre(题材方向)
- 创建: `creativeDirection:"novel"`, `creationMode:"continuous"`
- 写 `project.md`: `# 书名` + 题材方向 + 一句灵感(手机端手动记录)
