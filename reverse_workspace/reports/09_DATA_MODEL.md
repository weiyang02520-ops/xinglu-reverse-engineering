# 09 — 数据模型报告 (Data Model)

> 全部模型基于代码证据反推, 原始 TS 类型已丢失。

## 1. Project (项目/书籍)

**文件系统组织** [CONFIRMED - main.js 路径常量]:
```
{workspace}/projects/{projectId}/
├── .novelforge/                    # 元数据
│   ├── deleted-project.json        # 回收站清单
│   ├── branches/                   # 分支目录
│   ├── chief-editor-chat.json      # 主编聊天(当前)
│   ├── chief-editor-chat-history.json  # 主编聊天历史
│   └── ...(其他状态)
├── chapters/chXXX/{agentName}.md   # 章节正文(按 agent 分文件)
├── 创作资料/{agentName}.md         # 设定资料(总纲/大纲/人物/世界/实体/关系/伏笔/时间线)
├── prompts/agents/                 # agent 提示词
└── project.md                      # 项目主文档(含题材方向/灵感, 手机端创建时写入)
```

**关键字段**(从 IPC/bridge 参数推断):
- `id` (string) — 项目 ID
- `name` (string) — 书名
- `creativeDirection`: `"novel"` (小说)
- `creationMode`: `"continuous"` (持续创作模式)
- `branchId` — 当前分支
- `workspaceMode`: `"simple" | "creative"` — 两种工作区模式
- `workflowSettings` — 工作流设置(updateWorkflowSettings)
- `chapterGroups` — 章节分组(updateChapterGroups)

## 2. Branch (分支) [CONFIRMED]

- 目录名: `branch_[a-z0-9_-]{1,80}` (正则)
- 分支策略: `updateBranchStrategy`
- 分支 = 故事线并行版本(类似 git 分支)

## 3. Chapter (章节) [CONFIRMED]

- 目录: `chapters/chXXX/` (3 位数字)
- 文件名: `{agentName}.md`
- 章节号正则: `^[a-z][a-z0-9_]{1,63}$` (内部 slug)
- 章节类型: 章节正文、章节细纲
- 分卷号、章节号 UI 字段
- 编辑器状态: 正文 + 历史版本 + 时间线
- 搜索: 正文搜索/替换(渲染器)

## 4. Agent (写作分身/智能体) [CONFIRMED]

字段(preload `novelforge:agents:update-*`):
- `title` — 名称
- `identity` — 身份设定
- `provider` — 模型提供商(providerId + modelId)
- `promptPaths` — 提示词文件路径
- `readFiles` — 要读取的文件(如创作资料)
- `outputFiles` — 输出文件(如章节文件)
- `finalTextSource` — 最终文本来源
- `order` — 执行顺序
- `id` — agent ID
- 系统预置: "叙事炉"(叙述者)、"上层叙述者"(架构)

## 5. Chat (对话) [CONFIRMED]

- `projectId` + `sessionId`(chapter-editor-view 用)
- 主编聊天: 消息流, run/stop, 历史记录
- 聊天能力配置: `novelforge.chiefEditorChatCapabilitiesByProject.v1` (per-project, localStorage)
- 附件: `创作资料/聊天附件/images`(目录常量)
- 移动端: `chat.send/stop` (bridge) + SSE `/bridge/events`

## 6. Membership (会员) [CONFIRMED]

- 凭证: `membership_credentials.json` (userData) — 登录态
- 权益: `membership_entitlements.json` — 已购权益(会员/创作点)
- 订单: `create-order` → `orderWatchUrl` 轮询 → `refresh-order-payment`
- 激活码: `redeem-activation-code`
- 套餐: `get-plans` (Plans: {id, name, price...})
- **创作点**: 官方模型计费货币(1 credit = N units, `NOVELFORGE_OFFICIAL_MODEL_QUOTA_UNITS_PER_CREDIT`)

## 7. Content 类型枚举 (创作资料分类) [CONFIRMED - renderer]

`canon|setup` → 设定; `key_memory` → 重点记忆; `material` → 创作资料; `image` → 图片资料; `outline` → 大纲; `skill` → 技能; `music` → 音乐资料; `video` → 视频资料; `generated_music` → 生成音乐; `generated_video` → 生成视频

另见 preload 路径: `创作资料/大纲`, `创作资料/聊天附件/images`

## 8. Skill (写作技能) [CONFIRMED]

- CRUD: list/read/save/delete/import/setEnabled
- 组织: organizeLibrary + organizationLocks(防并发)
- 文件位于: `prompts/...` / 技能目录
- UI: "安装写作技能"、工具规则、恢复默认

## 9. 其他模型

| 模型 | 证据 |
|---|---|
| StartupNotice | `startup-notice`, localStorage `novelforge.startupNotice.seenIds` |
| LegalAgreement | `/v1/app/legal-agreements` |
| Plan / Order / Payment | membership 模块 |
| OfficialModel | catalog + usage(余额) + 权益 |
| SupportThread | 客服会话(thread/messages/read/status) |
| Product (成品) | artifacts: list-products, preview(HTML), product folder |
| Material | materials: import/list/read/write/delete, 媒体(音频/视频/图片) |
| PublisherBinding | publisher: 平台绑定(平台+账号+书籍) |
| Feedback | feedback: submit(kind 切换器) |
| LocalIdentity | `local_identity.json`: 匿名设备标识(可重置) |
| WindowState | `window_state.json`: 窗口位置/大小 |

## 10. 存储位置汇总

- **userData/**: local_identity.json, membership_credentials.json, membership_entitlements.json, support_chat_state.json, official_network_compatibility.json, mobile_bridge.json, window_state.json
- **workspace/projects/**: 项目数据(用户创作内容)
- **localStorage**: 主题/缩放/窗口布局/功能开关等 UI 状态
