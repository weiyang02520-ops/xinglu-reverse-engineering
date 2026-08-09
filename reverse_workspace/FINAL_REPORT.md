# 最终报告 — XingLu (星炉) v0.4.4 逆向分析

> 分析对象: `xinglu-latest.exe` (122,522,853 bytes)
> 分析方式: 纯静态(未执行任何目标程序)
> 完成日期: 2026-08-09

## 1. XingLu 是什么类型的软件

**星炉 (XingLu) 是一款面向网络小说作者的 AI 创作桌面软件**(Windows x64)。
核心能力: 用多 Agent(主编 + 写作分身)按章节自动创作小说, 管理创作资料(大纲/人物/世界/伏笔/时间线), 生成图片/音乐/视频, 支持手机远程协同, 并能自动发布到起点/番茄等平台。

内部代号 `@novelforge/desktop`(NovelForge Desktop), 版本 0.4.4, 由「万绪工作室」运营(域名 xushilu.cn)。

## 2. 技术栈

| 层 | 技术 |
|---|---|
| 桌面壳 | Electron (Chromium 38 系) + electron-builder (NSIS) |
| 前端 | React + Vite(主窗口/章节编辑器/悬浮层三窗口 SPA) |
| 主进程 | esbuild 打包 ESM bundle(4.2MB 单文件) |
| 移动端 | Capacitor 包装的 PWA(Android APK) |
| 图像 | sharp (libvips) |
| 文档解析 | 内嵌 mammoth/jszip/docx/PDF 解析器 |
| 更新 | electron-updater (generic, download.xushilu.cn) |

无任何自研原生代码; 无数据库(文件系统+JSON); 无真实混淆(仅压缩)。

## 3. 安装包结构

```
xinglu-latest.exe (NSIS-3 Unicode, 32 位 stub, 未签名)
└── $PLUGINSDIR/app-64.7z (121.7MB, 主载荷)
    └── Electron 应用目录
        ├── XingLu.exe (225MB) + Chromium 运行时 DLL/PAK
        ├── resources/app.asar (40MB) ← 全部业务逻辑
        └── resources/app.asar.unpacked/sharp (图像库)
```

## 4. 解包文件统计

- 三层解包: NSIS → 7z → ASAR(自写 Python 解包器)
- **438 个文件, 520MB**(不含原始安装包)
- 其中 asar 内 395 文件 (60.9MB)
- 索引: `indexes/FILE_TREE.txt`(521 行) + `indexes/FILES.csv`(438 行, 含 SHA256)

## 5. 主要目录用途

| 目录 | 用途 |
|---|---|
| extracted/ | 三层解包产物(第三方材料, 不入 Git) |
| formatted/ | 美化后的 bundle(可读版本) |
| indexes/ | 文件树/CSV/URL/API/存储键/路由/字符串索引 |
| reports/ | 01–16 全套分析报告 + 证据链 |
| reconstructed/readable_project/ | 逆向重建可读工程(17 文件) |
| scripts/ | 自写辅助脚本(asar 解包/索引/混淆检测/checkpoint) |

## 6. 前端架构

- **入口**: web/index.html → index-CvAAoCbC.js(加载器) → rendererApp-D0lJ3WIN.js(React 应用)
- **三窗口**: 主窗口 / 章节编辑器(surface=chapter-editor) / 全局悬浮层(surface=global-overlay)
- **零网络渲染器**: 所有网络/文件操作经 preload(contextBridge, window.novelforge) → 主进程 150 个 IPC handler
- **启动序列**: ignite(点亮星炉)→workspace→project→ready, 静态加载器 + 淡入

## 7. 页面

主工作区(项目列表/简单模式/创作模式)、聊天面板、章节编辑器、资料库、大纲管理、模型库、技能库、客服、会员中心、回收站、发布助手、设置(外观/会员/模型/技能/客服/反馈/关于)。移动端: 连接/项目/聊天/资料/章节/生成/设置页。

## 8. 路由

无 URL 路由(纯状态切换)。导航 = React state + 窗口管理 + IPC。详细图见 reports/07。

## 9. API

- **官方**: api.xushilu.cn 20 个 /v1/ 端点(账号/订单/套餐/公告/模型目录/客服)
- **LLM 中转**: a6api.com, vectorengine.ai/.cn(OpenAI 兼容)
- **搜索**: Serper / 智谱 / 博查 / 统一网关
- **媒体**: OpenAI 图像 / Suno 音乐 / 可灵视频
- **本地桥**: HTTP 服务器(8787/8891-8999), 22 个命令, SSE 事件
- 详见 reports/08

## 10. 数据模型

