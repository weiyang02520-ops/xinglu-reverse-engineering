# PROVIDERS — 模型提供商接入设计

## 1. 目标

- 用户配置任意 **OpenAI Chat Completions 兼容** 服务(Base URL / API Key / Model)。
- 同一套代码适配: OpenAI、DeepSeek、Qwen(阿里)、Moonshot、OpenRouter、本地 Ollama 等。
- 不绑定任何厂商 SDK, 纯 HTTP 调用。

## 2. 配置

`config/settings.json`(见 DATA_MODEL §5):

```json
{
  "default_model": { "base_url": "https://api.deepseek.com/v1", "api_key": "…", "model": "deepseek-chat" },
  "models": { "writer": {…}, "reviewer": {…} }
}
```

- `api_key` 可为空字符串 → 跳过 Authorization 头(本地 Ollama 等无需 Key)。
- `base_url` 末尾 `/` 处理: 统一拼 `/chat/completions`。
- 支持环境变量覆盖(便于非交互场景): `NOVEL_BASE_URL`, `NOVEL_API_KEY`, `NOVEL_MODEL`。

## 3. 客户端接口

```python
# llm/client.py
class LLMClient:
    def __init__(self, cfg: ModelConfig, http_timeout=120): ...
    def chat(self, messages, model=None, temperature=None, stream=True, tools=None)
        -> StreamingResult | CompletionResult
    def count_tokens(self, text) -> int   # 估算(字符/2 或 tiktoken 可选)

# 统一返回:
#   - text: 最终文本
#   - tool_calls: [{id, name, arguments_json}]
#   - usage: {prompt_tokens, completion_tokens}
#   - error: 结构化错误(超时/限流/网络/无效Key)
```

## 4. 请求示例

```http
POST {base_url}/chat/completions
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "…"},
    {"role": "user", "content": "…"}
  ],
  "temperature": 0.8,
  "stream": true,
  "tools": [ … ]          # 可选
}
```

流式: 解析 SSE `data:` 行, 累积 `delta.content` / `delta.tool_calls`。

## 5. 错误处理

| 错误 | 识别 | 处理 |
|---|---|---|
| 网络/超时 | 连接异常 / 读取超时 | 重试 1 次(指数退避 2s) → 报错给用户 |
| 401/403 | HTTP 401/403 | 明确提示"API Key 无效或权限不足", 不重试 |
| 429 限流 | HTTP 429 / 响应含 rate_limit | 等待重试(可选, 默认提示用户) |
| 5xx | 500/502/503 | 重试 1 次 → 报错 |
| 模型不存在 | 400 含 model 相关错误 | 提示检查 model 名 |
| 上下文超长 | 400 含 context/token 相关 | 触发上下文裁剪(缩小上下文包)后重试 1 次 |

- 所有错误**不输出 Key**, 不输出完整请求体。

## 6. 模型能力协商(简化)

第一版不做能力探测, 提供手动配置项:

```json
"capabilities": { "tool_calls": true, "vision": false, "max_context_tokens": 128000 }
```

- `tool_calls: false` → 运行时跳过 tools 参数(纯文本模式, 兼容弱模型)。
- `max_context_tokens` → 上下文包预算上限(默认按 128K 模型 25% 预留)。
- 可选 `reasoning` 开关(若用户模型支持, 在请求中加 `reasoning_effort`/`thinking` 参数, 由适配器按模型名判断, 参考逆向研究中常见的模型差异处理思想)。

## 7. 已验证兼容性目标(第一版发布时测试)

| 服务 | Base URL 示例 | 备注 |
|---|---|---|
| OpenAI | https://api.openai.com/v1 | - |
| DeepSeek | https://api.deepseek.com/v1 | tool_calls 支持 |
| Qwen (DashScope 兼容) | https://dashscope.aliyuncs.com/compatible-mode/v1 | OpenAI 兼容模式 |
| Moonshot | https://api.moonshot.cn/v1 | - |
| OpenRouter | https://openrouter.ai/api/v1 | 中转 |
| Ollama (本地) | http://127.0.0.1:11434/v1 | 无需 Key |

> 这些是公开通用端点, 与任何商业软件无关; 各服务是否支持 tool_calls 由用户自行确认。

## 8. 用量统计(本地)

- 每次调用记录到 `data/logs/usage.jsonl`: 时间/模型/prompt_tokens/completion_tokens/耗时。
- 提供 `usage` 命令查看累计(纯本地, 无任何上报)。

## 9. 安全

- Key 只在请求头使用, 永不写入日志/报错/记忆文件。
- settings.json 文件权限建议 600(写入时尝试 chmod)。
- 首次连接做最小验证: 空对话请求(或 models 列表若支持), 确认可达后才进入主流程。
