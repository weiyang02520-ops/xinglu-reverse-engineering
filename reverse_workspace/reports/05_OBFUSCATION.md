# 05 — 混淆检测报告 (Obfuscation Analysis)

## 结论

**所有 JS 均为"普通打包压缩"(minification),不是真正的代码混淆(obfuscation)。**

## 检测数据

| 文件 | eval() | new Function | hex escape | 平均标识符长度 | 短变量声明 |
|---|---|---|---|---|---|
| main.js (4.2MB) | 0 | 8 | 600* | 5.7 | 13,429 |
| rendererApp (993KB) | 0 | 0 | 3 | 5.8 | 2,940 |
| mobile (480KB) | 0 | 0 | 2 | 5.9 | 1,341 |
| preload.cjs (19KB) | 0 | 0 | 0 | 7.8 | 28 |

\* main.js 的 hex escape 集中在 OOXML/PDF 解析器(如 ` ` 换行符),非字符串加密。

## 判定依据

1. **无 eval / new Function 动态执行** → 排除字符串数组 + 索引函数混淆
2. **无字符串加密特征** → 中文字符串全部明文可读(2295 条已提取)
3. **标识符仍保留语义片段** → 例如 `novelforge:*` 通道名、`shouldRetryResponse`、`refreshApiKey`、`chapterManageUrl` 等长命名
4. **控制流未平坦化** → while 循环极少, 无 switch-dispatch 模式
5. **构建工具特征明确**: esbuild (main.js: `var X=Object.create` 风格 + createRequire shim) 和 Vite (renderer: 独立 chunk 边界)

## 混淆 vs 压缩结论

- esbuild `--minify` (main.js) — 变量改名 + 空白压缩
- Vite 生产构建 (renderer) — 同上
- 业务字符串、IPC 通道名、API 端点、错误消息**全部保留明文**

## 对逆向的影响

- **高可读性**: 中文字符串是理解功能的金矿(2295 条)
- 组件名/模块名丢失 → 需用行为 + 字符串反向命名
- 单文件拍平 → 需人工划分模块边界(按功能聚类)
