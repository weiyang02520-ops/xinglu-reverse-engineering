# 11 — 本地存储报告 (Local Storage)

## 1. localStorage 键 [CONFIRMED - rendererApp 明文]

| Key | 用途 | 敏感性 |
|---|---|---|
| `novelforge.appearanceTheme.v1` | 主题 dark/light | 低 |
| `novelforge.interfaceScale.v1` | 界面缩放比例 | 低 |
| `novelforge.workspaceMode.v2` | 工作区模式(simple/creative) | 低 |
| `novelforge.creativeDockLayout` | 停靠面板布局 | 低 |
| `novelforge.creativeWorkspaceWindows` | 悬浮窗口配置 | 低 |
| `novelforge.floatingChapterEditor.position` | 章节编辑器浮窗位置 | 低 |
| `novelforge.floatingChapterEditor.size.v2` | 章节编辑器浮窗大小 | 低 |
| `novelforge.chapterEditor.presentation` | 章节编辑器呈现模式(docked/floating) | 低 |
| `novelforge.chapterEditor.nativeFloatingBounds.v1` | 原生浮窗边界 | 低 |
| `novelforge.chiefEditor.voiceRecordingDialogPosition.v1` | 语音录制对话框位置 | 低 |
| `novelforge.chiefEditorChatCapabilitiesByProject.v1` | 每项目聊天能力开关 | 低 |
| `novelforge.chiefEditorChatCapabilitiesMigratedToProject.v1` | 能力迁移标记 | 低 |
| `novelforge.creativeWorkspaceDefaultProjectChat.v1` | 默认项目聊天 | 低 |
| `novelforge.productPreviewChapterSortDirection.v1` | 成品预览章节排序 | 低 |
| `novelforge.startupNotice.seenIds` | 已读公告 ID 集合 | 低 |
| `novelforge.support.clientId` | 客服客户端 ID | 中(匿名标识) |
| `novelforge:chapter-editor-font-size` | 编辑器字号 | 低 |
| `novelforge:chief-editor-audio-mini-player` | 音频迷你播放器状态 | 低 |

## 2. userData/ JSON 文件 [CONFIRMED - main.js]

| 文件 | 用途 | 敏感性 |
|---|---|---|
| `local_identity.json` | 本地设备匿名标识(可 reset) | 中 |
| `membership_credentials.json` | **会员登录凭证(token)** | **高** |
| `membership_entitlements.json` | 会员权益缓存 | 中 |
| `support_chat_state.json` | 客服会话状态 | 中 |
| `official_network_compatibility.json` | 官方网络兼容设置 | 低 |
| `mobile_bridge.json` | **配对密钥 pairingKey + 状态** | **高(局域网访问凭证)** |
| `window_state.json` | 窗口位置/大小 | 低 |

## 3. 项目文件系统 (workspace/projects/) [CONFIRMED]

```
projects/
├── {projectId}/            # 每项目目录
│   ├── .novelforge/
│   │   ├── branches/
│   │   ├── chief-editor-chat.json
│   │   ├── chief-editor-chat-history.json
│   │   └── deleted-project.json   (回收站)
│   ├── chapters/chXXX/{agent}.md
│   ├── 创作资料/*.md
│   ├── prompts/agents/
│   └── project.md
└── 垃圾箱/                  # 回收站目录
```

## 4. 无数据库 [CONFIRMED 高置信]

- 未发现 sqlite/better-sqlite3/leveldb/electron-store
- 项目以纯文件系统 + JSON 组织
- 聊天历史 JSON 文件(可能较大)

## 5. 移动端

- Service Worker Cache: `novelforge-mobile-shell-v3`(静态资源)
- `/bridge` API 数据不缓存(sw.js 显式排除)
- 无移动端本地项目数据(全部实时同步桌面端)
