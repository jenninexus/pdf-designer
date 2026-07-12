"""Generate collage layout candidates from a directory of images.

The PowerPoint-Designer experience, local and deterministic: point this at a
folder of images and it writes one candidate HTML layout per applicable layout
family, plus an index.html gallery that shows every candidate side by side so
you can compare and pick — then export the winner with html_to_pdf.py (print)
or --png (pixel canvases for social sizes).

Design SSOT: docs/COLLAGE-DESIGN.md. Canvas presets + tokens:
themes/default-collage.json.

Usage:
    python -m pdf_tool.collage path/to/images
    python -m pdf_tool.collage path/to/images --canvas letter-portrait --layout auto
    python -m pdf_tool.collage path/to/images --canvas square --layout hero-mosaic
    python -m pdf_tool.collage path/to/images --hero best-shot.png --title "Project Showcase"
    python -m pdf_tool.collage path/to/images --png     # also screenshot each candidate

Candidates are written to <imagesDir>/_candidates/ (or --out DIR). If a
collage-source.json exists in the images directory, its canvas/layout/hero/
title/theme values are used as defaults (CLI flags win). Same inputs always
produce the same layouts — no RNG; frame-scatter jitter is hashed from
filenames.
"""

import hashlib
import json
import struct
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
FAMILIES = ["uniform-grid", "hero-mosaic", "masonry", "filmstrip", "spotlight-caption", "frame-scatter"]

_REPO_ROOT = Path(__file__).resolve().parents[2]
_THEME_PATH = _REPO_ROOT / "themes" / "default-collage.json"

MODES = {
    "dark": {"bg": "#0b0d12", "text": "rgba(240,242,246,0.94)", "dim": "rgba(240,242,246,0.68)", "border": "rgba(79,209,201,0.14)"},
    "light": {"bg": "#ffffff", "text": "#171b24", "dim": "rgba(23,27,36,0.72)", "border": "rgba(23,27,36,0.14)"},
}


# ---------------------------------------------------------------- image dims

def _png_size(data: bytes):
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return None


def _gif_size(data: bytes):
    if data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = struct.unpack("<HH", data[6:10])
        return w, h
    return None


def _jpeg_size(data: bytes):
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
        i += 2 + seg_len
    return None


def image_size(path: Path):
    """Return (width, height), via header parsing, Pillow fallback, or 1:1."""
    data = path.read_bytes()[:65536]
    for parser in (_png_size, _gif_size, _jpeg_size):
        size = parser(data)
        if size:
            return size
    try:
        from PIL import Image

        with Image.open(path) as im:
            return im.size
    except Exception:
        return (1000, 1000)


def scan_images(images_dir: Path):
    """Top-level image files, sorted by name for deterministic layouts."""
    images = []
    for p in sorted(images_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            w, h = image_size(p)
            images.append({"file": p.name, "w": w, "h": h, "ar": w / h})
    return images


# ---------------------------------------------------------------- presets

def load_canvas_preset(name: str):
    presets = json.loads(_THEME_PATH.read_text(encoding="utf-8"))["canvas_presets"]
    if name not in presets:
        raise SystemExit(f"Unknown canvas preset '{name}'. Options: {', '.join(presets)}")
    p = presets[name]
    px_w, px_h = p["px"]
    if p.get("unit") == "in":
        # Letter presets: use half of the 300dpi pixel size (150dpi) on screen.
        px_w, px_h = px_w // 2, px_h // 2
    return {"id": name, "px_w": px_w, "px_h": px_h, "print_in": (p.get("width"), p.get("height")) if p.get("unit") == "in" else None}


def _hash01(text: str) -> float:
    """Deterministic 0..1 float from a string (replaces RNG)."""
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


# ---------------------------------------------------------------- layout bodies
# Each family returns inner-HTML for the .canvas div. Images are referenced
# relative to the candidates dir (../<file> by default).

def _img(src_prefix: str, image: dict) -> str:
    return f'<img src="{src_prefix}{image["file"]}" alt="{image["file"]}" loading="eager">'


def _grid_cols(n: int, canvas) -> int:
    ideal = (n * canvas["px_w"] / canvas["px_h"]) ** 0.5
    return max(1, min(6, round(ideal)))


def body_uniform_grid(images, canvas, src, opts):
    cols = _grid_cols(len(images), canvas)
    cells = "".join(f'<div class="cell">{_img(src, im)}</div>' for im in images)
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);">{cells}</div>'


