# 证据索引 (Evidence Index)

> 每条关键结论 → 证据 → 位置 → 可信度。
> 目的: 回答"你为什么这么认为?"

## 安装包与软件身份

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| NSIS-3 Unicode 安装器 | 7z 识别 `Type=Nsis, SubType=NSIS-3 Unicode`; PE32 i386; overlay 魔数 `DEADBEEF "NullsoftInst"` | evidence/7z_listing.txt, 01 报告 | CONFIRMED |
| 产品名 星炉 v0.4.4 | XingLu.exe 版本资源 (ProductName=星炉, FileVersion=0.4.4); package.json @novelforge/desktop 0.4.4 | extracted/app/XingLu.exe, asar/package.json | CONFIRMED |
| 未签名 | Authenticode NotSigned; 证书表 VA=0 | 01 报告 | CONFIRMED |
| 更新域名 xushilu.cn | app-update.yml url=https://download.xushilu.cn/updates/win | extracted/app/resources/app-update.yml | CONFIRMED |

## 技术栈

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| Electron | app.asar + Chromium 运行时(icudtl/pak/v8 snapshot) + SquirrelAwareVersion | 02 报告 | CONFIRMED |
| React | rendererApp 676 处 hooks, React 运行时符号(react.transitional.element) | formatted/rendererApp | CONFIRMED |
| Vite | modulepreload polyfill + `__vite__mapDeps` + 哈希文件名 | formatted/web-entry | CONFIRMED |
| esbuild 主进程 | createRequire shim + 单文件 ESM | formatted/main.js 首行 | CONFIRMED |
| 移动端 Capacitor | capacitor.config.json appId=com.novelforge.mobile + native-bridge.js + 空 plugins | extracted/apk/ | CONFIRMED |
| 无 Cordova | cordova.js/cordova_plugins.js 均为 0 字节占位; 无插件 | apk assets/public/ | CONFIRMED |
| 无自研原生代码 | XingLu.exe 导入表 = 标准 Electron; 业务全在 asar | 14 报告 | CONFIRMED |

## API

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 官方 API api.xushilu.cn | main.js 常量 v4e="https://api.xushilu.cn" | formatted/main.js | CONFIRMED |
| 20 个 /v1/ 端点 | main.js 明文路径字面量 | indexes/ENDPOINTS.json | CONFIRMED |
| 3 个 LLM 中转 | api.a6api.com / api.vectorengine.ai / .cn 明文 | formatted/main.js | CONFIRMED |
| 4 个搜索提供商 | Serper/智谱/博查/网关 请求头+端点明文 | 08 报告 | CONFIRMED |
| 多媒体生成 | OpenAI images / Suno fetch 轮询 / 可灵 Omni 轮询 明文 | 08 报告 | CONFIRMED |
| 模型适配器 8 个 | kdt 数组(id/matches/createRequestOverrides) | formatted/main.js | CONFIRMED |
| 支付奇象 | NOVELFORGE_QIXIANG_PAY_* 环境变量 | formatted/main.js | CONFIRMED |

## IPC / Bridge

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 150 个 IPC handler | ipcMain.handle("novelforge:…") 正则提取 | formatted/main.js | CONFIRMED |
| 渲染器零网络 | 仅 4 处 fetch(占位), 0 XHR/axios; 29 处 window.novelforge | formatted/rendererApp | CONFIRMED |
| Mobile Bridge 端点 | fPt 函数明文(/mobile/health, /bridge, /bridge/events…) | formatted/pretty/main.pretty.js | CONFIRMED |
| 22 个桥命令 | bPt 函数 switch 明文 | formatted/pretty/main.pretty.js | CONFIRMED |
| 配对密钥鉴权 | DM 函数(header x-novelforge-key/Bearer/?key === pairingKey) | formatted/pretty/main.pretty.js | CONFIRMED |
| 协议版本 v2 | mobile bundle "需要连接协议 v2" | formatted/pretty/mobile.pretty.js | CONFIRMED |

## 存储

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 项目=文件系统 | 路径常量 projects/, chapters/chXXX/, 创作资料/, .novelforge/ | formatted/main.js | CONFIRMED |
| 7 个 userData JSON | userData 路径常量(local_identity/membership_*/mobile_bridge…) | formatted/main.js | CONFIRMED |
| 18 个 localStorage 键 | novelforge.* 字面量 | formatted/pretty/rendererApp.pretty.js | CONFIRMED |
| 无数据库 | 无 sqlite/leveldb/better-sqlite3 特征 | 11 报告 | CONFIRMED(高置信) |

## 功能

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 主编工作流 T7 | 函数明文(章节循环/Agent 调度/断点续写) | formatted/pretty/main.pretty.js | CONFIRMED(存在)/RECONSTRUCTED(组织) |
| 26 个 AI 工具 | 工具 schema name+description 明文 | 15 报告 / evidence/tool-registry.md | CONFIRMED |
| 发布平台 2 个 | Z9e={qidian:write.qq.com, fanqie:fanqienovel.com} | formatted/pretty/main.pretty.js | CONFIRMED |
| 官方模型 ID 8 个 | kdt 适配器 id 字段 | formatted/pretty/main.pretty.js | CONFIRMED |
| 内置 Agent 5 个 | chief_editor/_chat/operation_guard/writing_agent/review_agent | formatted/pretty/main.pretty.js | CONFIRMED |
| 创作资料分类 10 类 | renderer d_ 函数映射(canon/setup/key_memory/…) | formatted/pretty/rendererApp.pretty.js | CONFIRMED |

## 启动与窗口

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 3 个业务窗口 | mountRendererApp surface 分发 + 章节编辑器/悬浮层 | formatted/pretty/rendererApp.pretty.js | CONFIRMED |
| 启动 4 阶段 | index-CvAAoCbC.js 明文(ignite→workspace→project→ready) | formatted/web-entry | CONFIRMED |
| 隐藏发布浏览器 | BrowserWindow + loadURL 外部站点 + executeJavaScript | formatted/pretty/main.pretty.js | CONFIRMED |

## 否定性结论

| 结论 | 证据 | 位置 | 可信度 |
|---|---|---|---|
| 无 Source Map | 全包 0 个 .map; 无 sourceMappingURL | 03 报告 | CONFIRMED |
| 无数据库 | 见上 | 11 报告 | CONFIRMED(高置信) |
| 无混淆(仅压缩) | 0 eval; 标识符平均 5.7 字符; 中文全明文 | 05 报告 | CONFIRMED |
| 无自研原生代码 | 14 报告 | CONFIRMED | 14 报告 |
