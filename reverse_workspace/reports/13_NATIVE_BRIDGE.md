# 13 — Native Bridge 分析报告

## 结论

XingLu 有两个独立的"桥"：**Electron IPC (桌面内部)** 与 **Mobile Bridge HTTP (桌面↔手机)**。无任何其他自定义 Native Bridge。 [CONFIRMED]

## 1. Electron IPC Bridge (renderer → preload → main)

### 通道规模 [CONFIRMED]
- `ipcMain.handle`: **150 个** invoke 通道
- `ipcRenderer.send/on`: 事件通道(启动序列、workflow 进度、聊天事件、窗口事件等)

### 暴露给渲染器的 API 模块 (preload.cjs contextBridge)

| 模块 | 能力 |
|---|---|
| `globalOverlayView` | 全局悬浮层会话管理(setSessions/getState/emitEvent/reportContentSize) |
| `chapterEditorView` | 章节编辑器(浮窗/停靠/setSession/getState/layout/emitEvent) |
| `chiefEditor` | **核心 AI**: analyzeInputClarity/chat/stopChat/extractOfficeDocument/run(工作流)/stop/skills CRUD/organizeLibrary/delete-confirmation |
| `projects` | 项目管理: list/create/select/delete/trash/restore/rename/branch 管理(create/select/delete/rename/strategy)/updateWorkflowSettings/updateChapterGroups/exportCurrent/importBackup |
| `agents` | 智能体管理: list/create/delete/duplicate/update-identity/update-provider/update-prompt-paths/update-read-files/update-output-files/update-final-text-source/update-order |
| `materials` | 素材库: list/import-files/delete-file/open-file/read-* (audio/image/video/file)/write-file/copy-media |
| `membership` | 会员: login/register/logout/login-or-create/redeem-activation-code/get-plans/create-order/get-order-status/refresh-order-payment/get-current |
| `officialModels` | 官方模型: get-catalog/refresh-catalog/get-usage-balance |
| `publisher` | 发布: list-platforms/open-platform/inspect-platform/inspect-current/bind-current-project/run-draft/run-mock/click/fill/snapshot/close |
| `outlineManager` | 大纲: get-status/generate-directions/apply-direction |
| `artifacts` | 成品: list-products/read-preview/write-preview/open-product-folder/open-product-history-folder |
| `provider` | 模型提供商: get-summary/save-chat-completions/select-model/delete-model |
| `paths` | 路径: open-local/open-containing-folder/select-project-files/to-project-relative |
| `system` | 系统: get-environment/check-app-update/start-app-update-download/install-app-update/open-external-url/get-local-identity/reset-local-identity/get-legal-agreements/get-startup-notice/get-official-website |
| `tokens` | 用量: get-summary |
| `mobileBridge` | 手机桥: get-status/restart |
| `support` | 客服: initialize/get-status/refresh-status/get-thread/send-message/mark-read/set-viewing |
| `feedback` | 反馈: submit |
| `workflow` | 工作流: stop + onProgress 事件 |
| `window` | 窗口: minimize/close/toggle-maximize/set-minimum-size/ensure-size/set-chapter-editor-docked |

### 事件流 (main → renderer)
- `novelforge:workflow:progress` — 主编工作流进度(agentId/stepId/label/status/phase/loopMode/chapterNumber/message/reads/writes)
- `novelforge:chief-editor:chat-event` — 聊天事件流
- `novelforge:chief-editor:chat-history-changed` — 历史变更
- `novelforge:chief-editor:delete-confirmation-request/cancelled` — 删除确认
- `novelforge:projects:changed` — 项目变更广播
- `novelforge:global-overlay-view:state/event` — 悬浮层状态
- `novelforge:chapter-editor-view:state/layout/event` — 编辑器状态
- `novelforge:system:app-update-download-state` — 更新下载进度
- 启动序列事件(static-loader/shown/fade-in 等)

## 2. Mobile Bridge HTTP (桌面 ↔ 手机)

见 08 报告(API 地图)第六节 — 完整协议已恢复:

- 认证: `x-novelforge-key` / Bearer / `?key` = pairingKey
- 端点: /mobile/health, /mobile/connect, /bridge/events (SSE), /bridge/media, /mobile/android.apk, /bridge (POST JSON-RPC)
- **22 个命令**: connection.ping, project.list/current/select/create/settings.read/write, chat.history/active/send/stop, chapter.list/read/write, resource.list/read/write/rename/delete, media.list, attachment.add, debug.chat_ui_state
- 配对密钥: 18 字节 random → base64url,存 `userData/mobile_bridge.json`
- 端口: 配置端口/8787/18789/8891-8999 自动探测
- SSE 事件用于实时推送(聊天流式输出等)

## 3. 无其他桥

- 无自定义 URL scheme
- 无 WebView IPC (除 Electron 标准)
- 无命名管道
- Capacitor 桥仅存在于 APK 内部(移动端壳), 不承载业务

## 4. JS → Native 边界总结

```
渲染器 (React) 
  → window.novelforge (contextBridge, preload)
  → ipcRenderer.invoke/send
  → 主进程 ipcMain.handle 150 处理器
  → Node.js (fs/electron API/网络 fetch/child_process)
  
手机 (PWA in WebView)
  → fetch HTTP
  → 桌面端本地 HTTP 服务 (127.0.0.1:PORT)
  → 主进程 (与桌面渲染器同源)
```
