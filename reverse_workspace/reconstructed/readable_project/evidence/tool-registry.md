# 关键证据摘录 — AI 工具注册表 (26 个)

> CONFIRMED — main.js 工具 schema 原文摘录(描述已解码中文)。

## 创作类

| 工具 | 描述(原文) |
|---|---|
| project_get_state | 查看当前星炉项目的结构化只读状态, 包括项目名、章节… |
| agents_inspect | 查看当前项目 Agent。mode=list 返回紧凑调度列表; mode=detail 按 agentId 返回… |
| references_inspect | 统一查看可被 Agent 显式引用的资源, 包括创作资料文件和… |
| structure_plan_get_status | 查看当前章节所在批次的结构规划状态。结构规划/细纲是… |
| files_find | 查找当前项目内文件路径。mode=recent 返回最近文件; mode=tree 返回… |
| files_read_text | 分页读取当前项目内某个 UTF-8 文本文件的内容。path 必须是项… |
| prepare_chapter_context | 准备目标章节所需的前文概要、总纲、指定分卷大纲、当… |
| search_project_file | 搜索项目资源, 返回 canonical ref、kind、preview 和 actions, 不返回完整正… |
| web_search | 联网搜索外部公开信息。engine=local 是本地搜索引擎, 适合用… |
| read_web_page | 读取已经确认的指定网页 URL 正文。适合在 web_search 找到重要结… |
| rename_project | 把当前项目名改为正在创作的小说/作品名。当前项目名… |
| workflow_run | 按当前 Agent 工作流启动创作流程。多轮项目按章节推进, 单… |
| files_edit_markdown | 创建或编辑当前项目内的 Markdown 文件。只允许 prompts/ 和 创作资料/ 下的 .md 文件, 可用于 Agent prompt 或项目物料; 可选在保存后强制重跑一个 Agent 一次。 |
| canon_update | (设定更新) |
| structure_plan_apply_direction | 把用户或主编选定的小说结构方向写入当前卷纲和当前批次… |

## Agent 管理类

| 工具 | 描述 |
|---|---|
| agents_edit | 新建、修改、复制或删除自定义 Agent。可设置 Agent 名称、描… |
| agents_update_read_files | 给某个 Agent 增加或移除固定读取文件/目录。operation=add 会追加并… |
| agents_update_input_refs | 用语义化资源引用来设置某个 Agent 显式读取哪些输入。可混… |
| agents_update_schedule | 更新 Agent 工作流调度。operation=set_enabled 启用/禁用单个 Agent; operation=set_order 设… |
| agents_set_final_text_source | 设置哪个 Agent 是正文 Agent。该 Agent 产物会同步到正文目录: 多… |

## 编辑器/发布类

| 工具 | 描述 |
|---|---|
| read_editor_state | 读取当前平台章节编辑页的文字状态, 包括草稿箱、已发… |
| select_editor_chapter | 在当前平台编辑页左侧选择一个章节。通常用于先切到草… |
| fill_editor_chapter | 把当前任务指定的本地章节标题和正文搬进编辑器。正文来自星炉项目文件, 不需要手写正文, 也不要改写正文。 |
| read_page_state | 读取当前发布后台页面的文字、候选作品和可点击元素。 |
| click_element | 点击 read_page_state 返回的可点击元素。只能用于进入作品/书籍管… |
| wait_page | 等待页面加载或用户登录后重新读取页面状态。 |
| finish_binding | 结束作品识别。已经识别到候选作品时必须调用; 如果页… |

## 附: 内置 Agent ID

```
chief_editor               (主编)
chief_editor_chat          (主编聊天)
chief_editor_operation_guard   (操作守卫)
chief_editor_writing_agent     (写作分身)
chief_editor_review_agent      (评审)
loop                       (自定义调度器)
token_meter                (Token 估算)
branch_default             (默认分支)
```
