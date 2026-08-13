# 16 — State and Storage

> 全部状态与持久化。证据：renderer bundle 字符串 [RUNTIME_CONFIRMED] + reports/10-11 [REPORT_CONFIRMED]。

## 1. 状态架构 [RUNTIME_CONFIRMED + REPORT_CONFIRMED]

- **无第三方状态库**（无 Redux/Zustand）：React Context + hooks + localStorage
- Provider 链：`Kr → Sd → Td`（全局 → 布局 → 主布局）
- 页面级：useState；跨组件：createContext
- 跨窗口：storage 事件（localStorage）+ 主进程 IPC 转发（chapter-editor-view / global-overlay-view）

## 2. 渲染器全局状态（localStorage）[RUNTIME_CONFIRMED]

| 键 | 值 | 用途 |
|---|---|---|
| `novelforge.appearanceTheme.v1` | light / dark | 主题 |
| `novelforge.interfaceScale.v1` | normal / medium / large | 缩放（1 / 1.1 / 1.3） |
| `novelforge.workspaceMode.v2` | simple / creative | 工作区模式 |
| `novelforge.creativeDockLayout` | dock 树 JSON | 停靠布局 |
| `novelforge.creativeWorkspaceWindows` | 浮窗配置 | 悬浮窗口 |
| `novelforge.floatingChapterEditor.position` | {x,y} | DOM 浮窗位置 |
| `novelforge.floatingChapterEditor.size.v2` | {w,h} | DOM 浮窗大小 |
| `novelforge.chapterEditor.presentation` | docked / floating | 编辑器呈现 |
| `novelforge.chapterEditor.nativeFloatingBounds.v1` | bounds | 原生浮窗边界 |
| `novelforge.chiefEditor.voiceRecordingDialogPosition.v1` | {x,y} | 语音录制框位置 |
| `novelforge.chiefEditorChatCapabilitiesByProject.v1` | per-project | 聊天能力开关 |
| `novelforge.chiefEditorChatCapabilitiesMigratedToProject.v1` | flag | 能力迁移标记 |
| `novelforge.creativeWorkspaceDefaultProjectChat.v1` | projectId | 默认项目聊天 |
| `novelforge.productPreviewChapterSortDirection.v1` | asc/desc | 成品预览排序 |
| `novelforge.startupNotice.seenIds` | ids | 已读公告 |
| `novelforge.support.clientId` | id | 客服匿名标识 |
| `novelforge:chapter-editor-font-size` | size | 编辑器字号 |
| `novelforge:chief-editor-audio-mini-player` | state | 音频迷你播放器 |

## 3. 主进程状态（userData/ JSON）[REPORT_CONFIRMED]

| 文件 | 内容 | 敏感性 |
|---|---|---|
| `local_identity.json` | 设备匿名标识 | 中 |
| `membership_credentials.json` | 会员登录凭证 | **高** |
| `membership_entitlements.json` | 会员权益缓存 | 中 |
| `support_chat_state.json` | 客服会话 | 中 |
| `official_network_compatibility.json` | 网络兼容设置 | 低 |
| `mobile_bridge.json` | 配对密钥 + 状态 | **高** |
| `window_state.json` | 窗口几何 | 低 |

## 4. 项目文件系统 [REPORT_CONFIRMED]

```
workspace/projects/{projectId}/
├── project.md（项目主文件）
├── .novelforge/
│   ├── branches/
│   ├── chief-editor-chat.json / -history.json
│   └── deleted-project.json（回收站）
├── chapters/chXXX/{agent}.md（每 Agent 一个章节文件）
├── 创作资料/*.md（素材）
└── prompts/agents/（Agent 注册表）
垃圾箱/（回收站）
```

## 5. 会话状态（主进程持有，跨窗口共享）

```
chapter-editor-view state: { sessionId, revision, presentation, panelBounds, dockSlot }
global-overlay-view state: { sessions, currentSession, revision }
workflow: progress 事件流（chat 与 workflow 面板共用）
projects: changed 广播（项目列表/当前项目变更）
```

## 6. 状态流图

```
┌─ 渲染器 ──────────────────────────┐   ┌─ 主进程 ────────────────────────┐
│ React Context（UI 状态）            │   │ 项目管理器（文件系统）              │
│  ├─ localStorage（UI 持久化）        │   │ 会话管理器（chapter-editor-view）  │
│  ├─ storage 事件（跨窗口同步）        │   │ 工作流引擎（workflow:progress）    │
│  └─ window.novelforge（IPC 面）      │◄─┤ 模型管理器（provider）             │
└───────────────────────────────────┘   │ 移动桥（/bridge + SSE）            │
                                        └─────────────────────────────────┘
```

## 7. AI Novel Studio 重建时需复刻的存储面

1. localStorage 键体系（命名空间 `novelforge.` → 自命名空间；键结构同形）
2. 主进程 userData JSON（凭证类改为系统凭据管理器，见 17）
3. 项目文件布局（纯文件系统 + JSON，无数据库）
4. 跨窗口状态同步双通道（storage 事件 + IPC 转发）
5. workflow:progress 事件流协议（聊天与工作流面板共享）

## Evidence

- localStorage 键：rendererApp 字符串 [RUNTIME_CONFIRMED]
- userData/项目文件：reports/10-11 [REPORT_CONFIRMED]
- 会话状态：main/preload [RUNTIME_CONFIRMED]
