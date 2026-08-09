# 14 — 原生二进制分类报告 (Binaries)

## 结论

**XingLu 不含任何自研原生代码。所有原生二进制均为 Electron/Chromium 运行时或第三方库。**
业务逻辑 100% 在 JavaScript (app.asar) 中。 [CONFIRMED]

## 分类清单

### P3 — Electron 运行时 (无需深入)

| 文件 | 大小 | 架构 | 说明 |
|---|---|---|---|
| XingLu.exe | 225.7MB | x64 | Electron 主程序(标准编译, 15 sections, 无 overlay) |
| resources/elevate.exe | 107KB | x86 | Squirrel 提权助手(electron-builder 附带) |
| d3dcompiler_47.dll | 4.7MB | x64 | Direct3D 编译器(Chromium) |
| dxcompiler.dll | 25.6MB | x64 | DirectX 编译器(Chromium) |
| dxil.dll | 1.5MB | x64 | DXIL 支持 |
| ffmpeg.dll | 3.1MB | x64 | 音视频解码(Chromium) |
| libEGL.dll / libGLESv2.dll | 0.5/8.0MB | x64 | ANGLE OpenGL 实现 |
| vk_swiftshader.dll | 5.5MB | x64 | SwiftShader 软件渲染 |
| vulkan-1.dll | 0.9MB | x64 | Vulkan 加载器 |

### P3 — Chromium 数据

| 文件 | 说明 |
|---|---|
| icudtl.dat (10.9MB) | ICU 国际化数据 |
| snapshot_blob.bin / v8_context_snapshot.bin | V8 快照 |
| chrome_100/200_percent.pak, resources.pak | Chromium 资源 |
| locales/*.pak | 语言包(en-US/en-GB/zh-CN/zh-TW) |

### P2 — 第三方库 (sharp 图像处理)

| 文件 | 说明 |
|---|---|
| libvips-42.dll (18.4MB) | sharp 依赖的 libvips 图像处理库 |
| libvips-cpp-8.18.3.dll | libvips C++ 绑定 |
| sharp-win32-x64-0.35.3.node | sharp Node 原生模块 |

### 导入表 (XingLu.exe)

`CRYPT32.dll, DWrite.dll, KERNEL32.dll, VERSION.dll, WINMM.dll, WS2_32.dll, ntdll.dll`
→ 标准 Electron 发行版导入, 与官方 Electron 一致 [CONFIRMED]

## 判定

- P0 (核心业务): **无**
- P1 (桥接): **无**(JS 全权负责)
- P2 (第三方): sharp 库族
- P3 (运行时): 全部 Electron/Chromium

## 原生逆向结论

XingLu.exe 无需反汇编逆向 — 它是未修改的 Electron 二进制(导入表与官方发行版一致), 所有业务逻辑在 app.asar 的 JS 中, 已在前述 JS 分析中完整覆盖。
