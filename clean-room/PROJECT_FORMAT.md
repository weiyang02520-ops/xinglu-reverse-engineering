# PROJECT_FORMAT — 项目文件格式规范

## 1. 目的

定义"一本小说"在磁盘上的完整文件格式, 保证:
- 人可读(纯 Markdown/JSON)
- 可版本控制(git 友好, 每文件独立)
- 可备份/迁移(整目录拷贝即迁移)
- 可程序化处理(元信息结构化)
- **长期可扩展**(2000 章级别不依赖单文件堆叠)

## 2. 目录总览

```
data/novels/<project_id>/
├── project.json                # 项目元信息
├── settings.json               # 项目级写作设置(非敏感)
├── .history/                   # 历史快照(undo-last-change, 见 §8)
├── outline/                    # ⭐ 事实源: 大纲
│   ├── summary.md              #   全书梗概(必)
│   ├── volumes/
│   │   ├── vol001.md           #   卷1 大纲(含章目列表)
│   │   └── vol002.md
│   └── chapters/
│       ├── ch0001.md           #   章细纲(一章一文件, 永久保留)
│       └── ch0002.md
├── characters/                 # ⭐ 事实源: 人物正式设定
│   └── <slug>.md
├── world/                      # ⭐ 事实源: 世界观正式设定
│   └── *.md
├── rules/                      # ⭐ 事实源: 用户确认的创作规则
│   └── writing_rules.md
├── chapters/                   # ⭐ 事实源: 已确认章节正文(最终版)
│   ├── ch0001.md
│   └── …
├── drafts/                     # 草稿(未确认)
│   ├── ch0003.draft.md
│   └── …
├── memory/                     # 派生记忆(可重建, 绝不覆盖事实源)
│   ├── index.md                #   记忆索引(快速检索)
│   ├── summaries/
│   │   ├── ch0001.md           #   每章摘要一文件
│   │   └── ch0002.md
│   ├── characters.md           #   人物当前状态(动态)
│   ├── world.md                #   世界当前状态(动态)
│   ├── timeline.md             #   时间线索引
│   ├── foreshadowing/
│   │   ├── F001.md             #   伏笔(每伏笔一文件)
│   │   └── index.md            #   伏笔索引表
│   └── long_term.md            #   长期记忆摘要
└── review/                     # 审稿记录(可选保留)
    └── ch0003.review.md
```

## 3. 命名规范

| 类型 | 规则 | 示例 |
|---|---|---|
| project_id | `[a-z][a-z0-9_-]{1,63}` | `wanxiang-journey` |
| 章节文件 | `ch` + 4 位数字(≥10000 允许 5 位) | `ch0001.md`, `ch1234.md` |
| 草稿文件 | `chNNNN.draft.md` | `ch0003.draft.md` |
| 人物文件 | 拼音/英文 slug | `lin-xiaoman.md` |
| 卷大纲 | `vol` + 3 位数字 | `vol001.md` |
| 章细纲 | `chNNNN.md`(outline/chapters/) | `ch0003.md` |
| 章节摘要 | `chNNNN.md`(memory/summaries/) | `ch0003.md` |

> 章节号 4 位零填充, 保证字典序 = 章节序。

## 4. 文件头元信息(章节)

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

## 5. 大纲文件约定

### outline/summary.md(全书梗概)

```markdown
# 全书梗概
## 设定一句话
## 主线
- 卷1: …
## 结局方向
```

### outline/volumes/vol001.md(分卷大纲, 一章不覆盖)

```markdown
# 第一卷 星城来客
## 卷目标
## 章目
- ch0001 初入星城
- ch0002 夜市风波
## 卷内关键事件
## 卷内伏笔
```

### outline/chapters/ch0003.md(章细纲, 生成后永久保留)

```markdown
# 第 3 章 细纲
- 开场: 夜市收尾
- 冲突: 黑市商人索要戒指
- 转折: 老陈出手, 揭示身份一角
- 结尾钩子: 戒指发光
```

> 历史章细纲**不会因生成下一章被覆盖** — 每章细纲独立文件, 可回读。

## 6. 记忆文件约定(派生, 可重建)

- 章节摘要: 每章一个文件(memory/summaries/chNNNN.md), **不把 2000 章堆在一个文件里**。
- 索引: memory/index.md 维护 章节→摘要文件、人物、伏笔 的映射, 供快速检索。
- 固定小节标题; 增量追加新条目; 旧条目合并压缩时保留原文到该文件 archive 节。
- 时间线/伏笔用表格; 伏笔每条一个文件 + 索引表(index.md)。

## 7. 事实源 vs 派生记忆(程序级强制)

| 目录 | 类别 | rebuild-memory 是否触碰 |
|---|---|---|
| chapters/ | 事实源(已确认正文) | ❌ 绝不 |
| characters/ | 事实源(正式设定) | ❌ 绝不 |
| world/ | 事实源(正式设定) | ❌ 绝不 |
| outline/ | 事实源(大纲) | ❌ 绝不 |
| rules/ | 事实源(创作规则) | ❌ 绝不 |
| drafts/ | 半成品(用户可弃) | ❌ |
| memory/ | 派生记忆 | ✅ 只重建这里 |
| .history/ | 快照(审计/回滚) | ❌(独立管理) |

- `rebuild-memory` 入口在程序层只允许写 memory/ 目录(白名单校验)。
- 派生记忆损坏 → 重建; 事实源损坏 → 用 .history/ 快照或手动恢复。

## 8. 历史快照(.history/)

```
.history/
├── index.jsonl          # {seq, tool, target, timestamp, note} 每行一条
├── 00001_outline_volumes_vol001.md.bak
├── 00002_characters_lin-xiaoman.md.bak
└── …
```

- 写入类工具执行前自动快照(见 TOOL_SYSTEM §7)。
- `undo-last-change` 顺序回滚最近一次 AI 写入。
- 默认保留 50 份(settings.history.max_snapshots)。

## 9. 审稿记录

`review/chNNNN.review.md`:
```markdown
# 第 3 章 审稿
- 结论: NEEDS_WORK      # PASS 只代表 READY, 不代表用户接受
- 一致性问题: 陈小刀在 ch0002 是"商人", 本稿写成"守卫"
- 文风建议: …
- 伏笔检查: 戒指来历未解释(建议延迟, 可接受)
- 修改意见:
  1. 第 4 段: …
```

## 10. 一致性规则(程序层强制)

- 章节号递增: 新草稿章节号 = current_chapter + 1(或显式指定)。
- `current_chapter` 只在章节 **CONFIRMED** 时更新(USER_CONFIRMED 收编流程)。
- 记忆文件可随时删除重建(`rebuild-memory`), 但**只重建 memory/**。
- 未知文件类型(如 PDF)放 `assets/` 目录, 不参与解析。
- 真实 API Key **不得**出现在任何项目文件中(SecretStore 见 PROVIDERS §3)。

## 11. Git 友好性

- 建议用户用 git 管理 `data/novels/<project_id>/`(章节历史可 diff/回滚)。
- 本软件不强制 git, 但文件格式天然支持。
- `.gitignore` 建议: `logs/`, `*.tmp`, `.history/`(可选, 快照由 undo 管理)。

## 12. 版本演进

- `project.json` 带 `format_version: 1`; 后续升级提供迁移脚本。
- 不向前兼容的变更需 `migrate` 命令(第一版不做, 设计上预留)。
