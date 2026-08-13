# 18 — Unknown and Gaps

> 当前无法确认、或仅有推断证据的项。明确禁止：对 UNKNOWN 自行设计"现代 UI"。
> 需要新证据来源：更多运行截图 / 进一步静态分析 / 行为测试（不执行第三方代码的前提下可观察）。

## 一、结构性 UNKNOWN（影响重建完整性）

| # | 项目 | 影响 | 现有证据 |
|---|---|---|---|
| 1 | 首页右列 380px 是否可见、内容为何 | 首页布局完整性 | 截图未覆盖 [UNKNOWN]；grid 列存在 [RUNTIME_CONFIRMED] |
| 2 | 项目卡片 72px 动作区按钮清单 | ProjectList 交互 | [UNKNOWN] |
| 3 | 新建项目对话框字段（写作预设/类型？） | Onboarding 流程 | project-manager-create-form 类存在 [RUNTIME_CONFIRMED]，字段 [UNKNOWN] |
| 4 | 聊天消息气泡布局（用户/总编是否分侧、对齐） | Chat 视觉 | [UNKNOWN] |
| 5 | Creative dock 默认布局（每面板初始位置/尺寸） | CreativeWorkspace 默认态 | [UNKNOWN] |
| 6 | dock 拖拽转浮窗的具体触发与动画 | 交互细节 | 类体系存在 [RUNTIME_CONFIRMED]，行为 [INFERRED] |
| 7 | 章节编辑器正文编辑方式（contenteditable/textarea/只读） | ChapterEditor 实现 | [UNKNOWN] |
| 8 | workflow-canvas 节点排布方向（纵向列表/流程图）与连线绘制 | Workflow 视觉 | 类存在 [RUNTIME_CONFIRMED]，布局方向 [UNKNOWN] |
| 9 | 节点→inspector 的打开交互 | 交互 | [INFERRED]（点节点/按钮） |
| 10 | 一级导航项完整清单（全局设置） | Settings 完整性 | 分区类族 [RUNTIME_CONFIRMED]，导航项集合 [UNKNOWN] |
| 11 | modal 对话框精确尺寸（宽高） | Dialogs | 截图有全局设置全貌 [SCREENSHOT_CONFIRMED]，精确 px [UNKNOWN] |
| 12 | 章节分组树精确行高/缩进 | SimpleWorkspace | [UNKNOWN] |

## 二、数值类 UNKNOWN（可用截图推断但未精确测量）

| 项 | 说明 |
|---|---|
| titlebar 控件（交通灯）的位置/间距 | token 有色值 [RUNTIME_CONFIRMED]，布局 [UNKNOWN] |
| 音乐播放器（titlebar 内）的形态 | 类族存在 [RUNTIME_CONFIRMED]，布局 [UNKNOWN] |
| 各对话框 padding/内部间距 | token 体系可推导，具体规则 [UNKNOWN] |
| 聊天消息间距/头像尺寸 | [UNKNOWN] |
| 启动图形动画细节 | 图形在 index.html [RUNTIME_CONFIRMED]，动画参数 [UNKNOWN] |

## 三、行为类 UNKNOWN

| 项 | 说明 |
|---|---|
| 键盘快捷键全集 | 仅 composer 相关推断 [INFERRED] |
| 拖拽排序细节（章节/文件夹） | [INFERRED] |
| 工具运行卡片的展开/折叠交互 | 类存在 [RUNTIME_CONFIRMED]，交互 [INFERRED] |
| 语音输入流程 | 位置持久化存在 [RUNTIME_CONFIRMED]，流程 [UNKNOWN] |
| 输入清晰度改写流程（触发条件） | IPC 存在 [RUNTIME_CONFIRMED]，触发 [UNKNOWN] |

## 四、无法从静态 bundle 获取、需运行时观察的

1. **动效细节**：dock 重组动画、面板切换过渡、节点状态变化的动画时长序列
2. **焦点/键盘导航顺序**
3. **拖拽的真实约束**（dock 分割比例最小/最大）
4. **多显示器/DPI 行为**
5. **全局悬浮层的实际使用场景**（何种操作触发 popover/modal）
6. **发布窗口 UI**（隐藏窗口，无渲染证据）

## 五、对重建的建议（记录，不执行）

- 第一优先级补证据：**更多用户截图**（工作区两种模式、章节编辑器、分支对话框、模型库、大纲）
- 静态可补：对 rendererApp.pretty.js 中 chat/creative 相关组件做定向字符串聚类（进一步细分函数边界）
- 若截图仍无法覆盖：对 UNKNOWN 项在重建文档中显式标注"占位实现"，不做主观补全

## 六、证据等级统计

- [RUNTIME_CONFIRMED]：布局 grid、全部 token 数值、类族清单、窗口参数、IPC 面、状态键——**覆盖重建所需 80%+**
- [SCREENSHOT_CONFIRMED]：首页、全局设置（与 bundle 吻合，无冲突）
- [INFERRED]：部分交互细节（已逐项标注）
- [UNKNOWN]：见上表 24 项
