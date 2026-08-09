# 渲染进程 — 状态与启动

> 状态键 CONFIRMED(明文); 组织 RECONSTRUCTED。

## 状态管理

无第三方状态库。React Context + Hooks + localStorage 持久化 + storage 事件跨窗口同步。

### localStorage 键

| 键 | 用途 |
|---|---|
| novelforge.appearanceTheme.v1 | 主题 light/dark |
| novelforge.interfaceScale.v1 | 界面缩放 |
| novelforge.workspaceMode.v2 | simple / creative |
| novelforge.creativeDockLayout | 停靠布局 |
| novelforge.creativeWorkspaceWindows | 悬浮窗口 |
| novelforge.floatingChapterEditor.position / .size.v2 | 章节编辑器浮窗 |
| novelforge.chapterEditor.presentation | docked / floating |
| novelforge.chapterEditor.nativeFloatingBounds.v1 | 原生浮窗边界 |
| novelforge.chiefEditorChatCapabilitiesByProject.v1 | 每项目聊天能力 |
| novelforge.chiefEditorChatCapabilitiesMigratedToProject.v1 | 迁移标记 |
| novelforge.creativeWorkspaceDefaultProjectChat.v1 | 默认项目聊天 |
| novelforge.productPreviewChapterSortDirection.v1 | 成品排序 |
| novelforge.startupNotice.seenIds | 已读公告 |
| novelforge.support.clientId | 客服客户端 ID |
| novelforge:chapter-editor-font-size | 编辑器字号 |
| novelforge:chief-editor-audio-mini-player | 音频迷你播放器 |

## 启动序列

```
1. index.html 内联脚本: 读 theme/scale → data-theme
2. web-entry (index-CvAAoCbC.js):
   - 预加载 rendererApp
   - surface 检测 (novelforgeSurface URL 参数)
   - 启动阶段: ignite(点亮星炉) → workspace(整理创作工作台)
              → project(接续《书名》) → ready(就绪)
3. preload: 静态加载器绘制 → 主进程窗口显示协调
4. mountRendererApp(surface):
   - chapter-editor → 章节编辑器
   - global-overlay → 悬浮层
   - 默认 → 主应用 (Provider → Layout → Main)
5. 初始数据就绪 → startup-initial-app-data-ready
```

## 跨窗口同步

- 监听 `storage` 事件: 主题/工作区模式/布局 等 localStorage 变化 → 同步到其他窗口
- IPC 状态同步: chapter-editor-view:state / global-overlay-view:state (主进程中转)
