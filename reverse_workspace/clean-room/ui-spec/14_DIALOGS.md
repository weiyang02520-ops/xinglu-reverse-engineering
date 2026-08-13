# 14 — Dialogs

> 对话框体系：modal / popover / 确认 / 输入 / 专用对话框。

## Purpose

应用内全部对话框：通用确认、文本输入、分支管理、故事摘要、删除确认、输入清晰度、窗口选择、Agent 编辑、会员注册等。

## 呈现模型（主进程）[RUNTIME_CONFIRMED]

- `modal`：全窗口遮罩（`Ux` 函数：modal 无锚点时铺满窗口 bounds）
- `popover`：从锚点弹出（`l7t`：按锚点 bounds 定位子视图）
- 渲染器侧：`modal-backdrop`（z-index 1/2 两层）

## 已确认对话框清单 [RUNTIME_CONFIRMED 类族 + REPORT_CONFIRMED]

| 对话框 | 类/通道 | 用途 |
|---|---|---|
| 通用确认 | `confirm-dialog` | 删除/危险操作确认 |
| 文本输入 | `text-input-dialog` | 名称/重命名输入 |
| 删除确认 | `chief-editor:delete-confirmation-request/resolve` | 聊天内删除门禁（可整体禁用） |
| 分支管理 | `branch-dialog`（base/header/body/toolbar/tabs/panel/error）+ `branch-card` | 项目分支创建/切换/删除/重命名 + 分支策略 |
| 分支策略 | `branch-strategy-card`（copy/eyebrow/radio）+ `branch-strategy-list` + `branch-strategy-summary` + `branch-strategy-note` | 分支策略选择 |
| 故事摘要 | `story-summary-*`（editor-dialog / form / field / mode-options / mode-slider / auto-update-card） | 故事梗概编辑 |
| 输入清晰度 | `input-clarity-dialog`（skeleton 占位类 `input-clarity-skeleton-*`） | 发送前改写输入 |
| 窗口选择 | `window-picker` | 全局悬浮层选择窗口 |
| 主编设置 | `chief-editor-settings-dialog` | 总编设置 |
| Agent 编辑 | `agent-dialog` / `agent-provider-dialog` | Agent 身份/模型配置 |
| 新建项目 | `project-manager-dialog` + `project-manager-create-form` + `project-name-field` | 新建项目 |
| 素材编辑 | `material-editor-dialog` | 素材编辑 |
| 会员注册 | `membership-register-dialog` | 注册 |
| 更新提示 | `app-update-dialog` | 应用更新 |

## 分支对话框细节 [RUNTIME_CONFIRMED]

```
branch-dialog（radius window 16px；base-shadow = material-shadow-window；backdrop #0000006b）
├── branch-dialog__header（标题 + 关闭）
├── branch-dialog__tabs（标签页：分支 / 策略？）
├── branch-dialog__body
│   ├── branch-card-list
│   │   └── branch-card__main
│   │       ├── title-row + current-pill（当前分支徽标）
│   │       ├── meta（源分支信息）
│   │       ├── actions（switch / rename / delete）
│   │       └── rename-form（重命名模式）
│   └── branch-strategy-list
│       └── branch-strategy-card（radio + eyebrow + copy）
└── branch-dialog__toolbar + error
```

- 分支策略：radio 选择（strategy-card__radio）、summary 说明
- 对话框阴影：light `inset 0 1px 0 #ffffffc7, 0 10px 28px -24px` + window 级阴影

## 故事摘要对话框 [RUNTIME_CONFIRMED]

- `story-summary-editor-dialog`：梗概编辑表单（field）
- 模式：`mode-options` / `mode-slider`（滑块切换模式）+ `auto-update-card`（自动更新开关）

## 通用视觉 [RUNTIME_CONFIRMED]

- 底色：panel（`--nf-color-surface-panel`）+ `--nf-branch-dialog-base`（panel 94% + 白 6%）
- 边框：border-subtle 70% + 白 30% 混合
- 圆角：--nf-radius-window 16px
- 阴影：--nf-material-shadow-window（`0 24px 64px -40px` light / `0 28px 72px -24px` dark）
- hover 行：primary 8% 混合（--nf-branch-dialog-hover）

## Controls

- 关闭、确认/取消、radio、tabs、重命名表单、滑块

## States

- 分支：当前分支（current-pill）、重命名编辑中（rename-form）、错误（dialog__error）
- 删除确认：请求/取消事件（onDeleteConfirmationRequest / Cancelled）

## Storage / State

- 分支结构：`projects:create-branch / select-branch / delete-branch / rename-branch / update-branch-strategy` [RUNTIME_CONFIRMED]
- 分支数据：项目 `.novelforge/branches/` [REPORT_CONFIRMED]
- 删除确认启用：`chief-editor:set-delete-confirmation-enabled`
- 对话框位置记忆：`voiceRecordingDialogPosition.v1` 等

## Window behavior

- 多数对话框：主窗口内 DOM modal（backdrop 层叠）
- 会话级 modal/popover：主进程用 global-overlay WebContentsView 呈现（bounds 定位，见 15）
- 输入清晰度：先弹窗再发送（异步 analyze-input-clarity）

## Evidence

- 类族/数值：CSS [RUNTIME_CONFIRMED]
- 呈现状态机：main.pretty.js（Ux/l7t modal/popover 分支）[RUNTIME_CONFIRMED]
- 对话框清单：reports/06 [REPORT_CONFIRMED]

## Unknown

- 各对话框精确尺寸
- confirm-dialog / text-input-dialog 的类族细节（类名出现但样式未逐一解析）
