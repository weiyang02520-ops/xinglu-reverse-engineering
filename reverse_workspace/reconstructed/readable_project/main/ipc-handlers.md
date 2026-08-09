# IPC 通道清单 (150 个)

> RECONSTRUCTED — 通道名从 preload.cjs/main.js 明文提取, **CONFIRMED**。
> 原始代码组织未知, 按功能域分组。

## projects (项目管理)

```
novelforge:projects:create          select          rename          delete
novelforge:projects:list            get-current     list-trash      restore-trash
novelforge:projects:delete-trash    open-trash-folder
novelforge:projects:create-branch   select-branch   delete-branch   rename-branch
novelforge:projects:update-branch-strategy
novelforge:projects:update-chapter-groups
novelforge:projects:update-workflow-settings
novelforge:projects:organize-folder-name
novelforge:projects:export-current  import-backup   ensure-chat
novelforge:projects:changed  (事件)
```

## agents (智能体)

```
novelforge:agents:list               create          delete          duplicate
novelforge:agents:update-identity    update-provider update-prompt-paths
novelforge:agents:update-read-files  update-output-files
novelforge:agents:update-final-text-source
novelforge:agents:update-order
```

## chief-editor (主编 AI)

```
novelforge:chief-editor:chat          chat-stop        get-history     clear-history
novelforge:chief-editor:run           analyze-input-clarity  cancel-input-clarity
novelforge:chief-editor:extract-office-document
novelforge:chief-editor:media-generation-cancel  select-generated-image
novelforge:chief-editor:get-settings  save-settings    reset-tool-prompt
novelforge:chief-editor:list-skills   read-skill      save-skill      delete-skill
novelforge:chief-editor:set-skill-enabled  import-skill
novelforge:chief-editor:organize-library   list-organization-locks
novelforge:chief-editor:set-organization-lock
novelforge:chief-editor:set-delete-confirmation-enabled
novelforge:chief-editor:resolve-delete-confirmation
事件: chat-event, chat-history-changed, delete-confirmation-request/cancelled, external-file-edit
```

## membership (会员)

```
novelforge:membership:login  register  logout  login-or-create
novelforge:membership:redeem-activation-code
novelforge:membership:get-plans  create-order  get-order-status  refresh-order-payment
novelforge:membership:get-current
```

## official-models / provider / tokens

```
novelforge:official-models:get-catalog  refresh-catalog  get-usage-balance
novelforge:provider:get-summary  save-chat-completions  select-model  delete-model
novelforge:tokens:get-summary
```

## materials / artifacts / outline

```
novelforge:materials:list  import-files  delete-file  open-file
novelforge:materials:read-file  read-audio  read-image  read-video  write-file  copy-media
novelforge:materials:open-structure-folder
novelforge:artifacts:list-products  read-preview  write-preview
novelforge:artifacts:open-product-folder  open-product-history-folder
novelforge:outline-manager:get-status  generate-directions  apply-direction
```

## publisher (发布)

```
novelforge:publisher:list-platforms  open-platform  inspect-platform  inspect-current
novelforge:publisher:bind-current-project  bind-detected-current-project
novelforge:publisher:resolve-binding-choice  clear-current-project-binding
novelforge:publisher:run-draft  run-mock  click  fill  snapshot  wait-stable
novelforge:publisher:open-url  close  open-platform
```

## mobile-bridge / support / feedback

```
novelforge:mobile-bridge:get-status  restart
novelforge:support:initialize  get-status  refresh-status  get-thread
novelforge:support:send-message  mark-read  set-viewing
事件: support:notification, support:status-changed, support:open-requested
novelforge:feedback:submit
```

## system / window / workflow

```
novelforge:system:get-environment  get-local-identity  reset-local-identity
novelforge:system:check-app-update  start-app-update-download  install-app-update
novelforge:system:get-app-update-download-state
novelforge:system:open-external-url  get-official-website
novelforge:system:get-legal-agreements  get-startup-notice
novelforge:system:set-official-network-compatibility  get-official-network-compatibility
novelforge:window:close  minimize  toggle-maximize  set-minimum-size  ensure-size
novelforge:window:set-chapter-editor-docked
novelforge:workflow:stop  事件: workflow:progress
novelforge:paths:open-local  open-containing-folder  select-project-files  to-project-relative
```

## chapter-editor-view / global-overlay-view (窗口会话)

```
novelforge:chapter-editor-view:set-session  get-state  focus  set-dock-slot
novelforge:chapter-editor-view:set-floating-bounds  report-presentation-ready
事件: state, layout, event
novelforge:global-overlay-view:set-sessions  get-state  report-content-size
novelforge:global-overlay-view:report-popover-ready
事件: state, event
```

## 启动序列

```
novelforge:window:static-loader-ready  static-loader-painted  static-loader-paint-request
novelforge:window:shown  fade-in-complete  startup-handoff-complete
novelforge:startup-window-shown  startup-window-fade-in-complete
novelforge:startup-renderer-prepared  startup-initial-app-data-ready
```
