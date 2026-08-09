# 06 — 页面识别报告 (Pages)

> 注意: 本项目是**单页应用(SPA)+ 多窗口 Electron**, 无传统多页面。
> "页面" = 视图(view)/面板(panel)/对话框(dialog)/窗口(surface)的组合。

## 1. 顶层结构

### 窗口 (Electron BrowserWindow) [CONFIRMED]

| 窗口 | 内容 | 说明 |
|---|---|---|
| 主窗口 | web/index.html (surface=默认) | 主工作区: 项目/章节/聊天 |
| 章节编辑器窗口 | surface=chapter-editor | 独立章节编辑器(可浮窗/停靠) |
| 全局悬浮层窗口 | surface=global-overlay | agent 会话悬浮窗口 |
| 发布浏览器(隐藏) | publisher 平台站点 | 自动发布自动化 |

## 2. 主工作区视图 [CONFIRMED]

主应用组件树: `Provider(Kr) → Layout(Sd) → Main(Td) → [v_(全局确认/会话) + B_(主工作区)]`

### 两种工作区模式 (workspaceMode) [CONFIRMED]
- `simple` — 简化模式 (simple-workspace / simple-project-*): 项目管理、章节列表、长按菜单、手写/语音
- `creative` — 创作模式 (creative-*): 多窗口停靠/悬浮布局, 资料库、大纲、聊天并排

## 3. 主要视图/面板

| 视图 | 类名前缀 | 功能 |
|---|---|---|
| 项目选择/管理 | project-list, project-manager-create-form | 项目列表、新建 |
| 项目回收站 | chief-project-trash-* | 删除/恢复/清空 |
| 章节管理 | simple-project-chapter-* | 章节分组、排序、搜索、拖拽 |
| 聊天 | chat-* | 主编聊天(消息/附件/媒体/工具运行/搜索/语音) |
| 主编工作流 | workflow-view-*, agent-node-* | Agent 节点可视化、进度 |
| 主编设置 | chief-settings-* | 设置(选项卡: 模型/写作/技能/反馈等) |
| 会员中心 | chief-membership-* | 账户/套餐/订单/支付/激活码/法律协议 |
| 技能库 | chief-skills-* | 技能列表/编辑/启停 |
| 客服 | chief-support-* | 客服聊天窗口 |
| 模型库 | model-library-* | 模型提供商/API Key 管理 |
| 素材库 | material-editor-*, creative-material-* | 创作资料管理 |
| 大纲管理 | creative-outline-* | 总纲/大纲/卷纲/章纲 |
| 成品 | artifacts (products/preview) | 成品预览(HTML) |
| 项目分支 | project-branches-dialog | 分支管理对话框 |
| 故事摘要 | story-summary-dialog | 故事梗概对话框 |
| 发布助手 | publisher (星炉发布助手) | 平台绑定/发布(隐藏窗口) |

## 4. 对话框/弹窗集 [CONFIRMED]

- `app-update-dialog` — 更新提示
- `membership-register-dialog` — 注册
- `project-branches-dialog` — 分支
- `story-summary-dialog` — 摘要
- `delete-content-confirmation` — 删除确认
- `input-clarity-dialog` — 输入清晰度(改写弹窗)
- `confirm-dialog` / `text-input-dialog` — 通用
- `window-picker` — 窗口选择器(全局悬浮层)
- `chief-editor-settings` — 主编设置
- `agent-dialog` — Agent 编辑

## 5. 聊天消息类型 [CONFIRMED]

- 文本(Markdown 渲染: 标题/列表/表格/代码块/引用/任务标记)
- 图片(网格/灯箱预览/下载/生成图片选择)
- 音频(播放器/歌词/候选人列表/下载)
- 视频(播放器/预览)
- 文件(章节链接/内联编辑/修订搜索/保存状态)
- 工具运行(chat-tool-run-*: 工具名/进度/结果)
- 媒体生成状态(chat-media-generation-status)

## 6. 移动端页面 [CONFIRMED - mobile bundle]

| 页面 | 功能 |
|---|---|
| 连接页 | 扫码连接/手动输入地址+配对密钥/二维码生成 |
| 项目页 | 项目列表/新建(从一句灵感开始)/切换 |
| 聊天页 | 总编聊天(思考中/回复中/工具使用), 语音输入(长按说话) |
| 资料页 | 资料管理(人物/世界/时间线/临时参考), 编辑冲突处理 |
| 章节页 | 正文查看/编辑/选择 |
| 生成页 | 图片生成(绘画版/风格版/精准版), 音乐生成 |
| 设置页 | 项目设置/模型选择(官方模型) |
| 写作方式 | 主编亲写 / 分身写作, 高质量 |

## 7. 各页面数据流

| 页面 | API | Storage | Native |
|---|---|---|---|
| 项目列表 | projects:list/create | localStorage workspaceMode | - |
| 聊天 | chief-editor:chat/run | 聊天历史(项目内 .novelforge/) | IPC 事件流 |
| 章节编辑 | chapter-editor-view:* | 编辑器状态 | 窗口管理 |
| 会员 | membership:* | membership_credentials.json | 支付链接 |
| 客服 | support:* | support_chat_state.json | 通知 |
| 发布 | publisher:* | 绑定配置 | 隐藏浏览器 |
