# 17 — Desktop Rebuild Map

> XingLu 可观察 UI → 未来 AI Novel Studio Desktop 组件映射。
> 只做映射，不写代码、不决定业务逻辑。数值/结构可复用（clean-room），品牌资产/代码不复制。

## 映射表

| # | XingLu observable UI | AI Novel Studio 对应组件 | 复用内容（clean-room 允许） | 不复用（第三方资产） |
|---|---|---|---|---|
| 1 | 无边框透明主窗口 + 自绘 titlebar | 主窗口 shell | frame:false、min 1100×720、自绘标题栏、窗口状态持久化 | — |
| 2 | 三 surface（默认 / chapter-editor / global-overlay） | 主 surface + 编辑器 surface + 悬浮 surface | surface URL 分发、WebContentsView 层叠、懒加载 | — |
| 3 | nf-window grid（292\|7\|1fr\|7\|380） | 主布局 grid | 列宽/行高/毛玻璃/氛围渐变数值 | — |
| 4 | 项目列表大卡片 | ProjectList | 卡片 grid、max-height、间距、hover | — |
| 5 | 总编聊天（Chief Chat） | Chief Chat | 消息类型集、tool-run 卡、composer 结构、能力开关组、历史加载、删除确认 | — |
| 6 | Chat Composer | ChatComposer | 20px 圆角、内高光、toolbar 34px 缩进、能力开关、模型选择、语音、发送/停止 | — |
| 7 | Simple Workspace | SimpleWorkspace | 章节分组树、搜索、手写、长按菜单、active-mark | — |
| 8 | Creative Workspace（dock tree + floating windows） | CreativeWorkspace | dock-tree-root/split/splitter、docked-panel、floating-window（280×180 min）、folder 树、持久化键 | — |
| 9 | 章节编辑器 surface（docked/floating/popover/modal） | ChapterEditor | 呈现状态机、dock 槽位、浮窗几何持久化、字号持久化、查找替换 | — |
| 10 | 素材库（folder 树 + 编辑对话框） | Materials | 文件夹组织、导入、整理锁、编辑器表单（标题/摘要/正文/身份/限制/备注） | — |
| 11 | 大纲管理（方向建议） | OutlineManager | 状态检查、方向生成/应用流程 | — |
| 12 | Workflow / Agent Node | WorkflowView | agent-node 116px 卡、状态 token 系（hover/active/done/selected）、pill 徽章、侧面板、运行按钮、token 统计 | — |
| 13 | Agent Inspector / Trace | AgentInspector | 检视面板、trace 面板、模型徽章按钮、provider 对话框 | — |
| 14 | Model Library | ModelLibrary | 56px 项卡、provider 表单、目录刷新、选择/删除 | — |
| 15 | Chief Settings（modal + 左导航 + 子 tab + segmented） | SettingsModal | 遮罩保留背景、16px 圆角、selection-slider、subtab-indicator、外观/缩放切换 | — |
| 16 | 分支对话框 | BranchDialog | tabs、card list、current-pill、重命名表单、策略 radio | — |
| 17 | 故事摘要 | StorySummaryDialog | 编辑表单、模式滑块、自动更新开关 | — |
| 18 | 对话框体系 | DialogSystem | modal/popover 呈现模型、backdrop 层级、通用确认/输入 | — |
| 19 | 全局悬浮层（agent 会话 popover） | GlobalOverlay | content-size 上报、popover 定位、会话切换 | — |
| 20 | 启动加载器（阶段机） | StartupScreen | ignite→workspace→project→ready、静态加载器→React 挂载→fade-in | 星炉品牌图形/文字/字体 |
| 21 | 设计 token 体系 | DesignTokens | 全部 --nf-* 数值（颜色/radius/shadow/type/control-height/scrollbar/easing） | — |
| 22 | 主题/缩放 | ThemeAndScale | data-theme 切换、1/1.1/1.3 缩放、themeStorageKey 机制 | — |
| 23 | 会员/邀请/客服/发布 | （AI Novel Studio 无此业务 → 不实现） | — | — |

## 不做映射的部分（不需要进入 AI Novel Studio）

- **会员体系**（chief-membership-*：账户/套餐/订单/支付/激活码/邀请）——依赖官方账号服务
- **客服**（chief-support-* / support IPC）——依赖官方后端
- **官方模型目录**（official-models:get-catalog / usage-balance）——AI Novel Studio 用自带 Provider 配置（openai_compatible），见核心 config
- **发布助手**（publisher:* 平台自动化）——超出创作本体
- **移动端桥**（mobile-bridge / APK）——Desktop 阶段不做
- **更新服务**（app-update 官方通道）
- **品牌资产**（星炉名称/logo/启动图形/OPPO Sans 字体）

## 替换对应关系（未来 Agent 体系）

| XingLu | AI Novel Studio 现有对应 |
|---|---|
| Chief Editor（总编） | Chief（现有 core/agents） |
| Writer agent node | Writer（现有） |
| Reviewer 审阅 | Reviewer（现有） |
| agent-node 工作流图 | 未来以 Chief/Writer/Reviewer 三节点呈现 |

> 不做替换方案设计，仅记录对应关系（任务边界：只恢复星炉真实行为）。

## 重建优先级建议（仅映射，非实现）

1. P0 结构层：DesignTokens / AppShell / 主布局 grid / 启动流程 / 三 surface 架构
2. P1 交互层：Chat（composer + tool-run + 能力开关）/ Simple & Creative workspace / 章节编辑器呈现状态机
3. P2 管理面：Settings modal / ModelLibrary / Materials / Outline / BranchDialog
4. P3 可视化：WorkflowView / AgentInspector / Trace
