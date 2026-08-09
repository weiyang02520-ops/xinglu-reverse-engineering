# 15 — 功能地图报告 (Feature Map)

> 每个功能标注: UI入口 → 页面 → 业务函数 → State → API → Storage → Native

## 1. 项目管理

```
功能: 创建/选择/重命名/删除/导出/导入项目, 分支管理, 回收站
UI: 项目列表页 → 项目卡片(选择/菜单) → 对话框
页面: 主工作区(simple-project-* / project-manager-*)
API: projects:create/select/rename/delete/list/list-trash/restore-trash/delete-trash/export-current/import-backup
     create-branch/select-branch/delete-branch/rename-branch/update-branch-strategy
     update-chapter-groups/update-workflow-settings/organize-folder-name/ensure-chat
State: 当前项目(主进程持有), 项目列表
Storage: workspace/projects/{id}/, .novelforge/branches/, 垃圾箱/
Native: - (纯文件系统)
二进制: - (JS)
```
**证据**: preload.cjs projects 模块; main.js 项目路径常量(projects/垃圾箱, .novelforge/branches)

## 2. 主编 AI 聊天

```
功能: 与"主编"对话(文字/语音/图片), 流式回复, 工具调用, 历史记录, 搜索
UI: 主编聊天面板(chat-* 组件群) → 输入区(attach/voice/clarity 按钮)
页面: 主工作区聊天面板; 移动端聊天页
API: chief-editor:chat/stop-chat/get-history/clear-history/analyze-input-clarity/cancel-input-clarity
     事件: chat-event, chat-history-changed
State: 聊天会话(主进程), 每项目能力开关(localStorage)
Storage: .novelforge/chief-editor-chat.json + history.json; 创作资料/聊天附件/images
Native: IPC 事件流
```
**证据**: preload chiefEditor 模块; renderer chat-* 组件类名(消息/附件/媒体/工具运行)

## 3. 主编工作流(自动写作)

```
功能: 按章节循环调度 Agent 写作, 断点续写, 章节细纲规划, 卷纲规划
UI: 工作流视图(workflow-view-*, agent-node-*) → 进度指示
页面: 主工作区; 章节编辑器
API: chief-editor:run/stop; 事件: workflow:progress
业务: T7(主循环) → Rkt/jkt/Dkt/Fkt(章节/细纲/卷纲) → agent 调度
State: 运行状态(runId/agentId/stepId/phase), token 估算
Storage: chapters/chXXX/{agent}.md, 创作资料/大纲/*
Native: IPC
```
**证据**: main.js T7/jkt/Dkt/Fkt 函数; workflow:progress 事件结构

## 4. 智能体(写作分身)管理

```
功能: 新建/编辑/复制/删除 Agent, 配置身份/模型/提示词/读写文件/顺序/启用
UI: Agent 编辑对话框(agent-dialog, agent-node-*)
页面: 主工作区设置; 工作流视图节点
API: agents:create/delete/duplicate/list
     update-identity/update-provider/update-prompt-paths/update-read-files
     update-output-files/update-final-text-source/update-order
State: 项目 Agent 列表(主进程)
Storage: prompts/agents/, chapters/chXXX/{agent}.md
Native: -
```

## 5. 章节编辑器

```
功能: 打开/编辑章节正文, 浮窗/停靠, 字号, 历史版本, 时间线, 搜索替换
UI: 章节编辑器窗口(chapter-editor-view)
页面: 独立窗口(surface=chapter-editor)
API: chapter-editor-view:set-session/get-state/focus/set-dock-slot/set-floating-bounds
State: 编辑器状态(layout/session), 字号(localStorage)
Storage: chapters/chXXX/*.md; novelforge:chapter-editor-font-size
Native: 窗口管理
```

## 6. 创作资料库

```
功能: 总纲/大纲/人物/世界/实体/关系/伏笔/时间线/重点记忆/设定沉淀管理, 素材导入
UI: 创作资料面板(creative-material-*, material-editor-*)
页面: 创作工作区资料库; 资料窗口
API: materials:list/import-files/delete-file/open-file/read-*/write-file/copy-media
     文件分类: canon/setup→设定, key_memory→重点记忆, material→创作资料, outline→大纲, ...
State: 资料树(渲染器)
Storage: 创作资料/{agent}.md, 创作资料/大纲/*, 小说物料/
Native: -
```

## 7. 大纲管理

```
功能: 总纲/分卷大纲/章节细纲, AI 生成方向, 应用方向
UI: 大纲面板(creative-outline-*), 分卷大纲窗口, 章节细纲窗口
页面: 创作工作区
API: outline-manager:get-status/generate-directions/apply-direction
     结构规划工具: structure_plan_get_status/apply_direction
业务: 结构规划状态检查(当前章节批次)
Storage: 创作资料/大纲/分卷大纲/, 创作资料/大纲/章节细纲/
Native: -
```

## 8. 会员与商业化

```
功能: 登录/注册/退出, 套餐购买, 订单支付, 激活码兑换, 创作点余额, 权益同步
UI: 会员中心(chief-membership-*) → 登录/注册对话框 → 套餐卡 → 支付二维码
页面: 主工作区设置; membership-register-dialog
API: membership:login/register/logout/login-or-create
     get-plans/create-order/get-order-status/refresh-order-payment
     redeem-activation-code/get-current
     官方模型: get-catalog/refresh-catalog/get-usage-balance
State: 登录态/权益(主进程)
Storage: userData/membership_credentials.json, membership_entitlements.json
Native: 支付链接打开(外部浏览器)
```
**证据**: renderer chief-membership-* 类名(plan-card/order/payment-qr/activation); main.js gEe 网络层

