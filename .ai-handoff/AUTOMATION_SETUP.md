# AI 自动交接系统 — 自动化设置说明

> 生成时间: 2026-08-09
> 状态: **已完全部署并验证**(私有仓库已创建, 真实 Push 成功)

## 1. 自动化怎么工作

```
ai-checkpoint.cmd 或 python scripts/ai_checkpoint.py
  → 检测 git 是否有实际变化
  → (定时模式) 距上次 checkpoint <45min 且无变化 → 跳过
  → 安全扫描(Secret 检测, 含模型 Key/私钥/Token)
  → 命中 → SECURITY BLOCKED PUSH(停止)
  → 更新 .ai-handoff 文档(CHANGELOG + checkpoint 快照)
  → git add -A → git commit "ai-checkpoint: <摘要>"
  → git push origin HEAD
```

## 2. 创建了哪些文件

```
.ai-handoff/
├── HANDOFF.md          — 交接主文档(12 节固定结构, 供外部 AI 读取)
├── STATUS.md           — 项目真实状态
├── CHANGELOG_AI.md     — AI 变更日志(每次 checkpoint 追加)
├── NEXT_TASKS.md       — 未完成任务(P0/P1/P2)
├── REVIEW_REQUEST.md   — 外部审查协议(重点检查什么/不要做什么)
└── checkpoints/        — 每次交接的历史摘要快照
scripts/ai_checkpoint.py  — 核心脚本
ai-checkpoint.cmd         — Windows 一键入口
.gitignore                — 敏感 + 第三方排除规则
```

## 3. 如何手动触发

- 双击 `ai-checkpoint.cmd`
- 或命令行: `python scripts/ai_checkpoint.py`
- 只提交不推送: `python scripts/ai_checkpoint.py --no-push`

## 4. 如何自动触发(定时)

**Windows 任务计划程序**(每 45 分钟):

```
操作: 启动程序
程序: python
参数: C:\Users\peng\Desktop\逆向\scripts\ai_checkpoint.py --mode auto --since-min 45
起始于: C:\Users\peng\Desktop\逆向
```

创建命令(PowerShell 管理员或用户级):

```powershell
schtasks /create /tn "AI Checkpoint" /tr "python C:\Users\peng\Desktop\逆向\scripts\ai_checkpoint.py --mode auto --since-min 45" /sc minute /mo 45
```

无变化时自动退出(exit 1), 不产生垃圾 Commit。

## 5. 当前 GitHub Remote

```
origin  https://github.com/weiyang02520-ops/xinglu-reverse-engineering.git
visibility: PRIVATE
default branch: main
```

## 6. 当前工作分支

- `main`(已跟踪 origin/main)
- 直接在主分支开发(本项目为单人分析项目, 不需要 ai-work 分支; 如需可随时创建)

## 7. Secret 如何保护

- `.gitignore` 排除: `.env*`, `*.key`, `*.pem`, `credentials*`, `secrets*` 等
- 推送前强制扫描: API_KEY/TOKEN/SECRET/PASSWORD/私钥/证书/JWT/`sk-` 风格 Key/GitHub Token 等 15+ 模式
- 命中 → `SECURITY BLOCKED PUSH`, 只显示脱敏值(前 4 字符)
- 扫描器自排除(不误报自身规则)
- 第三方材料(exe/7z/asar/dll/extracted/)整体排除, 不入库

## 8. Push 失败如何处理

- 本地 checkpoint 始终先完成(commit 已落盘)
- Push 失败时输出原因, 不影响本地工作
- 手动重试: `git push origin HEAD`
- 常见原因: 网络/认证 → 检查 `gh auth status`

## 9. 外部 AI 应读取哪些文件

```
README/本文件(可选) → .ai-handoff/HANDOFF.md → 先看
      ↓
STATUS.md / NEXT_TASKS.md / REVIEW_REQUEST.md
      ↓
reverse_workspace/reports/   (01–14 全套分析报告)
reverse_workspace/scripts/   (辅助脚本, 含安全扫描)
reverse_workspace/indexes/   (文件索引)
```

HANDOFF.md 第 12 节有 Git 信息, 第 11 节有审查重点。

## 10. 如何关闭这套自动化

- 手动: 不运行脚本即可(无后台进程)
- 定时任务: `schtasks /delete /tn "AI Checkpoint" /f`(如果创建过)
- 彻底: 删除 `scripts/ai_checkpoint.py`, `ai-checkpoint.cmd`, `.ai-handoff/` 目录
- 移除全局 CLAUDE.md 中的 "AI Checkpoint Policy" 段落

## 验证记录

| 测试 | 结果 |
|---|---|
| 无变化不创建空 Commit | ✅ |
| 有变化创建 checkpoint(本地) | ✅ commit 4baec65 |
| 私有仓库创建 + 首次 Push | ✅ |
| 真实 Push(带变化) | ✅ commit b401f33 |
| 定时模式无变化跳过 | ✅ |
| 定时模式有变化且超阈值 | ✅(since-min 0 时) |
| 安全扫描拦截假 Key | ✅ 脱敏显示 sk-t… |
| 扫描器自排除(误报修复) | ✅ |
| Windows cmd 入口 | ✅ 工作正常(乱码仅为编码显示) |
