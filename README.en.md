<div align="center">

# Dynamic Island Gradient

**Stop the Dynamic Island from cutting your wallpaper in half.**

Adds a smooth fade-out mask to the top of any wallpaper so the iPhone's
Dynamic Island and status bar blend into the picture instead of slicing it.

[![License: MIT](https://img.shields.io/badge/License-MIT-8a63d2.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()
[![No Network](https://img.shields.io/badge/network-none-blue.svg)]()
[![Single File](https://img.shields.io/badge/build-one%20HTML%20file-orange.svg)]()

[简体中文](README.md) · English

<img src="screenshots/example-before.jpg" width="240" alt="Before">
<img src="screenshots/example-after.jpg" width="240" alt="After">

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

Drag the split handle to compare before / after:

<img src="screenshots/desktop-dark.png" alt="Interface">

---

## Usage

**No install. No build. No network.**

1. Download the repo (or just `index.html`)
2. **Double-click `index.html`** — it opens in your browser
3. Drop your wallpaper in, drag the split line to taste
4. Hit "Download", AirDrop it to your iPhone, set as wallpaper

> Want it online? Enable GitHub Pages for the repo and use it from your phone.

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
├── index.html            ← the app (single file, double-click)
├── 使用说明.html          ← illustrated manual (Chinese)
├── help.html             ← manual, ASCII filename for phones
├── 启动.command           ← double-click to serve locally (LAN access)
├── README.md / README.en.md
├── CHANGELOG.md
├── LICENSE               ← MIT
├── docs/
└── screenshots/
```

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
