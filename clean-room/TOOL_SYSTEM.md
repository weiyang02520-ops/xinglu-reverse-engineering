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
| `search_memory(keyword)` | 在记忆索引/文件中搜索 | 片段 |
| `get_recent_chapters(n)` | 最近 n 章摘要(从 memory/summaries/) | 文本 |

### 记忆/资料类

| 工具 | 说明 | 返回 |
|---|---|---|
| `read_outline()` | 全书梗概 + 当前卷大纲 + 当前章细纲 | 文本 |
| `read_character(name)` | 读人物正式设定(characters/) | 文本 |
| `read_world()` | 读世界观正式设定(world/) | 文本 |
| `list_foreshadowings(status)` | 伏笔索引(open/closed) | JSON |

### 写入类(权限受限 + 自动快照)

| 工具 | 说明 | 权限 |
|---|---|---|
| `update_outline(text)` | 更新大纲/细纲(写前快照) | Chief 仅 |
| `update_character(name, text)` | 更新/创建人物设定(写前快照) | Chief 仅 |
| `update_world(text)` | 更新世界观(写前快照) | Chief 仅 |
| `write_chapter_draft(n, text)` | 写章节草稿(写前快照) | Writer 仅 |
| `save_memory_entry(kind, text)` | 追加记忆条目(写前快照) | Chief 仅(确认后自动触发) |

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
    snapshot_before_write(ctx, name, args)            # 写入前快照到 .history/ (§7)
    result = tool.fn(ctx, args)
    return truncate(result, MAX_TOOL_OUTPUT)          # 默认 4K 字符
```

### 路径安全

- 所有 `path` 参数解析后必须 `resolve()` 且以 `project_root` 为前缀, 否则拒绝。
- 禁止 `..` 逃逸 / 绝对路径 / 符号链接指向项目外。

### 权限矩阵

| Agent | read_* | search | update_outline | update_character/world | write_chapter_draft | save_memory |
|---|---|---|---|---|---|---|
| Chief | ✅ | ✅ | ✅ | ✅ | ❌(不直接写正文) | ✅ |
| Writer | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Reviewer | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Summarizer(内部) | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |

## 4. 工具 schema(OpenAI 格式示例 — 由 Provider 层转换)

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

> 注意: 这是**内部统一 schema**; OpenAICompatibleProvider 负责转换成厂商 JSON 格式; Agent Runtime 不接触厂商格式。

## 5. 工具输出截断策略

- 单工具输出 > 4K 字符 → 截断 + 追加 `(已截断, 共 N 字符, 如需更多用 read_file 指定范围)`。
- `read_file` 支持 `offset/limit` 参数(字符级)。
- 工具结果统一加入消息历史, 计入 ContextBudget(见 ARCHITECTURE §4)。

## 6. 防滥用

- 每轮对话工具调用上限: `max_tool_calls_per_turn`(默认 8)。
- 写操作全部走"临时文件 + rename"原子写。
- 写入类工具返回被覆盖前的旧内容前 N 字, 供 Agent 感知。

## 7. 恢复能力(undo-last-change)

> "临时文件 + rename"只防文件写一半, 不防 AI 把正确内容改错。因此**所有 AI 重要写入前先保留旧版本**。

### .history/ 快照机制

- 位置: `data/novels/<id>/.history/`
- 触发: 每次写入类工具执行**之前**, 复制目标文件旧内容 → 快照文件
- 命名: `<操作序列号>_<相对路径带下划线>.bak`
- 快照记录(索引): `.history/index.jsonl` — 每行 `{seq, tool, target, timestamp, note}`
- 保留: 默认最近 50 份(`history.max_snapshots`), 超出清理最旧

### undo-last-change

```
$ python -m app undo-last-change
# 读取 .history/index.jsonl 最后一条 → 用快照内容恢复目标文件 → 标记该条已回滚
```

- 回滚后目标文件状态 = AI 写入前; 被回滚的快照保留(可再次回滚到更早)。
- 仅支持顺序回滚(一条条 undo), 不做任意点恢复(保持简单)。
- 用户手动编辑**不**触发快照(只保护 AI 写入)。

### 快照覆盖范围(第一版)

| 内容 | 快照 | 说明 |
|---|---|---|
| 大纲(outline/*) | ✅ | update_outline 前 |
| 人物(characters/*) | ✅ | update_character 前 |
| 世界观(world/*) | ✅ | update_world 前 |
| 章节草稿(drafts/*) | ✅ | write_chapter_draft 前 |
| 记忆(memory/*) | ✅ | save_memory_entry 前 |
| 已确认章节(chapters/*) | ✅ | 收编时覆盖前(草稿→正式 若同名) |

## 8. 扩展(第二版, 不在 MVP)

- `web_search`(用户自己的搜索 API Key)
- `image_gen`(用户自己的图像 API)
- 文件导入(docx/md 批量导入素材)
