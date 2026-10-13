<div align="center">

# Dynamic Island Gradient

**岛影 (Dǎo Yǐng)** — *"island shadow"*, a pun on 倒影 (reflection)

Adds a smooth fade-out mask to the top of any wallpaper so the iPhone's
Dynamic Island and status bar blend into the picture instead of slicing it.

[![License: MIT](https://img.shields.io/badge/License-MIT-8a63d2.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()
[![No Network](https://img.shields.io/badge/network-none-blue.svg)]()
[![Single File](https://img.shields.io/badge/build-one%20HTML%20file-orange.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[简体中文](README.md) · English

<img src="screenshots/hero.jpg" width="880" alt="Two real wallpapers inside official iPhone 17 Pro Max bezels — the top gradient blends the Dynamic Island into the picture">

</div>

---

## The problem

Since the iPhone 14 Pro, there's a permanent black pill at the top of the
screen. Put a bright photo behind it and the hardware visibly **cuts the
image in half**. Apple's own wallpapers get a darkened top; your own photos
don't.

This tool does exactly one thing: it lays a solid-to-transparent gradient over
the top of the wallpaper.

```
┌──────────────┐         ┌──────────────┐
│  sky          │         │██████████████│  ← solid: covers the island
│              │         │██████████████│
│              │   ──►   │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  ← fade zone
│   mountains   │         │   mountains   │  ← original, untouched
└──────────────┘         └──────────────┘
```

Two **device-accurate** comparisons — left is the original, where the black
Dynamic Island visibly slices the picture; right is after the mask, where it
blends in and even the lock-screen clock reads better.

<img src="screenshots/compare-portrait.jpg" alt="Beach portrait: left is the original with a bright blue sky behind the island; right is after the mask">

<img src="screenshots/compare-rain.jpg" alt="Rainy street at dusk: left is the original, right is after the mask">

> Device bezels are from Apple Design Resources (iPhone 17 Pro Max), used solely
> to depict a mock-up. That image is © Apple Inc. and is **not** covered by this
> project's MIT licence.

Drag the split handle to compare before / after:

<img src="screenshots/desktop-dark.png" alt="Interface">

The manual is embedded too — one click slides it in, no network, no extra file:

<img src="screenshots/manual-drawer.png" width="620" alt="Built-in manual">

---

## Usage

**No install. No build. No network. One file, works on Windows, macOS and Linux.**

### Fastest path: use it online

**→ [uppjs.com/daoying.html](https://uppjs.com/daoying.html)**

Nothing to download — open it in a browser, drop a photo in, tune the gradient, export.
It runs the *same code* as the single-file build, entirely inside your browser:
your image is never uploaded and the page never talks to the network
(pull your cable and check).

Want something you can keep on the desktop and run fully offline? Read on.

### Just want to use it

Grab a build from the **[Releases page](https://github.com/js-ping/dynamic-island-gradient/releases/latest)**:

| Download | What it is |
|---|---|
| `Daoying-v2.2.0-single-file.html` | **Recommended** — one 67 KB file, double-click and go |
| `Daoying-v2.2.0-Windows-macOS-Linux.zip` | Standalone app + both launchers + manual + README |

Or clone the repo and use `index.html` directly — the contents are identical:

```bash
git clone https://github.com/js-ping/dynamic-island-gradient.git
```

### Opening it

| OS | How to open | Notes |
|---|---|---|
| **Windows** | Double-click `index.html` | If Notepad opens instead, right-click → *Open with* → your browser; or double-click `启动.bat` |
| **macOS** | Double-click `index.html` | Opens in your default browser. Use `启动.command` to serve over LAN for a phone |
| **Linux** | Double-click `index.html` | Or `xdg-open index.html` |

Then:

1. Drop your wallpaper in (or click to pick, or paste with `Ctrl+V` / `⌘V`)
2. Drag the white split line to compare before / after
3. Hit "Download", AirDrop it to your iPhone, set as wallpaper

> The manual is embedded — click "说明书" in the header. This one file can be copied
> to a USB stick, sent over chat, or dropped on any computer and used by double-clicking.
> **It needs no companion files.**

### Browser support

Chrome / Edge / Safari / Firefox and anything else modern — desktop or mobile.

> The one exception is **HEIC** photos: Chrome / Edge / Firefox can't decode them
> (Safari can). The tool says so explicitly rather than failing silently — convert to JPEG.

---

## Features

| Feature | Detail |
|---|---|
| **Three colour modes** | Solid black / sampled from the top of the image / custom colour |
| **Coverage strength** | 0–100%, so you can dim rather than fully cover |
| **Two-stage geometry** | Solid height + fade end height, in percent (auto-converted to pixels for the loaded image) |
| **Four easing curves** | Ease-out / linear / ease-in / smoothstep, with a live curve thumbnail |
| **Drag to compare** | Split handle follows mouse, finger, or arrow keys |
| **Lock-screen mockup** | A simulated iPhone lock screen beside the canvas on wide windows (real clock) |
| **Island guide** | Dashed overlay showing the Dynamic Island and status-bar safe area |
| **Banding dither** | A near-invisible noise layer to kill gradient banding on OLED |
| **Remembers settings** | Your slider values persist in browser local storage |
| **Full-resolution export** | JPEG / PNG at the original resolution, filename encodes all parameters |
| **Light / dark** | Follows the system, or switch manually |

**Input methods:** drag & drop · file picker · `⌘V` paste · built-in sample image

---

## Privacy

- **No network requests.** Not a single `fetch`, `XMLHttpRequest`, `WebSocket`,
  or external asset (no webfonts, no icon CDNs, no analytics).
- **Images never leave the tab.** They are processed in memory and never
  written to storage.
- **Only settings persist.** Sliders live in `localStorage`; clear them from
  your browser settings any time.
- **Auditable.** The whole tool is one `index.html` you can read top to bottom.

**It works identically with Wi-Fi turned off.**

---

## How it stays fast

<details>
<summary>Expand</summary>

The naive approach is `getImageData` → per-pixel `for` loop → `putImageData`.
An iPhone wallpaper is 1320×2868 ≈ **3.8 million pixels**; doing that on every
slider tick drops frames.

Instead:

1. The easing curve is **discretised into 64 gradient stops** and handed to
   `createLinearGradient()` — compositing happens on the GPU.
2. Each redraw is **two `drawImage` calls plus one `fillRect`**, roughly
   constant cost regardless of resolution.
3. "Sample from image" scales the target region down to **1×1 pixel** with
   `drawImage` — the scaler itself performs the box average, dozens of times
   faster than summing in JS.
4. Redraws are coalesced with `requestAnimationFrame`.

Result: dragging sliders on a 1320×2868 image is real-time.

</details>

---

## Layout

```
DynamicIslandGradient/
├── index.html            ← everything lives here (single file, all three OSes)
├── 启动.bat               ← Windows launcher (in case .html is hijacked by an editor)
├── 启动.command           ← macOS launcher (also serves over LAN for phones)
├── 使用说明.html          ← the same manual as a standalone page (Chinese)
├── help.html             ← manual, ASCII filename for phones
├── README.md / README.en.md
├── CHANGELOG.md
├── LICENSE               ← MIT
├── docs/
└── screenshots/
```

**Only `index.html` is required — everything else is for reading or hacking on.**

---

## FAQ

**Does exporting shrink my image?**
No — export is at the original resolution, pixel for pixel. JPEG quality
defaults to 95% and is adjustable.

**HEIC doesn't open?**
Chrome and Firefox can't decode HEIC. Use Safari, or convert to JPEG first.
The tool says so explicitly rather than failing silently.

**Can I use it on my phone?**
Yes. Double-click `启动.command` on your Mac, connect your phone to the same
Wi-Fi, and open the address it prints. The layout is mobile-ready.

---

## License

MIT © [js-ping](https://github.com/js-ping)
