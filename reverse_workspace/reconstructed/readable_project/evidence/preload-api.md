# 关键证据摘录 — preload 暴露的 API

> CONFIRMED — preload.cjs 原文(截取核心结构, 非逐字全文)。

```js
t.contextBridge.exposeInMainWorld("novelforge", {
  globalOverlayView: {
    setSessions(e) { return t.ipcRenderer.invoke("novelforge:global-overlay-view:set-sessions", e); },
    getState() { return t.ipcRenderer.invoke("novelforge:global-overlay-view:get-state"); },
    onState(e) { /* on('novelforge:global-overlay-view:state') */ },
    onEvent(e) { /* on('novelforge:global-overlay-view:event') */ },
    emitEvent(e) { t.ipcRenderer.send("novelforge:global-overlay-view:event", e); },
    reportContentSize(e, r, n) { /* send report-content-size {sessionId, revision, size} */ },
    reportPopoverReady(e, r) { /* send report-popover-ready */ },
  },
  chapterEditorView: {
    setDockSlot(e) { /* send set-dock-slot */ },
    setSession(e) { return t.ipcRenderer.invoke("novelforge:chapter-editor-view:set-session", e); },
    getState() { /* invoke get-state */ },
    onState/onLayout/onEvent(e) { /* on state/layout/event */ },
    setFloatingBounds(e, r = !1) { /* send set-floating-bounds {bounds, commit} */ },
    reportPresentationReady(e, r) { /* send report-presentation-ready {sessionId, revision} */ },
    focus() { /* invoke focus */ },
  },
  chiefEditor: {
    analyzeInputClarity(e) { /* invoke */ },
    cancelInputClarity(e) { /* invoke */ },
    extractOfficeDocument(e) { /* invoke (docx→文本) */ },
    chat(e) { /* invoke chief-editor:chat */ },
    stopChat(e) { /* invoke chat-stop */ },
    cancelMediaGeneration(e) { /* invoke */ },
    onChatEvent(e) { /* on chief-editor:chat-event */ },
    onHistoryChanged(e) { /* on chat-history-changed */ },
    getHistory(e) / clearHistory() { /* invoke */ },
    selectGeneratedImage(e) { /* invoke */ },
    getSettings(e) / saveSettings(e, r) / resetToolPrompt() { /* invoke */ },
    listSkills() / readSkill(e) / saveSkill(e) / setSkillEnabled(e) / deleteSkill(e) / importSkill() { /* invoke */ },
    organizeLibrary(e) / listOrganizationLocks() / setOrganizationLock(e) { /* invoke */ },
    run(e) { /* invoke chief-editor:run (工作流) */ },
    stop() { /* invoke workflow:stop */ },
    onProgress(e) { /* on workflow:progress */ },
  },
  projects: {
    getCurrent() / list() / ensureForChat() / exportCurrent() / importBackup() / create(e) / select(e) / delete(e) /
    listTrash() / restoreFromTrash(e) / deleteFromTrash(e) / openTrashFolder() / rename(e) / organizeFolderName(e) /
    updateWorkflowSettings(e) / updateChapterGroups(e) /
    createBranch() / selectBranch(e) / deleteBranch(e) / renameBranch(e) / updateBranchStrategy(e) { /* invoke */ },
  },
  agents: { /* list/create/delete/duplicate/update-* 同上 */ },
  materials: { /* list/import/read-*/write/delete/open/copy */ },
  membership: { /* login/register/logout/login-or-create/redeem/plans/orders */ },
  officialModels: { /* catalog/usage */ },
  publisher: { /* platforms/bind/run-draft/mock/click/fill/snapshot */ },
  outlineManager: { /* status/generate/apply */ },
  artifacts: { /* products/preview/folders */ },
  provider: { /* models */ },
  paths: { /* open/select */ },
  system: { /* env/update/identity/legal/website */ },
  tokens: { /* summary */ },
  mobileBridge: { /* status/restart */ },
  support: { /* chat */ },
  feedback: { /* submit */ },
  workflow: { /* stop + progress */ },
  window: { /* controls */ },
});
```

完整 150 通道清单见 `main/ipc-handlers.md`。
