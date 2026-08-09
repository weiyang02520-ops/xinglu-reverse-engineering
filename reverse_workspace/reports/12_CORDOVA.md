# 12 — Cordova 分析报告

## 结论

**桌面端不涉及 Cordova。移动端(APK)使用 Capacitor 而非 Cordova。**
Cordova 在本次逆向中不适用。 [CONFIRMED]

## 证据

1. **桌面端 (Electron)**: 无 cordova.js / cordova_plugins.js / 插件目录
   - 桌面端与外部通信方式: Electron IPC + HTTP bridge(见 13 报告)
2. **移动端 (APK)**: 
   - `assets/capacitor.config.json`: `{"appId":"com.novelforge.mobile","appName":"星炉","webDir":"dist","server":{"androidScheme":"https","cleartext":true}}` [CONFIRMED]
   - `assets/capacitor.plugins.json`: `[]` (无原生插件) [CONFIRMED]
   - `assets/native-bridge.js` (53KB) — Capacitor 标准桥 [CONFIRMED]
   - `assets/public/cordova.js` 和 `cordova_plugins.js` — **0 字节占位文件**(Capacitor 兼容遗留产物) [CONFIRMED]
   - 6 个 classes.dex — Capacitor Android 运行时 + WebView
   - `appId = com.novelforge.mobile`

## 移动端技术栈结论

- **Capacitor 3+**(基于 native-bridge.js 结构)
- 无任何自定义原生插件(plugins.json 为空)
- WebView 加载 `assets/public/` 打包的 PWA
- 与桌面端的通信**不经过 Capacitor 桥**, 而是直接 HTTP 请求桌面端 `/bridge` 服务(网络层为纯 Web fetch)

## 修正记录

- 最初线索 "Cordova" 被否定 → 实为 Capacitor [CONFIRMED]
- android.apk 的 26 字节头部前缀是 **APK Signing Block(v2 签名)** 偏移对齐特性 [HIGHLY_LIKELY]
  - 证据: EOCD 之后 `APK Sig Block 42` 标记出现在 Central Directory 前
