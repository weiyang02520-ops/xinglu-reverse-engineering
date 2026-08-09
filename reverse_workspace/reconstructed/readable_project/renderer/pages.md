# 渲染进程 — 页面/视图

> RECONSTRUCTED — 从 rendererApp bundle 的组件结构与类名反推。
> 原始组件名已丢失(压缩), 以下用功能语义命名。

## 窗口 (surface)

| surface | 组件 | 用途 |
|---|---|---|
| (默认) | 主应用 | 工作台/项目/聊天/设置 |
| chapter-editor | 章节编辑器 | 独立章节编辑(浮窗/停靠) |
| global-overlay | 全局悬浮层 | Agent 会话悬浮窗口 |

## 主工作区视图

| 视图 | 语义组件 | 功能 |
|---|---|---|
| 项目选择 | ProjectList | 项目列表/新建/导入 |
| 简单工作区 | SimpleWorkspace | 章节分组/排序/搜索/长按菜单 |
| 创作工作区 | CreativeWorkspace | 多窗口停靠/悬浮, 资料库+大纲+聊天 |
| 回收站 | ProjectTrash | 恢复/彻底删除 |
| 主编设置 | ChiefSettings | 外观/会员/模型库/技能/客服/发布/反馈/关于 |
| 模型库 | ModelLibrary | 自定义模型 CRUD |
| 技能库 | SkillLibrary | 技能列表/编辑器 |
| 客服 | SupportChat | 客服聊天/通知 |
| 分支管理 | ProjectBranchesDialog | 分支创建/切换 |
| 故事摘要 | StorySummaryDialog | 梗概查看/更新 |
| 发布助手 | PublisherPanel | 平台绑定/发布 |

## 对话框

- 通用: confirm-dialog / text-input-dialog
- 专用: app-update-dialog / membership-register-dialog / project-branches-dialog
- 编辑器: story-summary-dialog / delete-content-confirmation / input-clarity-dialog
- 窗口: window-picker(悬浮层窗口切换)

## 聊天界面组件群 (chat-*)

- chat-thread / chat-message-stack / chat-message-*
- chat-composer / chat-input / chat-send-button / chat-stop-button
- chat-attach-button / chat-attachment-* (文件/图片/音频/视频)
- chat-voice-button (语音输入)
- chat-search-highlight (聊天搜索)
- chat-tool-run-* (工具调用展示: 工具名/进度/结果)
- chat-media-generation-* (媒体生成状态)
- chat-image-lightbox / chat-image-grid-choice (图片预览/选择)
- chat-audio-player / chat-audio-preview (音频播放)
- chat-video-player / chat-video-preview (视频)
- chat-model-quick-select (快速切换模型)
- chat-input-clarity-button (输入清晰度)

## 工作流视图 (workflow-* / agent-node-*)

- agent-node-* (Agent 节点卡片: 身份/模型/状态/配置)
- workflow-agent-model-line / workflow-view-actions
- agent-inspector-panel / agent-trace-panel (运行追踪)
- inspector-system-prompt-* (系统提示词检查)
