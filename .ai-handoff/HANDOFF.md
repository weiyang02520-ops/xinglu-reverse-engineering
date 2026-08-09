# Project Handoff

> 自动生成入口: `scripts/ai_checkpoint.py`
> 本文件在每次 Checkpoint 时由脚本**自动重写**, 内容来自单一事实源 `.ai-handoff/PROJECT_STATE.md` + git 事实。
> 请勿手改本文件, 需修改状态请改 PROJECT_STATE.md。

## 1. 项目目标

对 `xinglu-latest.exe`(星炉 XingLu v0.4.4, AI 网络小说创作桌面软件)进行完整的静态逆向分析: 解包安装包 → 识别技术栈 → 恢复前端/路由/API/数据模型 → 分析原生模块与桥接 → 重建可读工程。

逆向目标已全部达成。后续新目标: 基于逆向学到的架构知识, 设计我们自己的个人版 AI 小说创作软件(clean-room, 见 clean-room/)。

## 2. 当前阶段

**逆向分析全部完成**(报告 01–16 + 证据链 + 最终报告 + 重建工程已交付, Git 已同步)。

当前: 进入 clean-room 设计阶段(自研软件设计文档, 不写代码)。

## 3. 本轮完成内容

- 按外部模型第一轮审核意见完成 10 条修订(详见 clean-room/REVIEW_FIXES.md): ① 仓库可见性以 API 实时查询为准(当前实测 public) ② HANDOFF 改用 checkpoint_base_commit ③ SecretStore 密钥安全存储 ④ Core Engine + Adapter 分层 ⑤ 长期可扩展文件结构 ⑥ 事实源/派生记忆分离 ⑦ 五状态章节状态机 ⑧ ContextBudget 动态预算 ⑨ BaseProvider 适配层 ⑩ .history/ + undo-last-change。
- checkpoint 脚本同步逻辑修复(见上轮)继续生效; 本轮新增可见性实时查询与 commit 语义修正。

## 4. 本轮修改文件

- `M .ai-handoff/CHANGELOG_AI.md`
- ` M .ai-handoff/HANDOFF.md`
- ` M .ai-handoff/PROJECT_STATE.md`
- ` M .ai-handoff/STATUS.md`
- ` M clean-room/AGENT_RUNTIME.md`
- ` M clean-room/ARCHITECTURE.md`
- ` M clean-room/CLEAN_ROOM_SPEC.md`
- ` M clean-room/DATA_MODEL.md`
- ` M clean-room/MVP_PLAN.md`
- ` M clean-room/PROJECT_FORMAT.md`
- ` M clean-room/PROVIDERS.md`
- ` M clean-room/TOOL_SYSTEM.md`
- ` M scripts/ai_checkpoint.py`
- `?? .ai-handoff/checkpoints/2026-08-09_15-35.md`
- `?? clean-room/REVIEW_FIXES.md`

## 5. 已验证结果

- 逆向分析全部 22 阶段完成(详见前轮)。
- 10 条审核修订全部完成, clean-room 8 文档 + REVIEW_FIXES.md 已更新。
- checkpoint 脚本: 可见性实时查询实测返回 public; HANDOFF checkpoint_base_commit 语义验证通过。
- Git 私有仓库(注: 经 API 实测当前可见性为 **public**, 非手写状态; 是否改回 Private 由用户决定)已同步。

## 6. 未验证内容

- clean-room 设计文档尚未经外部模型审核(设计合理性待审)。
- clean-room 仅设计, 未写任何正式软件代码, 无运行验证。
- ChatGPT GitHub App 对私有仓库的读取授权(需用户在 https://github.com/settings/installations 操作)。

## 7. 当前架构

逆向产出结构:
- reverse_workspace/reports/ — 01–16 全套分析报告 + EVIDENCE_INDEX.md
- reverse_workspace/reconstructed/readable_project/ — 逆向重建可读工程(17 文件)
- reverse_workspace/indexes/ — 文件/URL/API/存储键索引
- reverse_workspace/scripts/ — 自写辅助脚本(asar 解包/索引/混淆检测)
- clean-room/ — 自研软件设计文档(新)
- .ai-handoff/ — AI 交接文档(PROJECT_STATE.md 为单一事实源)

## 8. 当前已知问题

- **GitHub 仓库当前可见性为 public**(API 实测) — 若需私有请用户在 GitHub 网页端修改(Settings → Danger Zone → Change visibility), 我未擅自改动。
- ChatGPT GitHub App 授权仍未操作(用户待办)。
- clean-room 设计等待第二轮外部审核。

## 9. 本轮关键决策

- 交接同步: 用单一事实源 PROJECT_STATE.md, 脚本每次 checkpoint 全量重写 HANDOFF/STATUS, 消除「Agent 忘了更新交接文档」导致的脱节。
- 自研软件: clean-room 设计, 不复刻 XingLu 商业模式(无会员/支付/官方商城), 使用用户自有 API, 数据本地保存。
- Git: 继续使用私有仓库 xinglu-reverse-engineering(逆向+设计同仓, 文档为主)。

## 10. 下一步建议

- P0: 提交第二轮审核(clean-room/REVIEW_FIXES.md 记录了修订; REVIEW_REQUEST.md 备好审查指引)。
- P0(用户): 决定仓库可见性(private/public)。
- P1: 按第二轮意见修订。
- P2: 审核通过后开始 M0 开发(软件能启动), 每里程碑实际运行验证后再进入下一里程碑。

## 11. 希望外部模型重点审查

- 10 条修订是否全部落实、是否引入新问题(REVIEW_FIXES.md 对照)。
- SecretStore 设计是否安全(Key 不出现在任何文件/日志)。
- Core/Adapter 分层是否彻底(Core 是否还有 UI 依赖)。
- 五状态章节状态机与事实源/派生记忆边界是否自洽。
- ContextBudget 优先级策略是否合理。
- 仓库可见性变更是否需要反映到文档(现在由脚本实时查询, 不手写)。

## 12. Git 信息

- Branch: main
- checkpoint_base_commit: a82b4cb14299 ai-checkpoint: add 3 new files
  (checkpoint 开始前的工作区 HEAD; 最新 checkpoint commit 以 GitHub 仓库 HEAD 为准)
- GitHub 仓库可见性: public(真实查询; 无法获取时显示 unknown)
- 最近 commit(本文件生成时): a82b4cb 2026-08-09 15:26:39 +0800
- 时间: 2026-08-09 15:38

## 13. Critical Files

- clean-room/CLEAN_ROOM_SPEC.md — 自研软件总规格(目标/范围/非目标)
- clean-room/ARCHITECTURE.md — 系统架构
- clean-room/DATA_MODEL.md — 数据模型
- clean-room/AGENT_RUNTIME.md — Agent 运行时
- clean-room/TOOL_SYSTEM.md — 工具系统
- clean-room/PROVIDERS.md — 模型提供商接入
- clean-room/PROJECT_FORMAT.md — 项目文件格式
- clean-room/MVP_PLAN.md — M0–M7 里程碑
- .ai-handoff/PROJECT_STATE.md — 本项目单一事实源(本文)

## 14. Recent Important Changes

- ai_checkpoint.py 交接同步逻辑重构(PROJECT_STATE 单一事实源 + 强制重写)。
- 新增 clean-room/ 设计文档 8 个。
- (本字段在每轮 checkpoint 后由下轮 Agent 更新为「上一轮关键变化」。)
