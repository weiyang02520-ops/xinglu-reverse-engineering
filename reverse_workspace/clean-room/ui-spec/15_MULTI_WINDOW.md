# 15 — Multi-Window

> Electron 多窗口架构：主窗口 + 两个 WebContentsView 子视图 + 隐藏窗口。全部 [RUNTIME_CONFIRMED]（main.pretty.js / preload.pretty.cjs / web-entry.pretty.js）。

## 1. 窗口/视图清单

| 名称 | 类型 | surface | 用途 |
|---|---|---|---|
| 主窗口 | BrowserWindow（frame:false） | 默认 | 主应用 |
| 章节编辑器 | WebContentsView（主窗口 contentView 内） | `chapter-editor` | 章节编辑 |
| 全局悬浮层 | WebContentsView（主窗口 contentView 内） | `global-overlay` | agent 会话悬浮/popover/modal |
| 发布浏览器 | BrowserWindow（隐藏、skipTaskbar） | — | 平台发布自动化 |
| 本地阅读器 | BrowserWindow（隐藏、透明、skipTaskbar、focusable:false） | — | 网页内容阅读（URL → 文本） |
| 托盘 | Tray（win32） | — | 关闭驻留 |

## 2. 主窗口参数

```
frame: false            // 自绘标题栏
autoHideMenuBar: true
show: false             // 加载完成后显示
minWidth: 1100, minHeight: 720
backgroundColor: "#fffdf8"
roundedCorners: true
transparent: win32 以外平台
win32: backgroundMaterial: "none", opacity: 0
webPreferences: { backgroundThrottling:false, contextIsolation:true,
                  nodeIntegration:false, preload:"preload.cjs", sandbox:true }
```

状态恢复：`userData/window_state.json` → `{x,y,width,height,isMaximized,savedAt}`；
夹紧规则：宽 `min(1280, max(900, saved))`、高 `min(900, max(720, saved))`，默认 1280×900。
保存时机：resize/move/maximize/unmaximize/close（200ms 防抖）。

## 3. WebContentsView 子视图机制

```
主窗口 contentView
├── addChildView(global-overlay view)   // 懒创建（T() 延迟）
├── addChildView(chapter-editor view)   // 懒创建（P() 延迟）
└── 主页面

创建：new WebContentsView({ webPreferences: { sandbox:true, contextIsolation:true,
      nodeIntegration:false, preload:"preload.cjs" } })
加载：webContents.loadFile(web/index.html, { query: { novelforgeSurface: "chapter-editor" | "global-overlay" } })
初始：setBackgroundColor("#00000000")（透明）、setBounds(全窗口)、setVisible(false)
就绪：did-finish-load → addChildView 加入 → 按需 setVisible(true) → invalidate() 重绘
```

## 4. 呈现状态机（主进程持有）

```
chapter-editor-view: { sessionId, revision, presentation, panelBounds, dockSlot, ... }
  presentation ∈ { docked, floating, popover, modal }

global-overlay-view: { sessions[], currentSession, ... }
  presentation ∈ { modal, popover }

布局计算（Ux 函数，窗口 resize 时重算）：
  modal    → 铺满窗口 bounds
  popover  → 按锚点 bounds 定位（l7t：bounds + setVisible）
  floating → 记录 bounds（chapterEditor.nativeFloatingBounds.v1）
  docked   → panelBounds（dock 槽位）
```

## 5. 状态同步（三个 surface 之间）

| 通道 | 方向 | 内容 |
|---|---|---|
| `novelforge:chapter-editor-view:state` | 主进程 → 渲染器 | 会话状态（getState/onState） |
| `novelforge:chapter-editor-view:layout` | 主进程 → 渲染器 | 布局/面板边界 |
| `novelforge:chapter-editor-view:event` | 双向 | 事件（emitEvent/onEvent） |
| `novelforge:chapter-editor-view:set-session` | 渲染器 → 主进程 | 打开会话 |
| `novelforge:chapter-editor-view:set-dock-slot` | 渲染器 → 主进程 | 停靠槽位 |
| `novelforge:chapter-editor-view:set-floating-bounds` | 渲染器 → 主进程 | 浮窗几何（commit 持久化） |
| `novelforge:global-overlay-view:state/event` | 同章节编辑器 | 悬浮会话 |
| `novelforge:global-overlay-view:report-content-size` | 渲染器 → 主进程 | 内容尺寸（popover 定位） |
| `novelforge:window:set-chapter-editor-docked` | 渲染器 → 主进程 | 停靠切换 |
| storage 事件 | 渲染器间 | localStorage 变更同步（主题/布局） |

## 6. Preload / contextBridge 边界

`window.novelforge`（19 模块，全部 invoke/on 白名单）[RUNTIME_CONFIRMED]：

globalOverlayView / chapterEditorView / chiefEditor / projects / agents / prompts /
artifacts / tokens / feedback / system / membership / support / paths / materials /
outlineManager / provider / officialModels / publisher / window

- 渲染器无直接网络/文件权限（sandbox），一切经 IPC（~150 通道）
- preload 同时处理静态加载器启动握手（static-loader-ready / paint-request / painted）

## 7. 关闭行为

- 主窗口关闭 → 拦截（win32）→ 托盘驻留（提示语"关闭窗口后，星炉会继续在右下角运行"）
- 托盘菜单：打开主窗口 / 退出创作
- 章节编辑器/悬浮层随主窗口生命周期（子视图，无独立生命周期）

## 8. 启动握手时序

```
preload: 观察 #nf-static-preloader → static-loader-ready(theme)
主进程: paint-request → preload 触发绘制（paint-prime 动画）
web-entry: mountRendererApp(surface) → startup-renderer-prepared
主进程: 初始应用数据 → startup-initial-app-data-ready
主进程: window:shown → 渲染器 dispatch startup-window-shown
主进程: fade-in-complete → 渲染器 dispatch startup-window-fade-in-complete
```

## Evidence

全部 [RUNTIME_CONFIRMED]（main.pretty.js 窗口工厂/子视图/呈现状态机；preload.pretty.cjs API 面；web-entry.pretty.js 启动）

## Unknown

- 发布窗口的完整 bounds/行为（隐藏窗口细节）
- popover 锚点计算的具体规则（report-content-size 如何参与）
- 多显示器行为
