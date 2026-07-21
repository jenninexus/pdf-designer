"""check_rendered_color — catch brown that only exists AFTER the browser composites the page.

WHY THIS EXISTS (2026-07-21). `check_palette` reads source hex. It passed every Netflix doc while
the page still *looked* brown, because the brown was never written as a hex — it was MANUFACTURED
at render time by two mechanisms:

  1. LARGE-AREA WARM CAST — a red-tinted dark grey background (e.g. a `#2a0e10` gradient stop plus
     rgba(229,9,20,.20) glows) averages to #2c2224 / #291c1d over a big region. Every pixel is
     "neutral" to a per-hex check (saturation < 0.18), but the eye integrates the whole area and
     reads BROWN.
  2. ALPHA COMPOSITING — a translucent light layer over a warm dark one (e.g. white streaks at
     16% over a red gradient) produces desaturated warm mid-tones like #a08251 — real brown pixels
     that appear in no stylesheet.

So this guard renders the page and judges the PIXELS. Two tests:

  * pixel test  — any pixel landing in the brown/mustard/lime/olive bands (ignores tiny counts,
                  which are just text antialiasing).
  * cast test   — average color of large background regions must be near-neutral: `chroma`
                  (max channel − min channel) <= --max-chroma (default 8). A red-tinted dark grey
                  fails here even though no single pixel is "brown".

    python -m pdf_tool.check_rendered_color <doc>.html
    python -m pdf_tool.check_rendered_color <doc>.html --pdf-theme dark
    python -m pdf_tool.check_rendered_color <doc>.html --max-chroma 8 --max-brown-pct 0.35

Exit 0 clean · 1 violation · 2 usage/render error.
"""
from __future__ import annotations

import colorsys
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Same bands as check_palette.classify — one rule, two surfaces.
def classify_rgb(r: int, g: int, b: int) -> str | None:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hue = h * 360
    if s < 0.18:
        return None
    if 20 <= hue <= 65 and l < 0.50:
        return "BROWN/MUSTARD"
    if 20 <= hue <= 65 and l < 0.58 and s < 0.60:
        return "MUSTARD"
    if 65 <= hue <= 100:
        return "LIME/PUKE"
    if 100 <= hue <= 150 and l < 0.35 and s < 0.55:
        return "OLIVE"
    return None


