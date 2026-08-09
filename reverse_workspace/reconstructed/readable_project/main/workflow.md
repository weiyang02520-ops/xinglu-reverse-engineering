# 主编工作流引擎

> RECONSTRUCTED — 逻辑从 main.js T7/jkt/Dkt/Fkt 等函数反推。
> 原始结构未知(esbuild 拍平), 以下按语义重建。

## 入口

`novelforge:chief-editor:run` → `T7({projectRoot, projectId, userBrief, startChapterNumber, signal, onProgress})`

## 主循环 (T7)

```
1. 定位项目根目录, 加载项目
2. 读取项目文件索引 (Mm) 和 Agent 注册表 (Ja, 过滤 enabled)
   - 无启用 Agent → 报错 "当前项目没有启用的自定义 Agent。"
3. 读取创作资料包 (p3t) + 项目状态 (creationMode, chapterProgress)
4. 确定起始章节 (startChapterNumber ?? currentChapterNumber)
5. 循环 (maxChapters 限制):
   a. 检查 signal (abort)
   b. creationMode == "continuous":
      - 有写作预设 (Rkt) → 预设流程 (Dkt: 检查产物存在则跳过规划)
      - 无预设 (jkt) → 默认流程 (细纲存在则跳过; 否则提示可先与主编确认方向)
      - 下一卷规划检查 (Fkt)
   c. 按注册表顺序调度全部启用 Agent
   d. 每章结束: 进度上报, token 估算上报
```

## 调度器细节

- **进度事件**: `{agentId, stepId, label, status, phase, loopMode:"chapter", chapterNumber, reads[], writes[], message}`
- **status**: active / skipped / stopped / done / error
- **phase**: checking_inputs / planning / writing / tool / finalizing / idle
- **Token 估算**: 每次模型调用上报 `{kind:"prompt"|"completion", promptTokens, completionTokens}`
- **长等待确认**: 模型无响应超时(`waitConfirmationMs`)→ 询问用户是否继续等

## 两个 Agent 执行器

| 执行器 | 条件 | 行为 |
|---|---|---|
| `jkt` | 无写作预设 | 细纲可选; 按用户说明/Agent 固定输入/最近正文继续 |
| `Dkt` | 有写作预设(continuous) | 结构规划 → 卷纲 → 章节细纲; 产物已存在则断点续写 |

## 结构规划

- `structure_plan_get_status`: 查询当前章节批次的规划状态
- `structure_plan_apply_direction`: 把选定的小说结构方向写入当前卷纲和批次细纲
- `prepare_chapter_context`: 组装前文梗概/总纲/分卷大纲/当前细纲 → 供 Agent 读取

## 相关文件

- `projects/{id}/chapters/chXXX/{agent}.md` — 各 Agent 的章节产物
- `创作资料/大纲/章节细纲/` — 章纲
- `创作资料/大纲/分卷大纲/` — 卷纲
- `创作资料/大纲/` — 大纲
- `.novelforge/branches/` — 分支
