# XingLu 静态逆向分析 — 进度追踪

> 目标文件: `xinglu-latest.exe` (122,522,853 bytes / 116.85 MiB)
> 工作目录: `reverse_workspace/`
> 分析开始: 2026-08-08
> 分析方式: 纯静态(未执行任何目标程序)

---

## 当前阶段: 主进程 AI 引擎深挖(chief-editor / publisher / workflow)

## 已完成

### 第一阶段: 安装包识别 [COMPLETED]
- 确认 NSIS-3 Unicode 安装器(32 位 PE stub + 116.7MB overlay 存档)
- 未签名、无证书
- 内部结构: `$PLUGINSDIR/app-64.7z` (主载荷) + `$R0/Uninstall XingLu.exe` + NSIS 标准插件
- 详报: `reports/01_INSTALLER_ANALYSIS.md`

### 第二阶段: 完整静态解包 [COMPLETED]
- 三层解包: NSIS → 7z → ASAR(自写脚本 `scripts/extract_asar.py`)
- 438 个文件,520MB,索引: `indexes/FILE_TREE.txt` + `indexes/FILES.csv`
- 应用核心: `resources/app.asar` (40MB) → 395 文件

### 第三~八阶段 [COMPLETED]
- 技术栈(02)、源码残留(03)、前端入口(04)、混淆检测(05)
- JS 自动索引: STRINGS.json(2295 条中文)、URLS.json(144)、ENDPOINTS.json(20)、STORAGE_KEYS.json、FUNCTION_HINTS.json(IPC 通道 140+)
- 详见各报告

### 第九~十四阶段 [COMPLETED 主要]
- API 地图(08): 官方 20 端点 + 3 个 LLM 中转 + 4 个搜索提供商 + mobile bridge 22 命令
- 数据模型(09)、状态管理(10)、本地存储(11)
- 页面/路由(06/07): 待细化, 已确认 3 个 surface + 主工作区 + 对话框集

## 关键发现(摘要)

1. **产品: 星炉 (XingLu) — AI 网络小说创作工具**,版本 0.4.4
2. **包名: @novelforge/desktop**,更新域名 xushilu.cn
3. **架构**: renderer(React) → preload.cjs (contextBridge, `window.novelforge`) → main.js (ipcMain 150 handlers) → 网络/本地
4. **AI 多模态**: OpenAI 兼容/Anthropic/Gemini 文本; 图像生成(OpenAI images API); Suno 音乐; 可灵 Omni 视频; 搜索(Serper/智谱/博查/网关)
5. **移动端**: PWA + APK, 通过 HTTP bridge(8787/18789/8891-8999)配对连接桌面端, 22 个命令
6. **发布自动化**: publisher 模块用隐藏 BrowserWindow 模拟操作起点/番茄/QQ阅读等平台
7. **项目文件系统**: projects/{id}/ 目录 + .novelforge/ 元数据, 无数据库
8. **AI 智能体系统**: agents(写作分身) + chief-editor(主编) + skills(技能库) + workflow(工作流)
9. **商业化**: membership 模块(登录/注册/订单/激活码/创作点/套餐)

## 失败尝试
- 7z 打开 app.asar 失败 → 自写解包器 ✓
- asar 头 3 字节偏差 → pickle size 计算 ✓
- android.apk 非标准 ZIP → 待分析(26 字节前缀)
- prettier 全局不可用 → workspace 本地安装 ✓

## 待确认问题
- android.apk 内部结构(v2 签名前缀?)
- publisher 平台完整清单与操作脚本
- chief-editor 工作流(多 agent 串行/并行?)

## 下一步行动
- [x] 主进程 AI 引擎深挖(chief-editor 运行流 / publisher / workflow)
- [ ] 页面/路由报告(06/07)细化
- [ ] 原生二进制 XingLu.exe 分析(14)
- [ ] 重建可读工程
- [ ] FINAL_REPORT
- 自动化测试记录
