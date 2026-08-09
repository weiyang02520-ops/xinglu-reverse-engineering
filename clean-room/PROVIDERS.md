# PROVIDERS — 模型提供商接入设计

## 1. 目标

- 用户配置任意 **OpenAI Chat Completions 兼容** 服务(Base URL / API Key / Model)。
- 同一套代码适配: OpenAI、DeepSeek、Qwen(阿里)、Moonshot、OpenRouter、本地 Ollama 等。
- 不绑定任何厂商 SDK, 纯 HTTP 调用。

## 2. 配置(settings.json — 不含任何真实密钥)

`config/settings.json` **只保存非敏感配置**, 真实 API Key 一律经 SecretStore(见 §3):

```json
{
  "default_model": {
    "provider": "openai_compatible",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "temperature": 0.8,
    "capabilities": { "tool_calls": true, "vision": false, "max_context_tokens": 128000 },
    "secret_reference": "deepseek-main"
  },
  "models": {
    "writer":   { "provider": "openai_compatible", "base_url": "...", "model": "...", "secret_reference": "deepseek-main" },
    "reviewer": { "provider": "openai_compatible", "base_url": "...", "model": "...", "secret_reference": "deepseek-main" }
  }
}
```

### 禁止事项(硬性规则)

- 真实 API Key **不进入** settings.json
- **不进入** Git(含 .ai-handoff、checkpoint)
- **不进入** 日志 / 报错信息
- **不进入** 小说数据目录(data/novels/)
- **不进入** 任何本项目文件(除 SecretStore 存储本身, 见下)

## 3. SecretStore(密钥安全存储抽象)

```python
# llm/secret_store.py
class SecretStore:
    """平台无关的密钥存储抽象。"""
    def get(self, reference: str) -> str | None: ...
    def set(self, reference: str, value: str) -> None: ...
    def delete(self, reference: str) -> None: ...
    def exists(self, reference: str) -> bool: ...
```

### 后端(第一版)

| 优先级 | 后端 | 说明 |
|---|---|---|
| 1 | **系统凭据管理器** | Windows: Credential Manager(Python `keyring` 库, 后端 win32 加密); macOS: Keychain; Linux: Secret Service |
| 2 | **环境变量** | 开发/CI 模式: `NOVEL_API_KEY`, `NOVEL_WRITER_API_KEY`, `NOVEL_REVIEWER_API_KEY`; 环境变量命中时优先于 SecretStore 读取(便于脚本) |

> 实现策略: 先尝试 keyring; 若系统无凭据服务(如 headless Linux), 明确提示用户改用环境变量, **不降级为明文文件**。

### 读取优先级

```
1. 环境变量(若存在) → 用环境变量的值
2. SecretStore.get(secret_reference) → 用存储值
3. 都没有 → 提示用户配置(config set-key 命令交互输入, 不回显)
```

### CLI 配置命令(Key 输入不回显)

```
$ python -m app config set-key deepseek-main
API Key: ********          ← 不回显, 写入 SecretStore
```

## 4. 客户端接口

```python
# llm/client.py — 内部统一数据模型, 与具体 HTTP 格式解耦
class ChatMessage:      # role/content/tool_calls/tool_call_id
class ToolCall:         # id/name/arguments_json
class Usage:            # prompt_tokens/completion_tokens
class ChatResult:       # text/tool_calls/usage/error

class BaseProvider(ABC):
    def chat(self, messages, model, temperature, stream, tools) -> ChatResult: ...
    def estimate_tokens(self, text) -> int: ...

class OpenAICompatibleProvider(BaseProvider):  # 第一版唯一实现
    # 内部处理 /chat/completions HTTP + SSE 流式 + tool_calls 解析
    # 统一转换成上面的内部模型后再交给 Agent Runtime
```

- **Agent Runtime 只依赖 `BaseProvider` 接口**, 不感知 OpenAI HTTP JSON 格式。
- 后续新增 `AnthropicProvider` / `GeminiProvider` 只需实现 BaseProvider(第一版**不实现**, 仅预留接口)。
- 流式: 解析 SSE `data:` 行, 累积 delta, 边累积边产出文本; tool_calls 流式段按 index 聚合。

## 5. 错误处理

| 错误 | 识别 | 处理 |
|---|---|---|
| 网络/超时 | 连接异常 / 读取超时 | 重试 1 次(指数退避 2s) → 报错给用户 |
| 401/403 | HTTP 401/403 | 明确提示"API Key 无效或权限不足"(绝不含 Key), 不重试 |
| 429 限流 | HTTP 429 / rate_limit | 提示用户稍后重试(可选等待) |
| 5xx | 500/502/503 | 重试 1 次 → 报错 |
| 模型不存在 | 400 含 model 相关 | 提示检查 model 名 |
| 上下文超长 | 400 含 context/token 相关 | 触发动态预算裁剪(ARCHITECTURE §4)后重试 1 次 |

## 6. 模型能力(手动配置, 不做自动探测)

```json
"capabilities": { "tool_calls": true, "vision": false, "max_context_tokens": 128000 }
```

- `tool_calls: false` → 运行时跳过 tools 参数(纯文本模式, 兼容弱模型)。
- `max_context_tokens` → 动态预算输入(ContextBudget)的上限参考值。
- 可选 `reasoning` 开关: 若用户模型支持, 由适配层按模型名决定是否附加 `reasoning_effort`/`thinking` 参数(模型差异处理, 与具体厂商无关的通用适配思想)。

## 7. 兼容性目标(第一版发布时测试)

| 服务 | Base URL 示例 | 备注 |
|---|---|---|
| OpenAI | https://api.openai.com/v1 | - |
| DeepSeek | https://api.deepseek.com/v1 | tool_calls 支持 |
| Qwen (DashScope 兼容) | https://dashscope.aliyuncs.com/compatible-mode/v1 | OpenAI 兼容模式 |
| Moonshot | https://api.moonshot.cn/v1 | - |
| OpenRouter | https://openrouter.ai/api/v1 | 中转 |
| Ollama (本地) | http://127.0.0.1:11434/v1 | 无需 Key(secret_reference 可省略) |

> 公开通用端点, 与任何商业软件无关; tool_calls 支持由用户确认。

## 8. 用量统计(本地)

- 每次调用记录到 `data/logs/usage.jsonl`: 时间/模型/prompt_tokens/completion_tokens/耗时。
- `usage` 命令查看累计(纯本地, 不上报)。

## 9. 安全清单(实现时逐条检查)

- [ ] settings.json 无真实 Key
- [ ] SecretStore 后端 = 系统凭据管理器(环境变量为开发模式)
- [ ] 日志/报错/记忆文件无 Key
- [ ] checkpoint 安全扫描包含 SecretStore 相关规则(不可检出 Key 值)
- [ ] 首次连接验证: 空对话请求确认可达