def _pick_hero(images, opts):
    if opts.get("hero"):
        for im in images:
            if im["file"] == opts["hero"]:
                return im
    return max(images, key=lambda im: im["w"] * im["h"])


def body_hero_mosaic(images, canvas, src, opts, text_card: str | None = None):
    hero = _pick_hero(images, opts)
    rest = [im for im in images if im is not hero]
    cols = 3 if canvas["px_h"] >= canvas["px_w"] else 4
    extra = 1 if text_card else 0
    rows = max(2, -(-(4 + len(rest) + extra) // cols))
    cells = [f'<div class="cell" style="grid-column:span 2;grid-row:span 2;">{_img(src, hero)}</div>']
    if text_card:
        cells.append(text_card)
    cells += [f'<div class="cell">{_img(src, im)}</div>' for im in rest]
    return (
        f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);'
        f'grid-template-rows:repeat({rows},1fr);">{"".join(cells)}</div>'
    )


def body_masonry(images, canvas, src, opts):
    """Packed columns: no cropping pressure — items sized by aspect via flex."""
    k = 3 if canvas["px_h"] >= canvas["px_w"] else 4
    columns = [[] for _ in range(k)]
    heights = [0.0] * k
    for im in images:
        i = heights.index(min(heights))
        columns[i].append(im)
        heights[i] += im["h"] / im["w"]
    cols_html = ""
    for col in columns:
        items = "".join(
            f'<div class="cell" style="flex:{im["h"] / im["w"]:.4f} 1 0;">{_img(src, im)}</div>' for im in col
        )
        cols_html += f'<div class="mcol">{items}</div>'
    return f'<div class="masonry">{cols_html}</div>'


def body_filmstrip(images, canvas, src, opts):
    """Justified rows: each image's width share ∝ its aspect ratio."""
    per_row = 4 if canvas["px_w"] > canvas["px_h"] else 3
    rows_html = ""
    for i in range(0, len(images), per_row):
        row = images[i : i + per_row]
        items = "".join(f'<div class="cell" style="flex:{im["ar"]:.4f} 1 0;">{_img(src, im)}</div>' for im in row)
        rows_html += f'<div class="frow">{items}</div>'
    return f'<div class="filmstrip">{rows_html}</div>'


def body_spotlight_caption(images, canvas, src, opts):
    title = opts.get("title") or "Untitled Collage"
    card = (
        '<div class="cell textcard"><div>'
        f"<h2>{title}</h2><p>{opts.get('subtitle', '')}</p>"
        "</div></div>"
    )
    return body_hero_mosaic(images, canvas, src, opts, text_card=card)


def body_frame_scatter(images, canvas, src, opts):
    n = len(images)
    cols = max(2, min(5, round(n ** 0.5)))
    rows = -(-n // cols)
    tiles = ""
    for idx, im in enumerate(images):
        r, c = divmod(idx, cols)
        jx = (_hash01(im["file"] + "x") - 0.5) * 8
        jy = (_hash01(im["file"] + "y") - 0.5) * 8
        rot = (_hash01(im["file"] + "r") - 0.5) * 12
        left = (c + 0.5) / cols * 100 + jx
        top = (r + 0.5) / rows * 100 + jy
        w = 100 / cols * 1.18
        tiles += (
            f'<div class="polaroid" style="left:{left:.1f}%;top:{top:.1f}%;width:{w:.1f}%;'
            f'transform:translate(-50%,-50%) rotate({rot:.1f}deg);z-index:{idx + 1};">'
            f'{_img(src, im)}</div>'
        )
    return f'<div class="scatter">{tiles}</div>'


BUILDERS = {
    "uniform-grid": body_uniform_grid,
    "hero-mosaic": body_hero_mosaic,
    "masonry": body_masonry,
    "filmstrip": body_filmstrip,
    "spotlight-caption": body_spotlight_caption,
    "frame-scatter": body_frame_scatter,
}


# ---------------------------------------------------------------- page shell

def render_candidate(family: str, images, canvas, opts) -> str:
    mode = MODES["light" if opts.get("theme") == "light" else "dark"]
    alt = MODES["light" if opts.get("theme") != "light" else "dark"]
    body = BUILDERS[family](images, canvas, opts.get("src_prefix", "../"), opts)
    print_css = ""
    if canvas["print_in"]:
        w_in, h_in = canvas["print_in"]
        print_css = f"""
  @page {{ size: {w_in}in {h_in}in; margin: 0; }}
  @media print {{
    :root {{ --bg: {alt["bg"]}; --text: {alt["text"]}; --dim: {alt["dim"]}; --border: {alt["border"]}; }}
    html[data-pdf-theme="dark"] {{ --bg: {MODES["dark"]["bg"]}; --text: {MODES["dark"]["text"]}; --dim: {MODES["dark"]["dim"]}; --border: {MODES["dark"]["border"]}; }}
    body {{ margin: 0; }}
    .canvas {{ width: {w_in}in; height: {h_in}in; margin: 0; box-shadow: none; }}
  }}"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{family} — collage candidate</title>
<style>
  :root {{ --bg: {mode["bg"]}; --text: {mode["text"]}; --dim: {mode["dim"]}; --border: {mode["border"]};
           --gutter: 12px; --radius: 10px; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--text);
         font-family: 'Inter', ui-sans-serif, system-ui, sans-serif; }}
  .canvas {{ width: {canvas["px_w"]}px; height: {canvas["px_h"]}px; margin: 0 auto; overflow: hidden;
             background: var(--bg); padding: var(--gutter); position: relative; }}
  .grid {{ display: grid; gap: var(--gutter); width: 100%; height: 100%; grid-auto-rows: 1fr; grid-auto-flow: dense; }}
  .cell {{ border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); min-height: 0; min-width: 0; }}
  .cell img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .masonry {{ display: flex; gap: var(--gutter); width: 100%; height: 100%; }}
  .mcol {{ flex: 1 1 0; display: flex; flex-direction: column; gap: var(--gutter); min-height: 0; }}
  .filmstrip {{ display: flex; flex-direction: column; gap: var(--gutter); width: 100%; height: 100%; }}
  .frow {{ flex: 1 1 0; display: flex; gap: var(--gutter); min-height: 0; }}
  .textcard {{ display: flex; align-items: center; justify-content: center; text-align: center;
               background: var(--bg); color: var(--text); padding: 8%; }}
  .textcard h2 {{ margin: 0 0 6px; font-size: 20px; color: var(--text); }}
  .textcard p {{ margin: 0; font-size: 12px; color: var(--dim); }}
  .scatter {{ position: relative; width: 100%; height: 100%; }}
  .polaroid {{ position: absolute; background: #fff; padding: 8px 8px 22px;
               box-shadow: 0 8px 24px rgba(0,0,0,0.35); }}
  .polaroid img {{ width: 100%; display: block; }}
  {print_css}
</style>
</head>
<body>
<div class="canvas">{body}</div>
</body>
</html>
"""


def render_index(families, images, canvas, out_dir: Path, opts) -> str:
    """PowerPoint-Designer-style picker: every candidate side by side."""
    scale = 320 / canvas["px_w"]
    thumb_h = canvas["px_h"] * scale
    cards = ""
    for fam in families:
        cards += f"""
  <a class="card" href="{fam}.html" target="_blank">
    <div class="thumb" style="height:{thumb_h:.0f}px;">
      <iframe src="{fam}.html" style="width:{canvas["px_w"]}px;height:{canvas["px_h"]}px;transform:scale({scale:.4f});" scrolling="no" tabindex="-1"></iframe>
    </div>
    <div class="label">{fam}</div>
  </a>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collage candidates — {opts.get("title") or out_dir.parent.name}</title>
<style>
  body {{ margin: 0; padding: 28px; background: #0b0d12; color: rgba(240,242,246,0.94);
         font-family: 'Inter', ui-sans-serif, system-ui, sans-serif; }}
  h1 {{ font-size: 18px; margin: 0 0 4px; }}
  p {{ color: rgba(240,242,246,0.6); font-size: 12px; margin: 0 0 22px; }}
  .row {{ display: flex; flex-wrap: wrap; gap: 20px; }}
  .card {{ text-decoration: none; color: inherit; border: 1px solid rgba(79,209,201,0.18);
          border-radius: 12px; overflow: hidden; background: #10131a; transition: transform 120ms ease, border-color 120ms ease; }}
  .card:hover {{ transform: translateY(-3px); border-color: rgba(79,209,201,0.55); }}
  .thumb {{ width: 320px; overflow: hidden; position: relative; }}
  .thumb iframe {{ border: 0; transform-origin: top left; pointer-events: none; position: absolute; top: 0; left: 0; }}
  .label {{ padding: 9px 12px; font-size: 12.5px; letter-spacing: 0.06em; text-transform: uppercase;
           color: #4fd1c9; border-top: 1px solid rgba(79,209,201,0.14); }}
</style>
</head>
<body>
<h1>Collage candidates — {opts.get("title") or out_dir.parent.name}</h1>
<p>{len(images)} images · canvas {canvas["id"]} ({canvas["px_w"]}×{canvas["px_h"]}px) · click a layout to open it full size</p>
<div class="row">{cards}</div>
</body>
</html>
"""


# ---------------------------------------------------------------- generation

def generate(images_dir, canvas_name=None, layout=None, hero=None, title=None,
             theme=None, out_dir=None, png=False):
    images_dir = Path(images_dir).resolve()
    if not images_dir.is_dir():
        raise FileNotFoundError(images_dir)

    source = {}
    source_file = images_dir / "collage-source.json"
    if source_file.exists():
        source = json.loads(source_file.read_text(encoding="utf-8"))

    canvas = load_canvas_preset(canvas_name or source.get("canvas") or "letter-portrait")
    layout = layout or source.get("layout") or "auto"
    opts = {
        "hero": hero or source.get("hero"),
        "title": title or (source.get("text", [{}])[0].get("content") if source.get("text") else None),
        "theme": theme or source.get("theme") or "dark",
    }

    images = scan_images(images_dir)
    if not images:
        raise SystemExit(f"No images found in {images_dir} (looked for {', '.join(sorted(IMAGE_EXTS))})")

    out = Path(out_dir).resolve() if out_dir else images_dir / "_candidates"
    out.mkdir(parents=True, exist_ok=True)

    families = FAMILIES if layout == "auto" else [layout]
    unknown = [f for f in families if f not in BUILDERS]
    if unknown:
        raise SystemExit(f"Unknown layout {unknown}. Options: auto, {', '.join(FAMILIES)}")

    written = []
    for fam in families:
        path = out / f"{fam}.html"
        path.write_text(render_candidate(fam, images, canvas, opts), encoding="utf-8")
        written.append(path)
        print(f"Saved: {path}")

    if layout == "auto":
        index = out / "index.html"
        index.write_text(render_index(families, images, canvas, out, opts), encoding="utf-8")
        written.append(index)
        print(f"Saved: {index}  <- open this to compare all candidates")

    if png:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": canvas["px_w"], "height": canvas["px_h"]})
            for fam in families:
                page.goto((out / f"{fam}.html").as_uri())
                png_path = out / f"{fam}.png"
                page.locator(".canvas").screenshot(path=str(png_path))
                print(f"Saved: {png_path}")
            browser.close()

    return written


def main() -> None:
    raw = sys.argv[1:]
    flags = {"--canvas": None, "--layout": None, "--hero": None, "--title": None, "--theme": None, "--out": None}
    png = False
    args = []
    i = 0
    while i < len(raw):
        arg = raw[i]
        if arg == "--png":
            png = True
        elif arg in flags:
            if i + 1 >= len(raw):
                raise SystemExit(f"{arg} requires a value")
            flags[arg] = raw[i + 1]
            i += 1
        elif "=" in arg and arg.split("=", 1)[0] in flags:
            key, val = arg.split("=", 1)
            flags[key] = val
        else:
            args.append(arg)
        i += 1

    if len(args) != 1:
        print(__doc__)
        raise SystemExit(1)

    try:
        generate(
            args[0],
            canvas_name=flags["--canvas"],
            layout=flags["--layout"],
            hero=flags["--hero"],
            title=flags["--title"],
            theme=flags["--theme"],
            out_dir=flags["--out"],
            png=png,
        )
    except ModuleNotFoundError:
        print(
            "Playwright is not installed yet (needed for --png). Run:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
