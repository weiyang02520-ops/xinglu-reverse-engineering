# REVIEW_FIXES — 外部模型第一轮审核修订记录

> 日期: 2026-08-09
> 状态: 10 条修订意见全部处理完毕, 等待第二轮审核。

## 逐条记录

### 1. GitHub 仓库真实状态与文档不一致

- **问题**: 外部模型经 GitHub API 读取到 `private=false / visibility=public`, 但 PROJECT_STATE/HANDOFF 手写声称 PRIVATE。
- **核实**: 真实查询确认仓库**当前为 public**(不是我此前创建时返回的 private — 之后被改动过)。
- **修改**:
  - checkpoint 脚本新增 `get_repo_visibility()`: 每次生成 HANDOFF 时实时查询 GitHub API(gh CLI 优先, 公开 API 兜底), 查不到显示 `unknown`, **不猜测**。
  - PROJECT_STATE 中删除"PRIVATE"手写声称, 明确 GitHub 可见性以 API 查询为准。
  - HANDOFF §12 增加 "GitHub 仓库可见性: <实时查询结果>" 字段。
- **未做**: 未擅自修改仓库可见性(需要用户决定)。**提醒用户**: 仓库当前是 **public**, 若希望私有, 请到 GitHub 仓库 Settings → Danger Zone → Change visibility 改回 Private。**建议改回 Private**(仓库含逆向分析文档, 且你要授权给 ChatGPT 阅读 — 即使是私有, 授权 App 后 ChatGPT 也能读)。

### 2. 修正 checkpoint 的 Commit 信息

- **问题**: HANDOFF 在 commit 前生成, 却声称写入了当前 HEAD, 导致内容过期。
- **修改**: HANDOFF §12 改用 `checkpoint_base_commit`(checkpoint 开始前的 HEAD), 并注明"最新 checkpoint commit 以 GitHub 仓库 HEAD 为准"。不制造"写回新 hash"的二次 commit。

### 3. API Key 存储重新设计

- **修改文件**: PROVIDERS.md(重写 §2/§3/§9)、DATA_MODEL.md(§9)、ARCHITECTURE.md(§7)
- **方案**: settings.json 只存 `provider/base_url/model/temperature/capabilities/secret_reference`; 新增 **SecretStore** 抽象, 第一版用 Python keyring(Windows Credential Manager), 开发模式环境变量回退; 真实 Key 绝不进入 Git/项目目录/日志/checkpoint/小说数据目录; 新增安全清单逐条检查。

### 4. CLI 只是测试入口, 不是最终架构

- **修改文件**: CLEAN_ROOM_SPEC.md(§6/§7)、ARCHITECTURE.md(§1/§2)、MVP_PLAN.md(头部注)
- **方案**: 明确 **Core Engine**(Project/Memory/Agent Runtime/Workflow/Tools/Providers, 无 UI 依赖) + **Adapter 层**(CLI Adapter 为 M0–M7 测试入口, Desktop UI Adapter 以后实现)。Core 禁止 import argparse/click/终端 IO; 强制规则写入架构文档。

### 5. 修改长篇小说文件结构

- **修改文件**: DATA_MODEL.md(§1/§5)、PROJECT_FORMAT.md(§2/§5)
- **方案**:
  - `memory/summaries/chNNNN.md`(每章摘要独立文件, 不再单文件堆叠)
  - `memory/characters.md`、`memory/world.md`、`memory/timeline.md`、`memory/foreshadowing/(每伏笔一文件+index.md)`、`memory/index.md`(检索索引)
  - `outline/volumes/volNNN.md`(一卷一文件)、`outline/chapters/chNNNN.md`(章细纲独立文件, **历史细纲不被下一章覆盖**)

### 6. 区分"事实源"和"派生记忆"

