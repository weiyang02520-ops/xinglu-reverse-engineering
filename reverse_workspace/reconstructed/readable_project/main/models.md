# 模型适配器与 LLM 客户端

> CONFIRMED(适配器 ID/环境变量) / RECONSTRUCTED(结构)。

## 提供商支持

| 能力 | 协议 | 特殊处理 |
|---|---|---|
| 文本生成 | OpenAI 兼容 `/chat/completions` | Bearer; 401 → refreshApiKey 重试 |
| Anthropic | `/v1/messages` | headers: anthropic-version, x-api-key |
| Gemini | `/v1beta/models/{model}:generateContent` | gemini 工具 schema |
| 图像生成 | `/images/generations`(b64_json), `/images/edits`(multipart) | 任务轮询 |
| Suno 音乐 | 任务创建 + `/fetch` 轮询 | tracks[] 返回 |
| 可灵 Omni 视频 | 任务创建 + 轮询 | videoUrl/coverUrl/duration/resolution/credits |
| 搜索 | Serper / 智谱 / 博查 / 统一网关 | 统一结果结构 |

## 模型适配器 (kdt 数组)

按 baseUrl/模型名自动匹配, 覆盖请求参数:

| 适配器 ID | 匹配 | 请求覆盖 |
|---|---|---|
| gemini_compatible | baseUrl 含 gemini 或模型名含 gemini | gemini 工具格式 |
| kimi_k2 | kimi-k2.6 / k2.5 / k2-thinking | 文本工具轮策略 |
| deepseek | deepseek | max_tokens 32768, thinking enabled |
| gpt_5_5 | gpt-5.5 | reasoning_effort xhigh |
| minimax_m3 | minimax-m3 | thinking adaptive, reasoning_split |
| qwen_3_6 | qwen3.6 / qwen3-6 | enable_thinking, budget 81920 |
| claude_compatible_chat | claude-opus-4.6~4.8, fable-5 | max_tokens 16000, effort max |
| glm_5_1 | glm-5.1 | tool_stream, thinking enabled |

未匹配 → `openai` 默认。

## 环境变量(模型/功能开关)

```
NOVELFORGE_CHAT_BASE_URL / CHAT_API_KEY / CHAT_MODEL
NOVELFORGE_IMAGE_BASE_URL / IMAGE_MODEL / IMAGE_ENABLED
NOVELFORGE_MUSIC_BASE_URL / MUSIC_MODEL / MUSIC_ENABLED
NOVELFORGE_VIDEO_BASE_URL / VIDEO_MODEL / VIDEO_ENABLED
NOVELFORGE_MODEL_WEB_SEARCH_* (搜索模型)
NOVELFORGE_PUBLISHING_BASE_URL / PUBLISHING_MODEL / PUBLISHING_ENABLED (发布)
NOVELFORGE_INPUT_CLARITY_* (输入清晰度分析)
NOVELFORGE_OPERATION_GUARD_* (操作守卫)
NOVELFORGE_OFFICIAL_MODEL_* (官方模型权益/配额)
NOVELFORGE_SEARCH_* (搜索提供商/缓存)
NOVELFORGE_VECTORENGINE_* (vectorengine 中转)
NOVELFORGE_QIXIANG_PAY_* (奇象支付: PID/KEY/回调URL)
NOVELFORGE_GATEWAY_URL / ACCOUNT_GATEWAY_URL / FALLBACK (官方 API)
NOVELFORGE_MOBILE_BRIDGE_PORT / HOST
NOVELFORGE_WORKSPACE_ROOT / DESKTOP_USER_DATA_DIR / RENDERER_URL
```

## 重试与错误处理

- 重试状态码: 408, 425, 429, 500, 502, 503, 504, 522, 524(指数退避)
- 401 → refreshApiKey(配置了才重试)
- 错误分类(渲染器): context 超长 / 限流 / 安全过滤 / 网络错误 / token 过期
- 官方模型: 创作点不足 → "请充值"; 未开通 → "请开通会员"
