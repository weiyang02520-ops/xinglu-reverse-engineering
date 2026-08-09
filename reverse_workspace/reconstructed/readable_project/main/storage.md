# 存储与文件系统

> CONFIRMED — 路径常量从 main.js 明文提取。

## 工作区根目录

检测特征(按顺序向上查找):
- `projects/default/prompts/00_共享规则.system.md`
- `projects/default/project.json`
- `projects/current.json`
- 或存在 `projects/` 目录且含子目录

环境变量可覆盖: `NOVELFORGE_WORKSPACE_ROOT`

## 项目目录布局

```
{workspace}/projects/{projectId}/
├── project.md                        ← 主文档(书名/题材方向/灵感)
├── chapters/chXXX/{agentName}.md     ← 章节正文(按 Agent 分文件)
├── 创作资料/
│   ├── 大纲/                         ← 大纲
│   │   ├── 分卷大纲/                 ← 卷纲
│   │   └── 章节细纲/                 ← 章纲
│   ├── 历史版本/                     ← 章节历史版本
│   ├── 聊天附件/images/              ← 聊天图片附件
│   └── {agentName}.md                ← 各 Agent 创作资料
├── prompts/agents/                   ← Agent 提示词
└── .novelforge/
    ├── deleted-project.json          ← 回收站元数据
    ├── branches/                     ← 分支目录
    ├── chief-editor-chat.json        ← 主编聊天(当前)
    ├── chief-editor-chat-history.json← 主编聊天历史
    └── …(其他状态)
```

回收站: `{workspace}/projects/垃圾箱/`

## userData/ 配置

| 文件 | 内容 |
|---|---|
| local_identity.json | 本地设备匿名标识 |
| membership_credentials.json | 会员登录凭证(token) |
| membership_entitlements.json | 会员权益缓存 |
| support_chat_state.json | 客服会话状态 |
| official_network_compatibility.json | 官方网络兼容设置 |
| mobile_bridge.json | 手机桥配对密钥+状态 |
| window_state.json | 窗口位置/大小 |

## 分支

- 目录名: `branch_[a-z0-9_-]{1,80}`
- 分支策略: 自动分支(章节完成后触发)/手动
- 每个分支有独立 chapters/ 与创作资料
