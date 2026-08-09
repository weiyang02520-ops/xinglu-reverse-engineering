# DATA_MODEL — 数据模型设计

> 全部数据以 JSON/Markdown 明文存于本地文件系统。无数据库。

## 1. 目录结构(单本小说)

```
data/novels/<project_id>/
├── project.json                # 项目元信息
├── settings.json               # 项目级写作设置(非敏感)
├── .history/                   # 历史快照(undo-last-change 用, 见 §8)
├── outline/                    # ⭐ 事实源: 大纲
│   ├── summary.md              #   全书梗概
│   ├── volumes/
│   │   └── vol001.md           #   分卷大纲(一卷一文件, 永不覆盖历史卷)
│   └── chapters/
│       ├── ch0001.md           #   章细纲(一章一文件, 生成后保留)
│       └── ch0002.md
├── characters/                 # ⭐ 事实源: 人物正式设定
│   └── <slug>.md               #   每角色一文件
├── world/                      # ⭐ 事实源: 世界观正式设定
│   ├── 世界观.md
│   └── 势力.md
├── rules/                      # ⭐ 事实源: 用户确认的创作规则
│   └── writing_rules.md
├── chapters/                   # ⭐ 事实源: 已确认章节正文(最终版)
│   ├── ch0001.md
│   └── …
├── drafts/                     # 草稿(未确认, 非事实源)
│   ├── ch0003.draft.md
│   └── …
├── memory/                     # 派生记忆(可重建, 不覆盖事实源)
│   ├── summaries/
│   │   ├── ch0001.md           #   每章摘要一文件
│   │   └── ch0002.md
│   ├── characters.md           #   人物当前状态(动态)
│   ├── world.md                #   世界当前状态(动态)
│   ├── timeline.md             #   时间线索引
│   ├── foreshadowing/          #   伏笔索引(每伏笔一文件或单文件+索引)
│   │   └── index.md
│   ├── long_term.md            #   长期记忆摘要
│   └── index.md                #   记忆索引(快速检索: 章节→摘要文件 映射)
└── review/                     # 审稿记录(可选保留)
    └── ch0003.review.md
```

## 2. 事实源 vs 派生记忆(核心边界)

| 类别 | 内容 | 特性 |
|---|---|---|
| **Canonical Sources(事实源)** | 章节正文(chapters/)、人物正式设定(characters/)、世界观正式设定(world/)、大纲(outline/)、用户确认的创作规则(rules/) | **唯一真相**; 只由"用户确认"或"明确编辑操作"修改; `rebuild-memory` **绝不覆盖** |
| **Derived Memory(派生记忆)** | 章节摘要(memory/summaries/)、人物当前状态、世界当前状态、时间线索引、伏笔索引、长期记忆摘要 | **可重建**; 从事实源 + LLM 派生; `rebuild-memory` 可安全重建 |

**规则**:
- `rebuild-memory` 只重建 `memory/` 目录, 绝不动 `chapters/`、`characters/`、`world/`、`outline/`、`rules/`。
- 记忆文件损坏/丢失 → 重建即可; 事实源损坏 → 需用户手动处理(有 .history/ 快照兜底)。
- 派生记忆的更新是"增量"(LLM 比对旧状态 + 新章节 → 新状态), 但旧状态本身永远可从事实源重建, 不依赖增量链条。

## 3. project.json

```json
{
  "id": "wanxiang-journey",
  "name": "万象之旅",
  "genre": "奇幻",
  "created_at": "2026-08-09T12:00:00Z",
  "updated_at": "2026-08-09T15:00:00Z",
  "status": "active",
  "current_volume": 1,
  "current_chapter": 3,
  "writing_style": "第三人称, 轻快, 短句",
  "editorial_notes": "用户对总编的长期要求",
  "defaults": {
    "writer_model": null,
    "reviewer_model": null
  },
  "auto_accept": false
}
```

> `auto_accept: false`(默认): Reviewer 通过只到 READY, 必须用户确认才正式收录。未来支持 `true`(全自动), 第一版不实现。

## 4. 章节文件(chNNNN.md)

```markdown
---
chapter: 3
volume: 1
title: 意外来客
status: confirmed        # draft | reviewing | ready | user_confirmed | confirmed
words: 2450
created_at: "2026-08-09T12:00:00Z"
updated_at: "2026-08-09T12:30:00Z"
summary: 林小满在夜市遭遇黑市商人, 意外获得城主戒指。
characters: [lin-xiaoman, lao-chen]
---

正文内容…
```

> `chapters/` 只放 **confirmed** 章节; `drafts/` 放未确认草稿; 章节号 4 位零填充(`ch0003`), 支持 2000+ 章排序。

## 5. 大纲结构(长期可扩展)

```
outline/
├── summary.md            # 全书梗概
├── volumes/
│   ├── vol001.md         # 卷1 大纲(含章目列表)
│   └── vol002.md         # 卷2 大纲
└── chapters/
    ├── ch0001.md         # 章细纲(生成后永久保留, 不被下一章覆盖)
    └── ch0002.md
```

- 章细纲**生成后保留为独立文件**, 供 Writer/Reviewer 参考、供回读历史规划。
- 新增章节规划 = 新建文件, 不覆盖旧文件。

## 6. 记忆文件格式

### memory/summaries/chNNNN.md(每章一文件)

```markdown
---
chapter: 1
---
摘要: 林小满来到星城, 遇到老陈, 得知城主失踪。
关键事件: [星城夜景, 老陈身份成谜]
伏笔: 城主的戒指(未解释)
```

### memory/index.md(记忆索引, 快速检索)

