# 10 — Outline

> 大纲管理：总纲/卷纲/章纲体系，与 Agent 写作流程联动（生成方向建议 → 应用）。

## Purpose

管理全书大纲结构（总纲、卷、章），支持 AI 生成"方向建议"并应用到正式大纲。

## Entry

- creative 工作区：`creative-outline-folder-list` 窗口（大纲窗）
- 与素材窗同为文件夹树体系（outlinePaths / outline-identity 类）

## Layout [RUNTIME_CONFIRMED 类族，数值 UNKNOWN]

```
creative-outline-folder-list
├── outline-main-group（主分组）
├── outline-group（卷/章分组）
│   └── outlinePaths（路径条目，同 creative-path-* 体系）
└── outline-identity（大纲条目身份标记）
```

## Hierarchy

```
OutlineManager
├── outline-folder-list（树）
│   └── 卷 → 章 分组路径
├── 状态（getStatus：大纲完整性/缺失项）
├── 方向生成（generateDirections）
└── 方向应用（applyDirection）
```

## Controls（IPC 面 [RUNTIME_CONFIRMED]）

| 操作 | IPC |
|---|---|
| 获取大纲状态 | `outline-manager:get-status` |
| 生成方向建议 | `outline-manager:generate-directions` |
| 应用方向建议 | `outline-manager:apply-direction` |

## States

- 大纲缺失/完整状态（get-status 返回）
- 方向生成中 / 可应用
- 应用结果（冲突/成功）

## Interactions

- 检查大纲 → get-status（报告缺失卷/章）
- 生成方向 → AI 给出 2+ 个方向建议
- 应用方向 → 写回大纲文件（用户确认后）

## Storage / State

- 大纲文件：`workspace/projects/{id}/` 下大纲 markdown（.md 身份解析：`identity.kind === "volume"` 有 summary；x7t 函数解析大纲文件 title/identity [RUNTIME_CONFIRMED]）
- 大纲身份：material-editor-outline-identity 同体系（大纲条目在素材库中可编辑）

## Window behavior

creative 模式 dock/floating 窗口；方向应用对话框为 modal（[INFERRED]）。

## Evidence

- 类族/IPC：CSS + preload [RUNTIME_CONFIRMED]
- 大纲文件解析：main.pretty.js x7t（identity.kind / summary 字段）[RUNTIME_CONFIRMED]
- 卷纲/章纲文件模型：reports/09 DATA_MODEL [REPORT_CONFIRMED]

## Unknown

- 大纲树的具体层级视觉（卷/章/节）
- 方向建议对话框的 UI（列表？卡片？）
- 大纲与章节文件的双向同步机制
