# 01 — Design System

> 全部数值 [RUNTIME_CONFIRMED]，直接提取自 `rendererApp-B0uB3ajR.css` 变量定义与样式规则。
> 语义 token 命名由本审计整理（原 CSS 使用 `--nf-color-*` 等真实变量名，未改名）。
> 双值 = light 值在前 / dark 值在后（`:root` 默认 light，`:root[data-theme=dark]` 覆盖）。

## 1. Colors（语义 token + 真实值）

### Surfaces

| 语义 | 变量 | light | dark | 用途 |
|---|---|---|---|---|
| --surface-app | `--nf-color-surface-bg` | `#f6f1e9` | `#1f1d1b` | 应用底层背景 |
| --surface-canvas | `--nf-color-surface-canvas` | `#fcf9f4` | `#23201e` | 画布/卡片内层 |
| --surface-panel | `--nf-color-surface-panel` | `#fffdf9` | `#282522` | 面板/卡片 |
| --surface-soft | `--nf-color-surface-soft` | `#faf6ef` | `#2e2a26` | 柔和次级面 |
| --surface-elevated | `--nf-surface-elevated` | (var 引用) | (var 引用) | 抬升层 |
| --surface-chief-panel | `--nf-color-chief-panel-bg` | `#fcf9f4` | `#25221f` | 总编面板 |
| --surface-field | `--nf-skin-field-bg` | `#fffdf9dc` | `#24211f` | 输入字段 |
| --surface-window | `--nf-color-window-bg` | `#22201e`(d) / `#fffdf9`(l) | — | 窗口底色 |
| --surface-muted-card | `--nf-skin-muted-card-bg` | `#fcf8f3` | `#25221f` | 弱化卡片 |
| --surface-hover | `--nf-skin-hover-bg` | `#fcf6ef` | `#332e2a` | 悬停面 |
| --surface-active | `--nf-skin-index-active-bg` | `#f2e8e0` | `#332a25` | 选中面 |
| --surface-drop | `--nf-skin-drop-bg` | `#f4ece4` | `#332a25` | 拖放目标面 |

### Text

| 语义 | 变量 | light | dark |
|---|---|---|---|
| --text-primary | `--nf-color-text-primary` | `#2d2722` | `#eee8e1` |
| --text-secondary | `--nf-color-text-secondary` | `#70675f` | `#c5bbb2` |
| --text-tertiary | `--nf-color-text-tertiary` | `#797069` | `#a3988f` |
| --text-muted | `--nf-color-text-muted` | `#746c65` | `#a79f97` |
| --text-meta | `var(--nf-color-text-tertiary)` | 同 tertiary | 同 tertiary |
| --text-placeholder | `var(--nf-color-text-tertiary)` | 同 tertiary | 同 tertiary |
| --text-disabled | `var(--nf-color-text-muted)` | 同 muted | 同 muted |
| --text-inverse | `--nf-skin-inverse-text` | `#241c18` | `#fff` |
| --text-inverse-muted | `--nf-color-text-inverse-muted` | (var 引用) | (var 引用) |
| --icon-muted | `--nf-skin-icon-muted` | `#84786f` | `#a3988f` |

### Border / Divider

| 语义 | 变量 | light | dark |
|---|---|---|---|
| --border-subtle | `--nf-color-border-subtle` | `#e8dfd6` | `#fff4e812`（12% 白） |
| --border-strong | `--nf-color-border-strong` | `#d7c9bd` | `#fff4e81a`（16% 白） |
| --border-inverse-subtle | `--nf-color-border-inverse-subtle` | `#241c183d` | `#f0e8df` |
| --skin-control-border | `--nf-skin-control-border` | `#e8dfd6` | `#fff4e812` |
| --skin-hover-border | `--nf-skin-hover-border` | `#dccdc1` | `#fff4e81a` |
| --skin-editor-border | `--nf-skin-editor-border` | `#e8dfd6` | `#fff4e812` |
| --skin-window-border | `--nf-skin-window-border` | `#e4d9ce` | `#fff4e812` |

### Accent（暖棕系主色）

| 语义 | 变量 | light | dark |
|---|---|---|---|
| --accent-primary | `--nf-color-primary` | `#6f5140` | `#b8896f` |
| --accent-active | `--nf-color-active` | `#9c745d` | `#b8896f` |
| --accent-active-text | `--nf-color-active-text` | `#6f4935` | `#c99a7f` |
| --accent-active-soft | `--nf-color-active-soft` | `#f4ede8` | `#b8896f24` |
| --accent-active-border | `--nf-color-active-border` | `#d7c2b4` | `#b8896f61` |
| --accent-hover | `--nf-skin-primary-hover` | `#c99a7f` | `#5d4132` |
| --surface-inverse | `--nf-color-surface-inverse` | `#6f5140` | `#b8896f` |

### Status

