# MVP_PLAN — 分阶段开发计划 (M0–M7)

> 铁律: 每步**实际运行成功**才算完成, 不以"代码写了"为准。
> 每步完成时运行 checkpoint 交接。
> CLI 是 M0–M7 的测试入口; Core Engine 不依赖 CLI(见 ARCHITECTURE §2)。

## 里程碑总览

| 里程碑 | 目标 | 验收标准(必须真实跑通) |
|---|---|---|
| M0 | 软件能启动 | CLI 可启动, 显示帮助, 配置校验通过 |
| M1 | 新建小说、保存章节 | 建项目/写章节/列章节/读章节 全流程可用 |
| M2 | 配置自己的 API 并成功对话 | 用用户真实 Key(经 SecretStore)完成一次对话 |
| M3 | 主编聊天 | 主编 Agent 可对话并调用工具(查大纲/人物) |
| M4 | 大纲/人物/世界观 | 主编可读/写大纲、人物、世界观文件 |
| M5 | AI 真正生成一章并保存 | Writer 完整生成一章正文并落盘(草稿) |
| M6 | Reviewer 审稿 | 审稿可发现预设 bug(注入错误测试) |
| M7 | 主编→Writer→Reviewer 完整跑通 | 一次 write + confirm 完成全流程 + 记忆更新 |

---

## M0 — 软件能启动

**范围**
- Core Engine 骨架: project/memory/agents/llm/tools 模块可 import
- Adapter: `adapters/cli/main.py`(argparse, 仅在此层)
- 配置: `config/settings.json` 读写 + 校验(必填 base_url/model; secret_reference 可选)
- SecretStore: keyring 后端初始化(Windows Credential Manager), 环境变量回退
- 日志目录初始化

**验收(实际运行)**
```
$ python -m adapters.cli --help      # 输出命令列表
$ python -m adapters.cli config validate   # 输出配置状态(不联网)
```
- 错误路径: 无配置文件 → 提示创建模板; 配置非法 JSON → 明确报错。

**测试**
- 单元: 配置读写/校验; SecretStore 读写(临时 keyring backend)
- 手动: 上述命令真实执行

---

## M1 — 新建小说、保存章节

**范围**
- Core: `project.create(name)` / `chapter.write(n)` / `chapter.list` / `chapter.read`
- 目录结构按 PROJECT_FORMAT(4 位章节号, 记忆目录骨架)
- 章节状态机: draft → confirmed(手动确认路径先行)

**验收(实际运行)**
```
$ python -m adapters.cli novel create 万象之旅
$ python -m adapters.cli chapter write 1 --title 初入星城
$ python -m adapters.cli chapter list      # 显示 ch0001 draft
$ python -m adapters.cli chapter confirm 1
$ python -m adapters.cli chapter list      # 显示 ch0001 confirmed
```
- 检查磁盘文件结构符合 PROJECT_FORMAT(含 memory/summaries/ 等骨架)。

**测试**
- 单元: 目录生成/章节读写/状态转换(临时目录)
- 手动: 上述命令真实执行

---

## M2 — 配置自己的 API 并成功对话

**范围**
- `llm/provider.py`: BaseProvider 接口 + OpenAICompatibleProvider
- `config set-key <ref>`(密钥经 SecretStore, 不回显)
- `chat` 命令(无 Agent, 直连模型)
- 错误处理: 401/429/超时/网络

**验收(实际运行)**
```
$ python -m adapters.cli config set default_model.base_url https://api.deepseek.com/v1
$ python -m adapters.cli config set-key deepseek-main     # 交互输入, 不回显
$ python -m adapters.cli config set default_model.model deepseek-chat
$ python -m adapters.cli chat "你好, 用一句话介绍你自己"   # 真实返回文本
```
- 必测: 错误 Key → 401 明确提示(不含 Key); 断网 → 明确报错不崩溃。
- 检查: settings.json 中**无真实 Key**; 日志中无 Key。

**测试**
- 单元: FakeProvider 注入(解析/错误映射/内部数据模型)
- 手动: 用户真实 Key 跑通一次

---

## M3 — 主编聊天

**范围**
- Agent 运行时(AGENT_RUNTIME): system prompt + tool_calls 循环(依赖 BaseProvider)
- 主编工具白名单: project_info / list_chapters / read_outline / read_character / search_memory(只读起步)
- `chat` 命令接入主编

**验收(实际运行)**
```
$ python -m adapters.cli chat "我们的小说现在写到哪了?"   # 主编查记忆后回答
$ python -m adapters.cli chat "帮我看看大纲里第一卷有几个章节"
```
- 主编回答必须**基于真实工具返回**(而非模型猜测) — 在回答里体现具体章节号/文件名。
- 弱模型(不支持 tool_calls)降级纯文本模式, 提示词中塞入上下文包。

**测试**
- 单元: FakeProvider 返回 tool_calls → 校验执行与回填; 状态机转换
- 手动: 真实对话含 ≥1 次工具调用

---

## M4 — 大纲/人物/世界观

**范围**
- 主编写入工具: update_outline / update_character / update_world / save_memory_entry(**写前快照**)
- `outline` 子命令与资料文件管理
- 项目资料读取进上下文包

