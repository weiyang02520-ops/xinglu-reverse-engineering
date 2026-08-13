# 03 — Home / Project List

> 首页 = 无项目选中时的主窗口内容：左侧项目卡片列表 + 中央总编聊天 + 底部 Chat Composer。
> 证据：CSS [RUNTIME_CONFIRMED] + 用户真实首页截图 [SCREENSHOT_CONFIRMED]。

## Purpose

应用启动后的默认视图（主窗口、surface=默认）：项目选择 + 总编聊天首页。选中项目后进入 simple/creative 工作区。

## Entry

- 启动默认进入；项目可被选中/切换（`novelforge:projects:select` IPC）
- 项目级"默认项目聊天"持久化：`novelforge.creativeWorkspaceDefaultProjectChat.v1`

## Layout（主 grid 三区）[RUNTIME_CONFIRMED]

```
┌──────────────┬──────────────────────────────────┐
│ 左侧 292px    │ 中央 minmax(560px,1fr)            │
│ 项目栏        │ 总编聊天区                        │
│  ┌────────┐  │  chief-header（头像|标题|搜索|分支）│
│  │项目大卡片│  │  消息流（大面积，滚动）             │
│  │× N     │  │  chat-composer（底部，20px 圆角）   │
│  └────────┘  │  composer-toolbar（能力|模型|语音|发送）│
│ 新建按钮      │                                  │
│ 设置入口      │                                  │
└──────────────┴──────────────────────────────────┘
```

- 第 5 列 380px 在首页态为空白/隐藏（截图未见右侧面板，[SCREENSHOT_CONFIRMED] 推断列仍占位，[INFERRED]）
- 左栏项目列表：`.project-list` — flex column、gap 8px、max-height **210px**、margin-bottom 16px、可滚动
- 项目卡片：`.project-list-item` — grid `minmax(0,1fr) 72px`、min-height **48px**、radius **8px**、border 1px subtle、背景 surface-canvas、padding 7px、gap 8px

## Hierarchy

```
App (surface=default)
└── nf-window (grid)
    ├── titlebar（品牌 mark + 音乐播放器）
    ├── 左栏
    │   ├── project-list
    │   │   └── project-list-item × N（项目名 + 72px 动作区）
    │   ├── project-manager-create-button（新建）
    │   └── 设置/分支入口（chief-branch-button 等）
    └── 中央
        ├── chief-header
        │   ├── 头像/品牌 mark（28px）
        │   ├── 标题区
        │   ├── chief-chat-search（148px 胶囊搜索框）
        │   └── chief-branch-button（分支按钮，min-width 62px）
        ├── chat 消息流（chat-* 系列，见 04）
        └── chat-composer + chat-composer-toolbar（见 04）
```

## Dimensions

| 区域 | 值 | 证据 |
|---|---|---|
| 左栏宽度 | 292px | CSS grid [RUNTIME_CONFIRMED] |
| 中央最小宽 | 560px | CSS grid [RUNTIME_CONFIRMED] |
| 项目列表最大高 | 210px | CSS [RUNTIME_CONFIRMED] |
| 项目卡片高 | ≥48px | CSS [RUNTIME_CONFIRMED] |
| 搜索框 | 148px 宽 × 32px 高（toolbar 高度） | CSS [RUNTIME_CONFIRMED] |
| 分支按钮 | min-width 62px × 36px，radius 8px | CSS [RUNTIME_CONFIRMED] |
| titlebar | 44/52px | CSS [RUNTIME_CONFIRMED] |

## Visual

- 左栏卡片：surface-canvas 底、subtle 边框、8px 圆角；hover 用 `--nf-skin-hover-bg`（推断，[INFERRED]）
- 搜索框：**999px 胶囊**、chip 半透明底、文字 secondary 72%、`inset 0 1px #fff9` 内高光、聚焦/展开宽度过渡 0.18s（`transition: width .18s cubic-bezier(.2,.8,.2,1)`）[RUNTIME_CONFIRMED]
- 分支按钮：面板底 + subtle 边框 + **font-weight 850** + compact 14px 字 [RUNTIME_CONFIRMED]

## Controls

- 新建项目按钮（`project-manager-create-button`，打开 `project-manager-dialog` 新建表单）
- 分支入口按钮（`chief-branch-button`）
- 搜索聊天记录（`chief-chat-search`）
- 项目卡片动作区（72px 列，含项目操作）
- 设置入口（全局设置，见 13）

## States

- 空项目列表：显示创建引导（`.project-list-note`）[RUNTIME_CONFIRMED 类存在，细节 UNKNOWN]
- 选中项目：active 标记（`.simple-project-active-mark` 类存在于 simple 体系；首页选中态 [INFERRED] 用 active 面）
- 无项目时总编聊天仍可用（`projects:ensure-chat` IPC 存在，[RUNTIME_CONFIRMED]）→ 聊天可先于项目存在

## Interactions

- 点击项目卡片 → `projects:select` → 广播 `novelforge:projects:changed` → 进入工作区
- 新建 → `project-manager-dialog`（表单：名称/类型等，字段 [UNKNOWN]，见 18）
- 搜索聚焦 → 宽度从 148px 展开（过渡 0.18s）[RUNTIME_CONFIRMED]
- 分支按钮 → `project-branches-dialog`（见 14）

## Storage / State

- localStorage：`novelforge.workspaceMode.v2`（simple/creative）、`novelforge.creativeWorkspaceDefaultProjectChat.v1`、主题/缩放
- IPC：`projects:list/create/select/rename/delete`、`projects:changed` 广播
- 项目数据：`workspace/projects/{id}/project.md` [REPORT_CONFIRMED]

## Window behavior

主窗口内单页面；无独立窗口。

## Evidence

- 布局/尺寸/控件：CSS [RUNTIME_CONFIRMED]
- 截图对照：截图"顶部窗口区域、左侧项目大卡片、新建按钮、中央总编聊天、搜索聊天记录、分支入口、设置入口、大面积聊天消息区域、底部大型 Chat Composer、能力按钮、模型选择、语音、发送按钮"全部在类结构中可对应 [SCREENSHOT_CONFIRMED + RUNTIME_CONFIRMED]
- 右侧 380px 列首页态内容：[UNKNOWN]（截图未覆盖，见 18）

## Unknown

- 项目卡片 72px 动作区的具体按钮（打开/删除/更多？）
- 新建对话框字段清单（类别/写作预设？）
- 首页右栏 380px 是否可见及内容
