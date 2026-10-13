<div align="center">

# 岛影

**Dynamic Island Gradient**

给壁纸顶部加一层渐变蒙版，让 iPhone 的灵动岛和状态栏自然融进画面。

[![License: MIT](https://img.shields.io/badge/License-MIT-8a63d2.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()
[![No Network](https://img.shields.io/badge/network-none-blue.svg)]()
[![Single File](https://img.shields.io/badge/build-one%20HTML%20file-orange.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

简体中文 · [English](README.en.md)

<img src="screenshots/hero.jpg" width="880" alt="岛影效果：两张真实壁纸放进 iPhone 17 Pro Max 官方机身，顶部渐变已与灵动岛融合">

</div>

---

> **名字的来历**：壁纸顶部那层暗部，像水面给画面投下的影子；灵动岛融进去，
> 就像它本来就在照片里。「岛影」也谐音「倒影」。

---

## 问题是这样的

iPhone 14 Pro 之后，屏幕顶部多了「灵动岛」—— 一块永久的黑色药丸。

如果你用一张明亮的照片当锁屏，顶部那块黑色硬件就会**硬生生切**在画面里。苹果自己的壁纸会做顶部压暗处理，你自己下的图不管。

**岛影只做一件事**：在壁纸顶部盖一层从实到透的渐变。

```
┌──────────────┐         ┌──────────────┐
│  天空          │         │▒▒▒▒▒▒▒▒▒▒▒▒▒▒│  ← 纯色区，盖住灵动岛
│              │         │▒▒▒▒▒▒▒▒▒▒▒▒▒▒│
│              │   ──►   │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  ← 过渡区
│   山  ⛰️       │         │   山  ⛰️      │  ← 原图一个像素都不动
└──────────────┘         └──────────────┘
```

下面是两张**真机比例**的效果对比 —— 左：原图，黑色灵动岛硬生生切在画面里；右：处理后，顶部渐变把它融进画面，连锁屏时间都看得更清了。

<img src="screenshots/compare-portrait.jpg" alt="海边人像：左为原图，顶部亮蓝色天空让灵动岛格外突兀；右为处理后，渐变让灵动岛融进画面">

<img src="screenshots/compare-rain.jpg" alt="雨夜街景：左为原图，右为处理后">

> 示例机身取自 Apple Design Resources（iPhone 17 Pro Max），仅用于效果演示。
> 该机身图片版权归 Apple Inc. 所有，不在本项目的 MIT 许可范围内。

界面直接拖动分割线就能对比前后：

<img src="screenshots/desktop-dark.png" alt="界面截图">

说明书也内嵌在里面，点一下从右侧滑出（不用联网、不用另开文件）：

<img src="screenshots/manual-drawer.png" width="620" alt="内置说明书">

---

## 怎么用

**不用装、不用配、不用联网。Windows、Mac、Linux 通吃，整个程序就是一个文件。**

| 系统 | 怎么开 | 说明 |
|---|---|---|
| **Windows** | 双击 `index.html` | 如果被记事本打开了，改用右键 →「打开方式」→ 你的浏览器；或者双击 `启动.bat` |
| **macOS** | 双击 `index.html` | 默认浏览器直接打开。想要手机同 WiFi 访问，双击 `启动.command` |
| **Linux** | 双击 `index.html` | 或 `xdg-open index.html` |

然后：

1. 把壁纸拖进页面（或点一下选文件，或按 `Ctrl+V` / `⌘V` 粘贴）
2. 左右拖动中间的白色分割线，对比处理前后
3. 点「下载壁纸」，传到 iPhone 设为锁屏

> 说明书也内置在里面了，点顶栏的「说明书」按钮随时看。
> 这一个文件可以随便拷到 U 盘、发微信、放到任何电脑上，双击即用 —— **不需要旁边的任何文件**。

### 支持的浏览器

Chrome / Edge / Safari / Firefox 等所有现代浏览器都可以，**桌面和手机都行**。

> 唯一的例外：**HEIC 格式**的照片，Chrome / Edge / Firefox 解不开（Safari 可以）。
> 遇到会明确提示，不会静默失败。转成 JPG 即可。

---

## 功能

| 功能 | 说明 |
|---|---|
| **三种渐变颜色** | 纯黑 / 同色采样（自动取壁纸顶部均色）/ 自定义颜色 |
| **覆盖强度** | 0~100%，可以只「压暗」不完全盖住 |
| **两段式高度控制** | 纯色区高度 + 渐变结束高度，都用百分比（自动换算成当前图的像素值） |
| **四种过渡曲线** | 缓出 / 线性 / 缓入 / S 型，配实时曲线缩略图 |
| **拖动对比** | 分割线随鼠标 / 手指 / 方向键移动，左右对照原图与处理后 |
| **锁屏实机预览** | 宽屏时旁边模拟一台 iPhone 锁屏，时间是真实时间 |
| **灵动岛参考框** | 虚线标出灵动岛与状态栏安全区的参考位置 |
| **抗色带噪点** | 极细噪点打散深色渐变在 OLED 上的色带 |
| **参数记忆** | 上次调的值下次还在（存浏览器本地） |
| **不缩图导出** | JPEG / PNG，按原分辨率输出，文件名带参数 |
| **深浅色主题** | 跟随系统，也可手动切换 |

### 支持的输入方式

拖拽 · 点选 · `⌘V` 粘贴剪贴板 · 自带示例图

---

## 隐私

这类工具最该讲清楚的就是这个。

- **无网络请求**。代码里没有一行 `fetch` / `XMLHttpRequest` / `WebSocket`，也没有任何外部资源（字体、图标库、统计脚本统统没有）。
- **图片不上传、不落盘**。全程在浏览器内存里处理，关掉标签页就没了。图片内容不会被写入任何存储。
- **只记参数**。你的滑杆设置存在浏览器 `localStorage`，随时可在浏览器设置里清掉。
- **可审计**。整个工具就是一个 `index.html`，用文本编辑器打开就能从头读到尾。

**你可以断网使用，效果完全一样。**

---

## 技术说明

<details>
<summary>为什么它拖动滑杆不卡（点开看）</summary>

多数同类工具的做法是 `getImageData` → 逐像素 `for` 循环 → `putImageData`。
一张 iPhone 壁纸是 1320×2868 ≈ **380 万个像素**，每次滑杆移动都要跑一遍这个循环，必然掉帧。

这里换了个路子：

1. 把过渡曲线**离散成 64 个色标**，交给 `createLinearGradient()` —— 合成由浏览器（GPU）完成；
2. 只对画布做**两次 `drawImage` + 一次 `fillRect`**，无论图片多大，开销都接近常数；
3. 「同色采样」用 `drawImage` 把目标区域缩放到 **1×1 像素** 再读回 —— 缩放本身就是一次 box 平均，比 JS 循环求和快几十倍；
4. 拖动时用 `requestAnimationFrame` 合并重绘，一帧最多画一次。

结果：1320×2868 的原图上拖滑杆是实时的。

</details>

<details>
<summary>正确性验证</summary>

无头 Chrome 自检覆盖以下断言：

- 顶部纯色区像素值 == 设定基色
- 「渐变结束高度」以下的像素与原图**逐字节一致**
- 导出 blob 类型 / 体积正常
- 桌面 1440px 与手机 390px 视口均无横向溢出、无 JS 报错

</details>

---

## 文件结构

```
DynamicIslandGradient/
├── index.html            ← 全部东西都在这里（单文件，双击即用，三平台通吃）
├── 启动.bat               ← Windows 双击入口（万一 html 被记事本抢走关联时用）
├── 启动.command           ← macOS 双击入口（也可起本地服务器给手机访问）
├── 使用说明.html          ← 同一份说明书的独立网页版（在线阅读方便）
├── help.html             ← 说明书英文名副本，手机上好输网址
├── README.md / README.en.md
├── CHANGELOG.md
├── LICENSE               ← MIT
├── docs/
│   ├── 使用说明.md         ← 说明书内容源（唯一）
│   ├── build_help.py     ← md → html + 注入 index.html（零依赖）
│   ├── 生成说明书.command   ← 双击重新生成说明书
│   └── 版本说明.md
└── screenshots/
```

**只有 `index.html` 是必需的，其他都是给你看/给你改的。**

---

## 常见问题

**Q：Windows 上双击打不开 / 打开了记事本？**
说明这台电脑把 `.html` 关联给了文本编辑器。三种解法任选：
① 右键 `index.html` →「打开方式」→ 选 Chrome / Edge，勾上「始终使用」；
② 双击同目录的 `启动.bat`（它会用系统默认浏览器打开）；
③ 把 `index.html` 直接拖进浏览器窗口。

**Q：导出的图会不会被压缩、变小？**
不会。导出就是原图分辨率，一个像素都不缩。JPEG 画质默认 95%，可以在面板里调。

**Q：HEIC 打不开？**
Chrome / Edge / Firefox 都解不了 HEIC，只有 Safari 可以。工具会明确提示，不会静默失败 —— 先转成 JPG 即可。

**Q：手机上能用吗？**
能。两个办法：① 把 `index.html` 存进 iCloud / 网盘，用手机浏览器打开；
② 电脑上双击 `启动.command`（macOS），手机连同一个 WiFi，访问终端显示的地址。布局已做移动端适配。

**Q：为什么「同色采样」的颜色有时候不太对？**
采样取的是图片最顶部中间三分之一的平均色。如果壁纸顶部正好有个深色物体，采样会被带偏 —— 这时改用「纯黑」或「自定义颜色」更稳。

---

## 开发与自检

改 `index.html` 里的 CSS 变量即可换配色，改 `const DEFAULTS` / `const PRESETS` 换默认参数，浏览器刷新就生效 —— 没有构建步骤，没有 npm，没有 node_modules。

说明书改 `docs/使用说明.md`，然后：

| 系统 | 重新生成 |
|---|---|
| Windows | 双击 `docs/生成说明书.bat` |
| macOS | 双击 `docs/生成说明书.command` |
| 任意 | `python3 docs/build_help.py` |

它会一次做三件事：生成独立网页版 `使用说明.html` + `help.html`，并注入 `index.html` 的内嵌说明书。**内容源只有 md 一份**，重复执行结果字节一致。

---

## License

MIT © [js-ping](https://github.com/js-ping)
