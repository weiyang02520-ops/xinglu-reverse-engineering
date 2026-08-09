# 发布自动化 (Publisher)

> CONFIRMED(平台 URL/命令) — 实现逻辑 RECONSTRUCTED。

## 平台

| ID | 名称 | 后台 URL |
|---|---|---|
| qidian | 起点 | https://write.qq.com/portal/dashboard/books |
| fanqie | 番茄 | https://fanqienovel.com/main/writer/book-manage?enter_from=book_detail |

## 流程

```
1. publisher:open-platform → 隐藏 BrowserWindow 打开作家后台
2. publisher:inspect-platform → AI 读取页面状态(登录/作品列表/草稿箱)
3. publisher:bind-current-project → 绑定当前星炉项目到检测到的作品
   (或 bind-detected-current-project → resolve-binding-choice 处理歧义)
4. publisher:run-draft → 自动把章节填入编辑器 → 保存草稿
   publisher:run-mock → 模拟运行(不真发)
5. publisher:snapshot → 截图留证
```

## AI 工具(发布场景)

- `read_editor_state` — 读编辑器文字状态(草稿箱/已发布内容)
- `select_editor_chapter` — 左侧选择章节
- `fill_editor_chapter` — 把本地章节标题+正文搬运进编辑器(明确禁止改写正文)
- `read_page_state` — 读页面文字/候选项/可点击元素
- `click_element` — 点击可点击元素(仅限进入作品/书籍管理)
- `wait_page` — 等待加载或登录后重读
- `finish_binding` — 结束作品识别(已识别到候选项时必须调用)

## 平台文案识别

内置正则匹配平台 UI 文案以辅助 AI 决策:
- 章节管理类: 作品管理/书籍管理/我的小说/创建作品/创建章节/草稿箱/已发布/未发布/继续创作…
- 数据面板类: 数据中心/收益/互动管理
- 平台名: 起点中文网/番茄小说/QQ阅读/小说阅读网/九天中文网/昆仑中文网/天方听书网/阅文集团…

## 浏览器管理

- 超时: 默认 45s(可配置, 范围 10-90)
- 导航失败重试(ERR_ABORTED 等)
- User-Agent: 桌面浏览器
- 状态管理: open → navigate → inspect → operate → close