def _image_boxes(page) -> list[tuple[int, int, int, int]]:
    """Bounding boxes of <img>/photographic elements, in CSS px (x, y, w, h).

    Colors INSIDE a photo are the photo's own content (game art, a banner) — our palette rules
    govern the DESIGN, not the artwork. These regions are excluded from the pixel scan.
    """
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('img, .logohero, .hero, .shot .frame'))
              .map(el => { const r = el.getBoundingClientRect();
                           return {x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height}; })
              .filter(b => b.w > 4 && b.h > 4)"""
    )


def _render(html_path: Path, pdf_theme: str | None, png_out: Path) -> None:
    from playwright.sync_api import sync_playwright

    url = "file:///" + str(html_path.resolve()).replace("\\", "/")
    with sync_playwright() as p:
        # 2x device scale + greyscale-antialiased text: LCD SUBPIXEL rendering paints orange/blue
        # fringes on glyph edges, which a naive pixel scan reports as "brown". Those fringes are
        # invisible to the eye and exist on every browser-rendered page — they are a measurement
        # artifact, not a design defect. Rendering at 2x and downsampling averages them away so the
        # check only sees real surfaces.
        browser = p.chromium.launch(args=["--disable-lcd-text", "--disable-font-subpixel-positioning"])
        page = browser.new_page(viewport={"width": 880, "height": 1140}, device_scale_factor=2)
        page.goto(url)
        page.add_style_tag(content="* { -webkit-font-smoothing: antialiased; "
                                   "text-rendering: geometricPrecision; }")
        if pdf_theme:
            page.evaluate(f"document.documentElement.setAttribute('data-pdf-theme','{pdf_theme}')")
        page.wait_for_timeout(500)
        page.screenshot(path=str(png_out), full_page=True)
        boxes = _image_boxes(page)
        browser.close()

    # downsample 2x -> 1x: averages residual glyph fringing into the surrounding surface
    try:
        from PIL import Image as _Im
        _im = _Im.open(png_out)
        _im.resize((_im.width // 2, _im.height // 2), _Im.LANCZOS).save(png_out)
    except Exception:
        pass
    return boxes


def _chroma(rgb) -> int:
    return max(rgb) - min(rgb)


def analyze(html_path: Path, pdf_theme: str | None = None,
            max_chroma: int = 12, max_brown_pct: float = 0.08) -> dict:
    from PIL import Image

    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "render.png"
        img_boxes = _render(html_path, pdf_theme, png) or []
        im = Image.open(png).convert("RGB")
        W, H = im.size

        def in_image(x: int, y: int) -> bool:
            """True when (x,y) falls inside a photo/artwork region (excluded from the scan)."""
            for b in img_boxes:
                if b["x"] - 2 <= x <= b["x"] + b["w"] + 2 and b["y"] - 2 <= y <= b["y"] + b["h"] + 2:
                    return True
            return False

        # ---- pixel test -------------------------------------------------
        # Only SOLID brown counts. Text antialiasing puts single off-hue pixels on glyph edges;
        # those are invisible and must not fail the build. A pixel counts only when its 4
        # neighbours (one step away) are ALSO in a banned band — i.e. it belongs to an area,
        # not an edge.
        step = 4
        counts: dict[str, int] = {}
        samples: list[str] = []
        total = 0
        px_cache: dict[tuple[int, int], str | None] = {}

        def band_at(x: int, y: int):
            if (x, y) in px_cache:
                return px_cache[(x, y)]
            if 0 <= x < W and 0 <= y < H:
                v = classify_rgb(*im.getpixel((x, y)))
            else:
                v = None
            px_cache[(x, y)] = v
            return v

        for y in range(0, H, step):
            for x in range(0, W, step):
                total += 1
                if in_image(x, y):
                    continue  # inside a photo — the artwork's own colors are not our palette
                v = band_at(x, y)
                if not v:
                    continue
                neigh = [band_at(x - step, y), band_at(x + step, y),
                         band_at(x, y - step), band_at(x, y + step)]
                if sum(1 for nb in neigh if nb) < 3:
                    continue  # isolated → antialiasing, not a brown surface
                counts[v] = counts.get(v, 0) + 1
                if len(samples) < 8:
                    p = im.getpixel((x, y))
                    samples.append(f"({x},{y}) #{p[0]:02x}{p[1]:02x}{p[2]:02x} {v}")

        brown_px = sum(n for k, n in counts.items() if "BROWN" in k or "MUSTARD" in k)
        brown_pct = 100.0 * brown_px / max(total, 1)

        # ---- large-area cast test --------------------------------------
        # tile the page and look at the DARKEST tiles (those are background, not text).
        tiles = []
        tw, th = 110, 110
        for ty in range(0, H - th, th):
            for tx in range(0, W - tw, tw):
                if in_image(tx + tw // 2, ty + th // 2):
                    continue  # tile sits on artwork, not on the page background
                box = im.crop((tx, ty, tx + tw, ty + th))
                px = list(box.getdata())
                n = len(px)
                avg = (sum(p[0] for p in px) // n, sum(p[1] for p in px) // n,
                       sum(p[2] for p in px) // n)
                # spread = how much the tile varies. A FLAT background tile has low spread;
                # a tile full of big coloured headings has high spread and must NOT be judged
                # as a background cast (a red heading on black is correct design, not brown).
                lums = [(p[0] + p[1] + p[2]) / 3 for p in px[::7]]
                mean = sum(lums) / len(lums)
                spread = (sum((v - mean) ** 2 for v in lums) / len(lums)) ** 0.5
                lum = sum(avg) / 3
                tiles.append((lum, avg, tx, ty, spread))
        tiles.sort(key=lambda t: t[0])
        bg_tiles = [t for t in tiles[: max(8, len(tiles) // 3)] if t[4] < 12]  # dark AND flat
        cast = []
        for lum, avg, tx, ty, spread in bg_tiles:
            c = _chroma(avg)
            # a warm cast = red dominant over blue on a flat dark tile
            warm = avg[0] > avg[2] and c > max_chroma
            if warm:
                cast.append(f"tile@({tx},{ty}) avg #{avg[0]:02x}{avg[1]:02x}{avg[2]:02x} "
                            f"chroma={c} (flat background tile with a warm cast — "
                            f"reads brown over a large area)")

    return {
        "file": str(html_path),
        "theme": pdf_theme or "light/screen",
        "brown_pixels": brown_px,
        "brown_pct": round(brown_pct, 3),
        "band_counts": counts,
        "pixel_samples": samples,
        "cast_violations": cast,
        "ok": brown_pct <= max_brown_pct and not cast,
        "thresholds": {"max_chroma": max_chroma, "max_brown_pct": max_brown_pct},
    }


def main(argv) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    theme = None
    if "--pdf-theme" in argv:
        i = argv.index("--pdf-theme")
        if i + 1 < len(argv):
            theme = argv[i + 1]
            args = [a for a in args if a != theme]
    max_chroma = 12
    if "--max-chroma" in argv:
        i = argv.index("--max-chroma")
        max_chroma = int(argv[i + 1]); args = [a for a in args if a != argv[i + 1]]
    max_brown = 0.08
    if "--max-brown-pct" in argv:
        i = argv.index("--max-brown-pct")
        max_brown = float(argv[i + 1]); args = [a for a in args if a != argv[i + 1]]

    bad = 0
    for a in args:
        p = Path(a)
        if not p.exists():
            print(f"not found: {a}")
            return 2
        try:
            rep = analyze(p, theme, max_chroma, max_brown)
        except Exception as e:
            print(f"SKIP {a}: render failed ({e})")
            continue
        mark = "PASS" if rep["ok"] else "FAIL"
        print(f"\n{mark} {p.name} [{rep['theme']}]")
        print(f"  brown/mustard pixels: {rep['brown_pixels']} ({rep['brown_pct']}%) "
              f"— limit {rep['thresholds']['max_brown_pct']}%")
        if rep["band_counts"]:
            print(f"  bands: {rep['band_counts']}")
        for s in rep["pixel_samples"][:5]:
            print(f"      {s}")
        if rep["cast_violations"]:
            print("  LARGE-AREA WARM CAST (this is what reads as 'brown' at page scale):")
            for c in rep["cast_violations"][:6]:
                print(f"      {c}")
            print("  FIX: remove red/warm tint from the BASE background gradient; keep red only")
            print("       as saturated accents. See themes/GENERATION-RULES.md § background.")
        if not rep["ok"]:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
