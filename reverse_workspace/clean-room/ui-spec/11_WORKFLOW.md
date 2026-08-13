# 11 — Workflow / Agent UI

> 总编写作工作流：Agent 节点可视化 + 运行进度 + Agent 检视/追踪。星炉的核心 Agent Harness 呈现。

## Purpose

展示"总编 → 多 Agent"写作工作流的静态结构（节点/连接）与运行态（进度/状态），并提供 Agent 配置检视（身份/模型/工具）。

## Entry

- 主 grid 中央区（`workflow-canvas` grid-area 2/3，z-index 8）[RUNTIME_CONFIRMED]
- 聊天中运行写作时进度事件联动（`novelforge:workflow:progress`）

## Layout [RUNTIME_CONFIRMED]

```
workflow-view
├── workflow-canvas（主区：surface-canvas 背景，overflow visible）
│   ├── workflow-map（节点图）
│   │   ├── agent-node × N（116px 卡片，可折叠）
│   │   │   ├── agent-node-top-actions（折叠/展开按钮）
│   │   │   ├── agent-node-index（序号）
│   │   │   ├── agent-node-identity（身份区：title + model summary）
│   │   │   │   ├── agent-node-title
│   │   │   │   └── agent-node-model-button（模型徽章按钮）
│   │   │   ├── agent-node-status（pill 状态徽章）
│   │   │   ├── agent-node-main / main-side（主体 + 侧信息）
│   │   │   └── agent-node-config-layer（配置层，config-button 展开）
│   │   └── workflow-arrow（节点连接箭头）
│   └── workflow-legend（图例：density-toggle 密度切换）
├── workflow-side-panel（右/下侧面板：radius 16px，shadow-panel，gap 12px，padding 16px）
│   ├── workflow-side-panel-header
│   ├── workflow-side-panel-agent（当前 agent 详情）
│   │   └── agent-inspector-panel / body（检视器）
│   ├── agent-runtime-panel（运行态）
│   ├── agent-trace-panel（追踪）
│   ├── workflow-panel-section（章节卡 / 输出卡）
│   │   ├── workflow-chapter-card（章节进度卡）
│   │   └── workflow-output-card（输出文件卡）
│   ├── workflow-panel-token（token 统计）
│   └── workflow-run-button（32×32 运行按钮）
└── workflow-heading + agent-settings-heading（标题）
```

## Agent Node 视觉 [RUNTIME_CONFIRMED]

- 尺寸：**116px 高**，宽 100%（网格内），radius **8px**
- 背景：surface-panel（light）/ chip-bg（dark）+ `--nf-shadow-card`
- 边框：border-subtle；transition 0.14s（border/shadow/opacity/transform）
- 内部 grid：`auto minmax(0,1fr)`，padding `11px 12px 10px`
- 状态徽章：pill 999px、**18px 高**、micro 11px 字、font-weight **820**、padding 0 7px

### 节点状态视觉 [RUNTIME_CONFIRMED（token 系）]

| 状态 | 证据（--nf-skin/node-* token） |
|---|---|
| 正常 | border-subtle + shadow-card |
| hover | `--nf-skin-node-hover-border` + `--nf-skin-node-hover-shadow`（`0 0 0` 或阴影提升） |
| 激活/running | `--nf-skin-node-active-bg` + `--nf-skin-node-active-border` + `--nf-skin-node-active-ring`（外环） |
| 完成 | `--nf-skin-node-done-bg` + `--nf-skin-node-done-border` |
| 选中 | `--nf-skin-node-selected-ring` + `--nf-skin-node-selected-inner` |
| active-agent 阴影 | `--nf-shadow-active-agent`（`0 16px 32px -24px`） |

## Agent Inspector / Trace

- `agent-inspector-panel` / `agent-inspector-body`：检视当前节点配置（身份/模型/输出路径 `agent-material-output-path`）
- `agent-trace-panel`：运行追踪
- `agent-runtime-panel`：运行时状态
- 打开方式：点节点或 config 按钮（`agent-node-config-button-active` 态）；[INFERRED] 展开侧面板
- agent 编辑对话框：`agent-dialog`（身份）、`agent-provider-dialog`（模型提供商，provider-api-fields / provider-option）

## 模型显示

- `agent-node-model-button`：节点上的模型徽章按钮（点击配置模型，[INFERRED]）
- `workflow-agent-model-line`：侧面板模型行

## 进度表达 [RUNTIME_CONFIRMED + INFERRED]

- 运行中：节点状态切换（active 系 + active-agent 阴影 + ring）
- 进度事件流：`novelforge:workflow:progress`（主进程推送，聊天 tool-run 与 workflow 共用）
- 章节卡（chapter-card）显示每章完成度；output-card 显示产出文件
- token 统计：workflow-panel-token（用量展示）

## Controls

- 运行/停止：`workflow-run-button`（32×32）/ `chiefEditor.stop()`（`novelforge:workflow:stop`）
- 节点：折叠（collapse-button）/ 展开（expand-button）/ 配置（config-button）
- 密度切换：`workflow-density-toggle`
- 图例：`workflow-legend-items`

## States

- idle / running（节点 active + ring）/ done（done 系）/ error（error 系 token，见 01）
- 选中（selected ring）
- 空态：`agent-empty-state`

## Interactions

- 运行写作 → workflow:progress 事件流 → 节点逐个转 active → done
- 点节点 → 侧面板显示 inspector（身份/模型/输出）
- 点模型按钮 → provider 选择对话框
- 展开配置层 → 节点内嵌配置表单（agent-node-config-layer）

## Storage / State

- Agent 注册表：`prompts/agents/`（每 agent 一个配置）[REPORT_CONFIRMED]
- IPC：`agents:list/create/duplicate/update-*`（identity/read-files/output-files/order/prompt-paths/provider/final-text-source/delete）[RUNTIME_CONFIRMED]
- 运行设置：`projects:update-workflow-settings`

## Window behavior

- workflow-canvas 是主窗口中央区的一部分（grid-area 2/3）
- inspector 在侧面板内；agent 编辑为 modal 对话框

## Evidence

- 节点/面板布局数值：CSS [RUNTIME_CONFIRMED]
- 状态 token：CSS [RUNTIME_CONFIRMED]
- IPC：preload agents/chiefEditor [RUNTIME_CONFIRMED]
- Agent 注册表文件：reports/11 [REPORT_CONFIRMED]

## Unknown

- 节点间连线（workflow-arrow）的具体绘制（SVG/线段/弯折）
- 节点排序（纵向列表 vs 横向流程图）——canvas 布局方向 [UNKNOWN]
- inspector 打开的具体交互（点节点？点按钮？）
- 运行进度与聊天的联动细节（并行更新？）
