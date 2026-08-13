# UI Component Inventory

> 从真实 CSS 类族恢复的全部可确认组件/类族清单。每项标注类族与计数（CSS 出现次数）。
> 全部 [RUNTIME_CONFIRMED]（直接提取自 rendererApp-B0uB3ajR.css）。

## 1. Shell / Window

| 组件 | 类族 | 计数 | 说明 |
|---|---|---|---|
| 应用窗口 | `.nf-window` | 2 | 主 grid 容器（292\|7\|1fr\|7\|380；44/52px+1fr） |
| 应用外壳 | `.nf-app-shell` | 2 | 圆角裁切外壳 |
| 标题栏 | `.titlebar*` | 9 | 品牌/音乐播放器 |
| 窗口控制 | `--nf-color-window-close/minimize/maximize` | 3 token | 交通灯三色 |
| 启动屏 | `.nf-startup-screen*` / `#nf-static-preloader` | index.html | 书卷图形 + 阶段机 |

## 2. 通用控件

| 组件 | 类族 | 计数 |
|---|---|---|
| 控件高度 token | `--nf-control-height-*` | 6 档（28-38px） |
| 图标尺寸 token | `--nf-icon-size-*` | 2（14/15px） |
| 滚动条 | `--nf-scrollbar-*` | 8 token（10px 宽） |
| 焦点环 | `--nf-shadow-focus` | 3px 主色环 |
| 分段切换 | `.chief-*-switcher` + `.chief-settings-selection-slider` | 5+ |
| 开关 | `.chief-settings-compact-switch` / `.chat-capability-switch*` | 3 |
| 徽章 | `.agent-node-status`（pill）/ `.branch-card__current-pill` | pill 体系 |
| 遮罩 | `.modal-backdrop` | 2（z-index 1/2） |
| toast | `.nf-centered-toast*` / `.nf-corner-toast*` | 4 |

## 3. Home / Project

| 组件 | 类族 | 计数 |
|---|---|---|
| 项目列表 | `.project-list*` | 6 |
| 项目卡片 | `.project-list-item` | 1 |
| 新建项目 | `.project-manager-create-*` / `.project-manager-dialog` / `.project-name-*` | 5 |
| 项目芯片 | `.project-chip` / `.project-select-button` / `.project-delete-button` | 4 |
| 分支按钮 | `.chief-branch-button` | 1 |
| 聊天搜索 | `.chief-chat-search*` | 3 |

## 4. Chat

| 组件 | 类族 | 计数 |
|---|---|---|
| 聊天头 | `.chief-header*` | 4 |
| 消息 | `.chat-message*` | 158 |
| 线程 | `.chat-thread*` | 14 |
| 历史 | `.chat-history*` | 7 |
| 工具运行 | `.chat-tool-run-*` | 66（body/details/divider/interjection/progress-*） |
| 附件 | `.chat-attachment-*` | 16（audio/image/file/icon/copy/remove/expanded/error/thumb/list） |
| 音频 | `.chat-audio-*` | 15（player/lyrics/candidate/preview/unavailable） |
| 图片 | `.chat-image-*` | 14（grid-choice/lightbox/download） |
| 文件 | `.chat-file-*` / `.chat-chapter-*` | 12（link/edit-chip/selection-popover） |
| 能力 | `.chat-capability-*` | 5（controls/switch/track/toggle） |
| Composer | `.chat-composer*` | 2（+toolbar） |
| 上下文菜单 | `.chat-context-menu*` | 2 |
| 媒体生成 | `.chat-media-generation-status` | 1 |
| 外部链接 | `.chat-external-url-link` | 1 |

## 5. Simple Workspace

| 组件 | 类族 | 计数 |
|---|---|---|
| 容器 | `.simple-workspace` / `.simple-project-*` | 55+ |
| 章节分组 | `.simple-project-chapter-group*` | 10（header/content/create/empty/toggle/editing） |
| 章节文件 | `.simple-project-chapter-file*` | 15（row/main/number/title/count/actions/select/separator/trailing） |
| 搜索 | `.simple-project-chapter-search` | 1 |
| 手写 | `.simple-project-chapter-handwrite` | 1 |
| 长按 | `.simple-project-chapter-long-press-hint` | 1 |
| 标记 | `.simple-project-active-mark` | 1 |

## 6. Creative Workspace

| 组件 | 类族 | 计数 |
|---|---|---|
| 停靠树 | `.creative-dock-tree-*` | 4（root/split/splitter） |
| 停靠面板 | `.creative-docked-panel*` | 5（header/body/grip/title） |
| 浮窗 | `.creative-window-*` | 12（titlebar/title/meta/header-action/grip/resize-handle/layer/scroll/body/empty） |
| 浮窗容器 | `.creative-floating-window` | 1 |
| 文件夹 | `.creative-folder-*` | 13（list/group/body/create/delete/toggle/organize/search） |
| 路径 | `.creative-path-*` | 8（item/list/root/open/delete/org-lock） |
| 项目窗 | `.creative-project-*` | 2 |
| 素材窗 | `.creative-material-*` | 2 |
| 聊天窗 | `.creative-chat-window` | 1 |
| 大纲窗 | `.creative-outline-folder-list` | 1 |
| 把手 | `.creative-grip-*` | 2 |
| 滚动区 | `.creative-scroll-area` | 1 |

