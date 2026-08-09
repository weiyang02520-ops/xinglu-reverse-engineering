# 置信度说明

> 本表列出重建工程每个文件的来源与置信度。**无任何文件来自 Source Map 或作者源码。**

| 文件 | 来源 | 置信度 |
|---|---|---|
| README.md | 重建组织 | CONFIRMED(结构)/INFERRED(组织方式) |
| architecture.md | 汇总自 reports/16 | CONFIRMED |
| api-map.md | 汇总自 reports/08 | CONFIRMED |
| main/ipc-handlers.md | preload.cjs + main.js 明文提取 | **CONFIRMED**(通道名) |
| main/workflow.md | main.js T7/jkt/Dkt 函数反推 | RECONSTRUCTED(逻辑)/INFERRED(命名) |
| main/mobile-bridge.md | main.js fPt/bPt 函数明文 | **CONFIRMED**(端点/命令) |
| main/models.md | main.js kdt 数组明文 | **CONFIRMED**(适配器 ID)/RECONSTRUCTED(结构) |
| main/publishers.md | main.js Z9e/eAe 明文 | **CONFIRMED**(平台 URL) |
| main/storage.md | main.js 路径常量明文 | **CONFIRMED** |
| renderer/pages.md | rendererApp 组件/类名反推 | RECONSTRUCTED |
| renderer/components.md | 类名枚举 | RECONSTRUCTED |
| renderer/state.md | localStorage 键明文 | **CONFIRMED**(键名) |
| renderer/startup.md | index.html + web-entry 明文 | **CONFIRMED** |
| mobile/bridge-client.md | mobile bundle + sw.js 明文 | **CONFIRMED**(协议)/INFERRED(实现) |
| data/models.md | IPC 参数/API 字段反推 | RECONSTRUCTED/INFERRED |
| data/local-storage.md | 键名明文 | **CONFIRMED** |
| evidence/preload-api.md | preload.cjs 原文摘录 | **CONFIRMED** |
| evidence/tool-registry.md | main.js 工具 schema 原文摘录 | **CONFIRMED** |

## 总体判断

- **IPC 通道名、API 端点、存储键、工具名、平台 URL**: 全部明文存在于 bundle, 高置信。
- **模块组织方式**: 原始 TS 结构丢失, 本工程的组织是**根据功能语义重建**, 仅供阅读研究。
- **函数内部实现**: 未逐行恢复(6.3MB 主进程 bundle 拍平), 逻辑以文字描述 + 关键摘录呈现。
- **UI 组件树**: 根据 JSX 结构 + 类名反推, 实际渲染细节未完全恢复。
