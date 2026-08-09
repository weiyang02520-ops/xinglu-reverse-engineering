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

- 第二轮审核通过(10 条修订确认落实, 无方向性问题)。
- 完成审核后小修: ① checkpoint 仓库名不再写死, 从 git remote 自动解析 owner/repo ② 明确两条确认路径(手动 confirm / AI 必须审稿) ③ 删除 Base URL HEAD 探测, config validate 只本地校验 ④ .history 支持 CREATE/UPDATE/DELETE ⑤ ContextBudget 每类硬上限 + 总预算恒等式 ⑥ 更新交接状态。
- 下一步: 直接进入 M0 开发(独立新目录 ai-novel-studio)。

## 4. 本轮修改文件

- `M .ai-handoff/PROJECT_STATE.md`
- ` M clean-room/AGENT_RUNTIME.md`
- ` M clean-room/ARCHITECTURE.md`
- ` M clean-room/DATA_MODEL.md`
- ` M clean-room/MVP_PLAN.md`
- ` M clean-room/PROJECT_FORMAT.md`
- ` M clean-room/PROVIDERS.md`
- ` M clean-room/TOOL_SYSTEM.md`
- ` M scripts/ai_checkpoint.py`

## 5. 已验证结果

- 逆向分析全部 22 阶段完成(详见前轮)。
- 两轮外部审核: 第一轮 10 条修订落实, 第二轮确认通过。
- checkpoint 脚本: remote 自动解析(4 种 URL 格式测试通过) + 可见性实时查询实测 public。
- **ChatGPT 已能实际读取 GitHub 仓库**(授权完成)。
- 小修全部完成(见 REVIEW_FIXES.md 与本轮 last_round)。

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
- 逆向仓库将保持为"逆向资料 + clean-room 设计 + 参考档案"; 正式自研软件在独立新仓库(ai-novel-studio)开发。

## 9. 本轮关键决策

- 交接同步: 用单一事实源 PROJECT_STATE.md, 脚本每次 checkpoint 全量重写 HANDOFF/STATUS, 消除「Agent 忘了更新交接文档」导致的脱节。
- 自研软件: clean-room 设计, 不复刻 XingLu 商业模式(无会员/支付/官方商城), 使用用户自有 API, 数据本地保存。
- Git: 继续使用私有仓库 xinglu-reverse-engineering(逆向+设计同仓, 文档为主)。

## 10. 下一步建议

- **P0: 开始 M0 开发(独立新目录 ai-novel-studio)** — 按 clean-room/MVP_PLAN.md: 工程骨架/Core 与 CLI 分离/配置系统/SecretStore/CLI 可启动; 真实执行 `python -m adapters.cli --help` + `config validate` + 单元测试, 全通过才 M0=PASS。
- P0: 新项目建立独立 .ai-handoff + checkpoint(已支持 remote 自动解析), push 到新 GitHub 仓库。
- P1: 新项目外部模型第一次代码审核。
- (逆向仓库工作结束, 仅维护文档。) — 用户可选: 决定仓库可见性 private/public。

## 11. 希望外部模型重点审查

- 10 条修订是否全部落实、是否引入新问题(REVIEW_FIXES.md 对照)。
- SecretStore 设计是否安全(Key 不出现在任何文件/日志)。
- Core/Adapter 分层是否彻底(Core 是否还有 UI 依赖)。
- 五状态章节状态机与事实源/派生记忆边界是否自洽。
- ContextBudget 优先级策略是否合理。
- 仓库可见性变更是否需要反映到文档(现在由脚本实时查询, 不手写)。

## 12. Git 信息

- Branch: main
- checkpoint_base_commit: 95896f317922 ai-checkpoint: add 2 new files
  (checkpoint 开始前的工作区 HEAD; 最新 checkpoint commit 以 GitHub 仓库 HEAD 为准)
- GitHub 仓库可见性: public(真实查询; 无法获取时显示 unknown)
- 最近 commit(本文件生成时): 95896f3 2026-08-09 15:38:56 +0800
- 时间: 2026-08-09 17:09

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
