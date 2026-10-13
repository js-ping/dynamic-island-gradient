# 第三方解码器（vendored）

这个目录里的东西**不是本项目的代码**，是为了让 HEIC 照片在 Chrome / Edge / Firefox
里也能打开，而从上游原样搬过来的。它单独只被 `tools/build_full.py` 用一次：
拼进「完整版」单文件产物里。

## 里面是什么

| 文件 | 是什么 |
|---|---|
| `libheif-bundle.js` | libheif 的 WebAssembly 构建，wasm 已 base64 内联，2.0 MB，浏览器可直接 `<script>` 引入 |
| `LICENSE-libheif.txt` | libheif 本身的许可证（LGPL-3.0，外加一段说明：示例程序和 Go/C++ 封装是 MIT） |
| `LICENSE-libheif-js.txt` | npm 包 `libheif-js` 外壳的许可证（LGPL-3.0） |

## 来源与校验

| 项 | 值 |
|---|---|
| npm 包 | `libheif-js` |
| 版本 | **1.23.5** |
| 包内路径 | `libheif-wasm/libheif-bundle.js` |
| 许可证 | **LGPL-3.0**（libheif 内嵌的 HEVC 解码器 libde265 同样是 LGPL） |
| 上游仓库 | <https://github.com/catdad-experiments/libheif-js> |
| libheif 上游 | <https://github.com/strukturag/libheif> |
| SHA-256 | `074b2b55ef3de477ba9f794ca381f3f0324c1cba8c91b4af07395f39c22d54cc` |
| 大小 | 2,044,206 字节 |

`tools/build_full.py` 每次构建都会打印这个文件的 SHA-256，和上表核对即可确认没人动过。

## 为什么选 `libheif-wasm` 而不是别的变体

`libheif-js` 包里一共有三种构建：

| 变体 | 大小 | 情况 |
|---|---|---|
| `libheif/libheif.js` | 3.19 MB | 纯 JS（asm.js），最慢 |
| `libheif-wasm/libheif.js` + `libheif.wasm` | 91 KB + 1.46 MB | 快，但是**两个文件**，不适合单文件分发 |
| **`libheif-wasm/libheif-bundle.js`** | **2.04 MB** | 快，wasm 已内联，**一个文件** ← 用它 |

## 这个文件是干净的吗

是。构建脚本每次都会检查，结论记在这儿：

- 全文不含 `</script`（否则拼进 HTML 会把脚本标签提前闭合）；
- 不含 `fetch(` / `XMLHttpRequest` / `WebAssembly.instantiateStreaming` —— **不发起任何网络请求**，
  wasm 以 base64 明文字面量内联，由 `WebAssembly.instantiate` 就地编译。这一点对得上说明书里
  「断网可用」的承诺；
- 不含 `<script src=` 之类的外部资源引用。

## 怎么自己更新到新版

```bash
npm install libheif-js@<新版本> --no-save
cp node_modules/libheif-js/libheif-wasm/libheif-bundle.js   tools/vendor/
cp node_modules/libheif-js/libheif-wasm/LICENSE             tools/vendor/LICENSE-libheif.txt
cp node_modules/libheif-js/LICENSE                          tools/vendor/LICENSE-libheif-js.txt
shasum -a 256 tools/vendor/libheif-bundle.js              # 更新下面文档里的哈希
```

然后**务必**在真机浏览器里重跑一遍 HEIC 用例：Chrome 里打开完整版，拖一张 iPhone 原图进去，
确认能出图、尺寸对得上。`libheif` 是上游项目，改版可能动 API。

## 许可证要留意的事

- 这几个文件是 **LGPL-3.0**，不是本项目的 MIT。用「完整版」的人拿到的是
  两段代码的**拼装结果**，因此完整版整体按 **MIT + LGPL-3.0（仅解码器部分）** 理解。
- 构建脚本会把两份许可证全文**内联进产物**（HTML 注释里），所以那个单文件本身
  就带齐了许可证，单独转发出去也不缺文件。
- 仓库里的 `index.html`（干净源码）**不含**这些代码，仍然是纯 MIT。
- libheif 自己**不带** HEVC 解码以外的专利许可。HEVC 涉及 MPEG-LA / Access Advance
  两个专利池 —— 这是 Google、Mozilla 当初不内置 HEVC 的同一个原因，
  也是这个项目选择「让用户自己决定要不要带解码器」而不是硬塞进主文件的原因。
