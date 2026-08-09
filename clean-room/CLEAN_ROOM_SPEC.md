# CLEAN_ROOM_SPEC — 个人版 AI 小说创作软件设计规格

> 状态: 设计草案(等待外部模型审核)
> 性质: **Clean-Room 设计** — 基于对同类产品(XingLu 星炉)架构的逆向研究总结出的通用设计思想, 不包含 XingLu 的任何代码、资源、API、品牌或受保护内容。

## 1. 设计目标

做一款**个人使用、本地优先、自带 API Key**的 AI 小说创作软件:

- 管理多本小说的项目结构(大纲/人物/世界观/章节)
- 通过"主编 → Writer → Reviewer"多 Agent 流程辅助创作长篇小说
- 所有 AI 请求走**用户自己的 API**(兼容 OpenAI 协议, 支持自定义 Base URL / API Key / Model)
- 所有数据保存在本地文件系统(纯文本 + JSON, 无数据库)
- 无会员/支付/官方商城/手机端/自动发布 — 第一版只做创作核心

## 2. 核心使用流程(最小闭环)

```
用户给出创作指令(写第 N 章 / 大纲调整 / 人物讨论)
  → 主编 Agent(Chief): 理解意图、查资料、规划任务
  → Writer Agent: 按规划写章节正文
  → Reviewer Agent: 审稿(逻辑/文风/与前文一致性), 必要时回退重写
  → 保存章节 + 更新记忆(摘要/人物状态/世界状态/时间线/伏笔)
```

## 3. 非目标(第一版明确不做)

| 不做 | 理由 |
|---|---|
| 手机端 / PWA | 个人桌面使用即可 |
| 自动发布(起点/番茄等) | 平台规则与授权风险, 不做 |
| 会员/订单/支付/激活码 | 个人软件, 无商业闭环 |
| 官方模型商城/创作点计费 | 用户自带 Key |
| Suno/视频/图片生成 | 超出第一版创作核心 |
| 云端同步/多设备 | 本地优先 |

## 4. 用户画像

- 个人小说作者, 想要 AI 辅助但**不想依赖某个商业平台**
- 有自己/第三方的 OpenAI 兼容 API(如 DeepSeek、Qwen、OpenRouter、本地 Ollama)
- 希望数据完全可控(纯文本文件, 可随时备份/迁移)
- 单机使用, 不需要协作

## 5. 设计原则

1. **本地优先**: 所有数据明文存本地文件, 无云依赖; 断网时除 AI 调用外全部可用。
2. **自带 Key**: 模型配置 = Base URL + API Key + Model, 存本地配置, 绝不外发。
3. **干净分离**: 不依赖任何商业平台 API; 仅使用公开通用协议(OpenAI Chat Completions 兼容)。
4. **长篇小说友好**: 上下文管理是第一设计目标 — 全书不能整本塞进 prompt。
5. **可验证**: 每个里程碑(M0–M7)都有明确的"实际运行成功"标准。
6. **简单**: 技术栈克制, 无数据库、无框架堆砌, 单机单进程。

## 6. 技术选型(草案)

| 组件 | 选择 | 理由 |
|---|---|---|
| 语言 | Python 3.11+ | 快速原型, AI 生态好, 无编译 |
| UI | 第一阶段 CLI + 后续可选 TUI/Web | M0–M2 用 CLI 最快验证; Web UI 留给 M3+ 增值 |
| 存储 | 文件系统 + JSON | 可读、可备份、可 diff |
| AI 协议 | OpenAI Chat Completions 兼容 | 覆盖 DeepSeek/Qwen/OpenRouter/Ollama/OpenAI 等 |
| 工作流 | 本地进程内编排 | 无队列/无服务端 |

> 注: 若后续要桌面 GUI, 可参考一般 Electron 架构思想, 但第一版不做。

## 7. 目录结构(草案)

```
ai-novel/
├── app/                    # 应用入口
│   └── main.py             # CLI 入口
├── core/                   # 领域逻辑
│   ├── project.py          # 项目管理
│   ├── chapter.py          # 章节读写
│   ├── memory.py           # 记忆(摘要/人物/世界/时间线/伏笔)
│   ├── outline.py          # 大纲
│   └── workflow.py         # 主编→Writer→Reviewer 流程
├── agents/                 # Agent 定义
│   ├── chief.py            # 主编
│   ├── writer.py           # Writer
│   └── reviewer.py         # Reviewer
├── llm/                    # 模型接入
│   ├── client.py           # OpenAI 兼容客户端(自定义 Base URL/Key/Model)
│   ├── context.py          # 上下文组装(记忆压缩/裁剪)
│   └── prompts.py          # 提示词模板
├── tools/                  # 工具系统(Agent 可调用)
│   ├── read_file.py
│   ├── write_file.py
│   └── search_memory.py
├── config/                 # 用户配置
│   └── settings.json       # 模型配置等
└── data/                   # 本地数据(小说项目)
    └── novels/<project_id>/
```

## 8. 设计边界(与 XingLu 的干净分离声明)

- 本设计**未使用** XingLu 的: 代码、资源、API 端点、品牌名、图标、UI 设计。
- 本设计**借鉴**的仅是公开的通用架构思想(多 Agent 写作流、记忆管理、文件化存储), 这些是领域通用概念。
- 本软件**不会**调用 xushilu.cn 任何服务。

## 9. 成功标准

- 用户用自己任意 OpenAI 兼容 Key, 能完成: 建小说 → 写大纲 → 主编对话 → 生成一章 → 审稿 → 保存。
- 一本 200 万字长篇的创作过程中, 单次请求的上下文保持在可控范围内(靠记忆系统, 见 ARCHITECTURE.md)。
- 所有数据可离线导出/备份(纯文件)。
