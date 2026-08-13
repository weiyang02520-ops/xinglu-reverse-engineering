# 00 — UI Audit Summary

> Phase 0 只读逆向审计：从星炉真实发行版 HTML/CSS/renderer JS 静态恢复 UI/UX/Layout/State 规格。
> 本目录全部文档为 clean-room 分析产物，仅记录数值、布局关系、行为语义，不包含第三方代码/资源。

## 审计对象（全部真实运行时资产）

| 文件 | 大小 | 作用 |
|---|---|---|
| `extracted/asar/dist/web/index.html` | 922 行 | 真实入口：主题/缩放/启动面分发 |
| `extracted/asar/dist/web/assets/rendererApp-B0uB3ajR.css` | 698 KB | 桌面全量样式（本审计核心证据） |
| `extracted/asar/dist/web/assets/rendererApp-D0lJ3WIN.js` | 993 KB | 桌面渲染主 bundle |
| `formatted/pretty/rendererApp.pretty.js` | 1.8 MB | 渲染 bundle 美化版 |
| `formatted/pretty/main.pretty.js` | 6.6 MB | Electron 主进程美化版（窗口架构） |
| `formatted/pretty/preload.pretty.cjs` | 25 KB | contextBridge API 面（19 模块完整清单） |
| `formatted/pretty/web-entry.pretty.js` | 9 KB | 启动编排（阶段机） |

辅助：`reports/01-16`（此前逆向报告，标注 [REPORT_CONFIRMED]）、用户真实截图（首页 / 全局设置）。

## 顶层结论（证据汇总）

1. **技术形态** [RUNTIME_CONFIRMED]：Electron 无边框透明主窗口 + React SPA + `WebContentsView` 子视图（chapter-editor / global-overlay 为同一主窗口内层叠视图，非独立 BrowserWindow）+ 1 个隐藏发布窗口 + 1 个隐藏本地 reader 窗口。

2. **设计系统** [RUNTIME_CONFIRMED]：完整的 CSS 变量 token 体系（`--nf-color-*` / `--nf-skin-*` / `--nf-material-*` / `--nf-type-*` / `--nf-radius-*` / `--nf-shadow-*`），暖米白 + 棕褐 accent，light/dark 双主题，interface scale 三级（1 / 1.1 / 1.3）。

3. **主布局** [RUNTIME_CONFIRMED]：`grid-template-columns: 292px 7px minmax(560px,1fr) 7px 380px` + `rows: 44/52px 1fr`。左侧项目栏 292px、中央主区、右侧面板 380px，两侧 7px 拖拽条。

4. **导航** [RUNTIME_CONFIRMED]：无 URL 路由，纯视图状态机；`novelforgeSurface` URL 参数分发 3 个 surface（默认 / chapter-editor / global-overlay）。

5. **工作区双模式** [RUNTIME_CONFIRMED]：`workspaceMode` = `simple`（项目管理/章节列表为主）或 `creative`（多面板停靠/悬浮布局）。

## 关键文件速查

| 主题 | 文档 |
|---|---|
| 完整证据索引 | 01 DESIGN_SYSTEM, 02 APP_SHELL, 15 MULTI_WINDOW, 16 STATE_AND_STORAGE |
| 页面级 | 03-14 |
| 重建映射 | 17 DESKTOP_REBUILD_MAP |
| 未确认项 | 18 UNKNOWN_AND_GAPS |
| 组件类目 | UI_COMPONENT_INVENTORY.md |

## 本阶段验收自评

- 布局 grid、token 数值、窗口行为、IPC 面、存储键：**全部直接证据**（[RUNTIME_CONFIRMED]）
- 视觉细节（毛玻璃、氛围渐变、卡片质感）：直接证据（CSS 原文数值）
- 交互动效（时长/缓动）：部分直接证据（transition 数值），部分 [INFERRED]
- 用户截图与 bundle 一致性：首页与全局设置均与 bundle 结构吻合（见 03 / 13 中的对照说明）

---

# 关键问题回答（13 问）

## 1. 是否已拥有足够证据较精确重建星炉桌面 UI？

**是。** 主布局 grid（292|7|1fr|7|380）、全部设计 token 数值、类族清单、窗口参数、IPC 面、状态键均为 [RUNTIME_CONFIRMED] 直接证据，覆盖重建所需约 80-85%。剩余未知项集中在交互细节与默认布局（见 18，24 项）。

## 2. 哪些页面可以达到高置信度重建？

- **高置信（结构+视觉+状态完整）**：App Shell / 首页布局 / Chat 系统（含 composer、tool-run、能力开关）/ Simple Workspace 树结构 / Creative Workspace dock 体系 / Settings modal / Dialogs（分支、故事摘要）/ 多窗口机制
- 高置信理由：上述区域类族完整（chief 251、chat 192、creative 54 类）+ grid/token 数值直接可考

