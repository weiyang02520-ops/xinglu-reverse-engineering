# 10 — 状态管理报告 (State Management)

## 结论

**无 Redux/Zustand/Pinia 等第三方状态库**。全部为 React Context + Hooks 自定义状态 + localStorage 持久化。[CONFIRMED - 渲染器无 store 库特征]

## 1. 渲染器状态架构 [CONFIRMED]

```
Provider 层级: Kr (最外层 Provider) → Sd → Td (主布局)
```

- `Kr` — 全局 Provider(经 use 链提供多个 context)
- `Sd` — 布局 Provider
- 页面级状态: `useState` 局部状态
- 跨组件共享: React Context(自定义, `createContext` 用法)

### 状态分类

| 类型 | 状态 | 持久化 |
|---|---|---|
| 全局 UI | 主题 (dark/light) | localStorage `novelforge.appearanceTheme.v1` |
| 全局 UI | 界面缩放 (normal/...) | localStorage `novelforge.interfaceScale.v1` |
| 全局 UI | 工作区模式 (simple/creative) | localStorage `novelforge.workspaceMode.v2` |
| 布局 | 停靠布局 | localStorage `novelforge.creativeDockLayout` |
| 布局 | 浮窗位置/大小 | `novelforge.floatingChapterEditor.position` / `.size.v2` |
| 布局 | 章节编辑器呈现 | localStorage `novelforge.chapterEditor.presentation` |
| 项目级 | 默认项目对话 | `novelforge.creativeWorkspaceDefaultProjectChat.v1` |
| 项目级 | 聊天能力开关 | `novelforge.chiefEditorChatCapabilitiesByProject.v1` |
| 窗口 | 章节编辑器字体大小 | `novelforge:chapter-editor-font-size` |
| 会话 | 语音录制位置 | `novelforge.chiefEditor.voiceRecordingDialogPosition.v1` |
| 会话 | 音频迷你播放器 | `novelforge:chief-editor-audio-mini-player` |
| 会话 | 客户端 ID | `novelforge.support.clientId` |
| 公告 | 已读公告 | `novelforge.startupNotice.seenIds` |

### 跨窗口同步 [CONFIRMED]
- 主窗口/章节编辑器/全局悬浮层之间用 `storage` 事件同步(监听 localStorage 变化)
- 多窗口共享状态通过主进程 IPC 转发(chapter-editor-view:state, global-overlay-view:state)

## 2. 主进程状态 [CONFIRMED]

- 项目树状态: 内存中构建, 变化时通过 `novelforge:projects:changed` 广播到渲染器
- 工作流状态: `novelforge:workflow:progress` 事件流(主编运行进度)
- 会话状态: chapter-editor-view / global-overlay-view 由主进程持有, 渲染器通过 getState/onState 同步
- 持久化: JSON 文件(userData/)由主进程读写

## 3. 渲染器缓存状态

- `Tr()` / `nv()` / `_r()` — 初始化状态读取函数(从 localStorage)
- 订阅 `storage` 事件 → 更新状态(多窗口一致)

## 4. 移动端状态

- 通过 `/bridge` 命令 + `/bridge/events` (SSE) 与桌面端同步
- 无本地持久化状态(轻量客户端)
