# 16 — 软件整体架构报告 (Architecture)

> 目标: 让没读过项目的人也能理解星炉(XingLu)如何运行。

## 1. 一句话架构

星炉是一个 **Electron 桌面应用**: 前端是 React 单页应用, 通过 preload 暴露的 IPC 桥调用主进程; 主进程持有全部业务逻辑(项目文件系统、AI 模型调度、本地 HTTP 服务器), 所有网络请求只在主进程发出。移动端是配套的 Capacitor PWA, 通过局域网 HTTP 桥连接桌面端协同工作。

## 2. 进程模型

```mermaid
graph TB
    subgraph 桌面端[Electron 进程]
        R1[渲染进程: 主窗口<br/>React SPA web/]
        R2[渲染进程: 章节编辑器<br/>surface=chapter-editor]
        R3[渲染进程: 全局悬浮层<br/>surface=global-overlay]
        P[preload.cjs<br/>contextBridge]
        M[主进程 main.js<br/>esbuild bundle 4.2MB]
        PUB[隐藏浏览器窗口<br/>发布平台自动化]
    end
    subgraph 移动端[手机]
        APP[Capacitor WebView<br/>PWA mobile/]
    end
    subgraph 外部[外部世界]
        API[api.xushilu.cn<br/>账号/会员/模型/客服]
        LLM[a6api/vectorengine<br/>LLM 中转]
        SEARCH[Serper/智谱/博查<br/>搜索]
        MEDIA[Suno/可灵/OpenAI<br/>多媒体]
        UPDATE[download.xushilu.cn<br/>更新/APK]
        PLAT[起点/番茄<br/>发布平台]
    end
    R1 --> P
    R2 --> P
    R3 --> P
    P -->|IPC 150 通道| M
    M -->|HTTP 本地桥 8787| APP
    M -->|fetch| API
    M -->|fetch| LLM
    M -->|fetch| SEARCH
    M -->|fetch| MEDIA
    M -->|autoUpdater| UPDATE
    PUB -->|隐藏浏览器| PLAT
```

## 3. 启动流程

```mermaid
sequenceDiagram
    participant M as 主进程
    participant P as preload
    participant R as 渲染进程
    participant U as 用户
    U->>M: 启动 XingLu.exe
    M->>M: 创建工作区窗口(web/index.html)
    M->>P: 注入 preload
    P->>R: 准备, 检测静态加载器
    P->>M: novelforge:window:static-loader-ready
    M->>P: static-loader-paint-request
    P->>R: 触发启动画面绘制
    R->>R: 启动阶段: ignite→workspace→project→ready
    R->>R: mountRendererApp(surface) 挂载 React
    R->>M: startup-renderer-prepared
    M->>R: 初始应用数据(项目列表/会话)
    R->>M: startup-initial-app-data-ready
    M->>R: window:shown + fade-in
    R->>U: 工作台显示
```

## 4. 用户操作流(以"让主编写一章"为例)

```mermaid
sequenceDiagram
    participant U as 用户
    participant R as 渲染进程(React)
    participant P as preload
    participant M as 主进程
    participant A as AI 模型
    U->>R: 点击"开始写作"或输入指令
    R->>P: window.novelforge.chiefEditor.run({brief, chapterNumber})
    P->>M: ipcRenderer.invoke("novelforge:chief-editor:run")
    M->>M: T7 工作流: 读取项目/Agent 注册表
    loop 每章
        M->>M: 规划(细纲/卷纲检查) → 断点续写判断
        M->>M: 按注册表顺序调度每个 Agent
        M->>A: 组装 prompt(项目文件+创作资料+前文) → LLM 调用
        A-->>M: 流式生成/工具调用
        M->>M: 工具执行(写文件/读文件/搜索/生成媒体)
        M->>R: workflow:progress 进度事件
        M->>M: 写入 chapters/chXXX/{agent}.md
    end
    M-->>R: run 完成(对话结果)
    R->>U: 显示章节/聊天回复
```

## 5. 网络层架构

```
所有网络请求只在主进程
├── 官方 API 封装 gEe(): POST/GET + Bearer token + ok 校验
│     api.xushilu.cn (备用 119.45.39.251)
├── LLM 客户端(多提供商)
│     OpenAI 兼容(chat/completions) | Anthropic | Gemini
│     + 适配器层(kdt): 按模型 ID 自动选择参数(thinking/effort/max_tokens)
│     + 401 自动刷新 API Key
├── 搜索网关
│     Serper / 智谱 / 博查 / 统一网关(v1/search)
├── 媒体生成
│     OpenAI 图像 / Suno 音乐 / 可灵视频(任务轮询)
├── 本地 HTTP 服务器(mobile bridge)
│     /bridge 命令 + SSE 事件 + 媒体 + APK 分发
└── 更新服务 electron-updater
```

## 6. 数据流全景

```mermaid
graph LR
    subgraph 持久化[持久化]
        WS[workspace/projects/<br/>文件系统项目]
        UD[userData/ JSON 配置]
        LS[localStorage UI 状态]
    end
    subgraph 主进程[主进程]
        PM[项目管理器]
        CM[聊天/会话]
        WM[工作流引擎]
        MM[模型管理器]
        MB[Mobile Bridge]
    end
    subgraph 渲染[渲染层]
        RV[React 视图]
        ST[状态/Context]
    end
    RV -->|IPC| PM
    RV -->|IPC| CM
    RV -->|IPC| WM
    RV -->|IPC| MM
    RV -->|HTTP| MB
    PM --> WS
    CM --> UD
    MM --> UD
    RV --> LS
    PM --> CM
    WM --> PM
    MM --> WM
```

## 7. 移动端协同

```mermaid
sequenceDiagram
    participant PH as 手机(PWA)
    participant MB as 桌面 HTTP 桥
    participant M as 主进程
    PH->>MB: GET /mobile/connect (配对密钥)
    MB-->>PH: {ok, protocolVersion, urls}
    PH->>MB: POST /bridge {id, protocolVersion, command, input}
    MB->>M: 分发到项目/聊天/章节处理器
    M-->>MB: {id, kind:"response", ok, output}
    M-->>PH: SSE /bridge/events (聊天流式/状态推送)
    PH->>MB: GET /bridge/media (素材读取)
    PH->>MB: GET /mobile/android.apk (下载安装)
```

## 8. 安全边界

- 渲染进程**无直接网络/文件权限**(sandbox), 全部经 IPC
- preload 只暴露白名单 API(contextBridge)
- mobile bridge 用配对密钥(18 字节随机, base64url)鉴权
- 项目文件按工作区根目录隔离(projects/ 布局)
- 无自研原生代码, 无系统级提权

## 9. 启动/更新/发布附加组件

- 启动: NSIS 安装器(7z 解压) → Electron → app.asar
- 更新: electron-updater (generic provider, download.xushilu.cn)
- 发布: 隐藏 BrowserWindow + AI 工具(读页面/点击/填充)
- 图像处理: sharp (libvips)
- Office 文档: mammoth/jszip 内嵌(docx 提取)
