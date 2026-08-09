# 01 — 安装包分析报告 (XingLu Installer)

> 目标: `xinglu-latest.exe`
> 大小: 122,522,853 bytes (116.85 MiB)
> 时间: 2026-08-08 (文件日期 2026-08-07 13:26, NSIS 打包时间)

## 1. 文件标识

| 属性 | 值 | 置信度 |
|---|---|---|
| SHA256 | `f78d80c0ece15b9dc8fefc0e0dc2a96e21cb48baf47e5ffa0ed7dc30949897f2` | [CONFIRMED] |
| MD5 | `80819b4ad3e9633edf2ff2c3156fbd58` | [CONFIRMED] |
| 类型 | PE32 (x86) GUI, Nullsoft Installer self-extracting archive | [CONFIRMED] |
| 架构 | x86 (i386) 安装器 stub | [CONFIRMED] |

## 2. PE 头部

| 属性 | 值 |
|---|---|
| Machine | 0x14c (x86) |
| Sections | 5 (.text .rdata .data .ndata .rsrc) |
| EntryPoint | 0x338f |
| ImageBase | 0x400000 |
| SizeOfImage | 2,469,888 bytes |
| Subsystem | GUI |
| Linker | 6.0 (旧版 NSIS stub) |
| TimeDateStamp | 2018-12-15 22:26:14 UTC |
| 数字签名 | **未签名** (Authenticode: NotSigned) |
| 编译时间 | 时间戳不可靠(NSIS 编译器固定),实际打包时间约为 2026-08-07 |

## 3. 安装器类型 [CONFIRMED]

- `file` 识别: "Nullsoft Installer self-extracting archive"
- 7-Zip 识别: `Type = Nsis`, `SubType = NSIS-3 Unicode`, `Method = Deflate`
- Overlay: 116.68 MiB (占文件 99.9%), 头部 `de ad be ef "NullsoftInst"` (NSIS 魔数)
- 内部包含 5649 处 zlib 特征(NSIS Deflate 压缩块)

## 4. 安装器内部结构 [CONFIRMED]

| 路径 | 大小 | 说明 |
|---|---|---|
| `$PLUGINSDIR/app-64.7z` | 121,712,724 | **主载荷**(7z, LZMA2/BCJ2, 32 blocks) |
| `$R0/Uninstall XingLu.exe` | 267,670 | 卸载程序(名称含 XingLu) |
| `$PLUGINSDIR/System.dll` | 6,931 | NSIS 标准插件 |
| `$PLUGINSDIR/UAC.dll` | 8,018 | NSIS 标准插件(权限提升) |
| `$PLUGINSDIR/StdUtils.dll` | 45,608 | NSIS 标准插件 |
| `$PLUGINSDIR/nsDialogs.dll` | 4,684 | NSIS 标准插件(自定义对话框) |
| `$PLUGINSDIR/nsProcess.dll` | 2,027 | NSIS 标准插件(进程检查) |
| `$PLUGINSDIR/nsis7z.dll` | 242,382 | NSIS 标准插件(7z 解压) |
| `$PLUGINSDIR/WinShell.dll` | 1,080 | NSIS 标准插件(快捷方式) |
| `$PLUGINSDIR/nsExec.dll` | 3,299 | NSIS 标准插件(执行命令) |
| `$PLUGINSDIR/modern-wizard.bmp` | 1,899 | 安装向导位图 |

**结论**: NSIS 脚本把 `app-64.7z` 作为载荷,安装时用 `nsis7z.dll` 解压到安装目录。

## 5. 产品身份线索

- `Uninstall XingLu.exe` → 软件名 XingLu [CONFIRMED]
- 打包时间戳 2026-08-07 13:26 → 与 "latest" 命名一致 [HIGHLY_LIKELY]

## 6. 判定汇总

- 安装器: NSIS 3 Unicode,32 位 stub [CONFIRMED]
- 主程序架构: x64(Electron,见 02 报告) [CONFIRMED]
- 签名: 无 [CONFIRMED]
- 域名 xushilu.cn 出现在 app-update.yml(见 02 报告) [CONFIRMED]
