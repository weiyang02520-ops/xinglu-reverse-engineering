# 02 — App Shell

> 应用外壳：主窗口结构、启动流程、三个 surface 的关系。

## 1. 顶层窗口结构 [RUNTIME_CONFIRMED]

```
Electron 主窗口（无边框、透明底、圆角）
└── contentView
    ├── [WebContentsView] global-overlay（surface=global-overlay，透明，层叠在上层）
    └── [WebContentsView] chapter-editor（surface=chapter-editor，透明，层叠）
    └── 主页面（surface=默认）
```

- 三个 surface 共享同一个 `web/index.html` + 同一 renderer bundle，由 URL 参数 `novelforgeSurface` 分发 [RUNTIME_CONFIRMED]（web-entry.pretty.js 第 313-320 行）
- 主窗口参数 [RUNTIME_CONFIRMED]（main.pretty.js yX 函数）：
  - `frame: false`（自绘标题栏）、`autoHideMenuBar: true`、`show: false`（加载完成后显示）
  - `minWidth: 1100`、`minHeight: 720`
  - `backgroundColor: "#fffdf8"`（light 暖白）；win32：`backgroundMaterial: "none"` + `opacity: 0`；非 win32：`transparent: true`
  - `roundedCorners: true`
  - 位置/大小持久化：`userData/window_state.json`（`{x, y, width, height, isMaximized, savedAt}`）
  - 默认尺寸夹紧：宽 `min(1280, max(900, saved))`、高 `min(900, max(720, saved))`；默认 `1280×900`
- 窗口级 CSS 圆角：`--nf-app-window-radius: 8px`，`clip-path: inset(0 round 8px)` 裁切内容

## 2. 主布局 Grid [RUNTIME_CONFIRMED]

`.nf-window` 是应用主容器（`display:grid`）：

```
┌────────────────────────────────────────────────────────────┐
│ titlebar                    rows: 44px（light）/ 52px（dark）  │
├──────────┬────┬──────────────────────┬────┬────────────────┤
│ 项目栏     │ 7px │  中央主区              │ 7px │  右侧面板       │
│ 292px    │ 拖  │  minmax(560px,1fr)   │ 拖  │  380px         │
│          │ 拽  │                      │ 拽  │                │
│          │    │                      │    │                │
└──────────┴────┴──────────────────────┴────┴────────────────┘
   col 1      col 2    col 3             col 4    col 5
```

- 列模板：`292px 7px minmax(560px,1fr) 7px 380px`
- 行模板：`44px 1fr`（light）→ `52px 1fr`（dark 覆盖）
- 7px 列为面板分隔条（resizer）；`--nf-skin-resizer` 色值（light `#efe7df` / dark `#fff4e812`），thumb `--nf-skin-resizer-thumb`
- 背景：`backdrop-filter: blur(18px) saturate(1.08)` 毛玻璃 + 三个氛围 radial-gradient（cool 青灰 / warm 暖橙 / paper 纸白）+ 顶部内高光 `inset 0 1px #fffefabd`
- 中央主区 `minmax(560px, 1fr)`：约 560px 是主区最小宽度（1200-292-380-14 = 514？实际 560 由 token 直接给出）

## 3. Titlebar [RUNTIME_CONFIRMED]

类：`.titlebar` / `.titlebar-leading` / `.titlebar-brand-mark` / `.titlebar-brand-copy` / `.titlebar-music-player`（+music-player-button/progress/time/title）

- 左侧：品牌 mark（logo 图形）+ brand copy
- 右侧/中部：内嵌音乐播放器（迷你播放器，标题/进度/时间）
- 高度 44/52px；无系统边框（frame:false），自绘控制按钮（关闭/最小化/最大化，macOS 交通灯三色：红 `#f97066` / 黄 `#f5c04f` / 绿 `#55c27a`）[RUNTIME_CONFIRMED - window-close/minimize/maximize token]

## 4. 启动流程 [RUNTIME_CONFIRMED]

```
静态加载器（index.html 内联 SVG 书卷图形 + 品牌 + 旅程进度 + 状态文本）
  │  phase 状态机（web-entry.pretty.js）:
  │    ignite   （0-1.5s）   状态文案「点亮星炉」
  │    workspace（1.5-3.5s） 「正在整理创作工作台」
  │    project  （3.5-5s）    「正在接续《书名》」/「正在接续上次创作」
  │    ready    （≥5s 或数据就绪）「工作台准备就绪」
  ▼
React 挂载（mountRendererApp(surface)）
  │  startup-renderer-prepared → startup-initial-app-data-ready
  ▼
窗口 shown → fade-in（360ms, cubic-bezier(.2,.8,.2,1)）→ 显示工作台
```

- 静态加载器 DOM：`#nf-static-preloader`（z-index 10001）+ `.startup-react-screen`（z-index 10000，radius 18px fallback）
- 启动参数：`novelforgeSurface`（chapter-editor / global-overlay → 不显示静态加载器）、`novelforgeDualViewChapterEditor=1`（双视图章节编辑器标记）
- 计时刻度：1500ms / 3500ms / 5000ms（阶段阈值）

## 5. Surface 分发逻辑 [RUNTIME_CONFIRMED]

| surface | 进入方式 | 内容 |
|---|---|---|
| 默认 | 主窗口加载 | 主应用（项目列表 / simple / creative 工作区） |
| chapter-editor | 主进程懒创建 WebContentsView，加载时注入参数 | 章节编辑器 |
| global-overlay | 同上 | 全局悬浮会话（agent 运行悬浮层 / popover） |

- 两个子视图延迟创建（setTimeout 懒加载），`setBounds(全窗口)`、`setVisible(false)` 先隐藏，`did-finish-load` 后按需显示
- 子视图背景 `#00000000`（透明），显示时 `invalidate()` 重绘
- 呈现模式状态机：`docked / floating / popover / modal`（详见 08 / 14 / 15）
- 关闭主窗口 → 托盘驻留（提示"关闭窗口后，星炉会继续在右下角运行"），托盘菜单：打开主窗口 / 退出创作

## 6. 缩放（Interface Scale）[RUNTIME_CONFIRMED]

- `novelforge.interfaceScale.v1`：normal / medium / large → 缩放因子 1 / 1.1 / 1.3
- 实现：优先 `webFrame.setZoomFactor`（Electron），否则 `documentElement.style.zoom`
- `index.html` 启动脚本在 React 挂载前应用（避免闪烁）

## 7. 主题（Theme）[RUNTIME_CONFIRMED]

- `novelforge.appearanceTheme.v1`：light / dark
- `document.documentElement.dataset.theme` 在 HTML 加载早期脚本设置（防闪烁）
- 深色下窗口 titlebar 高 52px（44→52），氛围层与 shadow 全部切换（见 01）

## 8. Evidence

- 窗口参数 / WebContentsView / 托盘 / window_state：main.pretty.js [RUNTIME_CONFIRMED]
- Grid 布局 / 毛玻璃 / 圆角：CSS .nf-window / .nf-app-shell [RUNTIME_CONFIRMED]
- 启动阶段机 / surface 分发：web-entry.pretty.js [RUNTIME_CONFIRMED]
- 截图对照：首页截图顶栏区域与 titlebar 结构吻合 [SCREENSHOT_CONFIRMED]
