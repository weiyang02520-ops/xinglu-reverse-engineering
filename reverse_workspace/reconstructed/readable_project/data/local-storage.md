# 数据模型 — 本地存储键

> CONFIRMED — 键名从 rendererApp/main.js 明文提取。

## localStorage (渲染器)

见 `../renderer/state.md` 完整清单。要点:

- 主题/缩放/工作区模式/布局 → UI 状态
- 聊天能力开关/默认项目聊天 → 功能偏好
- 公告已读/客服客户端 ID → 会话状态
- **无敏感数据**(登录态在主进程 JSON)

## userData/ (主进程)

见 `../main/storage.md`。要点:

- **membership_credentials.json** — 会员登录凭证(敏感)
- **mobile_bridge.json** — 手机桥配对密钥(敏感, 局域网鉴权)
- local_identity.json / window_state.json / 其余 → 配置

## 项目文件系统

见 `../main/storage.md`。创作内容全部在此, 无数据库。
