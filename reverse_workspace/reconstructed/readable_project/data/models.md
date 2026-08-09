# 领域模型

> RECONSTRUCTED/INFERRED — 从 IPC 参数、API 字段、UI 字符串反推。
> 原始 TS 类型丢失; 字段名来自代码中可见的键。

## Project

```ts
interface Project {
  id: string;              // 项目 ID (目录名)
  name: string;            // 书名
  creativeDirection: "novel";
  creationMode: "continuous";
  branchId?: string;       // 当前分支
  workspaceMode?: "simple" | "creative";
  workflowSettings?: WorkflowSettings;
  chapterGroups?: ChapterGroup[];
  chapterProgress: { currentChapterNumber: number };
  inspiration?: string;    // 一句灵感
  genre?: string;          // 题材方向
}
```

## Agent

```ts
interface Agent {
  id: string;
  title: string;           // 名称
  identity: string;        // 身份设定
  provider: ProviderRef;   // {providerId, modelId, apiKey?}
  promptPaths: string[];   // 提示词文件
  readFiles: string[];     // 固定读取文件
  inputRefs?: string[];    // 语义化资源引用
  outputFiles: string[];   // 输出文件 (如 chapters/chXXX/xx.md)
  finalTextSource?: boolean; // 是否为正文 Agent
  order: number;           // 调度顺序
  enabled: boolean;
}
```

## Chapter

```ts
interface Chapter {
  number: number;              // 章节号
  slug: string;                // ^[a-z][a-z0-9_]{1,63}$
  title: string;
  content: string;             // 正文 (Markdown)
  files: ChapterFile[];        // 各 Agent 产物
  status: "draft" | "done";
}
```

## ChatMessage / ChatEvent

```ts
interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;             // Markdown
  attachments?: Attachment[];  // file/image/audio/video
  createdAt: string;
}

interface ChatEvent {
  kind: "thinking" | "responding" | "tool_start" | "tool_done"
      | "assistant_committed" | "done" | "error" | "interjection";
  agentId?: string;
  toolName?: string;
  seq: number;
}
```

## WorkflowProgress

```ts
interface WorkflowProgress {
  agentId: string;             // 如 chief_editor / loop / token_meter
  stepId: string;
  label: string;               // 如 "自定义调度器" / "Token 估算"
  status: "active" | "skipped" | "stopped" | "done" | "error";
  phase: string;               // checking_inputs/planning/writing/tool/finalizing/idle
  loopMode?: "chapter";
  chapterNumber?: number;
  message?: string;
  reads?: string[];            // 读取的文件路径
  writes?: string[];           // 写入的文件路径
  tokenUsage?: { kind: "prompt"|"completion", promptTokens, completionTokens };
}
```

## Membership

```ts
interface MembershipState {
  account?: { username: string; createdAt: string };
  plan?: { id: string; name: string; ... };
  credits: number;             // 创作点余额
  entitlements: { ... };       // 权益
  orderWatchUrl?: string;      // 支付轮询
}
```

## ContentKind (创作资料分类)

```ts
type ContentKind =
  | "canon" | "setup"          // 设定
  | "key_memory"               // 重点记忆
  | "material"                 // 创作资料
  | "image"                    // 图片资料
  | "outline"                  // 大纲
  | "skill"                    // 技能
  | "music" | "video"          // 音乐/视频资料
  | "generated_music" | "generated_video"; // 生成媒体
```

## Skill

```ts
interface Skill {
  id: string;
  name: string;
  description: string;         // 什么时候应该使用
  content: string;             // 技能正文
  enabled: boolean;
  builtin: boolean;            // 内置技能
  locked?: boolean;            // 锁定后不追官方更新
}
```

## PublisherBinding

```ts
interface PublisherBinding {
  platform: "qidian" | "fanqie";
  projectId: string;
  workName: string;
  workBackendUrl: string;
  chapterManageUrl: string;
  savedDraftChapterNumber: number;
  uploadedChapterNumber: number;
}
```
