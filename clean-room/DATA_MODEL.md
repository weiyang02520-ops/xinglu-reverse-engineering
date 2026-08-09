# DATA_MODEL — 数据模型设计

> 全部数据以 JSON/Markdown 明文存于本地文件系统。无数据库。

## 1. 目录结构(单本小说)

```
data/novels/<project_id>/
├── project.json            # 项目元信息
├── settings.json           # 项目级写作设置
├── outline/
│   ├── summary.md          # 全书梗概
│   ├── vol_001.md          # 第一卷大纲
│   ├── vol_002.md          # …
│   └── chapter_plan.md     # 当前章细纲(滚动)
├── characters/
│   ├── 角色A.md            # 人物设定文件(每角色一个)
│   └── …
├── world/
│   ├── 世界观.md
│   └── 势力.md             # 组织/势力
├── chapters/
│   ├── ch001.md            # 章节正文(Markdown)
│   ├── ch002.md
│   └── …
├── memory/
│   ├── chapter_summaries.md # 章节摘要索引(滚动, 含旧章摘要压缩)
│   ├── characters.md        # 人物当前状态(动态)
│   ├── world.md             # 世界当前状态(动态)
│   ├── timeline.md          # 时间线
│   ├── foreshadowing.md     # 伏笔登记
│   └── long_term.md         # 长期记忆/设定沉淀
└── drafts/
    ├── ch003.draft.md      # 未确认的草稿
    └── …
```

## 2. project.json

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
  }
}
```

## 3. 章节文件(chNNN.md)

```markdown
# 第 3 章 意外来客

> meta: {"chapter": 3, "volume": 1, "status": "confirmed",
>        "characters_used": ["林小满", "老陈"], "summary": "…",
>        "created_at": "...", "updated_at": "..."}
> (元信息存于文件顶部 YAML/注释块, 便于 grep)

正文内容…
```

章节状态机: `draft`(草稿) → `reviewing`(审稿中) → `confirmed`(已确认)

## 4. 记忆文件格式

### chapter_summaries.md(滚动摘要)

```markdown
## ch001 初入星城
摘要: 林小满来到星城, 遇到老陈, 得知城主失踪。
关键事件: [星城夜景, 老陈身份成谜]
伏笔: 城主的戒指(未解释)

## ch002 夜市风波
摘要: …
## ch003(草稿) …
(旧章节摘要会由 LLM 定期合并压缩成"第1-10章总览")
```

### characters.md(人物状态)

```markdown
## 林小满
- 身份: 穿越者, 女, 20岁
- 目标: 找到回原世界的方法
- 现状: 在星城落脚, 与老陈同行, 持有城主戒指
- 关系: 老陈(导师级伙伴), 陈小刀(敌对)
- 情绪: 警惕 → 开始信任老陈
- 关键记忆: 记得原世界的音乐
```

### world.md(世界状态)

```markdown
## 星城
- 现状: 城主失踪, 治安由商会接管
- 最近变化: 夜市风波后警戒加强
- 势力: 商会(表面), 黑市(暗)
```

### timeline.md(时间线)

```markdown
| 章 | 时间 | 事件 |
|---|---|---|
| ch1 | 入城当夜 | 遇见老陈 |
| ch2 | 次日 | 夜市风波, 获得戒指 |
```

### foreshadowing.md(伏笔登记)

```markdown
| ID | 伏笔 | 埋设章 | 状态 | 计划回收章 |
|---|---|---|---|---|
| F001 | 城主的戒指 | ch1 | open | ~ch15 |
| F002 | 老陈的过去 | ch2 | open | 卷2 |
```

### long_term.md(长期记忆)

```markdown
## 写作约定(用户设定)
- 不写血腥细节
- 主角不降智
## 设定沉淀
- 星城货币: 星贝
- 星城特有: 会唱歌的灯
```

## 5. 配置(全局 config/settings.json)

```json
{
  "default_model": {
    "base_url": "https://api.deepseek.com/v1",
    "api_key": "sk-…",          // 本地存储, 权限 600
    "model": "deepseek-chat"
  },
  "models": {
    "writer": { "base_url": "...", "api_key": "...", "model": "..." },
    "reviewer": { "base_url": "...", "api_key": "...", "model": "..." }
  },
  "context": {
    "max_recent_chapters": 5,
    "max_recent_text_chars": 3000,
    "summary_chapter_batch": 10
  },
  "workflow": {
    "max_review_rounds": 3,
    "max_tool_calls_per_turn": 8
  }
}
```

> 角色级模型可选(如 Writer 用便宜的模型, Chief 用强的); 缺省继承 default_model。

## 6. 数据一致性规则

- 章节正文是**唯一真相源**; 记忆是**派生数据**(可随时从正文重建)。
- 每次章节确认后: 更新 current_chapter / 生成摘要 / 增量更新人物与世界状态 / 追加时间线 / 登记伏笔。
- 记忆文件均由 LLM 增量维护, 提供 `rebuild-memory` 命令全量重建(容错)。
- 所有写操作: 临时文件 + rename, 防半截。

## 7. 文件规模估算(长篇)

| 文件 | 规模(200 万字书) |
|---|---|
| chapters/*.md | 2000 章 × 1K 字 ≈ 2MB |
| chapter_summaries.md | 滚动保留 ≈ 100KB |
| characters.md | ≈ 20KB |
| 其余记忆 | < 100KB 合计 |

→ 全书本地存储 < 5MB, 备份/迁移无压力。
