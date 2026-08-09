# 04 — 前端入口分析报告 (Frontend Entry)

## 1. 桌面端 (web/)

```
web/index.html (27.8KB)
├── <script> 内联启动脚本 (主题/缩放初始化)
│     storage keys: novelforge.appearanceTheme.v1, novelforge.interfaceScale.v1
│     URL 参数: novelforgeSurface (chapter-editor | global-overlay)
├── ./assets/index-CvAAoCbC.js  (6.7KB, Vite entry loader)
│     ├── 预加载 ./rendererApp-D0lJ3WIN.js  (993KB, 主应用)
│     └── 预加载 ./rendererApp-B0uB3ajR.css  (698KB)
└── <div id="root"> (React 挂载点)
```

### index-CvAAoCbC.js (启动加载器)
- 功能: modulepreload 优化 + 启动序列协调
- **启动阶段**: ignite(点亮星炉) → workspace(正在整理创作工作台) → project(正在接续《书名》) → ready(工作台准备就绪)
- 监听事件: `novelforge:startup-window-shown`, `novelforge:startup-window-fade-in-complete`, `novelforge:startup-renderer-prepared`, `novelforge:startup-initial-app-data-ready`
- surface 检测: `novelforgeSurface` 参数 → 章节编辑器(chapter-editor) / 全局悬浮层(global-overlay) / 主窗口(默认)

### rendererApp-D0lJ3WIN.js (主应用)
```
mountRendererApp(surface)
└── React StrictMode → createRoot(#root)
    ├── surface="chapter-editor" → 章节编辑器组件 (浮窗模式)
    ├── surface="global-overlay" → 全局悬浮层组件 (agent 会话/窗口选择器)
    └── 默认 → 主应用: Provider(Kr) → Layout(Sd) → Main(Td)
            ├── v_ (全局删除确认/会话处理)
            └── B_ (主工作区: 项目/章节/对话)
```

## 2. 移动端 (mobile/)

```
mobile/index.html (894B)  — 星炉万象文新手机端
├── ./assets/index-D-s4yRj5.js  (480KB)
├── ./assets/index-BI4wBiTZ.css  (77KB)
├── manifest.webmanifest (PWA)
└── sw.js — Service Worker (cache: novelforge-mobile-shell-v3)
      特别排除: /bridge, /bridge/* (桌面端桥接 API 不走缓存)
```

## 3. 多窗口架构 [CONFIRMED]

| 窗口 | 载体 | 用途 |
|---|---|---|
| 主窗口 | web/index.html (默认 surface) | 主工作区 |
| 章节编辑器 | web/index.html?novelforgeSurface=chapter-editor | 浮窗/停靠章节编辑器 |
| 全局悬浮层 | web/index.html?novelforgeSurface=global-overlay | agent 会话悬浮窗口 |
| 发布浏览器 | 隐藏 BrowserWindow (loadURL 外部站点) | 自动发布到小说平台 |
| 静态启动窗 | nf-static-preloader 元素 | 启动画面 (preload.cjs 管理) |

## 4. 启动序列 (preload.cjs + entry loader)

1. 渲染进程加载 → preload 检查 `nf-static-preloader` → 通知主进程 `novelforge:window:static-loader-ready`
2. 主进程调度 → 发送 `novelforge:window:static-loader-paint-request` → preload 触发绘制
3. 启动阶段推进: ignite → workspace → project → ready (index.html 内联脚本)
4. `mountRendererApp(surface)` 挂载 React → 报告 `novelforge:startup-renderer-prepared`
5. 初始数据就绪 → `novelforge:startup-initial-app-data-ready`
6. 淡入完成 → 主进程显示窗口
