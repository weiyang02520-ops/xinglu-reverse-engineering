# 04 — Chat

> 总编聊天系统：贯穿首页（无项目时）与工作区（simple/creative 内嵌或独立窗）。
> 这是星炉最核心的交互区，也是"Agent Harness 感"的来源。

## Purpose

与"总编"（Chief Editor）对话的实时聊天：用户指令 → Agent 运行 → 流式消息 + 工具运行可视化 → 章节/素材产出。支持多消息类型（文本/图片/音频/视频/文件/工具运行）。

## Entry

- 首页中央区（无项目）；simple 工作区右侧聊天；creative 工作区独立 chat-window 面板
- 聊天历史持久化在项目内：`.novelforge/chief-editor-chat.json` + `chief-editor-chat-history.json` [REPORT_CONFIRMED]

## Layout [RUNTIME_CONFIRMED]

```
chief-header（28px 头像 | 标题 | 搜索 148px | 分支按钮 62px）
─────────────────────────────────────────────
chat 消息流（scroll，大面积）           ┌ chat-message 用户（右侧/标记）
                                        ├ chat-message 总编（含 tool-run 内联）
                                        ├ chat-tool-run（工具运行卡片）
                                        └ chat-history-load-button（顶部加载历史）
─────────────────────────────────────────────
chat-composer（radius 20px，grid）
  ├ grid-area: toolbar → chat-composer-toolbar
  │   └ chat-capability-controls（能力开关组，flex wrap gap 7px）
  │       └ chat-capability-toggle / switch（每能力一个开关）
  ├ 输入区（textarea，可附件）
  └ 发送按钮（+ 语音按钮 + 模型快速选择）
```

- composer 背景：`linear-gradient(180deg, #ffffff85, transparent 72%)` 覆盖在 panel/field 混色上，`inset 0 1px 0 #ffffffeb` 内高光 + 底部内描边 + 双外阴影；padding `8px 12px 8px 8px`，gap 8px [RUNTIME_CONFIRMED]
- toolbar 左缩进 34px（为模型选择器/头像让位），gap 10px [RUNTIME_CONFIRMED]

## Hierarchy

```
ChiefChat
├── chief-header（见 03）
├── ChatMessageList
│   ├── ChatMessage（user / assistant）
│   │   ├── chat-avatar（角色头像）
│   │   ├── Markdown 渲染正文
│   │   ├── 附件卡片（chat-attachment-*：audio/image/file）
│   │   ├── chat-tool-run（工具运行：name/progress/result/detail）
│   │   └── chat-media-generation-status（媒体生成状态）
│   ├── ChatToolRun（独立卡片：list/details/continuation/interjection）
│   └── ChatHistoryLoader（chat-history-load-button）
└── ChatComposer
    ├── chat-composer-toolbar
    │   ├── chat-capability-controls（能力开关组）
    │   └── 附件按钮（chat-attach-button）
    ├── 输入 textarea
    └── 发送 / 语音 / 模型选择（图标按钮）
```

## 消息类型（全部 [RUNTIME_CONFIRMED] 类族）

| 类型 | 类族 | 能力 |
|---|---|---|
| 文本 | chat-message + Markdown | 标题/列表/表格/代码块/引用 |
| 图片 | chat-image-grid-choice / lightbox | 网格、灯箱（prev/next/count）、下载、生成图选择 |
| 音频 | chat-audio-attachment / player / lyrics | 播放器、歌词、候选列表、下载 |
| 视频 | chat-video 系（附在 attachment） | 预览 |
| 文件 | chat-file-link / file-edit-chip | 章节链接、内联编辑、外部编辑标记 |
| 工具运行 | chat-tool-run-* | 工具名、进度数字、结果、明细 |
| 外部链接 | chat-external-url-link | 打开外部 URL |
| 上下文菜单 | chat-context-menu | 消息操作 |

## Chat Composer 结构 [RUNTIME_CONFIRMED]