- **修改文件**: DATA_MODEL.md(§2)、PROJECT_FORMAT.md(§7)
- **方案**: 明确 **Canonical Sources**(章节正文/人物正式设定/世界观正式设定/大纲/用户确认的创作规则)vs **Derived Memory**(章节摘要/人物当前状态/世界当前状态/时间线索引/伏笔索引/长期记忆摘要)。`rebuild-memory` 只允许操作 memory/ 目录(程序级白名单强制), 绝不覆盖事实源。

### 7. 修正章节状态机

- **修改文件**: DATA_MODEL.md(§4/§7)、AGENT_RUNTIME.md(§6)、PROJECT_FORMAT.md(§10)、MVP_PLAN.md(M6/M7)
- **方案**: 五状态 `DRAFT → REVIEWING → READY → USER_CONFIRMED → CONFIRMED`; **Reviewer PASS 只进入 READY**, 用户确认后才写入正式 chapters/、更新 current_chapter、更新正式记忆; `auto_accept: false` 默认(M7 负向验收: 不 confirm 则保持 READY)。

### 8. 上下文预算改成动态预算

- **修改文件**: ARCHITECTURE.md(§4 重写)、PROVIDERS.md(§6)
- **方案**: **ContextBudget** 按 `max_context_tokens - reserve_output - 系统提示词` 动态计算输入预算; 优先级 P0(当前章细纲/当前人物/最近正文) > P1(当前卷大纲/活跃伏笔/最近摘要) > P2(世界状态/长期记忆) > P3(较旧摘要); 超预算按优先级裁剪。25-30K 不是固定默认值, 只是大上下文模型的可能结果。

### 9. Provider 架构预留真正的适配层

- **修改文件**: PROVIDERS.md(§4)、AGENT_RUNTIME.md(§4)
- **方案**: `BaseProvider` 抽象接口(chat/estimate_tokens), 内部统一数据模型(ChatRequest/ChatResult/ToolCall/Usage); 第一版只实现 `OpenAICompatibleProvider`, `AnthropicProvider`/`GeminiProvider` 仅预留接口; Agent Runtime 不依赖任何厂商 HTTP 格式。

### 10. 给 AI 写操作增加恢复能力

- **修改文件**: TOOL_SYSTEM.md(§7 重写)、PROJECT_FORMAT.md(§8)、MVP_PLAN.md(M4/M7)
- **方案**: 所有 AI 重要写入(大纲/人物/世界/正文/记忆)前自动快照旧版本到 `.history/`(index.jsonl + 快照文件, 默认保留 50 份); `undo-last-change` 顺序回滚; 用户手动编辑不触发快照; 不做复杂版本系统。

---

## 修改文件汇总

| 文件 | 修改内容 |
|---|---|
| scripts/ai_checkpoint.py | ① 实时查询可见性 ② checkpoint_base_commit |
| .ai-handoff/PROJECT_STATE.md | ① 删除 PRIVATE 手写声称, 标注以 API 为准 ③+ 本轮状态 |
| clean-room/PROVIDERS.md | ③⑤⑧⑨ 重写 |
| clean-room/DATA_MODEL.md | ③⑤⑥⑦ 重写 |
| clean-room/ARCHITECTURE.md | ④⑧ 重写 |
| clean-room/AGENT_RUNTIME.md | ⑦⑨ 重写 |
| clean-room/TOOL_SYSTEM.md | ⑩ 重写 |
| clean-room/PROJECT_FORMAT.md | ⑤⑥⑦⑩ 重写 |
| clean-room/CLEAN_ROOM_SPEC.md | ④ 修订 |
| clean-room/MVP_PLAN.md | ④⑦⑩ 修订 |
| clean-room/REVIEW_FIXES.md | 本文件(新增) |

## 遗留事项(需用户/外部模型关注)

1. **仓库可见性**: 当前为 **public**。建议用户在 GitHub 网页端改回 Private(或确认保持 public — 由用户决定, 我不擅自改)。
2. 等待第二轮外部审核。