```markdown
# 记忆索引
## 章节摘要
| 章节 | 摘要文件 | 一句话 |
|---|---|---|
| ch0001 | memory/summaries/ch0001.md | 初入星城, 遇老陈 |
| ch0002 | memory/summaries/ch0002.md | 夜市风波, 获戒指 |
## 人物
| 名字 | 设定文件 | 状态文件 |
## 伏笔
| ID | 状态 | 文件 |
```

> 索引由程序/LLM 维护, 用于快速定位, 不承载内容本身。

### memory/characters.md(人物当前状态, 派生)

```markdown
## 林小满
- 身份: 穿越者, 女, 20岁
- 目标: 找到回原世界的方法
- 现状: 在星城落脚, 与老陈同行, 持有城主戒指
- 关系: 老陈(导师级伙伴), 陈小刀(敌对)
- 情绪: 警惕 → 开始信任老陈
```

### memory/foreshadowing/(伏笔索引)

```markdown
# 伏笔
| ID | 伏笔 | 埋设章 | 状态 | 计划回收章 | 文件 |
|---|---|---|---|---|---|
| F001 | 城主的戒指 | ch0001 | open | ~ch0015 | memory/foreshadowing/F001.md |
```

### 其他派生文件

- `memory/world.md` — 世界当前状态(动态)
- `memory/timeline.md` — 时间线索引(表格)
- `memory/long_term.md` — 长期记忆摘要(写作约定/设定沉淀)

## 7. 章节状态机

```
DRAFT ──write──→ REVIEWING ──reviewer PASS──→ READY ──user confirm──→ USER_CONFIRMED ──收编──→ CONFIRMED
  │                    │                          │
  └──编辑──→ DRAFT     └──reviewer NEEDS_WORK──→ DRAFT(重写循环 ≤K 轮)
```

| 状态 | 含义 | 谁能进入 |
|---|---|---|
| `DRAFT` | 草稿(写作中/可编辑) | Writer 创建 / 用户手动创建 |
| `REVIEWING` | 提交审稿 | 主编/用户提交 |
| `READY` | Reviewer 通过, 等待用户确认 | Reviewer PASS |
| `USER_CONFIRMED` | 用户已确认 | 用户确认动作 |
| `CONFIRMED` | 已收编: 移入 chapters/、更新 current_chapter、更新记忆 | 收编流程 |

**关键规则**:
- **Reviewer PASS ≠ 用户接受**。PASS 只进入 READY。
- 只有 **USER_CONFIRMED → CONFIRMED** 才会:
  - 草稿移入正式 `chapters/`
  - 更新 `project.json` 的 `current_chapter`
  - 触发正式记忆更新(摘要/人物/世界/时间线/伏笔)
- `auto_accept: false` 时, 即使 Reviewer 通过, 也要用户确认; `true`(未来)时 READY 自动收编。
- 用户主动拒绝 → 回到 DRAFT(可保留草稿供修改)。

### 两条确认路径(重要)

**A. 用户手动创建/编辑的章节(M1 起可用)**
- 用户显式执行 `confirm` = "这是用户本人确认的正文"
- 允许: `DRAFT → USER_CONFIRMED → CONFIRMED`
- 无需 Reviewer(章节不是 AI 生成的, 用户已亲自确认)

**B. AI Writer 生成的章节(M5 起)**
- 必须: `DRAFT → REVIEWING → READY → USER_CONFIRMED → CONFIRMED`
- **禁止 AI 绕过 Reviewer 直接确认**(无论 auto_accept 与否)
- 程序层强制: AI 写入的草稿, confirm 命令必须先经过 READY 状态

## 8. 历史快照(.history/)

- 目录: `data/novels/<id>/.history/`, 不参与记忆重建, 不进正式数据。
- 快照内容: 每次 AI 写入前的旧文件副本(章节/大纲/人物/世界/记忆)。
- 命名: `<时间戳>_<相对路径>.bak`(或按操作序列号)。
- 命令: `undo-last-change`(取最近快照回滚)。
- 只保留最近 N 份(默认 50), 超出清理最旧(防膨胀)。

## 9. 配置(全局 config/settings.json — 不含真实密钥)

```json
{
  "default_model": {
    "provider": "openai_compatible",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "secret_reference": "deepseek-main"
  },
  "models": { "writer": {…}, "reviewer": {…} },
  "context": {
    "reserve_output_tokens": 4096,
    "max_recent_chapters": 5,
    "max_recent_text_chars": 3000
  },
  "workflow": { "max_review_rounds": 3, "max_tool_calls_per_turn": 8 },
  "history": { "max_snapshots": 50 },
  "auto_accept": false
}
```

> API Key 走 SecretStore(见 PROVIDERS §3), 此处只有 `secret_reference`。

## 10. 数据一致性规则

- 章节正文等事实源是**唯一真相**; 记忆是**派生数据**(可随时 `rebuild-memory`)。
- 章节状态机由 Workflow 严格驱动; current_chapter 只在 CONFIRMED 时更新。
- 所有写操作: 临时文件 + rename; AI 写前先快照到 .history/。
- `rebuild-memory` 只允许操作 memory/ 目录(程序级强制)。

## 11. 文件规模估算(长篇)

| 文件 | 规模(200 万字书) |
|---|---|
| chapters/*.md | 2000 章 × 1K 字 ≈ 2MB |
| memory/summaries/ | 2000 个文件 × 300 字 ≈ 600KB |
| 其余记忆/大纲 | < 200KB 合计 |

→ 全书本地存储 < 5MB; 每章摘要独立文件, 检索/更新只动相关文件, 不整文件重写。
