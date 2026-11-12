# Island Fade

A gradient at the top of your wallpaper so the iPhone Dynamic Island blends into the photo.

Single HTML file, double-click to run · macOS / Windows / Linux · offline · MIT

**Download**: <https://github.com/js-ping/dynamic-island-gradient/releases>

---

## What it does

The Dynamic Island is black. On a light wallpaper it looks pasted on. Island Fade darkens the top
edge with a gradient so the island becomes part of the picture.

- Four easing curves, with a live curve preview
- Draggable split view against the original; lock-screen mockup on wide screens
- Banding dithering, quality choice, remembered settings, paste from clipboard
- Exports a 1:1 JPEG named after the parameters
- Zero network requests

## Two builds

| File | Size | HEIC |
|---|---|---|
| `Daoying-v2.2.1-full-heic.html` | 2.1 MB | Bundled decoder — works in any browser (recommended) |
| `Daoying-v2.2.1-single-file.html` | 74 KB | Relies on the browser; Safari only |

HEIC uses HEVC, which is covered by patent pools, so Chrome / Edge / Firefox ship no decoder.
The full build inlines an open-source decoder (libheif-js, LGPL-3.0) — 2 MB heavier, no surprises.

## Usage

1. Download the HTML file and open it.
2. Drop in a wallpaper.
3. Drag the split line, pick a curve, export.

## Build from source

```bash
python3 docs/build_help.py      # markdown → in-app manual
python3 tools/build_full.py     # full build with the bundled decoder → dist/
```

## License

MIT for the project. The inlined decoder is LGPL-3.0; both license texts ship inside the file.
