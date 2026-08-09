# Project State (单一事实源)

> 本文件是 HANDOFF.md / STATUS.md 的唯一内容来源。
> Agent 每轮完成后**必须更新**本文件(阶段/完成/验证/下一步等), 再运行 checkpoint。
> 脚本每次 checkpoint 会基于本文件 + git 事实重写 HANDOFF.md 和 STATUS.md。

## project_goal

对 `xinglu-latest.exe`(星炉 XingLu v0.4.4, AI 网络小说创作桌面软件)进行完整的静态逆向分析: 解包安装包 → 识别技术栈 → 恢复前端/路由/API/数据模型 → 分析原生模块与桥接 → 重建可读工程。

逆向目标已全部达成。后续新目标: 基于逆向学到的架构知识, 设计我们自己的个人版 AI 小说创作软件(clean-room, 见 clean-room/)。

## phase

**逆向分析全部完成**(报告 01–16 + 证据链 + 最终报告 + 重建工程已交付, Git 已同步)。

当前: 进入 clean-room 设计阶段(自研软件设计文档, 不写代码)。

## last_round

- 修复 AI checkpoint 交接同步逻辑: 引入单一事实源 `.ai-handoff/PROJECT_STATE.md`, 脚本每次 checkpoint 强制重写 HANDOFF.md 与 STATUS.md, 保证「实际项目状态 = HANDOFF = STATUS」一致。
- 完成 clean-room/ 自研小说 AI 软件设计文档(8 个文件: CLEAN_ROOM_SPEC / ARCHITECTURE / DATA_MODEL / AGENT_RUNTIME / TOOL_SYSTEM / PROVIDERS / PROJECT_FORMAT / MVP_PLAN), 仅设计, 未写任何软件代码。

## verified

- 逆向分析全部 22 阶段完成: 安装包三层解包(438 文件), 技术栈(Electron+React+Vite+Capacitor), 150 IPC 通道, 20+ API 端点, 22 桥命令, 26 AI 工具, 数据模型, 本地存储, 重建可读工程(17 文件)。
- FINAL_REPORT.md 与 EVIDENCE_INDEX.md 已生成。
- Git 私有仓库 `weiyang02520-ops/xinglu-reverse-engineering`(PRIVATE)已同步。
- checkpoint 脚本同步逻辑已修复并本地验证(HANDOFF/STATUS 由 PROJECT_STATE 强制重写)。
- checkpoint 脚本已实测: 无变化不建空 commit / 安全扫描拦截假 Key / 定时模式阈值 / 真实 push 成功。

## unverified

- clean-room 设计文档尚未经外部模型审核(设计合理性待审)。
- clean-room 仅设计, 未写任何正式软件代码, 无运行验证。
- ChatGPT GitHub App 对私有仓库的读取授权(需用户在 https://github.com/settings/installations 操作)。

## architecture

逆向产出结构:
- reverse_workspace/reports/ — 01–16 全套分析报告 + EVIDENCE_INDEX.md
- reverse_workspace/reconstructed/readable_project/ — 逆向重建可读工程(17 文件)
- reverse_workspace/indexes/ — 文件/URL/API/存储键索引
- reverse_workspace/scripts/ — 自写辅助脚本(asar 解包/索引/混淆检测)
- clean-room/ — 自研软件设计文档(新)
- .ai-handoff/ — AI 交接文档(PROJECT_STATE.md 为单一事实源)

## known_issues

- 旧 HANDOFF/STATUS 内容过期问题已修复(改为强制重写); 旧 checkpoint 快照仍保留(历史记录, 不回改)。
- clean-room 设计尚未外部评审。
- ChatGPT 对私有仓库的访问需用户手动授权 App(已知步骤, 未代做)。

## key_decisions

- 交接同步: 用单一事实源 PROJECT_STATE.md, 脚本每次 checkpoint 全量重写 HANDOFF/STATUS, 消除「Agent 忘了更新交接文档」导致的脱节。
- 自研软件: clean-room 设计, 不复刻 XingLu 商业模式(无会员/支付/官方商城), 使用用户自有 API, 数据本地保存。
- Git: 继续使用私有仓库 xinglu-reverse-engineering(逆向+设计同仓, 文档为主)。

## next_steps

- P0: 提交 clean-room 设计给外部模型审核(REVIEW_REQUEST.md 已备好审查指引)。
- P1: 按审核意见修订设计文档。
- P2: 审核通过后开始 M0 开发(软件能启动), 每里程碑实际运行验证后再进入下一里程碑。

## review_focus

- clean-room 设计是否与 XingLu 干净分离(不使用其 API/资产/商标, 仅借鉴通用架构思想)。
- 长篇小说上下文管理设计(章节摘要/人物状态/世界状态/时间线/伏笔/长期记忆)是否可行。
- 最小流程 主编→Writer→Reviewer 的 Agent 运行时设计是否自洽。
- MVP 范围是否克制(无手机端/发布/会员/媒体生成)。
- 里程碑 M0–M7 每步可独立验证的标准是否明确。

## critical_files

- clean-room/CLEAN_ROOM_SPEC.md — 自研软件总规格(目标/范围/非目标)
- clean-room/ARCHITECTURE.md — 系统架构
- clean-room/DATA_MODEL.md — 数据模型
- clean-room/AGENT_RUNTIME.md — Agent 运行时
- clean-room/TOOL_SYSTEM.md — 工具系统
- clean-room/PROVIDERS.md — 模型提供商接入
- clean-room/PROJECT_FORMAT.md — 项目文件格式
- clean-room/MVP_PLAN.md — M0–M7 里程碑
- .ai-handoff/PROJECT_STATE.md — 本项目单一事实源(本文)

## recent_changes

- ai_checkpoint.py 交接同步逻辑重构(PROJECT_STATE 单一事实源 + 强制重写)。
- 新增 clean-room/ 设计文档 8 个。
- (本字段在每轮 checkpoint 后由下轮 Agent 更新为「上一轮关键变化」。)
