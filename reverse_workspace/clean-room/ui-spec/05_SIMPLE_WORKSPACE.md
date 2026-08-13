# 05 — Simple Workspace

> 简化工作区模式（`workspaceMode: "simple"`）：以"项目 + 章节管理 + 聊天"为主的工作台。

## Purpose

轻量创作模式：选中项目后进入，左侧/中部为章节列表管理，右侧保留总编聊天。适合快速写作流程，不加载多面板停靠系统。

## Entry

- 从首页选择项目进入（`projects:select` → workspaceMode=simple 时）
- 模式切换：`novelforge.workspaceMode.v2` = "simple" | "creative"（全局设置可切，见 13）

## Layout [RUNTIME_CONFIRMED（类族）+ INFERRED（具体排布）]

```
nf-window grid（292 | 7 | minmax(560,1fr) | 7 | 380）
├── 左栏 292px：项目信息 + 章节分组树
│   ├── simple-project-active-mark（当前项目标记）
│   ├── simple-project-chapter-search（章节搜索）
│   └── simple-project-chapter-group × N（可折叠分组）
│       ├── group-header（标题 + toggle）
│       ├── group-files
│       │   └── simple-project-chapter-file-row × N
│       │       ├── file-number（章节号）
│       │       ├── file-title
│       │       ├── file-character-count（字数）
│       │       └── file-actions（长按菜单）
│       └── group-create（新建分组）
└── 中央/右：总编聊天（见 04，chief-* / chat-*）
```

## Hierarchy

```
SimpleWorkspace
├── SimpleProjectHeader（active-mark / 项目名 / 动作）
├── SimpleChapterPanel
│   ├── chapter-search
│   ├── chapter-group（折叠树）
│   │   ├── group-header（icon / title / toggle / editing）
│   │   ├── group-create / group-empty
│   │   └── group-files
│   │       └── chapter-file（row / main / select / trailing）
│   │           ├── number + title
│   │           └── character-count + actions
│   └── chapter-handwrite（手写入口）
└── ChiefChat（内嵌，见 04）
```

## Dimensions

- 分组行：`simple-project-chapter-file-row`（flex，含 number/title/count/actions 段）；separator 分隔文件项 [RUNTIME_CONFIRMED 类存在，具体数值 UNKNOWN]
- 长按提示：`simple-project-chapter-long-press-hint`（长按触发操作菜单）

## Visual

- 章节文件行：文件卡片式（file-main 主区 + trailing 尾区），选中/激活用 active 体系（--accent-active-soft / text）
- 搜索：复用胶囊搜索（推断同 chief-chat-search 体系，[INFERRED]）
- 空状态：`simple-project-chapter-group-empty` / `simple-empty-note`

## Controls

- 分组创建/折叠/重命名（group-create / toggle / toggle-editing）
- 章节文件选择（file-select）、章节动作（file-actions）
- 手写（chapter-handwrite）、长按菜单（long-press-hint）
- 搜索（chapter-search）
- 项目标记（active-mark）

## States

- 分组折叠/展开（group-toggle）
- 分组重命名模式（toggle-editing）
- 空分组/空项目（group-empty / empty-note）
- 章节选中/激活（file-select）
- 长按操作提示

## Interactions

- 点章节文件 → 打开章节编辑（chapter-editor surface / dock）
- 长按 → 上下文动作菜单（重命名/删除/移动？[INFERRED]）
- 搜索 → 过滤章节列表
- 手写 → 手写输入模式（simple-project-chapter-handwrite）

## Storage / State

- `novelforge.workspaceMode.v2`
- 章节分组结构持久化：`projects:update-chapter-groups` IPC [RUNTIME_CONFIRMED]
- 章节文件：`workspace/projects/{id}/chapters/chXXX/{agent}.md` [REPORT_CONFIRMED]

## Window behavior

主窗口内单页；章节编辑器可浮出（见 08）。

## Evidence

- 类族存在性：CSS [RUNTIME_CONFIRMED]
- 分组持久化 IPC：preload [RUNTIME_CONFIRMED]
- 具体视觉数值（行高/缩进）：[UNKNOWN]（CSS 类名存在但未逐一解析）

## Unknown

- 章节分组树在 292px 栏内的精确滚动/嵌套样式
- 长按菜单的具体动作集
- simple 模式下聊天是否占据右 380px 列（[INFERRED] 是）
