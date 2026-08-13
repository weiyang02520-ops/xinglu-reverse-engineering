# 09 — Materials / Library

> 创作资料库：项目的非章节素材（人物/世界/设定/参考文件），支持导入、编辑、整理、锁定。

## Purpose

管理"创作资料"（素材）：Markdown 设定文件 + 媒体文件（图片/音频/视频），供总编/Agent 读取与写作参考。

## Entry

- creative 工作区：`creative-material-window` 窗口（素材窗）
- 素材路径树：`creative-path-list`（folder 组织）
- 聊天附件/消息可引用素材文件

## Layout [RUNTIME_CONFIRMED 类族]

```
creative-material-window
├── creative-material-header-import（导入按钮）
├── creative-organize-header-button（整理按钮）
└── creative-folder-list（文件夹树，见 06）
    └── creative-path-item（素材条目）
        ├── creative-path-open-button
        └── creative-path-delete-button

material-editor-dialog（素材编辑对话框）
├── material-editor-form
│   ├── material-editor-title-field（标题）
│   ├── material-editor-summary-field（摘要）
│   ├── material-editor-body-input（正文）
│   ├── material-editor-outline-identity（大纲身份）
│   ├── material-editor-limit-status（字数限制状态）
│   └── material-editor-user-note（用户备注）
├── material-editor-state（保存状态）
└── material-file-card（文件卡片：top/title/references）
```

## Hierarchy

```
Materials
├── 素材窗（creative-material-window）
│   ├── 文件夹树（creative-folder-*）
│   └── 素材条目（path-item：open/delete）
├── 导入（materials:import-files IPC → 系统文件选择）
├── 编辑（material-editor-dialog：标题/摘要/正文/身份/限制/备注）
├── 整理（organize-library IPC + organization-lock 锁定）
└── 媒体读取（readImage/readAudio/readVideo → dataURL）
```

## Dimensions

- 素材卡片：file-card（top/title/references 结构）
- 编辑器对话框：标题/摘要/正文表单 + 字数状态

## Visual

- 文件夹分组 + 路径条目（root-path-item 标识根路径）
- 文件引用链（material-file-references）

## Controls

- 导入（import-files）、删除（deleteFile）、打开（openFile/readFile）
- 编辑（material-editor-dialog）、整理（organize-library）
- 锁（set-organization-lock：并发整理保护）
- 打开结构文件夹（open-structure-folder）

## States

- 文件夹折叠/空态（folder-empty / search-empty）
- 整理锁定中（lock-button）
- 编辑器保存状态（material-editor-state）

## Interactions

- 导入文件 → `materials:import-files` → 复制进项目素材目录
- 整理 → `organize-library` → 按规则重组文件夹（异步，locks 防冲突）
- 打开 → `materials:open-file`（外部编辑器）或 `read-file`（内嵌预览）
- 拖放 → `paths:from-dropped-files`（拖入文件转项目相对路径）[RUNTIME_CONFIRMED]

## Storage / State

- 素材文件：`workspace/projects/{id}/创作资料/*.md` + 媒体文件 [REPORT_CONFIRMED]
- 整理锁：主进程列表（list-organization-locks）

## Window behavior

creative 模式中为 dock/floating 窗口之一；编辑对话框为 modal。

## Evidence

- 类族：CSS [RUNTIME_CONFIRMED]
- IPC：preload materials 模块 [RUNTIME_CONFIRMED]
- 文件布局：reports/11 [REPORT_CONFIRMED]

## Unknown

- 素材条目的元数据类型（人物/世界观/时间线分类？）
- 编辑器的字数限制具体规则
- 引用链（file-references）如何建立与展示
