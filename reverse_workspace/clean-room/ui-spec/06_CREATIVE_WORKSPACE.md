# 06 — Creative Workspace

> 创作工作区（`workspaceMode: "creative"`）：多面板停靠/悬浮布局系统。这是 AI Novel Studio 后续最重要的区域。
> 核心事实：**停靠树（dock tree）系统 + 独立悬浮窗 + 文件夹树**，类似 IDE 布局但以"创作窗口"为单位。

## Purpose

创作模式下，把"项目 / 素材 / 大纲 / 聊天 / 章节编辑器"组织为可停靠、可悬浮、可拖拽的面板窗口体系。

## Entry

- 全局设置切换 workspaceMode=creative（`novelforge.workspaceMode.v2`）
- 布局持久化：`novelforge.creativeDockLayout`（停靠布局）+ `novelforge.creativeWorkspaceWindows`（悬浮窗配置）

## Layout [RUNTIME_CONFIRMED 类族 + 结构关系]

```
CreativeWorkspace（占满主 grid 中央 + 右列区域）
└── creative-dock-tree-root（flex 容器，padding 3px，z-index 4）
    ├── creative-dock-tree-split（水平/垂直分割）
    │   ├── creative-dock-tree-splitter（分割条，可拖动）
    │   └── ...递归子 split
    └── creative-docked-panel（停靠面板）
        ├── creative-docked-panel-header
        │   └── creative-docked-panel-title
        ├── creative-docked-panel-body
        └── creative-docked-panel-grip（拖拽把手）
    └──（独立）creative-floating-window × N（悬浮窗，绝对定位）
```

### 窗口种类（creative-window-* 类族）[RUNTIME_CONFIRMED]

| 窗口 | 类 | 内容 |
|---|---|---|
| 项目窗 | `creative-project-window` / `creative-project-list` | 项目列表/选择 |
| 素材窗 | `creative-material-window`（+material-header-import） | 创作资料库 |
| 聊天窗 | `creative-chat-window` | 总编聊天 |
| 大纲窗 | `creative-outline-folder-list` | 大纲（卷/章） |

### 文件夹树（creative-folder-*）[RUNTIME_CONFIRMED]

```
creative-folder-list
├── creative-folder-group（可折叠分组）
│   ├── creative-folder-toggle
│   ├── creative-folder-create-row / create-button
│   ├── creative-folder-delete-button
│   └── creative-folder-body
│       └── creative-path-list
│           ├── creative-path-item（素材条目）
│           │   ├── creative-path-open-button
│           │   └── creative-path-delete-button
│           └── creative-root-path-item
├── creative-folder-search（+clear/submit）
├── creative-folder-organize-button（整理）
└── creative-folder-empty / list-empty / search-empty
```

### 浮窗（creative-floating-window）[RUNTIME_CONFIRMED]

```
creative-floating-window（absolute；min-width 280px；min-height 180px；radius 16px；border subtle 78%）
├── creative-window-titlebar
│   ├── creative-window-title + title-meta
│   └── creative-window-header-action（关闭/最小化等）
├── creative-window-grip（拖拽把手）
├── creative-window-body
│   └── creative-window-scroll
├── creative-window-resize-handle（右下/四角缩放）
└── creative-window-layer（层级管理）
```

## ASCII 状态关系图

```
┌────────────────────────────────────────────────────────┐
│ creative-dock-tree-root                                │
│ ┌──────────────┬─────────────────────────────────────┐ │
│ │ split (vert) │  split (horiz)                      │ │
│ │ docked-panel │  ┌──────────────┬─────────────────┐ │ │
│ │ [素材库]      │  │ docked-panel │ docked-panel    │ │ │
│ │              │  │ [大纲]       │ [聊天]          │ │ │
│ │              │  └──────────────┴─────────────────┘ │ │
│ └──────────────┴─────────────────────────────────────┘ │
│    ┌───────────────────────────┐   ┌────────────────┐  │
│    │ floating-window [章节编辑器]│   │ floating-window│  │
│    │ （可拖动/缩放/置顶）         │   │ [项目]         │  │
│    └───────────────────────────┘   └────────────────┘  │
└────────────────────────────────────────────────────────┘
     ↑ dock 布局持久化: novelforge.creativeDockLayout
     ↑ 浮窗持久化:      novelforge.creativeWorkspaceWindows
```

