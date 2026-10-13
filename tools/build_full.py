#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把干净的 index.html 与内联 HEVC 解码器拼成「完整版」单文件。

用法：
    python3 tools/build_full.py                    # 输出到 dist/Daoying-full-heic.html
    python3 tools/build_full.py --out 某个路径.html
    python3 tools/build_full.py --check            # 只做校验，不写文件

设计要点：
  · index.html 永远是干净的 70 KB 源码，不带任何 LGPL 代码 —— 仓库保持纯 MIT；
  · 解码器只在「完整版」存在，是分发给普通用户的那个文件；
  · 拼装是幂等的：反复跑，产物字节一致。
"""

import argparse
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
VENDOR = ROOT / "tools" / "vendor"
BUNDLE = VENDOR / "libheif-bundle.js"
LICENSE_LIBHEIF = VENDOR / "LICENSE-libheif.txt"
LICENSE_WRAPPER = VENDOR / "LICENSE-libheif-js.txt"
DEFAULT_OUT = ROOT / "dist" / "Daoying-full-heic.html"

# 上游版本（换了版本记得同步改 tools/vendor/README.md）
VENDOR_NAME = "libheif-js"
VENDOR_VERSION = "1.23.5"
VENDOR_UPSTREAM = "https://github.com/catdad-experiments/libheif-js"
BUNDLE_SHA256 = "074b2b55ef3de477ba9f794ca381f3f0324c1cba8c91b4af07395f39c22d54cc"

BEGIN_RE = re.compile(r"<!-- DECODER:BEGIN.*?-->.*?<!-- DECODER:END -->", re.S)


def die(msg: str) -> None:
    print("✗ " + msg, file=sys.stderr)
    sys.exit(1)


def read(path: pathlib.Path) -> str:
    if not path.exists():
        die("找不到 " + str(path))
    return path.read_text(encoding="utf-8")


def check_vendor(bundle: str, licenses: str) -> str:
    """解码器自身必须满足的前提。返回 SHA-256。"""
    if "</script" in bundle.lower():
        die("解码器里出现了 </script，拼进 HTML 会提前闭合脚本标签 —— 需要转义后再注入")

    if len(bundle) < 1_000_000:
        die(f"解码器只有 {len(bundle)} 字节，像是没下全")
    if len(bundle) > 4_000_000:
        die(f"解码器有 {len(bundle)} 字节，比预期大很多，确认一下是不是拿错了变体")

    for name in ("libheif", "HeifDecoder"):
        if name not in bundle:
            die(f"解码器里找不到 {name}，文件可能不对")

    # ---- 联网与外部资源：说明书里承诺了「断网可用」，这几条必须挡住 ----
    if "instantiateStreaming" in bundle:
        die("解码器会流式加载 .wasm —— 那就要联网，与「不联网」的承诺冲突")
    if "wasmBinary" not in bundle:
        die("解码器里没有内联 wasm（缺 wasmBinary）—— 会把 .wasm 当成外部文件去下载，单文件就废了")
    for bad in ("WebSocket", "sendBeacon", "instantiateStreaming"):
        if bad in bundle:
            die(f"解码器里出现了 {bad}，可能真的会往外连，需人工复核")

    # Emscripten 运行时会留一段「wasm / 预载文件以外部 URL 形式存在时」的兜底代码
    # （XMLHttpRequest、fetch、importScripts、createLazyFile…）。因为 wasm 已经内联，
    # 这些分支在运行时永远不会被走到。浏览器实测的记录见 docs/版本说明.md。
    # 这里只记录，不拦。
    found = [k for k in ("XMLHttpRequest", "fetch(", "importScripts", "new Worker(") if k in bundle]
    if found:
        print("· 说明：解码器内含 Emscripten 运行时兜底代码 —— " + "、".join(found))
        print("  它们服务于「wasm 作为外部文件」的情形；本构建 wasm 已内联，这些分支不可达。")
        print("  真机实测零网络请求的记录见 docs/版本说明.md。")

    if "</script" in licenses.lower():
        die("许可证文本里出现了 </script，换一种内联方式")
    if "-->" in licenses:
        die("许可证文本里出现了 -->，不能直接放进 HTML 注释")

    return hashlib.sha256(bundle.encode("utf-8")).hexdigest()


def build() -> str:
    html = read(INDEX)
    bundle = read(BUNDLE)
    lic_lib = read(LICENSE_LIBHEIF)
    lic_wrap = read(LICENSE_WRAPPER)

    sha = check_vendor(bundle, lic_lib + lic_wrap)
    if sha != BUNDLE_SHA256:
        print("⚠ 解码器哈希与记录的不一致：")
        print("    记录值 " + BUNDLE_SHA256)
        print("    实际值 " + sha)
        print("  如果你是有意升级上游版本，请一并更新 tools/vendor/README.md 与这里的常量。")

    if not BEGIN_RE.search(html):
        die("index.html 里找不到 <!-- DECODER:BEGIN --> / <!-- DECODER:END --> 标记")

    license_blob = (
        "<!--\n"
        "  以下两个组件以 LGPL-3.0 授权，随「完整版」一起分发。\n"
        "  本文件的其余部分（岛影自身）为 MIT 许可，见仓库根目录 LICENSE。\n"
        "\n"
        "  1) " + VENDOR_NAME + " " + VENDOR_VERSION + " —— " + VENDOR_UPSTREAM + "\n"
        "  2) libheif / libde265 —— https://github.com/strukturag/libheif\n"
        "\n"
        "  下面依次是两份许可证全文。\n"
        "-->\n"
        "<script type=\"text/plain\" id=\"license-lgpl3\">\n"
        "===== " + VENDOR_NAME + " " + VENDOR_VERSION + " (LGPL-3.0) =====\n"
        + lic_wrap + "\n"
        "===== libheif (LGPL-3.0) =====\n"
        + lic_lib + "\n"
        "</script>\n"
    )

    injected = (
        "<!-- DECODER:BEGIN 自动生成区 · 勿手改 · 由 tools/build_full.py 注入 HEIC 解码器 -->\n"
        '<script id="heif-decoder">\n'
        "/*! " + VENDOR_NAME + " " + VENDOR_VERSION + " — LGPL-3.0 — " + VENDOR_UPSTREAM + "\n"
        " *  libheif 的 WebAssembly 构建，wasm 已内联，不发起任何网络请求。\n"
        " *  许可证全文在本文件下方的 <script type=\"text/plain\" id=\"license-lgpl3\"> 里。 */\n"
        + bundle + "\n"
        "</script>\n"
        + license_blob
        + "<!-- DECODER:END -->"
    )

    out = BEGIN_RE.sub(lambda _: injected, html, count=1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="拼出带内置 HEIC 解码器的完整版单文件")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出路径")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    orig_len = len(INDEX.read_bytes())
    out = build()
    out_bytes = out.encode("utf-8")

    print("干净源码 index.html        {:>10,} 字节".format(orig_len))
    print("内置解码器                  {:>10,} 字节".format(BUNDLE.stat().st_size))
    print("—" * 46)
    print("完整版                      {:>10,} 字节  （{:.1f} KB / {:.2f} MB）".format(
        len(out_bytes), len(out_bytes) / 1024, len(out_bytes) / 1024 / 1024))
    print()
    print("解码器 SHA-256  " + hashlib.sha256(BUNDLE.read_bytes()).hexdigest())

    if args.check:
        print("\n✓ 校验通过（未写文件）")
        return

    dest = pathlib.Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(out_bytes)

    # 单文件之外再给一份人可读的许可证随附文件，方便连 zip 一起发
    title = "岛影（Daoying）完整版 · 第三方组件说明"
    notice = "\n".join([
        title,
        "=" * 40,
        "",
        "「完整版」那个单文件 = 岛影自身代码（MIT） + 下面这个第三方组件（LGPL-3.0）。",
        '组件全文许可证已内联在 HTML 文件内部（搜索 id="license-lgpl3"），此处再随附一份。',
        "",
        "组件：    {} {}".format(VENDOR_NAME, VENDOR_VERSION),
        "用途：    解析 HEIC / HEIF（iPhone 相机默认格式）",
        "上游：    {}".format(VENDOR_UPSTREAM),
        "libheif： https://github.com/strukturag/libheif",
        "SHA-256： {}".format(hashlib.sha256(BUNDLE.read_bytes()).hexdigest()),
        "",
        "许可证全文：",
        "",
        read(LICENSE_WRAPPER),
        "",
        read(LICENSE_LIBHEIF),
        "",
    ])
    if notice.count(title) != 1:
        die("随附说明的标题重复了，检查一下字符串拼接")
    (dest.parent / "第三方组件说明.txt").write_text(notice, encoding="utf-8")

    print("✓ 已写出 " + str(dest.relative_to(ROOT)))
    print("✓ 已写出 " + str((dest.parent / "第三方组件说明.txt").relative_to(ROOT)))


if __name__ == "__main__":
    main()
