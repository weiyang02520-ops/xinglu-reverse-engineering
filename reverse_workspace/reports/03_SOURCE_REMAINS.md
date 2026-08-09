# 03 — 源码残留搜索报告 (Source Remains)

## 结论

**发布包中没有任何 Source Map、构建配置或原始源码残留。**

## 搜索范围与结果

| 项目 | 结果 |
|---|---|
| `*.map` / `*.js.map` / `*.css.map` | 0 个 [CONFIRMED] |
| `sourceMappingURL` 注释 | 0 处 [CONFIRMED] |
| `vite.config.*` / `webpack.config.*` / `rollup.config.*` / `tsconfig.json` / `babel.config.*` | 0 个 [CONFIRMED] |
| `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` | 0 个 [CONFIRMED] |
| `src/` / `pages/` / `components/` 目录 | 无(仅 dist 产物) [CONFIRMED] |
| 开发机路径 / 用户名路径 | 未发现 (grep 无匹配) |
| `.git` 目录 | 无 [CONFIRMED] |
| 调试残留 | 无; 仅有 `__novelforgeDebug` hook(运行期注入, 用于调试) |

## 唯一配置类文件

- `package.json` (285B, 压缩) — 仅依赖声明: electron-updater, pngjs, sharp
- `app-update.yml` — 更新配置
- `manifest.webmanifest` / `sw.js` — PWA 配置

## 影响

- 无 Source Map → **无法恢复原始源码结构**, 只能从 bundle 逆向重建
- 原始 TypeScript 源文件、模块目录、注释已完全丢失
- 唯一保留的开发信息: 环境变量名 (`NOVELFORGE_*`)、IPC 通道名 (`novelforge:*`)、中文 UI 字符串
- 这三点是重建工程的主要依据

## 判定

- 源码残留: **不存在** [CONFIRMED]
- Source Map 恢复: **不可行**
- 重建方式: Bundle 逆向 + 语义命名(标记 RECONSTRUCTED/INFERRED)
