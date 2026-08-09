# AGENT_RUNTIME — Agent 运行时设计

## 1. 设计目标

- 三个 Agent(Chief / Writer / Reviewer)共享**同一套运行时**, 只是系统提示词和工具权限不同。
- 运行时通过 **BaseProvider 接口**与模型交互, **不感知任何厂商 HTTP 格式**(OpenAI/Anthropic/Gemini 差异由 Provider 层消化)。
- 可被单测(注入 FakeProvider)。

## 2. Agent 定义

```python
@dataclass
class AgentDef:
    id: str                    # "chief" / "writer" / "reviewer"
    name: str                  # 中文名(主编/写作分身/审稿)
    system_prompt: str         # 由 PROMPTS 模板 + 项目上下文渲染
    tools: list[str]           # 允许的工具白名单
    max_tool_rounds: int       # 每轮对话最多工具调用轮次
    default_model: str | None  # 模型覆盖(可选, 指向 settings.models)
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
     a. resp = provider.chat(model, messages, tools)   # BaseProvider 接口
     b. if resp.tool_calls:
          for each call:
            result = tool_registry.execute(call.name, call.arguments, ctx)
            messages.append(tool_result_message)
        else:
          return resp.text     # 纯文本完成
  3. 超过轮数 → 返回当前内容 + 标记 "tool_rounds_exceeded"
```

- 工具结果上限: 单次工具输出截断(默认 4K 字符), 超长用摘要。
- 所有 LLM 调用走 Provider 层(流式可选)。

## 4. Provider 接口(Agent Runtime 只依赖它)

```python
# llm/provider.py
class BaseProvider(ABC):
    def chat(self, request: ChatRequest) -> ChatResult: ...
    def estimate_tokens(self, text: str) -> int: ...

class ChatRequest:      # model/messages/temperature/stream/tools/context_budget
class ChatResult:       # text/tool_calls/usage/error   ← 统一内部数据模型
class ToolCall:         # id/name/arguments_json
class Usage:            # prompt_tokens/completion_tokens

class OpenAICompatibleProvider(BaseProvider):   # 第一版唯一实现
    # 内部: HTTP + SSE 流式 + tool_calls 解析 → 转成 ChatResult

class AnthropicProvider(BaseProvider):   # 预留接口, 第一版不实现
    ...
class GeminiProvider(BaseProvider):      # 预留接口, 第一版不实现
    ...
```

- **强制**: Agent Runtime / Workflow / Tools 一律 import `BaseProvider`, 不得 import `OpenAICompatibleProvider` 的 HTTP 细节。
- `provider.chat` 内部完成: 模型名解析、工具 schema 转换、流式聚合、错误映射、token 估算。
- tool_calls / streaming / usage 统一为内部数据模型, 厂商差异不泄露到上层。

## 5. 会话/消息模型

```python
@dataclass
class ChatMessage:
    role: "system" | "user" | "assistant" | "tool"
    content: str
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
```

- 每轮 CLI 对话是**有状态会话**(项目级), 会话消息存内存。
- 会话消息**不含全书正文**, 只含上下文包 + 工具结果。

## 6. 工作流引擎(workflow.py)

### 命令(CLI Adapter 层提供入口, Core 提供 API)

| 命令 | 流程 |
|---|---|
| `chat` | 用户 ↔ 主编自由对话(主编可调用工具查/改资料) |
| `write <chapter>` | 主编规划 → Writer 写作 → Reviewer 审稿 → READY → **用户确认** → 收编 |
| `review <chapter>` | 仅 Reviewer 审稿 |
| `outline <text>` | 主编更新大纲/细纲 |
| `confirm <chapter>` | 用户确认(USER_CONFIRMED → CONFIRMED) |
| `undo-last-change` | 从 .history/ 回滚最近一次 AI 写入 |

### write 流程(与状态机一致, 见 DATA_MODEL §7)

```
1. 主编: 组装上下文包 → 产出《任务卡》(细纲确认/创作要求/给 Writer 的指示)
2. Writer: 读任务卡+素材 → 写 drafts/chNNNN.draft.md (状态 DRAFT, 写前快照)
3. 提交审稿 → 状态 REVIEWING
4. Reviewer: 读草稿 → 输出:
   - PASS → 状态 READY(等待用户确认, 不自动收编)
   - NEEDS_WORK → 修改意见列表(具体到段落) → 回到 DRAFT 重写(≤K 轮)
5. 用户 `confirm` → USER_CONFIRMED → 收编流程:
   a. 草稿移入 chapters/chNNNN.md, 状态 CONFIRMED
   b. 更新 project.json current_chapter
   c. 记忆更新(summaries/chNNNN.md / characters / world / timeline / foreshadowing)
6. (auto_accept=true 时: READY 自动收编, 第一版默认 false 不实现)
```

### 状态机

```
DRAFT → REVIEWING → READY → USER_CONFIRMED → CONFIRMED
                  ↘ NEEDS_WORK → DRAFT(重写循环)
```

**两条确认路径**:
- **A. 用户手动章节**: `DRAFT → USER_CONFIRMED → CONFIRMED`(用户显式 confirm, 无需 Reviewer — M1 起可用)
- **B. AI Writer 章节**: 必须 `DRAFT → REVIEWING → READY → USER_CONFIRMED → CONFIRMED`(**禁止 AI 绕过 Reviewer 直接确认** — M5 起; 程序层强制校验: AI 写入的草稿在 READY 前不可 confirm)

失败路径: ERROR(可重试) / ABORTED(用户取消) / ESCALATED(升级主编决策)

## 7. 提示词模板(prompts.py)

- 全部模板为原创, 参数化渲染(项目名/章节号/记忆片段…)。
- 模板目录:
  - `chief_system.md` — 主编系统提示词
  - `writer_system.md` — Writer 系统提示词
  - `reviewer_system.md` — Reviewer 系统提示词
  - `summarizer.md` — 章节摘要/记忆更新专用(内部 Agent)
- 每模板含"规则清单", 例如 Writer 明确: "只写正文, 不改人物设定; 设定冲突时在结尾标注"。

## 8. 幂等与容错

- 同一写作任务重跑 → 覆盖草稿(提示词含章节号, 不重复追加); 覆盖前自动快照到 .history/。
- LLM 返回 JSON 解析失败 → 重试 1 次 → 按纯文本兜底解析。
- 中途 Ctrl+C → 草稿保留, 状态标记 draft(不丢数据)。
- 每次 LLM 调用记录: 模型/耗时/输入输出字符数/usage(不含 Key)。
- Provider 层返回结构化错误(超时/401/429/超长), 超长时触发上下文裁剪重试 1 次。

## 9. 可测试性

- `FakeProvider` 注入: 预设返回(文本 / tool_calls / 空输出 / 异常 / 超长), 验证运行时行为。
- 工具注册表独立可单测(路径校验/截断/权限/快照)。
- 记忆更新逻辑可对固定输入断言输出文件。
- 状态机单测: 每个状态转换的合法/非法路径。
