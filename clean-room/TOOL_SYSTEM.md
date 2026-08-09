# TOOL_SYSTEM — 工具系统设计

## 1. 目标

Agent(主要是主编)在对话/规划中能调用工具读写项目数据, 与 LLM 的 tool_calls 对接。

## 2. 工具清单(第一版)

### 只读类

| 工具 | 说明 | 返回 |
|---|---|---|
| `project_info` | 项目元信息(书名/类型/风格/进度) | JSON |
| `read_file(path)` | 读项目内文本文件(白名单校验) | 文本(截断) |
| `list_files(dir)` | 列目录 | 文件列表 |
| `read_chapter(n)` | 读指定章节(默认只读前 N 字, 可指定范围) | 文本 |
| `list_chapters()` | 章节清单(号/标题/状态) | JSON |
| `search_memory(keyword)` | 在记忆文件中搜索关键词(标题匹配或行匹配) | 片段 |
| `get_recent_chapters(n)` | 最近 n 章摘要 | 文本 |

### 记忆/资料类

| 工具 | 说明 | 返回 |
|---|---|---|
| `read_outline()` | 全书梗概 + 当前卷大纲 + 当前细纲 | 文本 |
| `read_character(name)` | 读人物设定 | 文本 |
| `read_world()` | 读世界观 + 势力 | 文本 |
| `list_foreshadowings(status)` | 伏笔清单(open/closed) | JSON |

### 写入类(权限受限)

| 工具 | 说明 | 权限 |
|---|---|---|
| `update_outline(text)` | 更新大纲/细纲(覆盖指定节) | Chief 仅 |
| `update_character(name, text)` | 更新/创建人物设定 | Chief 仅 |
| `update_world(text)` | 更新世界观 | Chief 仅 |
| `write_chapter_draft(n, text)` | 写章节草稿 | Writer 仅 |
| `save_memory_entry(kind, text)` | 追加记忆条目(摘要/时间线/伏笔) | Chief 仅(确认后自动触发) |

> Reviewer **无写入工具**(只读 + 输出审稿文本), 防止误改正文。

## 3. 工具注册与执行

```python
# tools/registry.py
TOOLS: dict[str, ToolDef] = {
  "read_file": ToolDef(fn=read_file, schema=..., permission="read"),
  "write_chapter_draft": ToolDef(fn=write_draft, schema=..., permission="writer"),
  ...
}

def execute(name, args, ctx) -> str:
    tool = TOOLS[name]
    check_permission(ctx.agent_id, tool.permission)   # 白名单
    check_path(ctx.project_root, args.get("path"))    # 路径校验
    result = tool.fn(ctx, args)
    return truncate(result, MAX_TOOL_OUTPUT)          # 默认 4K 字符
```

### 路径安全

- 所有 `path` 参数解析后必须 `resolve()` 且以 `project_root` 为前缀, 否则拒绝。
- 禁止 `..` 逃逸 / 绝对路径 / 符号链接指向项目外(第一版不做 symlink 解析, resolve 即可)。

### 权限矩阵

| Agent | read_* | search | update_outline | update_character/world | write_chapter_draft | save_memory |
|---|---|---|---|---|---|---|
| Chief | ✅ | ✅ | ✅ | ✅ | ❌(不直接写正文) | ✅ |
| Writer | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Reviewer | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Summarizer(内部) | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |

## 4. 工具 schema(OpenAI 格式示例)

```json
{
  "name": "write_chapter_draft",
  "description": "把完整的章节正文写入草稿文件(仅 Writer 可调用)",
  "parameters": {
    "type": "object",
    "properties": {
      "chapter": { "type": "integer", "description": "章节号" },
      "content": { "type": "string", "description": "完整正文(Markdown)" }
    },
    "required": ["chapter", "content"]
  }
}
```

## 5. 工具输出截断策略

- 单工具输出 > 4K 字符 → 截断 + 追加 `(已截断, 共 N 字符, 如需更多用 read_file 指定范围)`。
- `read_file` 支持 `offset/limit` 参数(字符级), 供 Agent 分段读取。
- 工具结果统一加入消息历史, 计入上下文预算(见 ARCHITECTURE §4)。

## 6. 防滥用

- 每轮对话工具调用上限: `max_tool_calls_per_turn`(默认 8), 防止失控循环。
- 写操作全部走"临时文件 + rename"原子写。
- 写入类工具返回被覆盖前的旧内容前 N 字, 供 Agent 感知。

## 7. 扩展(第二版, 不在 MVP)

- `web_search`(用户自己的搜索 API Key)
- `image_gen`(用户自己的图像 API)
- 文件导入(docx/md 批量导入素材)