## 9. 官方模型

```
功能: 官方模型目录/余额/用量, 模型选择, 创作点消耗
UI: 模型选择器(chat-model-quick-select), 模型库(model-library-*)
API: official-models:get-catalog/refresh-catalog/get-usage-balance; tokens:get-summary
业务: 模型适配器(kdt): gemini_compatible/kimi_k2/deepseek/gpt_5_5/minimax_m3/qwen_3_6/claude_compatible_chat/glm_5_1
Storage: 权益缓存; NOVELFORGE_OFFICIAL_MODEL_* 环境变量
```

## 10. 模型库(自定义)

```
功能: 添加/编辑/删除自定义模型(名称/模型名/说明/来源/API Key/Base URL)
UI: 模型库面板(model-library-*), 高级设置
API: provider:get-summary/save-chat-completions/select-model/delete-model
业务: OpenAI 兼容 chat/completions, 401→refreshApiKey 重试
Storage: 本地配置(模型列表)
```

## 11. 写作技能库

```
功能: 安装/新建/编辑/启停/删除技能, 组织整理, 版本锁定
UI: 技能库面板(chief-skills-*), 技能编辑器(chief-skill-editor-*)
API: chief-editor:list-skills/read-skill/save-skill/set-skill-enabled/delete-skill/import-skill
     organize-library/list-organization-locks/set-organization-lock
业务: 内置技能 + 自定义技能; 技能锁定后不追官方更新
Storage: 技能文件(prompts/…)
```

## 12. 客服支持

```
功能: 客服聊天, 消息/已读/状态, 新回复通知
UI: 客服面板(chief-support-*), 新回复通知(support-reply-notification-*)
API: support:initialize/get-status/get-thread/send-message/mark-read/set-viewing/refresh-status
     远程: /v1/support/chat/{thread,messages,read,session,status}
Storage: userData/support_chat_state.json; novelforge.support.clientId
Native: 系统通知
```

## 13. 发布助手(自动化投稿)

```
功能: 绑定平台账号/作品, 检测后台状态, 自动发布章节(草稿/直接发布), 模拟运行
UI: 发布助手窗口(星炉发布助手), 绑定对话框
页面: 独立窗口 + 隐藏 BrowserWindow
API: publisher:list-platforms/open-platform/inspect-platform/inspect-current
     bind-current-project/bind-detected-current-project/resolve-binding-choice
     run-draft/run-mock/click/fill/snapshot/wait-stable/close
平台: qidian(起点 write.qq.com), fanqie(番茄 fanqienovel.com)
业务: AI 工具(读页面状态→点击/填充→发布), 平台文案识别正则
Native: 隐藏浏览器窗口, clipboard, screenshot
```

## 14. 素材与媒体

```
功能: 素材导入/预览/播放/下载, 图片/音频/视频/文件
UI: 素材面板(creative-material-*), 媒体预览
API: materials:read-audio/read-image/read-video/read-file/open-file
     媒体生成: chief-editor:media-generation-cancel, select-generated-image
业务: 图像生成(OpenAI), 音乐生成(Suno), 视频生成(可灵)
Storage: 创作资料/聊天附件/images, 素材目录
```

## 15. 手机连接

```
功能: 手机配对(扫码/手动), 手机远程操作(聊天/章节/资料/语音)
UI: 连接手机(扫码连接), mobile bridge 服务
API: mobile-bridge:get-status/restart; HTTP bridge 22 命令
业务: 本地 HTTP 服务器, 配对密钥, SSE 事件
Storage: userData/mobile_bridge.json
Native: 本地服务器
```

## 16. 系统与更新

```
功能: 检查更新/下载/安装, 窗口控制, 本地身份, 公告, 官网, 法律协议, 反馈
UI: 更新对话框(app-update-dialog), 设置→检查更新
API: system:check-app-update/start-app-update-download/install-app-update/get-environment
     get-local-identity/reset-local-identity/get-startup-notice/get-legal-agreements/get-official-website
     window:* (close/minimize/toggle-maximize/set-minimum-size/ensure-size)
     feedback:submit; 远程: /v1/app/*
Storage: userData/local_identity.json, window_state.json, startupNotice.seenIds
Native: electron-updater, BrowserWindow
```

## 17. 客服之外的工具能力(主编工具集)

```
写作用工具: project_get_state, agents_inspect, references_inspect, files_find,
  files_read_text, files_edit_markdown, search_project_file, web_search, read_web_page,
  prepare_chapter_context, workflow_run, rename_project, canon_update
编辑器工具: read_editor_state, select_editor_chapter, fill_editor_chapter,
  read_page_state, click_element, wait_page, finish_binding
Agent 管理: agents_edit, agents_update_read_files, agents_update_input_refs,
  agents_update_schedule, agents_set_final_text_source
结构规划: structure_plan_get_status, structure_plan_apply_direction
```

## 18. 启动与多窗口

```
功能: 启动序列(静态加载器→应用就绪), 章节编辑器/悬浮层独立窗口
UI: nf-static-preloader 启动画面
API: window:static-loader-*, startup-*
State: 启动阶段(ignite→workspace→project→ready)
Native: BrowserWindow 管理
```