| 语义 | 变量 | light | dark |
|---|---|---|---|
| --danger | `--nf-color-error` | `#d94444` | `#dc887c` |
| --danger-soft | `--nf-color-error-soft` | `#ffe3e3` | `#3b2725` |
| --danger-text | `--nf-color-error-text` | `#8f2020` | `#efb0a8` |
| --done（完成态） | `--nf-color-done` | `#6f5140` | `#b8896f` |
| --done-soft | `--nf-color-done-soft` | `#f2ece7` | `#332823` |
| --done-text | `--nf-color-done-text` | `#5a4032` | `#d8b29d` |
| --done-border | `--nf-color-done-border` | `#d6c8bd` | `#6b4d3e` |
| --wait（等待态） | `--nf-color-wait` | `#b28a57` | `#c9a363` |
| --wait-text | `--nf-color-wait-text` | `#7a4b10` | `#e4c58f` |

### Window 控制色（仿 macOS 交通灯）

| 语义 | 值 |
|---|---|
| --window-close | `#f97066`（红） |
| --window-minimize | `#f5c04f`（黄） |
| --window-maximize | `#55c27a`（绿，light）/ `#b8896f`（dark） |

### Overlay / Backdrop

| 语义 | 值 |
|---|---|
| modal backdrop（分支对话框） | light `#2f241b38` / dark `#0000006b` |
| overlay 遮罩 | `--nf-skin-...` 半透明层，见 14_DIALOGS |
| 材质 overlay | `--nf-material-overlay-default` light `#fffdf9ad` / dark `#fff4e80a` |
| 材质 overlay-hover | light `#6f51400f` / dark `#fff4e812` |
| 材质 overlay-selected | light `#6f51401a` / dark `#b8896f24` |

### 氛围层（App 背景彩色氛围）

| 变量 | light | dark |
|---|---|---|
| `--nf-skin-atmosphere-cool` | `#6cbeb50e` | `transparent` |
| `--nf-skin-atmosphere-warm` | `#e1a45b0f` | `transparent` |
| `--nf-skin-atmosphere-paper` | `#fffdf880` | `transparent` |

## 2. Radius（主设计系统）

| 语义 | 变量 | 值 | 用途证据 |
|---|---|---|---|
| --radius-window | `--nf-radius-window` | **16px** | 对话框/大型容器 |
| --radius-app-window | `--nf-app-window-radius` | **8px**（CSS）/ 18px（index.html 启动屏 fallback） | 窗口整体圆角 |
| --radius-card | `--nf-radius-card` | **14px** | 卡片 |
| --radius-control | `--nf-radius-control` | **11px** | 按钮/控件 |
| --radius-input | `--nf-radius-input` | **16px** | 输入框 |
| --radius-panel | `var(--nf-radius-window)` | 16px | 面板 |
| --radius-pill | `--nf-radius-pill` | **999px** | 徽章/胶囊/segmented |
| 实际使用分布 | — | 999px×107 / 8px×67 / 12px×34 / 10px×29 / 6px×21 / 7px×19 / 9px×17 / 14px×15 / 18px×9 / 11px×9 / 16px×4 | 全套出现频率 |
| chat-composer | — | **20px**（大圆角输入容器） | [RUNTIME_CONFIRMED] 样式规则 |

## 3. Shadows（材质系统）

| 语义 | 变量 | light | dark |
|---|---|---|---|
| --shadow-control | `--nf-shadow-control` | `0 8px 20px -16px #0000003d` | `0 8px 20px -22px var(--nf-skin-panel-shadow)` |
| --shadow-card | `--nf-shadow-card` = `--nf-material-shadow-card` | `0 12px 30px -26px #3e332c47` | `0 14px 36px -26px #0000003d` |
| --shadow-panel | `--nf-shadow-panel` | `0 18px 44px -38px #3e332c40` | `0 24px 60px -28px #0000004d` |
| --shadow-popover/menu | `--nf-material-shadow-menu` | `0 18px 42px -30px #3e332c40` | `0 24px 54px -30px #0000004d` |
| --shadow-window | `--nf-material-shadow-window` | `0 24px 64px -40px #3e332c45` | `0 28px 72px -24px #0000005c` |
| --shadow-active-agent | `--nf-shadow-active-agent` | `0 16px 32px -24px #6f514073` | `0 16px 32px -24px #0000004d` |
| --shadow-focus | `--nf-shadow-focus` | `0 0 0 3px #b8896f24` | `0 0 0 3px color-mix(primary 18%)` |
| 分支对话框内层高光 | `--nf-branch-dialog-shadow` | `inset 0 1px 0 #ffffffc7, 0 10px 28px -24px #4b382c57` | `var(--nf-material-shadow-card)` |

规律：阴影一律为**大模糊半径 + 大负扩散**（-24~-40px），形成柔和的"浮起"而非深投影；浅色主题用暖棕半透明（#3e332c 系），深色主题用黑色半透明。

## 4. Typography

