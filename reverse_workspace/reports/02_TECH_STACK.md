# 02 — 技术栈识别报告 (Tech Stack)

## 1. 一句话结论

**XingLu 星炉 v0.4.4 是一款基于 Electron 的 AI 网络小说创作桌面软件**(Windows x64),配套移动端 PWA(手机控制端)。

## 2. 证据链

### Electron [CONFIRMED]
- `resources/app.asar` (40MB) — Electron 标准应用包
- `XingLu.exe` (225MB, x64, 15 sections) — Electron 主程序
- 全套 Chromium 运行时: `icudtl.dat`, `v8_context_snapshot.bin`, `snapshot_blob.bin`, `chrome_100/200_percent.pak`, `resources.pak`
- 全套 GPU 库: `d3dcompiler_47.dll`, `dxcompiler.dll`, `dxil.dll`, `libEGL.dll`, `libGLESv2.dll`, `vk_swiftshader.dll`, `vulkan-1.dll`, `ffmpeg.dll`
- `locales/*.pak` (en-US, en-GB, zh-CN, zh-TW)
- `LICENSE.electron.txt`, `LICENSES.chromium.html`
- `SquirrelAwareVersion: 1` 版本资源 — electron-builder + Squirrel
- `app-update.yml` → electron-updater 自动更新

### 应用身份 [CONFIRMED]
- 版本资源: CompanyName=XingLu, FileDescription=星炉, ProductName=星炉, FileVersion=0.4.4
- `package.json`: name=`@novelforge/desktop`, version=0.4.4, description=`星炉桌面端`, type=module, main=dist/main.js
- 更新源: `https://download.xushilu.cn/updates/win` (domain xushilu.cn)
- updaterCacheDirName: `@novelforgedesktop-updater`

### 前端框架 — React [CONFIRMED]
- `rendererApp-D0lJ3WIN.js`: 676 处 hooks (useState/useEffect) 特征, 8 处 React 标记
- 内嵌 React 完整运行时(`createRoot`, `StrictMode`, `react.transitional.element` 符号)
- JSX 编译产物(jsx() 调用)
- 无 Vue/Angular/Svelte 特征

### 构建工具 — Vite [CONFIRMED]
- `index-CvAAoCbC.js`: Vite 标准 entry(modulepreload polyfill, `__vite__mapDeps`, `vite:preloadError` 事件, import.meta.url)
- 哈希文件命名: `rendererApp-D0lJ3WIN.js` (Vite 风格)
- 主进程用 esbuild 打包(ESM, `createRequire` shim, 单文件 4.2MB)

### 主进程依赖 [CONFIRMED]
- `electron-updater@^6.8.9` — 自动更新
- `sharp@^0.35.3` (libvips-42.dll) — 图像处理
- `pngjs@^5.0.0` — PNG 处理
- 内嵌库(esbuild 拍平, 非 node_modules): lodash, jszip, mammoth(docx), PDF 解析器, XML 解析器, markdown 解析器

### 移动端 [CONFIRMED]
- PWA: `mobile/index.html` + `manifest.webmanifest` + `sw.js` (Cache `novelforge-mobile-shell-v3`)
- 移动端也是 React + Vite (`index-D-s4yRj5.js`, 121 hooks)
- `mobile/android.apk` (6.1MB) — 供手机下载安装的 Android 包装(APK 带非标准前缀,待确认)

## 3. 技术栈全景

```
┌─ 桌面端 (Windows x64) ─────────────────────────────┐
│  Electron 38.x (Chromium + Node.js)                │
│  ├─ 主进程 main.js (esbuild ESM bundle, 4.2MB)     │
│  ├─ preload.cjs (contextBridge → window.novelforge)│
│  └─ renderer: React 19 + Vite (web/)               │
├─ 移动端 PWA ───────────────────────────────────────┤
│  React + Vite, service worker, 连接桌面端           │
└─ 后端/云服务 ──────────────────────────────────────┘
   api.xushilu.cn (账号/会员/模型目录/客服)
   download.xushilu.cn (更新/APK分发)
   第三方: a6api.com, vectorengine.ai/cn (LLM中转)
            bochaai.com (搜索), Suno, 可灵 (多媒体)
```

## 4. 判定汇总

| 技术 | 判定 | 证据 |
|---|---|---|
| Electron | [CONFIRMED] | asar + Chromium 运行时 + SquirrelAware |
| React | [CONFIRMED] | hooks/JSX/运行时符号 |
| Vite | [CONFIRMED] | 标准 entry + 哈希文件名 |
| esbuild (主进程) | [CONFIRMED] | ESM 单文件 bundle 特征 |
| Node.js (runtime) | [CONFIRMED] | Electron 内嵌 |
| TypeScript | [HIGHLY_LIKELY] | esbuild+React 项目惯例; 无直接证据(.d.ts 未打包) |
| Cordova | [REJECTED] | 无 cordova.js/插件; 手机端走自定义 /bridge HTTP 协议 |
| .NET/Java/Rust/Go 自研代码 | [REJECTED] | 无对应二进制 |
| 数据库 | [UNKNOWN→待定] | 未发现 sqlite; 项目以文件系统组织(.novelforge/) |
