# 07 — Chapters

> 章节管理：simple 工作区的章节树 + creative 模式中的章节文件组织 + 章节与聊天/编辑器的联动。

## Purpose

按分组组织章节文件，提供搜索、排序、拖拽、选中打开编辑。

## Entry

- simple 工作区：左栏 `simple-project-chapter-*` 树（见 05）
- creative 工作区：章节文件作为素材路径存在于文件夹树（`creative-path-item` 打开章节）
- 聊天消息中的章节链接（`chat-chapter-link-*` / `chat-chapter-editor-panel`）可直达编辑器

## Layout [RUNTIME_CONFIRMED 类族]

```
章节分组树（simple 模式）
simple-project-chapter-group
├── group-header（icon + title + toggle + editing）
├── group-files
│   └── simple-project-chapter-file
│       ├── file-row（cursor:grab；grid；gap 4px）
│       │   ├── file-main（number + title + select）
│       │   └── file-trailing（character-count + actions）
│       └── file-separator
├── group-create
└── group-empty
├── chapter-search（搜索）
├── chapter-handwrite（手写）
└── chapter-long-press-hint（长按提示）
```

## Dimensions

- 章节行：grid `minmax(0,1fr)`、gap 4px、cursor grab（可拖拽）[RUNTIME_CONFIRMED]
- 分组容器：无背景无边框无内边距（纯树容器）[RUNTIME_CONFIRMED]

## Visual

- 章节文件行：文件卡片式；选中/激活用 active 色（--accent-active-soft）
- 字数徽标：`file-character-count`（micro 字号）
- 拖拽行：grab 光标

## Controls

- 分组：创建/折叠/重命名/删除（group-create / toggle / toggle-editing）
- 章节：选择（file-select）、动作菜单（file-actions）、拖拽排序（grab）
- 搜索（chapter-search）、手写（chapter-handwrite）
- 长按菜单（long-press-hint）

## States

- 分组折叠展开 / 重命名编辑中 / 空态
- 章节选中 / 激活 / 拖拽中
- 搜索过滤结果（无结果态 [INFERRED]）

## Interactions

- 点击章节 → `chapter-editor-view:set-session`（打开编辑器会话，dock 或浮动）
- 拖拽章节/分组 → 重排（`projects:update-chapter-groups` IPC）
- 聊天内章节链接 → 打开对应章节编辑器
- 外部文件编辑（`chief-editor:external-file-edit` 事件，编辑器外改动同步）

## Storage / State

- 分组结构：`projects:update-chapter-groups`
- 章节文件：`chapters/chXXX/{agent}.md`（每 agent 一个文件）[REPORT_CONFIRMED]
- 当前章节会话：主进程 `chapter-editor-view` state（见 08/15）

## Window behavior

章节打开进入 chapter-editor surface（dock/floating/popover，见 08）。

## Evidence

- 类族/数值：CSS [RUNTIME_CONFIRMED]
- 分组 IPC / 章节会话 IPC：preload [RUNTIME_CONFIRMED]
- 章节文件布局：reports/11 [REPORT_CONFIRMED]

## Unknown

- 章节行内 action 菜单内容（打开/删除/重命名/移动？）
- 排序维度（章节号/自定义拖序/按 agent）
- 章节文件与 agent 的关系展示（多 agent 文件如何合并显示一章）
