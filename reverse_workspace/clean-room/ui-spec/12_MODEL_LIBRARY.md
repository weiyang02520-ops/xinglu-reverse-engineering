# 12 — Model Library

> 模型库：管理模型提供商（OpenAI 兼容/Anthropic/Gemini 等）与 API Key、选择当前模型。

## Purpose

配置与选择 LLM 提供商/模型：添加、编辑、删除、设为当前；官方模型目录 + 自定义 API。

## Entry

- 全局设置（chief-settings）内一级入口 / 聊天 composer 模型选择器
- 主进程模型管理器：`provider:get-summary` / `official-models:get-catalog`

## Layout [RUNTIME_CONFIRMED]

```
model-library
├── model-library-heading（+ heading-actions：fetch-button 拉取目录、add-toggle 添加）
├── model-library-list（grid，gap 7px）
│   └── model-library-item（56px 卡片，grid [minmax(0,1fr) auto]，gap 12px）
│       ├── item-icon（提供商图标）
│       ├── 名称/描述（item-copy）
│       ├── item-actions（select-button / edit-button / delete-button）
│       └── advanced-row / advanced-toggle（高级配置展开）
├── model-library-edit-form（编辑表单：provider 选择 + API 字段）
├── model-library-empty（空态）
└── model-library-fetch-button（官方目录刷新）
```

## Dimensions

- 模型项：min-height **56px**、radius **14px**（--nf-radius-card）、border subtle 54%、padding `7px 9px 7px 10px`、gap 12px [RUNTIME_CONFIRMED]
- 列表：grid gap 7px [RUNTIME_CONFIRMED]

## Visual

- 项背景：surface-panel 36% 透明度（透出下层）
- 编辑表单：`model-library-edit-form`（provider-api-fields 同 agent-provider-dialog 体系）

## Controls

| 操作 | IPC |
|---|---|
| 添加 | `provider:save-chat-completions`（保存 OpenAI 兼容配置） |
| 选择 | `provider:select-model` |
| 删除 | `provider:delete-model` |
| 摘要 | `provider:get-summary` |
| 官方目录 | `official-models:get-catalog` / `refresh-catalog` / `get-usage-balance` |

## States

- 空态：model-library-empty（引导添加）
- 高级模式：advanced-toggle 展开 advanced-row（高级字段）
- 选中项：select-button 标记当前

## Interactions

- 点 select → 设为当前模型（聊天 composer 同步显示）
- 添加 → 表单（Base URL / API Key / 模型名）
- 官方模型 → 目录选择（provider-option 列表）
- 余额：usage-balance（官方模型用量）

## Storage / State

- 模型配置：主进程 userData JSON（reports/11：`membership_credentials.json` 等之外另有模型配置，[INFERRED] 位置见 reports/09）
- 当前选择：主进程 provider 状态（聊天选择器同步）

## Window behavior

设置对话框（modal）内的面板；非独立窗口。

## Evidence

- 布局/尺寸：CSS [RUNTIME_CONFIRMED]
- IPC：preload provider/officialModels [RUNTIME_CONFIRMED]

## Unknown

- 官方模型目录 UI 形态（列表/网格/筛选）
- 高级字段清单（温度/上下文/工具开关？）
- API Key 输入的安全呈现（掩码？）
