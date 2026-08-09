# 移动端 (PWA / Capacitor)

> CONFIRMED(协议/配置) — 实现 RECONSTRUCTED。

## 包体

- `mobile/index.html` — 星炉万象文新手机端
- `manifest.webmanifest` — PWA 清单(appId: com.novelforge.mobile)
- `sw.js` — Service Worker(cache: novelforge-mobile-shell-v3, **排除 /bridge**)
- `android.apk` — Capacitor 包装(6 个 dex, 无原生插件)

## 连接桌面端

- 扫码连接(二维码含连接信息)
- 手动输入: 桌面端地址 + 端口 + 配对密钥
- 协议版本: v2(不兼容时提示更新两端)
- 失败提示: 同 Wi-Fi / 地址端口一致 / VPN 防火墙

## 功能页面

| 页面 | 功能 |
|---|---|
| 项目页 | 列表/新建(从一句灵感开始)/切换(回到对应聊天记录和资料) |
| 聊天页 | 总编聊天(思考中/回复中/工具使用), 语音输入(长按说话), 流式渲染 |
| 资料页 | 人物设定/世界设定/时间线/临时参考/设定沉淀; 编辑冲突处理(另一端更新) |
| 章节页 | 正文查看/编辑/选择 |
| 生成页 | 图片(绘画版/风格版/精准版), 音乐(下载/上一首/下一首) |
| 设置页 | 项目设置/模型选择(官方模型/自定义仅电脑端)/写作方式(主编亲写/分身写作)/长期偏好 |

## 与桌面端同步机制

- 聊天: chat.send → SSE 流式返回; chat.stop 中止
- 资料: resource.read/write → 冲突检测("已在另一端更新")→ 覆盖/放弃
- 章节: chapter.read/write → 同上
- 设置: project.settings.read/write → "项目设置已同步"
- 媒体: media.list + /bridge/media 读取

## 桌面端推送的 SSE 事件

- 聊天流式输出(总编思考中/回复中/使用工具)
- 项目/资料/章节变更通知
- 写作进度(已写到第 N 章)
