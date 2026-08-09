# 星炉 (XingLu) — 逆向重建可读工程

> **重要声明**: 本工程是**逆向重建**, 不是作者原始源码。
> 原始 TypeScript 源码、模块结构、变量名、注释在构建时已丢失(无 Source Map)。
> 本工程基于发布包(app.asar)的 JS Bundle 静态逆向, 按功能重新组织。
> 每个文件顶部标注: 来源 / 置信度。

## 置信度标记

| 标记 | 含义 |
|---|---|
| `CONFIRMED` | 从 bundle 明文证据直接恢复(IPC 通道名/API 端点/字符串/路径) |
| `RECONSTRUCTED` | 从 bundle 拆解整理(功能归属明确, 但原始结构未知) |
| `INFERRED` | 根据行为/字符串推测(原始结构/命名无法确认) |
| `UNKNOWN` | 无法确认 |

## 原始发布包结构(供对照)

```
xinglu-latest.exe (NSIS 安装器)
└── app-64.7z (Electron 应用)
    ├── XingLu.exe          (Electron 主程序, 无自研代码)
    ├── resources/app.asar  (全部业务逻辑, 395 文件)
    │   ├── package.json    (@novelforge/desktop 0.4.4)
    │   ├── dist/main.js    (主进程, esbuild bundle)
    │   ├── dist/preload.cjs
    │   ├── dist/web/       (桌面端 React 前端)
    │   └── dist/mobile/    (移动端 PWA + android.apk)
    └── resources/app.asar.unpacked/sharp/
```

## 重建工程结构

```
readable_project/
├── README.md                    ← 本文件
├── CONFIDENCE.md                ← 每文件来源/置信度
├── api-map.md                   ← API 总览(指向完整报告)
├── architecture.md              ← 架构摘要
├── main/                        ← 主进程逻辑(RECONSTRUCTED)
│   ├── ipc-handlers.md          ← 150 个 IPC 通道清单
│   ├── workflow.md              ← 主编工作流引擎
│   ├── mobile-bridge.md         ← 本地 HTTP 桥协议
│   ├── models.md                ← 模型适配器
│   ├── publishers.md            ← 发布自动化
│   └── storage.md               ← 文件系统布局
├── renderer/                    ← 渲染进程(RECONSTRUCTED)
│   ├── pages.md                 ← 页面/视图
│   ├── components.md            ← 组件群
│   ├── state.md                 ← 状态管理
│   └── startup.md               ← 启动序列
├── mobile/                      ← 移动端(RECONSTRUCTED)
│   └── bridge-client.md         ← 桥客户端
├── data/                        ← 数据模型
│   ├── models.md                ← 领域模型
│   └── local-storage.md         ← 存储键
└── evidence/                    ← 关键证据摘录
    ├── preload-api.md           ← contextBridge 暴露的 API
    └── tool-registry.md         ← 26 个 AI 工具
```

## 快速导航

| 想知道 | 看 |
|---|---|
| 这是什么软件 | `architecture.md` |
| 有哪些 API | `api-map.md` + `main/ipc-handlers.md` |
| 主进程怎么工作 | `main/workflow.md` |
| 手机怎么连接 | `main/mobile-bridge.md` |
| 支持哪些模型 | `main/models.md` |
| 页面长什么样 | `renderer/pages.md` |
| 数据存哪里 | `data/local-storage.md` + `main/storage.md` |
| 完整分析报告 | `../reports/` (01–16) |
| 证据链 | `../reports/EVIDENCE_INDEX.md` |
