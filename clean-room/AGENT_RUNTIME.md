# AGENT_RUNTIME — Agent 运行时设计

## 1. 设计目标

- 三个 Agent(Chief / Writer / Reviewer)共享**同一套运行时**, 只是系统提示词和工具权限不同。
- 支持 OpenAI 兼容的 `tool_calls`(函数调用)与纯文本两种模式。
- 运行时与 LLM 提供商解耦(任何 OpenAI 兼容 API 可用)。
- 可被单测(注入 fake LLM)。

## 2. Agent 定义

```python
@dataclass
class AgentDef:
    id: str                    # "chief" / "writer" / "reviewer"
    name: str                  # 中文名(主编/写作分身/审稿)
    system_prompt: str         # 由 PROMPTS 模板 + 项目上下文渲染
    tools: list[str]           # 允许的工具白名单
    max_tool_rounds: int       # 每轮对话最多工具调用轮次
    default_model: str | None  # 模型覆盖(可选)
```

### 三个 Agent 的职责边界

| Agent | 系统提示词要点 | 工具 | 产出 |
|---|---|---|---|
| **Chief 主编** | 创作负责人: 理解用户意图, 查记忆, 规划, 分派任务, 决策 | 全部(只读类 + 记忆类 + 写大纲/细纲) | 规划文本 / 任务卡 / 大纲更新 / 聊天回复 |
| **Writer** | 专注写作: 按细纲和前文写正文, 不擅自改设定 | 读文件 + 写章节草稿 + 查记忆 | 章节草稿 / 修改稿 |
| **Reviewer** | 审稿: 检查一致性(人物/世界/时间线/伏笔)、文风、逻辑; 输出通过或修改意见 | 读文件 + 查记忆 + 写批注(只读, 不改正文) | 审稿报告(通过/需修改+具体意见) |

## 3. 运行时循环(Agent loop)

```
run_agent(agent, messages, tools, max_rounds):
  1. messages = [system_prompt(渲染后)] + messages
  2. 循环 (round < max_rounds):
     a. resp = llm.chat(model, messages, tools)
     b. if resp.tool_calls:
          for each call:
            result = tool_registry.execute(call.name, call.arguments)
            messages.append(tool_result_message)
        else:
          return resp.content   # 纯文本完成
  3. 超过轮数 → 返回当前内容 + 标记 "tool_rounds_exceeded"
```

- 工具结果上限: 单次工具输出截断(默认 4K 字符), 超长用摘要。
- 所有 LLM 调用走统一 client(流式可选)。

## 4. 会话/消息模型

```python
@dataclass
class ChatMessage:
    role: "system" | "user" | "assistant" | "tool"
    content: str
    tool_calls: list | None = None
    tool_call_id: str | None = None
```

- 每轮 CLI 对话是**有状态会话**(项目级), 会话消息存内存, 可配置持久化(可选, 第一版内存即可)。
- 重要: 会话消息**不含全书正文**, 只含上下文包 + 工具结果。

## 5. 工作流引擎(workflow.py)

### 命令

| 命令 | 流程 |
|---|---|
| `chat` | 用户 ↔ 主编自由对话(主编可调用工具查/改资料) |
| `write <chapter>` | 主编规划 → Writer 写作 → Reviewer 审稿 → 保存 |
| `review <chapter>` | 仅 Reviewer 审稿 |
| `outline <text>` | 主编更新大纲/细纲 |

### write 流程实现(与 ARCHITECTURE §5 一致)

```
1. 主编: 组装上下文包 → 产出《任务卡》(细纲确认/创作要求/给 Writer 的指示)
2. Writer: 读任务卡+素材 → 写 chNNN.draft.md
3. Reviewer: 读草稿 → 输出:
   - PASS → confirmed
   - NEEDS_WORK → 修改意见列表(具体到段落)
4. NEEDS_WORK → 意见回给 Writer 重写(最多 max_review_rounds 轮)
5. 仍不过 → 升级主编决策(接受 / 重新规划 / 交人工)
6. 确认后: 记忆更新(chapter_summaries/characters/world/timeline/foreshadowing)
```

### 状态机

```
write 命令: PLANNING → WRITING → REVIEWING → (REVISING)* → CONFIRMED
失败路径: ERROR(可重试) / ABORTED(用户取消) / ESCALATED(升级主编)
```

## 6. 提示词模板(prompts.py)

- 全部模板为原创, 参数化渲染(项目名/章节号/记忆片段…)。
- 模板目录:
  - `chief_system.md` — 主编系统提示词
  - `writer_system.md` — Writer 系统提示词
  - `reviewer_system.md` — Reviewer 系统提示词
  - `summarizer.md` — 章节摘要/记忆更新专用(内部 Agent)
- 每模板含"规则清单", 例如 Writer 明确: "只写正文, 不改人物设定; 设定冲突时在结尾标注"。

## 7. 幂等与容错

- 同一写作任务重跑 → 覆盖草稿(提示词含章节号, 不重复追加)。
- LLM 返回 JSON 解析失败 → 重试 1 次 → 按纯文本兜底解析。
- 中途 Ctrl+C → 草稿保留, 状态标记 draft(不丢数据)。
- 每次 LLM 调用记录: 模型/耗时/输入输出字符数(不含 Key)。

## 8. 可测试性

- `FakeLLM` 注入: 预设返回(文本 / tool_calls / 空输出 / 异常), 验证运行时行为。
- 工具注册表独立可单测(路径校验/截断/错误)。
- 记忆更新逻辑可对固定输入断言输出文件。