## 7. Chapter Editor

| 组件 | 类族 | 计数 |
|---|---|---|
| 视图根 | `.chapter-editor-view-root` | 1 |
| 拖拽条 | `.chapter-editor-view-window-drag-strip` | 1 |
| Dock 宿主 | `.chapter-editor-dock-host` | 1 |
| 行 | `.chapter-editor-row` | 1 |
| 标题 | `.chapter-editor-title` / `-input` | 2 |
| 查找替换 | `.chapter-editor-search-*` | 4（replace/group/count/clear） |
| 面板 | `.chapter-editor-panel` | 1 |

## 8. Materials

| 组件 | 类族 | 计数 |
|---|---|---|
| 文件卡 | `.material-file-*` | 4（card/top/title/references） |
| 编辑器 | `.material-editor-*` | 8（dialog/form/title/summary/body/outline-identity/limit-status/state/user-note） |
| 导入 | `.material-import-button` / `.material-folder-button` / `.material-open-button` / `.material-delete-button` | 4 |
| 维护者 | `.material-maintainer-label` | 1 |

## 9. Outline

| 组件 | 类族 | 计数 |
|---|---|---|
| 大纲窗 | `.creative-outline-folder-list` / `.outline-*`（main-group/group/identity/folder-list） | 6 |

## 10. Workflow / Agent

| 组件 | 类族 | 计数 |
|---|---|---|
| 画布 | `.workflow-canvas` / `.workflow-map` / `.workflow-arrow` | 3 |
| 侧面板 | `.workflow-side-panel*` | 4（header/agent） |
| 运行 | `.workflow-run-button` / `.workflow-side-action-button*` | 3 |
| 密度 | `.workflow-density-toggle` | 1 |
| 图例 | `.workflow-legend-items` | 1 |
| 章节/输出卡 | `.workflow-chapter-card` / `.workflow-output-card` / `.workflow-panel-section*` / `.workflow-panel-token` | 6 |
| Agent 节点 | `.agent-node*` | 20（main/identity/title/index/status/model-button/model-summary/collapse/expand/config-*） |
| 检视器 | `.agent-inspector-*` | 2（panel/body） |
| 追踪 | `.agent-trace-panel` / `.agent-runtime-panel` | 2 |
| Agent 对话框 | `.agent-dialog` / `.agent-provider-dialog` / `.agent-provider-option` / `.agent-provider-api-fields` | 4 |
| 空态 | `.agent-empty-state` / `.agent-dot` | 2 |

## 11. Model Library

| 组件 | 类族 | 计数 |
|---|---|---|
| 列表 | `.model-library-list*` / `.model-library-item*` | 12（heading/actions/item-actions/icon/copy/select/edit/delete/add-toggle/fetch/advanced/empty） |

## 12. Settings

| 组件 | 类族 | 计数 |
|---|---|---|
| 外壳 | `.chief-settings-shell` / `-backdrop` / `-nav` / `-nav-title` / `-content` / `-main` | 7 |
| 子页 | `.chief-settings-subtab-indicator` / `-subdialog*` | 3 |
| 行 | `.chief-settings-item*` / `-mode-row` / `-selection-slider` / `-control` | 8 |
| 分区 | `.chief-appearance-*` / `-general-*` / `-generation-*` / `-feedback-*` / `-membership-*` / `-invite-*` / `-avatar-*` / `-about-*` | 30+ |
| 按钮 | `.chief-settings-action-button*` / `-button` | 3（+danger/muted） |

## 13. Dialogs

| 组件 | 类族 | 计数 |
|---|---|---|
| 分支 | `.branch-dialog*` / `.branch-card*` / `.branch-strategy-*` | 30 |
| 故事摘要 | `.story-summary-*` | 7（editor-dialog/form/field/mode-options/mode-slider/auto-update-card） |
| 输入清晰度 | `.input-clarity-*` / `--nf-input-clarity-skeleton-*` | 3 |
| 通用 | `.modal-backdrop` / `confirm-dialog` / `text-input-dialog` | 3 |

## 14. 其它业务类族

| 类族 | 计数 | 说明 |
|---|---|---|
| `--nf-color-*` | 34 token | 语义色 |
| `--nf-skin-*` | 44 token | 皮肤 |
| `--nf-material-*` | 12 token | 材质 |
| `--nf-type-*` | 15 token | 字号 |
| `--nf-radius-*` | 6 token | 圆角 |
| `--nf-shadow-*` | 8 token | 阴影 |
| `publisher-*` | 14 | 发布助手（不重建） |
| `chief-membership-*` | 30+ | 会员（不重建） |
| `chief-invite-*` | 10+ | 邀请（不重建） |
| `chief-support-*` | 3 | 客服（不重建） |
| `chief-skills-*` | 3 | 技能（可选） |

> 注：计数为类名前缀匹配次数（含组合选择器重复引用），非唯一类数量。
