# 架构摘要

> 完整分析见 `../reports/16_ARCHITECTURE.md`。

## 进程模型

```
Electron (XingLu.exe)
├── 主进程 main.js (esbuild ESM bundle, 4.2MB)
│   ├── 150 个 IPC handler
│   ├── 项目文件系统管理
│   ├── AI 工作流引擎 (T7)
│   ├── LLM/搜索/媒体客户端
│   ├── Mobile Bridge HTTP 服务器 (8787/8891-8999)
│   ├── 发布自动化 (隐藏 BrowserWindow)
│   └── electron-updater
├── preload.cjs → window.novelforge (contextBridge)
└── 渲染进程 (React SPA)
    ├── 主窗口 (web/index.html)
    ├── 章节编辑器窗口 (surface=chapter-editor)
    └── 全局悬浮层 (surface=global-overlay)
```

## 关键设计

1. **渲染器零网络**: 所有网络请求只在主进程, 渲染器只通过 `window.novelforge.*` 调用。
2. **无数据库**: 项目 = 文件系统目录(`projects/{id}/`), 配置 = userData JSON, UI 状态 = localStorage。
3. **AI 多提供商**: 文本(OpenAI 兼容/Anthropic/Gemini) + 图像(OpenAI) + 音乐(Suno) + 视频(可灵) + 搜索(Serper/智谱/博查)。
4. **模型适配器**: 按模型 ID 自动切换参数(thinking/reasoning_effort/max_tokens)。
5. **手机协同**: 局域网 HTTP 桥(JSON-RPC 风格命令 + SSE 事件), 配对密钥鉴权。
6. **自动发布**: AI 通过工具(读页面/点击/填充)操作起点/番茄作家后台。

## 数据流(用户 → 章节文件)

```
用户指令 → React 聊天 → novelforge.chiefEditor.run()
→ 主进程 T7 工作流循环(逐章)
→ 规划阶段(细纲/卷纲) → Agent 调度(注册表顺序)
→ LLM 调用 + 工具执行(读创作资料/写文件/搜索)
→ 写入 chapters/chXXX/{agent}.md
→ workflow:progress 事件回传渲染器
```