| 语义 | 变量 | 值 |
|---|---|---|
| --font-sans | `--nf-font-sans` | `"OPPO Sans 4.0 Embedded", "OPPO Sans 4.0", "OPPO Sans", "Microsoft YaHei", "PingFang SC", sans-serif` |
| --font-mono | `--nf-font-mono` | `"SFMono-Regular", Consolas, "Liberation Mono", monospace` |

> 字体为第三方商业字体，**禁止复制/分发**；重建时仅记录 fallback 链，改用等效开源字体（如思源黑体）+ 相同字号层级。

### 字号层级（--nf-type-*）

| token | 值 | 用途 |
|---|---|---|
| --nf-type-micro | 11px | 角标/工具提示 |
| --nf-type-caption | 12px | 说明文字（160 次引用） |
| --nf-type-toolbar | 13px | 工具栏文字 |
| --nf-type-dense-menu-copy | 13px | 密集菜单正文 |
| --nf-type-compact | 14px | 紧凑文本（180 次引用，主力） |
| --nf-type-dense-menu-title | 15px | 密集菜单标题 |
| --nf-type-ui | 15px | UI 常规（81 次） |
| --nf-type-body | 16px | 正文（39 次） |
| --nf-type-reading | 17px | 阅读文本 |
| --nf-type-chapter-editor-reading | var(--nf-type-reading) | 编辑器阅读字号 |
| --nf-type-subtitle | 18px | 副标题 |
| --nf-type-heading | 19px | 标题 |
| --nf-type-title | 20px | 大标题 |
| --nf-type-dialog-title | 21px | 对话框标题 |
| --nf-type-display | 27px | 展示级（品牌/大数字） |

## 5. Spacing

gap 实际分布（真实 CSS 统计，全部出现值）：**2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18**（单位 px），主力区间 4–12px：
`8px×103` / `10px×73` / `12px×69` / `6px×66` / `7px×61` / `5px×58` / `4px×46` / `14px×28` / `16px×12`

padding 主力：`0 8px` / `0 10px` / `0 12px` / `10px` / `10px 12px` / `12px` / `14px`。

间距系统特征：**步进 1px 的细粒度间距**（非标准 4/8 体系），密度高；水平 padding 常用 8-14px，卡片内 12-14px。

## 6. Controls（尺寸与状态）

### 控件高度

| token | 值 | 用途 |
|---|---|---|
| --nf-control-height-dense | 28px | 最密 |
| --nf-control-height-compact | 30px | 紧凑 |
| --nf-control-height-toolbar | 32px | 工具栏 |
| --nf-control-height-prominent | 34px | 主要 |
| --nf-control-height-standard | 36px | 标准 |
| --nf-control-height-dialog | 38px | 对话框内 |

### 图标

| token | 值 |
|---|---|
| --nf-icon-size-compact | 14px |
| --nf-icon-size-control | 15px |

### 滚动条（自定义）

| token | 值 |
|---|---|
| 宽度 | 10px |
| thumb | `color-mix(border-strong 52%, transparent)` / dark `#fff4e824` |
| thumb-hover | `color-mix(primary 66-72%, border-strong)` |
| thumb-active | `var(--nf-color-primary)` |
| track | transparent |

### 控件视觉要点 [RUNTIME_CONFIRMED]

- **按钮**：radius 11px，高 28-38px，hover 用 `--nf-skin-hover-bg`，主按钮 accent 填充 + `--accent-hover`；focus ring = `--nf-shadow-focus`（3px 主色 18-24% 透明度外圈）
- **输入框**：radius 16px（--nf-radius-input），field 背景 + `--nf-shadow-control`，聚焦时 `--nf-shadow-focus`
- **segmented control**：胶囊形（999px），选中态用 `--accent-active-soft` 面 + `--accent-active-text`（证据：chief-appearance-mode-switcher / chief-interface-scale-switcher 类）
- **chat-composer**：radius **20px**，`inset 0 1px 0 #ffffffeb`（顶部内高光）+ 双外阴影，背景 = panel 渐变 + 顶部白色渐隐，padding `8px 12px 8px 8px`，grid 布局，gap 8px [RUNTIME_CONFIRMED]
- **滚动条**：10px 主色，hover/active 加深
- **tooltip/badge**：pill 999px、micro 11px 字号

### 动效

| token | 值 |
|---|---|
| --nf-ease-standard | `cubic-bezier(.2,.8,.2,1)` |
| 过渡时长分布 | 0.16s / 0.18s / 0.2s（控件）/ 360ms（启动屏入场） |

## 7. 证据等级说明

- 全部 token 数值 [RUNTIME_CONFIRMED]（CSS 变量定义原文）
- 用途推断（"卡片/按钮"）基于类名与选择器上下文 [RUNTIME_CONFIRMED + INFERRED 混合]，关键处单独标注
- 交互状态（hover/active/disabled）中 hover/active 有 CSS 证据；disabled 部分有 token（--text-disabled）但完整规则 [UNKNOWN]，见 18
