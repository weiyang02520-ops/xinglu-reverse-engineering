# 08 — Chapter Editor

> 章节编辑器：以独立 surface（WebContentsView）承载的阅读/编辑视图，可 dock、可浮动、可原生浮窗。

## Purpose

编辑/审阅章节正文：标题、正文阅读视图、查找替换、字号调节；与聊天（chief-editor）共享会话。

## Entry

- 任意位置打开章节会话：`chapterEditorView.setSession({...})`（invoke `novelforge:chapter-editor-view:set-session`）
- 章节列表点击、聊天章节链接、creative 素材路径打开
- 双视图模式：`novelforgeDualViewChapterEditor=1` URL 参数（并排双章节视图，[RUNTIME_CONFIRMED 参数存在，UI 细节 UNKNOWN]）

## Layout [RUNTIME_CONFIRMED 类族]

```
chapter-editor-view-root（surface 根）
├── chapter-editor-view-window-drag-strip（顶部拖拽条，窗口拖动）
├── chapter-editor-dock-host（dock 承载区）
├── chapter-editor-row（行布局）
├── chapter-editor-title / title-input（标题 + 可编辑标题输入）
├── 正文阅读区（阅读字号 token: --nf-type-chapter-editor-reading = 17px）
└── chapter-editor-search-replace
    ├── chapter-editor-search-group
    ├── chapter-editor-search-count（匹配计数）
    └── chapter-editor-search-clear（清除）
```

## 呈现状态机（主进程持有）[RUNTIME_CONFIRMED]

| presentation | 行为 |
|---|---|
| `docked` | 停靠进主窗口（`chapter-editor-dock-host` 槽位）；`set-dock-slot` 指定槽位；bounds = `panelBounds` |
| `floating` | DOM/原生浮窗：`set-floating-bounds({bounds, commit})`；持久化 `novelforge.chapterEditor.nativeFloatingBounds.v1` |
| `popover` | 从锚点弹出（悬浮会话），`report-popover-ready` |
| `modal` | 全窗口遮罩模态（会话确认类） |

- 状态同步：主进程 `chapter-editor-view:state`（getState/onState）+ `layout` 事件（onLayout）
- 就绪上报：`report-presentation-ready({sessionId, revision})`
- 焦点管理：`focus()` invoke；`returnFocus` 决定焦点回退目标（"chapter-editor" 或主窗口）

## Dimensions

- 字体大小持久化：`novelforge:chapter-editor-font-size`（IPC 通道同名）[RUNTIME_CONFIRMED]
- 阅读字号：--nf-type-reading 17px（token [RUNTIME_CONFIRMED]）
- 拖拽条：`window-drag-strip`（无边框窗口的移动区域）

## Visual

- surface 背景透明（`#00000000`），内容卡片自带圆角（radius 16px panel 系）
- 正文：阅读字号 17px、正文行距 [INFERRED]

## Controls

- 标题输入（title-input）
- 查找替换（search-replace / group / count / clear）
- 拖拽条（拖动窗口/面板）
- 字号调节（IPC 键）

## States

- docked / floating / popover / modal 呈现态
- 会话加载中 / 就绪（report-presentation-ready）
- 会话切换（set-session 新会话）
- 外部编辑同步（external-file-edit）

## Interactions

- 打开会话 → 主进程更新 view state → 渲染器渲染对应章节
- 停靠切换：`novelforge:window:set-chapter-editor-docked`（窗口级）
- 浮窗拖动 → `set-floating-bounds`（实时 + commit 持久化）
- 关闭浮窗 → 返回 dock 或隐藏（[INFERRED]）

## Storage / State

| 键 | 内容 |
|---|---|
| `novelforge.chapterEditor.presentation` | docked/floating |
| `novelforge.chapterEditor.nativeFloatingBounds.v1` | 原生浮窗边界 |
| `novelforge.floatingChapterEditor.position` / `.size.v2` | 浮窗几何（DOM 浮窗用） |
| `novelforge:chapter-editor-font-size` | 字号 |
| 主进程 state | sessionId / revision / presentation / panelBounds / dockSlot |

## Window behavior

- **非独立 BrowserWindow**：chapter-editor 是主窗口内的 WebContentsView（surface=chapter-editor），主进程用 contentView 层叠管理 [RUNTIME_CONFIRMED]
- 懒创建：首次需要时创建视图（setTimeout 延迟），`setVisible(false)` 常驻隐藏
- 显示时 `setBackgroundColor("#00000000")` + invalidate（透明重绘）

## Evidence

- 呈现状态机/视图管理：main.pretty.js（C()/l7t/s7t/Ux 等函数 + chapter-editor-view IPC）[RUNTIME_CONFIRMED]
- 类族/字号 token：CSS [RUNTIME_CONFIRMED]
- 存储键：reports/11 [REPORT_CONFIRMED]

## Unknown

- 正文编辑方式（contenteditable / textarea / 只读 + 另编辑器）
- 双视图模式的并排行为
- dock 槽位数量与命名
- 字体大小范围（最小/最大）