**验收(实际运行)**
```
$ python -m adapters.cli chat "把第一卷的目标改成: 主角建立自己的商队"
$ python -m adapters.cli outline show           # 看到修改生效
$ python -m adapters.cli chat "给林小满补充设定: 她会唱歌"
$ python -m adapters.cli character show 林小满  # 看到更新
$ python -m adapters.cli undo-last-change       # 回滚最近一次 AI 修改
$ python -m adapters.cli character show 林小满  # 看到回滚生效
```
- 磁盘文件真实变化, 再次对话主编能引用; .history/ 快照存在且 undo 可用。

**测试**
- 单元: 权限矩阵(Writer 调 update_outline 应被拒); 快照/undo 逻辑
- 手动: 上述真实跑通

---

## M5 — AI 真正生成一章并保存

**范围**
- Writer Agent(读素材 → 写草稿)
- `write <n>` 命令(主编规划 → Writer 写作 → 草稿落盘, 状态 DRAFT)
- 上下文包组装(ContextBudget 动态预算)

**验收(实际运行)**
```
$ python -m adapters.cli write 1      # 基于 M4 的大纲, 生成 ch0001.draft.md
$ python -m adapters.cli chapter read 1 --draft   # 看到完整正文
```
- 生成章节能呼应大纲设定与人物(人工检查)。
- 长文本输出流式显示, 中断不丢草稿。
- 用 ContextBudget 在小上下文模型配置下验证自动裁剪生效。

**测试**
- 单元: ContextBudget(预算计算/优先级裁剪)、草稿原子写、快照
- 手动: 真实生成一章

---

## M6 — Reviewer 审稿

**范围**
- Reviewer Agent(只读工具 + 审稿报告)
- `review <n>` 命令; 报告写 review/chNNNN.review.md
- 一致性检查项: 人物名/世界事实/时间线/伏笔
- 状态机: DRAFT → REVIEWING → READY(通过时, **不自动收编**)

**验收(实际运行)**
```
$ python -m adapters.cli review 1     # 生成审稿报告; 通过则状态变 READY
$ python -m adapters.cli chapter list # 显示 ch0001 ready(不是 confirmed)
```
- **注入测试**: 在草稿中故意写错(人名/事实) → 审稿报告必须指出 → 状态回 DRAFT。
- 通过案例: 正确草稿 → PASS → READY。

**测试**
- 单元: 审稿报告解析(通过/需修改); READY 不自动确认的状态机断言
- 手动: 注入 bug 真实审出

---

## M7 — 主编→Writer→Reviewer 完整跑通一章

**范围**
- 完整 write 流程: 主编规划 → Writer → Reviewer → (修改循环 ≤3 轮) → READY → **用户 confirm** → CONFIRMED
- 收编: 草稿移入 chapters/、更新 current_chapter、记忆更新(摘要/人物/世界/时间线/伏笔)
- `rebuild-memory` 命令(只重建 memory/, 不碰事实源)

**验收(实际运行)**
```
$ python -m adapters.cli write 3      # 全程自动, 流式展示各阶段
# 输出: PLANNING → WRITING → REVIEWING → READY
$ python -m adapters.cli confirm 3    # 用户确认
# 输出: USER_CONFIRMED → CONFIRMED(收编 + 记忆更新)
$ python -m adapters.cli memory show  # 摘要/时间线/伏笔已更新
$ python -m adapters.cli chapter read 3   # confirmed 章节
$ python -m adapters.cli chat "第三章发生了什么?"  # 主编能回答(记忆生效)
```
- **负向验收**: 不 confirm 时, 章节保持 READY, current_chapter 不变。
- **恢复验收**: undo-last-change 可回滚一次 AI 写坏的大纲。
- **重建验收**: rebuild-memory 后事实源(chapters/characters/world/outline)字节不变, 记忆重建成功。
- 完整跑通 = M7 达成。MVP 结束。

**测试**
- 集成: 全流程一次(真实 LLM)
- 回归: M0–M6 全部命令仍可用

---

## 里程碑依赖图

```mermaid
graph LR
    M0 --> M1 --> M2 --> M3 --> M4 --> M5 --> M6 --> M7
```

## 每步交付物

| 步 | 交付 |
|---|---|
| M0 | 可启动 CLI + 配置校验 + SecretStore 可用 |
| M1 | 项目/章节 CRUD 可用 |
| M2 | 真实对话跑通(用户 Key, 不出现在任何文件中) |
| M3 | 主编对话 + 工具调用 |
| M4 | 大纲/人物/世界观可读写 + undo 可用 |
| M5 | 一章真实生成落盘(草稿) |
| M6 | 审稿能抓 bug, READY 状态正确 |
| M7 | 全流程 + 用户确认 + 记忆更新 + 重建/回滚验证 |

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 用户模型不支持 tool_calls | M3 起提供纯文本降级模式; M2 先验证 |
| 上下文预算与模型不匹配 | ContextBudget 按 max_context_tokens 动态计算(M5 验证) |
| 审稿"过审但质量差" | 审稿标准写进 Reviewer 提示词; 用户确认门槛兜底 |
| 长篇小说一致性随时间下降 | 记忆增量更新 + 事实源/派生记忆分离 + 定期"设定对账"(可选) |
| AI 改错内容 | .history/ 快照 + undo-last-change(写入前自动) |
| API 费用不可控 | 本地 usage 统计 + 动态预算 |

## 第一版明确不做的(再次确认)

手机端 / 自动发布 / 会员 / 支付 / 客服 / 官方模型商城 / Suno / 视频生成 / 云同步 / Anthropic/Gemini Provider 实现(仅接口)。