Project / Agent / Chapter / ChatMessage / WorkflowProgress / Membership / ContentKind / Skill / PublisherBinding — 全部见 reconstructed/data/models.md。

## 11. 本地存储

- localStorage 18 键(UI 状态, 无敏感)
- userData 7 个 JSON(membership_credentials.json 为登录态)
- 项目 = 文件系统目录(projects/{id}/, .novelforge/ 元数据)
- **无数据库**

## 12. Cordova 插件

**不适用**。移动端是 Capacitor(无原生插件)。桌面端无 Cordova。

## 13. Native Bridge

- Electron IPC: 150 invoke 通道 + 事件流
- Mobile Bridge: HTTP JSON-RPC + SSE(配对密钥鉴权, 协议 v2)
- 发布浏览器: 隐藏 BrowserWindow + executeJavaScript
- 详见 reports/13

## 14. 原生代码

**无自研原生代码**。XingLu.exe 为标准 Electron 二进制(导入表与官方一致), 业务 100% 在 JS。

## 15. 功能模块

项目管理(含分支/回收站/导出导入)、主编 AI 聊天(多模态)、自动写作工作流(多 Agent 逐章调度)、智能体管理、章节编辑器、创作资料库、大纲管理、会员商业化(登录/套餐/订单/激活码/创作点)、官方模型、自定义模型库、技能库、客服、发布自动化(起点/番茄)、素材与媒体生成、手机协同、系统更新。详见 reports/15。

## 16. 软件完整运行流程

```
启动(XingLu.exe) → 主进程加载 app.asar → 创建窗口 → React 挂载
→ 用户选择/创建项目 → 主编聊天或一键写作
→ 工作流引擎逐章调度 Agent → LLM 调用(+工具: 读写文件/搜索/生成媒体)
→ 章节写入 projects/{id}/chapters/ → 进度实时回显
→ 会员体系保障官方模型计费(创作点)
→ 手机可配对远程操作; 写完后一键发布到起点/番茄
```

## 17. 哪些源码基本恢复

- IPC 通道(150)、API 端点(20+)、桥命令(22)、AI 工具(26)、模型适配器(8)
- 本地存储键(18)、userData 文件(7)、项目目录布局
- 页面/视图/组件群、启动序列、工作流逻辑(语义级)
- 发布平台、官方模型清单、环境变量体系

## 18. 哪些源码属于重建

全部可读工程均为重建(RECONSTRUCTED/INFERRED), 无原始源码级恢复:
- 组件/函数命名、模块组织、UI 树(按语义重建)
- 数据模型(字段来自证据, 结构为推测)
- 原始 TS 类型/目录/注释不可恢复

## 19. 哪些内容无法恢复

- 原始源码结构/命名/注释
- 函数级实现细节(6.3MB 拍平 bundle 只恢复语义)
- 服务端逻辑与数据库
- UI 精确视觉样式(仅类名)

## 20. 尚未解决的问题

- android.apk 的 v2 签名前缀细节(已判定, 未深挖)
- SSE 事件完整清单(命令已恢复, 事件类型未穷举)
- 部分业务函数(如 token 计价公式)内部实现
- 星炉后端协议细节(仅客户端视角)

## 21. 下一步深入方向

1. 用 DevTools Protocol 思路精读 workflow 各工具执行器(6.3MB main.js 内)
2. 提取 SSE 事件类型全集(移动端协同完整时序)
3. 分析 docx/PDF 提取器的完整支持范围(办公文档导入)
4. 若有合法途径, 动态验证 bridge 协议
5. 重建工程可进一步拆分为可读的伪代码级模块

---

# 最终状态表

| 类别 | 内容 |
|---|---|
| **已经完整提取** | 安装包三层解包(438 文件)、IPC 通道 150、API 端点 20+、桥命令 22、AI 工具 26、模型适配器 8、存储键 18+7、页面/组件/对话框清单、发布平台 2、官方模型 8、环境变量 100+、中文字符串 2295 |
| **已经理解** | 软件类型与商业模型、完整技术栈、三窗口架构、IPC/桥协议、工作流引擎、数据流、启动序列、移动端协同机制、发布自动化原理 |
| **部分理解** | 各 AI 工具执行器内部实现(语义级, 非代码级)、SSE 事件全集、docx 解析细节、支付回调时序 |
| **已经重建** | reconstructed/readable_project/(17 文件 44K 字, 标注置信度) |
| **仍然未知** | 原始源码结构/命名、服务端实现、token 计价公式、部分工具内部细节、APK 签名细节 |
| **发布包中不存在, 无法恢复** | 开发者 Git 历史、服务端后端源码、未打包的源文件、原始注释、Source Map、构建配置、开发环境变量实际值、私有密钥/账号 |
