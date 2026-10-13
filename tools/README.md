# tools —— 为什么会有这个目录

岛影发布**两种形态**，功能一模一样，只差一件事：能不能解 HEIC。

| | 源码版 | 完整版 |
|---|---|---|
| 文件 | `index.html` | `dist/Daoying-full-heic.html` |
| 大小 | 约 70 KB | 约 2 MB |
| HEIC（iPhone 相机默认格式） | 靠浏览器自带能力 —— 只有 Safari 能解 | 内置开源解码器，**任何浏览器都能解** |
| 许可证 | 纯 **MIT** | MIT + LGPL-3.0（仅解码器那一段） |
| 在哪 | 仓库里，是唯一需要维护的源文件 | 由构建脚本拼出来，发布到 Releases，不进版本库 |

## 为什么要分成两份

HEIC 里装的是 **HEVC** 编码，而 HEVC 有专利授权成本。Chrome、Edge、Firefox 都因此
**刻意没有内置** HEVC 解码器（这也是它们把钱押在免授权的 AVIF 上的原因），
只有 Safari 靠 macOS / iOS 的系统解码能力能读。

岛影的目标用户素材几乎全在 iPhone 上，**默认就是 HEIC** —— 一打开先撞一次「解不开」，
等于把路堵死。所以要自带解码能力。

但把 2 MB 的 LGPL 代码硬塞进 MIT 的主文件里，对克隆仓库的人来说是负担：
仓库变重、许可证变复杂、想读源码的人要先翻过 200 万字符的 wasm 字面量。
分成「干净的源 + 拼装出来的成品」两边都舒服：**仓库保持轻、纯、可读，用户拿到的成品开箱即用。**

## 怎么构建

```bash
python3 tools/build_full.py                 # 产出 dist/Daoying-full-heic.html
python3 tools/build_full.py --check         # 只校验，不写文件
python3 tools/build_full.py --out 自定义路径.html
```

双击入口：`生成完整版.command`（macOS）/ `生成完整版.bat`（Windows）。

只需要 Python 3 标准库，不用 pip 装任何东西。构建是**幂等**的 —— 反复跑，产物字节一致。

构建脚本每次都做这些检查，任何一条不过就直接失败：

- 解码器里不能有 `</script`（否则拼进 HTML 会提前闭合脚本标签）；
- 必须有内联的 `wasmBinary`（否则会把 `.wasm` 当成外部文件去下载，单文件就废了）；
- 不能有 `WebSocket` / `sendBeacon` / `instantiateStreaming`（真联网的迹象）；
- 解码器里必须有 `libheif`、`HeifDecoder` 这两个符号；
- 两份许可证里不能有 `</script` 或 `-->`。

## 文件清单

| 文件 | 作用 |
|---|---|
| `build_full.py` | 拼装脚本，唯一干活的东西 |
| `生成完整版.command` / `.bat` | 双击入口 |
| `vendor/libheif-bundle.js` | HEIC 解码器（libheif 的 WebAssembly 构建，wasm 已内联） |
| `vendor/LICENSE-libheif.txt` | libheif 的许可证，构建时被内联进产物 |
| `vendor/LICENSE-libheif-js.txt` | npm 外壳的许可证，同上 |
| `vendor/README.md` | 出处、版本、SHA-256、升级步骤 |

## 拼装结果长什么样

在 `index.html` 里有一对标记：

```html
<!-- DECODER:BEGIN 自动生成区 · 勿手改 · 由 tools/build_full.py 注入 HEIC 解码器 -->
<!-- DECODER:END -->
```

构建脚本把这两行之间的内容换掉，注入两样东西：

1. `<script id="heif-decoder">` —— 解码器本体；
2. `<script type="text/plain" id="license-lgpl3">` —— 两份 LGPL 许可证全文，
   用 `type="text/plain"` 是为了让它**不执行、只随文件传播**。这样那个单文件
   被单独转发出去时，许可证是跟着走的，不缺文件。

`index.html` 里与解码器相关的代码全部由 `HAS_HEIF` 这个常量兜着：

```js
const HAS_HEIF = typeof window.libheif === 'function';
```

解码器不在时它是 `false`，所有与 HEIC 有关的分支都不会进入 ——
**源码版的行为与加这一整块功能之前完全一致**。
