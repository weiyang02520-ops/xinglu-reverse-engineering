# 13 — Settings

> 全局设置（chief-settings 体系）与主编设置（chief-editor-settings-dialog）。大型圆角 modal + 左侧一级导航 + 顶部/内部二级导航。

## Purpose

应用级配置：外观（主题/缩放）、模型库、写作选项、技能、会员、客服等；主编设置：总编行为（模型/写作/技能/反馈）。

## Entry

- 首页/工作区"设置入口"打开全局设置 [SCREENSHOT_CONFIRMED]
- 主编设置：`chief-editor-settings`（独立对话框）

## Layout [RUNTIME_CONFIRMED + SCREENSHOT_CONFIRMED]

```
chief-settings-backdrop（遮罩：工作区保留在背景，模糊/暗化 [SCREENSHOT_CONFIRMED]）
└── chief-settings-shell（大型圆角 modal，radius window 16px）
    ├── 左侧一级导航 chief-settings-nav
    │   ├── chief-settings-nav-title
    │   └── 导航项 × N（选中项有 selection-slider 滑块指示）
    ├── 顶部/内部二级导航（chief-settings-subtab-indicator）
    │   └── 子选项卡（带底部指示条）
    ├── chief-settings-content
    │   ├── 分区（general/appearance/membership/invite/feedback/skills/support...）
    │   │   ├── chief-settings-section + item（每项：icon + copy + actions）
    │   │   └── mode-row / mode-switcher（segmented）
    │   └── chief-settings-subdialog（嵌套子对话框）
    └── chief-settings-action-button（操作按钮，-danger / -muted 变体）
```

## 已确认设置项 [RUNTIME_CONFIRMED 类族]

| 分区 | 类族 | 内容 |
|---|---|---|
| 外观 | chief-appearance-mode-switcher / chief-interface-scale-switcher | 主题 light/dark、缩放 normal/medium/large |
| 常规 | chief-general-section / chief-chief-model-section | 总编模型 |
| 生成 | chief-generation-section / generation-switcher / generation-option-row | 写作生成选项 |
| 高质审阅 | chief-high-quality-review-focus-item | 审阅聚焦项 |
| 反馈 | chief-feedback-section / field / intro / kind-switcher / error | 意见反馈 |
| 会员 | chief-membership-*（account-panel / plan / order / 激活码 / 邀请） | 账户/套餐/订单/邀请 |
| 邀请 | chief-invite-*（hero / reward / stats-grid / website-card / copy） | 邀请奖励 |
| 头像 | chief-avatar-*（card / picker / preview / settings-item） | 头像设置 |
| 关于 | chief-about-*（version-card / update-result / font-notice） | 版本/更新 |

## Segmented Control 证据 [RUNTIME_CONFIRMED]

- `chief-appearance-mode-switcher` / `chief-interface-scale-switcher` / `chief-generation-switcher` / `chief-feedback-kind-switcher`
- `chief-settings-selection-slider`：**滑块式选中指示器**（非高亮色块，是滑动条）
- `chief-settings-mode-row` + `mode-switcher`：行内切换控件

## Dimensions

- 对话框：radius 16px（--nf-radius-window），大型（截图显示接近全宽/高，精确尺寸 [UNKNOWN]）
- 导航项：nav 区 + selection-slider
- 控件高度：--nf-control-height-dialog 38px（对话框内控件）

## Visual

- backdrop：工作区保留在背景 + 遮罩（`chief-settings-backdrop`；overlay token 见 01）[SCREENSHOT_CONFIRMED]
- 项行：item + item-icon + item-copy + item-actions + inline-actions
- danger 按钮：`action-button-danger`（--nf-color-error 系）
- 紧凑开关：`chief-settings-compact-switch`（toggle 变体）

## Controls

- 一级导航（nav-title 分组）
- 子选项卡（subtab-indicator）
- segmented（mode-switcher + selection-slider）
- 开关（compact-switch）
- 操作按钮（action-button / -danger / -muted）
- 嵌套对话框（subdialog + backdrop）

## States

- 选中导航项（slider 位置）
- 子选项卡激活（indicator）
- 反馈错误（feedback-error）
- 会员登录/注册（account-action-button--login/--register）

## Interactions

- 切主题 → `novelforge.appearanceTheme.v1` + data-theme 切换（全窗即时生效）
- 切缩放 → `novelforge.interfaceScale.v1` + setZoomFactor（1 / 1.1 / 1.3）
- 保存总编设置 → `chief-editor:get-settings / save-settings`
- 会员操作 → membership IPC（login-or-create / register / plans / order / redeem）
- 反馈提交 → feedback:submit

## Storage / State

- localStorage：`novelforge.appearanceTheme.v1` / `novelforge.interfaceScale.v1` / `novelforge.workspaceMode.v2`
- 总编设置：主进程（get/save-settings）
- 会员凭证：userData `membership_credentials.json`（**高敏感**，不入库）[REPORT_CONFIRMED]

## Window behavior

主窗口内 modal 覆盖层；`chief-editor-settings-dialog` 独立对话框（可嵌套 subdialog）。

## Evidence

- 全部类族/数值：CSS [RUNTIME_CONFIRMED]
- 截图对照：全局设置截图（遮罩、大型圆角 modal、左侧一级导航、顶部/内部二级导航、segmented、外观设置、interface scale、light/dark）与类结构完全吻合 [SCREENSHOT_CONFIRMED + RUNTIME_CONFIRMED]

## Unknown

- 一级导航项完整清单（外观/模型/写作/技能/会员/客服…？）
- modal 精确尺寸（宽高比）
- 子选项卡的具体组