## 3. 哪些页面仍主要依赖推断？

- Workflow 画布节点排布方向（纵向/流程图）[UNKNOWN]
- Chapter Editor 正文编辑方式 [UNKNOWN]
- Creative dock 默认布局与拖拽转浮窗细节 [INFERRED/UNKNOWN]
- 首页右列 380px 内容 [UNKNOWN]
- 所有精确 modal 尺寸与部分交互触发 [UNKNOWN]

## 4. 用户首页截图与 bundle 是否一致？

**一致。** 截图全部元素（顶部窗口区、左侧项目大卡片、新建按钮、中央总编聊天、搜索、分支入口、设置入口、聊天消息区、底部大型 composer、能力按钮、模型选择、语音、发送）都能在 bundle 类结构与 grid 布局中一一对应，无冲突项。

## 5. 用户全局设置截图与 bundle 是否一致？

**一致。** 截图（工作区保留背景、遮罩、大型圆角 modal、左侧一级导航、顶部/内部二级导航、segmented controls、外观设置、interface scale、light/dark）与 chief-settings-* 类族（shell/backdrop/nav/subtab-indicator/mode-switcher/selection-slider）完全对应。

## 6. SimpleWorkspace 到底是什么结构？

项目+章节管理导向的简化工作区：292px 左栏为**章节分组树**（simple-project-chapter-group → file-row：章节号/标题/字数/动作 + 搜索 + 手写 + 长按菜单），中央/右侧为总编聊天。分组结构通过 `projects:update-chapter-groups` 持久化。

## 7. CreativeWorkspace 到底是什么结构？

**停靠树 + 悬浮窗系统**（`creative-dock-tree-root` flex 容器内递归 split/splitter + docked-panel，加独立 `creative-floating-window` 绝对定位浮窗），窗口种类为项目/素材/聊天/大纲四类，素材内部为文件夹树（creative-folder-* + path-item）。布局持久化 `novelforge.creativeDockLayout` + `novelforge.creativeWorkspaceWindows`。**不是 VS Code 式面板系统**，而是"创作窗口"为单位、可 dock 可悬浮的轻量布局（浮窗最小 280×180，radius 16px）。

## 8. ChapterEditor 如何 dock / float？

Chapter editor 是主窗口内 **WebContentsView**（surface=chapter-editor），呈现由主进程状态机管理：`docked`（set-dock-slot 指定槽位，panelBounds 定位）/ `floating`（set-floating-bounds 实时 + 持久化 nativeFloatingBounds.v1 或 DOM 浮窗 position/size）/ `popover`（锚点弹出）/ `modal`（铺满）。懒创建、透明背景、可见性由主进程控制。

## 9. Chat-first 首页和项目内工作区是什么关系？

同一主布局（nf-window grid）的不同视图态：首页 = 项目列表 + 聊天（右列 380px 未占用 [UNKNOWN]）；选中项目后 workspaceMode 决定 simple（章节树+聊天）或 creative（dock 布局，聊天变为其中一窗 creative-chat-window）。聊天是**贯穿层**：无项目可用（ensure-chat），进入项目后承载项目会话（chat 历史存项目 .novelforge/）。

## 10. Workflow / Agent Node 实际如何呈现？

`workflow-canvas`（主 grid 中央区 grid-area 2/3）内放 **agent-node 卡片**（116px 高、8px 圆角、状态 token 体系：hover/active+ring/done/selected），节点含序号、身份、模型徽章按钮、pill 状态徽章（18px 高、micro 字、font-weight 820）、折叠/配置层；旁挂 `workflow-side-panel`（16px 圆角 shadow-panel）显示 inspector/trace/runtime/章节卡/输出卡/token；运行经 `novelforge:workflow:progress` 事件流驱动节点状态切换。

## 11. 哪些 UI 部分完全不需要进入 AI Novel Studio？

会员体系、客服、官方模型目录、发布助手、移动端桥、官方更新通道、品牌资产（星炉名称/图形/OPPO Sans 字体）。见 17 映射表末节。

## 12. 如果开始 Desktop v0.1，还有没有必须先解决的 UI 信息 blocker？

**有 3 项必须优先补证据（无证据不应实现）**：
1. Creative dock 的**默认布局**（四窗初始位置与比例）
2. **Workflow 画布节点排布方向**与连线绘制
3. **章节编辑器正文编辑形态**（可编辑/只读、输入方式）
次要：首页右列 380px 内容、新建项目表单字段、modal 精确尺寸。
补证手段：更多运行截图（工作区/编辑器/对话框），不执行第三方代码。