## Dimensions

| 项 | 值 | 证据 |
|---|---|---|
| dock-tree padding | 3px | CSS [RUNTIME_CONFIRMED] |
| 浮窗最小尺寸 | 280×180px | CSS [RUNTIME_CONFIRMED] |
| 浮窗圆角 | 16px（--nf-radius-panel） | CSS [RUNTIME_CONFIRMED] |
| 浮窗阴影 | `0 24px 54px -34px` card-shadow | CSS [RUNTIME_CONFIRMED] |
| 分割条 | 7px（主 grid 分隔列同体系，[INFERRED] dock 内部同尺寸） | — |

## Visual

- docked-panel：透明底（`box-shadow:none!important`，面板融入 dock 背景）
- floating-window：chip-bg 底 + subtle 边框 + 大阴影（浮起感）
- 项目窗/素材窗/聊天窗/大纲窗：独立 titlebar + grip + resize-handle

## Controls

- 拖拽：panel-grip / window-grip（停靠面板移动）
- 缩放：window-resize-handle（浮窗）
- 关闭/最小化：window-header-action
- 分割：dock-tree-splitter（拖动改比例）
- 文件夹：create/delete/organize/search/toggle
- 路径操作：path-open / path-delete / organization-lock（锁定整理）

## States

- 活动窗口/焦点：`creative-window-layer` + active 体系
- 空态：creative-window-empty / folder-empty / folder-search-empty
- 锁：`organization-lock-button`（素材整理锁定，防止并发修改；IPC `list-organization-locks` / `set-organization-lock`）

## Interactions

- 拖 panel 到 dock 边 → 重新分割（dock tree 动态重组）
- 拖 panel 出 dock → 变 floating-window
- 浮窗拖动/缩放 → 实时更新（`novelforge.creativeWorkspaceWindows`）
- 章节编辑器：dock 槽位（`chapter-editor-view:set-dock-slot`）或浮窗（`set-floating-bounds`）——见 08
- 默认项目聊天：`novelforge.creativeWorkspaceDefaultProjectChat.v1`（creative 模式默认打开哪个项目会话）

## Storage / State

| 键 | 内容 |
|---|---|
| `novelforge.workspaceMode.v2` | simple/creative |
| `novelforge.creativeDockLayout` | 停靠树布局 |
| `novelforge.creativeWorkspaceWindows` | 悬浮窗位置/大小/种类 |
| `novelforge.creativeWorkspaceDefaultProjectChat.v1` | 默认项目聊天 |
| `novelforge.chapterEditor.presentation` | 章节编辑器呈现（docked/floating） |
| `novelforge.floatingChapterEditor.position/size.v2` | 浮窗章节编辑器几何 |

## Window behavior

- dock 内面板：主窗口 grid 内布局
- floating-window：**DOM 内绝对定位浮窗**（非 Electron 窗口；仅章节编辑器可另走原生浮窗 `nativeFloatingBounds.v1`）
- global-overlay surface 可叠在任意工作区之上（popover/modal 呈现，见 15）

## Evidence

- 全部类族与数值：CSS [RUNTIME_CONFIRMED]
- 持久化键：renderer bundle + reports/11 [RUNTIME_CONFIRMED + REPORT_CONFIRMED]
- dock/floating 行为（拖拽重组/悬浮转换）：类结构与键存在 [INFERRED 细节]，行为细节 UNKNOWN（见 18）

## Unknown

- dock 分割方向初始化时的默认布局（每面板默认位置）
- 拖拽转浮窗的具体触发（拖出阈值）
- splitter 宽度是否为主 grid 同款 7px
- 面板关闭后如何重新打开（菜单？）
