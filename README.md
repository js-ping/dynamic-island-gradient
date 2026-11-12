# 岛影 · Island Fade

给 iPhone 壁纸顶部加一层渐变，让灵动岛和状态栏自然融进画面。

单文件 HTML，双击就用 · Mac / Windows / Linux · 不上传、不联网 · MIT

**下载**：<https://github.com/js-ping/dynamic-island-gradient/releases>

---

## 做什么

iPhone 的灵动岛是黑的，放在浅色壁纸上会「贴」在画面里。岛影在图片顶部压一层渐变暗部，
灵动岛就变成了画面的一部分。

- 四种过渡曲线（线性 / ease-out / ease-in-out / 指数），带实时曲线图
- 可拖动的分割线对比原图；宽屏右侧有锁屏实机预览
- 抗色带噪点、画质选择、参数记忆、剪贴板导入
- 导出 1:1 原分辨率 JPEG，文件名带上参数
- 纯前端，**网络请求 0 条**

## 两个下载版本

| 文件 | 大小 | HEIC |
|---|---|---|
| `Daoying-v2.2.1-full-heic.html` | 2.1 MB | **内置解码器，任何浏览器都能开**（推荐） |
| `Daoying-v2.2.1-single-file.html` | 74 KB | 靠浏览器自带能力，只有 Safari 能解 |

为什么有两种：HEIC 里是 HEVC，被专利池覆盖，Chrome / Edge / Firefox 都刻意不内置解码器。
完整版把开源解码器（libheif-js，LGPL-3.0）内联进文件，所以体积大 2 MB，但换任何浏览器都不卡壳。

## 用法

1. 下载 html，双击。
2. 拖一张壁纸进去。
3. 拖顶部那条分割线调高度，选曲线，导出。

> 手机上想用：把文件放进 iCloud 云盘，用 Safari 打开即可（HEIC 建议用完整版）。

## 从源码构建

```bash
python3 docs/build_help.py      # md → 说明书，注入 index.html
python3 tools/build_full.py     # 生成带内置解码器的完整版 → dist/
```

## 说明

- 许可证：主体 MIT；完整版里内联的解码器为 LGPL-3.0，两份许可证全文都随文件走。
- HEVC 本身涉及 MPEG-LA / Access Advance 专利池，本项目不提供专利许可，商用前请自行评估。
- 曾经的在线版（网页托管）已撤下：只要页面靠浏览器解码，HEIC 那个坑就会再踩一次。