- **能力按钮组**：`chat-capability-controls` 内多个 `chat-capability-toggle`（开关式，`chat-capability-switch` + track）——**能力以开关呈现，而非普通按钮**；按项目持久化：`novelforge.chiefEditorChatCapabilitiesByProject.v1`
- 模型快速选择：composer 内模型切换（preload `provider:selectModel`，[RUNTIME_CONFIRMED]）
- 语音：`voiceRecordingDialogPosition.v1` 存储（语音录制对话框，位置记忆）
- 发送/停止：`chiefEditor.chat` / `chat-stop` IPC（停止运行）
- 输入清晰度：`chief-editor:analyze-input-clarity`（输入改写弹窗 `input-clarity-dialog`）——发送前可选"清晰化"改写

## States

- 流式生成中：总编消息流式追加（`chief-editor:chat-event` 事件流）+ 工具运行进度（`chat-tool-run-progress-number`/digit 动画）
- 停止：composer 发送按钮变停止按钮（`chat-stop`）
- 思考中：等待态（`--nf-color-wait` 琥珀色，`chat-continuation-wait`/dots 类）
- 历史加载：顶部 `chat-history-load-button`（chat-history-loader）
- 删除确认：`chief-editor:delete-confirmation-request`（可整体禁用：`set-delete-confirmation-enabled`）

## Interactions

- 发送消息 → `chiefEditor.chat({...})` → invoke → 主进程 Agent 运行 → `onChatEvent` 流式事件渲染
- 运行进行中 → `novelforge:workflow:progress` 进度事件（与 workflow 面板共享，见 11）
- 消息内文件 → 章节链接可打开 chapter-editor（`chat-chapter-editor-panel` 类）
- 工具运行块 → 可展开明细（chat-tool-run-details / divider / continuation）
- 搜索 → 148px 胶囊输入，聚焦展开

## Storage / State

- 项目级聊天历史：`.novelforge/chief-editor-chat*.json` [REPORT_CONFIRMED]
- 能力开关按项目：`novelforge.chiefEditorChatCapabilitiesByProject.v1` [RUNTIME_CONFIRMED]
- 语音对话框位置：`novelforge.chiefEditor.voiceRecordingDialogPosition.v1`
- 无项目时可用 `projects:ensure-chat` 创建隐式聊天会话

## Window behavior

- 首页：嵌在中央区
- creative：独立窗 `creative-chat-window`（见 06）
- global-overlay surface：悬浮层可承载聊天会话（多窗口同步，见 15）

## 为什么是 "Agent Harness" 而非普通聊天机器人（UI 原因分析）

1. **工具运行是头等消息类型**：`chat-tool-run-*` 有 66 个样式类（body/details/progress-number/digit/continuation/interjection），运行过程以进度数字 + 明细卡内联在对话流中——用户看到"Agent 在做什么"
2. **能力开关组**：composer 上是能力开关矩阵而非单一发送键——用户配置"这轮对话允许 Agent 用什么能力"
3. **停止/中断**：专门的 stop 通道 + 删除确认门禁——Agent 动作可被用户随时打断
4. **媒体生成状态**：chat-media-generation-status 把异步生成任务（图/乐）接进对话流
5. **历史 + 分支**：chat-history 加载器 + project-branches 入口——对话是项目资产而非一次性请求
6. **多窗口承接**：章节编辑器/全局悬浮层可共享同一会话（chapter-editor-view:set-session）——对话是跨窗口的"运行状态"

## Evidence

- 全部类族/样式：CSS [RUNTIME_CONFIRMED]
- IPC 通道：preload.pretty.cjs chiefEditor 模块 [RUNTIME_CONFIRMED]
- 截图对照：首页截图的聊天消息区域/composer/能力按钮/模型选择/语音/发送按钮全部对应 [SCREENSHOT_CONFIRMED]

## Unknown

- 能力开关的具体能力清单（写作/搜索/图片/音乐…？[INFERRED] 自 reports/15）
- 消息气泡的左右布局细节（用户/总编是否分侧）[UNKNOWN]
- composer 键盘快捷键（Enter 发送 / Shift+Enter 换行）[UNKNOWN]
