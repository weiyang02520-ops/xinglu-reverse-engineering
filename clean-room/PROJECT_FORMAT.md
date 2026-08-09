# PROJECT_FORMAT — 项目文件格式规范

## 1. 目的

定义"一本小说"在磁盘上的完整文件格式, 保证:
- 人可读(纯 Markdown/JSON)
- 可版本控制(git 友好, 每文件独立)
- 可备份/迁移(整目录拷贝即迁移)
- 可程序化处理(元信息结构化)

## 2. 目录总览

```
data/novels/<project_id>/
├── project.json
├── settings.json                 # 可选, 项目级
├── outline/                      # 大纲
│   ├── summary.md                # 全书梗概(必)
│   ├── vol_001.md                # 分卷大纲(按卷)
│   ├── vol_002.md
│   └── chapter_plan.md           # 当前章细纲(滚动, 主编维护)
├── characters/                   # 人物
│   └── <slug>.md                 # 每角色一文件
├── world/                        # 世界观
│   └── *.md                      # 世界观/势力/地理…
├── chapters/                     # 正文
│   ├── ch001.md
│   └── …
├── drafts/                       # 草稿(未确认)
│   ├── ch003.draft.md
│   └── …
├── memory/                       # 记忆(派生数据, 可重建)
│   ├── chapter_summaries.md
│   ├── characters.md
│   ├── world.md
│   ├── timeline.md
│   ├── foreshadowing.md
│   └── long_term.md
└── review/                       # 审稿记录(可选保留)
    └── ch003.review.md
```

## 3. 命名规范

| 类型 | 规则 | 示例 |
|---|---|---|
| project_id | `[a-z][a-z0-9_-]{1,63}` | `wanxiang-journey` |
| 章节文件 | `ch` + 3 位数字(≥1000 允许 4 位) | `ch001.md`, `ch1234.md` |
| 草稿文件 | `chNNN.draft.md` | `ch003.draft.md` |
| 人物文件 | 拼音/英文 slug | `lin-xiaoman.md` |
| 卷大纲 | `vol_` + 3 位数字 | `vol_001.md` |

## 4. 文件头元信息(章节)

章节文件顶部 YAML 风格元块(便于脚本/grep 解析, 也便于 LLM 读取):

```markdown
---
chapter: 3
volume: 1
title: 意外来客
status: confirmed        # draft | reviewing | confirmed
words: 2450
created_at: "2026-08-09T12:00:00Z"
updated_at: "2026-08-09T12:30:00Z"
summary: 林小满在夜市遭遇黑市商人, 意外获得城主戒指。
characters: [lin-xiaoman, lao-chen]
---
```

> 用 `---` 分隔的 YAML 而非 JSON, 便于人工编辑。

## 5. 大纲文件约定

`outline/summary.md`:
```markdown
# 全书梗概

## 设定一句话
## 主线
- 卷1: …
## 结局方向
```

`outline/vol_001.md`:
```markdown
# 第一卷 星城来客

## 卷目标
## 章目
- ch1 初入星城
- ch2 夜市风波
- ch3 意外来客
## 卷内关键事件
## 卷内伏笔
```

`outline/chapter_plan.md`(滚动, 仅当前章):
```markdown
# 第 3 章 细纲
- 开场: 夜市收尾
- 冲突: 黑市商人索要戒指
- 转折: 老陈出手, 揭示身份一角
- 结尾钩子: 戒指发光
```

## 6. 记忆文件约定

- 全部 Markdown, 使用固定小节标题(见 DATA_MODEL §4)。
- 每章更新时**追加新条目**, 旧条目可被合并压缩(不删除历史, 压缩时保留原文段落到 `archive` 节)。
- 时间线用表格; 伏笔用表格含状态字段。

## 7. 审稿记录

`review/chNNN.review.md`:
```markdown
# 第 3 章 审稿

- 结论: NEEDS_WORK
- 一致性问题: 陈小刀在 ch2 是"商人", 本稿写成"守卫"
- 文风建议: …
- 伏笔检查: 戒指来历未解释(建议延迟, 可接受)
- 修改意见:
  1. 第 4 段: …
```

## 8. 一致性规则(程序层强制)

- 章节号递增: 新草稿章节号 = current_chapter + 1(或显式指定)。
- project.json 的 `current_chapter` 只在章节 confirmed 时更新。
- 记忆文件可随时删除重建(`rebuild-memory` 命令从 chapters + characters + world + outline 全量重建)。
- 未知文件类型(如用户放的 PDF)一律放 `assets/` 目录, 不参与解析。

## 9. Git 友好性

- 建议用户用 git 管理 `data/novels/<project_id>/`(章节历史可 diff/回滚)。
- 本软件不强制 git, 但文件格式天然支持。
- `.gitignore` 建议: `logs/`, `*.tmp`。

## 10. 版本演进

- `project.json` 带 `format_version: 1`; 后续升级提供迁移脚本。
- 不向前兼容的变更需 `migrate` 命令(第一版不做, 设计上预留)。
