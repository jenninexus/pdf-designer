"""check_overflow — the page-fit guard for the pinned-footer layout.

The layout system pins the footer/signature to the bottom of a FIXED-HEIGHT
`.page`. Two things protect against the 2026-07-19 overlap bug (a section bleeding
past the page edge onto the next sheet and overlapping it):

1. **`overflow: hidden` on the print `.page` (the structural guarantee).** Any
   content taller than the box is CLIPPED at the page edge instead of bleeding
   onto the next sheet. Overlap can no longer happen visually — worst case, a
   too-tall page's tail is cut off, which is loud and obvious. This lives in
   `themes/default-resume.css` and every template.

2. **This guard (the authoring signal).** It renders the document in the SAME
   headless Chromium the exporter uses, neutralizes the fixed-height/flex clamp
   (so the real content height becomes measurable), and for each page compares
   its body's natural height + footer against the box. A page whose OWN content
   exceeds its box is reported; exit is non-zero so it can gate an export.

⚠ Scope / honest limitation: DOM measurement cannot perfectly predict Chromium's
print pagination — a `break-inside: avoid` block that gets relocated to the next
page is handled by (1) `overflow: hidden`, not by this measurement. This guard
reliably catches the common, important case (a single page packed taller than its
box → content would clip → data loss). For a definitive check, render the exported
PDF to an image and read it (`pdf_to_png`, or pypdfium2) — that is ground truth.

Usage:
    python -m pdf_tool.check_overflow document.html
    python -m pdf_tool.check_overflow document.html --pdf-theme dark
    python -m pdf_tool.check_overflow document.html --tolerance 4
    python -m pdf_tool.check_overflow a.html b.html            # several at once
"""

from __future__ import annotations

import sys
from pathlib import Path

# US Letter at 96dpi = 8.5in × 96 = 816 CSS px. The measurement viewport MUST be this wide;
# see the note in check_overflow() for why a wider viewport silently hides real overflow.
_LETTER_PX = 816

# Records the fixed print-box height BEFORE we neutralize the layout.
_BOX_JS = r"""
() => Array.from(document.querySelectorAll('.page, .page-sheet'))
        .map(el => Math.round(el.clientHeight))
"""

# ⚠ The core difficulty: in the print layout a `.page` has a FIXED height and its
# `.page-main` is `flex:1`, so the browser CLIPS overflow — `scrollHeight` is
# clamped to the box and the overflow is invisible to the DOM. To see the true
# content height we must first NEUTRALIZE the constraint: make every `.page`
# height:auto/overflow:visible and every flex body `flex:none`. Then each page's
# natural `scrollHeight` reveals how tall it really wants to be. Compare that to
# the box height captured beforehand.
_NEUTRALIZE_CSS = r"""
  .page, .page-sheet {
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
  }
  .page-main, .letter-main {
    flex: none !important;
    min-height: 0 !important;
  }
"""

# After neutralizing, measure the page-main body's natural height PLUS the pinned
# footer's height — that sum is what the page actually needs. (Measuring the whole
# .page is wrong: its margin-top:auto footer collapses to 0 in an auto-height box
# and under-reports.)
_NATURAL_JS = r"""
() => Array.from(document.querySelectorAll('.page, .page-sheet')).map(el => {
  const body = el.querySelector(':scope > .page-main, :scope > .letter-main') || el;
  const foot = el.querySelector(':scope > .page-sig, :scope > .page-foot, :scope > .letter-sign, :scope > .signature');
  const bodyH = body.scrollHeight;
  const footH = foot ? foot.getBoundingClientRect().height + 12 : 0;  // +12 ≈ its padding-top gap
  return Math.round(bodyH + footH);
});
"""


def check_overflow(html_path: str, pdf_theme: str | None = None, tolerance: int = 3) -> list[dict]:
    """Return a list of overflow records (empty = clean).

    Each record: {index, box, content, overflow_px, footerCollision}.
    `tolerance` px absorbs sub-pixel rounding in Chromium's layout.
    """
    from playwright.sync_api import sync_playwright

    p_html = Path(html_path).resolve()
    if not p_html.exists():
        raise FileNotFoundError(p_html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # ⚠ CRITICAL: measure at the REAL paper width. In print media the `.page` is
        # `width: auto`, so it inherits the VIEWPORT width. Playwright's default viewport is
        # 1280px — far wider than a Letter page's 816px — which makes text wrap into fewer
        # lines and under-reports content height badly. (Measured on a real doc: 726px at
        # 1280 vs 940px at 816 — the guard reported 205px of headroom on a page that was
        # actually 9px OVER, and a footer overlap shipped. Fixed 2026-07-21.)
        page = browser.new_page(viewport={"width": _LETTER_PX, "height": 1056})
        page.goto(p_html.as_uri())
        if pdf_theme:
            page.evaluate(
                "theme => { document.documentElement.dataset.pdfTheme = theme; }",
                pdf_theme,
            )
        page.emulate_media(media="print")
        page.evaluate("() => document.body.getBoundingClientRect().height")
        # 1) box heights while the fixed print layout is still in force
        boxes = page.evaluate(_BOX_JS)
        # 2) neutralize the height/flex clamp, then read the true content heights
        page.add_style_tag(content=_NEUTRALIZE_CSS)
        page.evaluate("() => document.body.getBoundingClientRect().height")
        naturals = page.evaluate(_NATURAL_JS)
        browser.close()

    problems = []
    for i, (box, content) in enumerate(zip(boxes, naturals)):
        overflow_px = content - box
        if overflow_px > tolerance:
            problems.append(
                {"index": i + 1, "box": box, "content": content, "overflow_px": overflow_px, "footerCollision": False}
            )
    return problems


def _check_one(html_path: str, pdf_theme: str | None, tolerance: int) -> bool:
    """Print a report for one file. Returns True if clean."""
    name = Path(html_path).name
    theme = f" [{pdf_theme}]" if pdf_theme else ""
    try:
        problems = check_overflow(html_path, pdf_theme=pdf_theme, tolerance=tolerance)
    except FileNotFoundError:
        print(f"FAIL {name}{theme}: file not found")
        return False
    if not problems:
        print(f"PASS {name}{theme}: no page overflows its print box.")
        return True
    print(f"FAIL {name}{theme}: {len(problems)} page(s) overflow — the pinned footer will collide.")
    for pr in problems:
        why = []
        if pr["overflow_px"] > tolerance:
            why.append(f"content {pr['content']}px > box {pr['box']}px (over by {pr['overflow_px']}px)")
        if pr["footerCollision"]:
            why.append("footer overlaps the last content block")
        print(f"  • page {pr['index']}: " + "; ".join(why))
    print("  Fix: move a section to the next page, or tighten this page's rhythm")
    print("  (line-height / section margins). See docs/LAYOUT-SYSTEM.md § content-fit rule.")
    return False


def main() -> None:
    args = sys.argv[1:]
    pdf_theme: str | None = None
    tolerance = 3
    files: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--pdf-theme":
            pdf_theme = args[i + 1]
            i += 1
        elif a.startswith("--pdf-theme="):
            pdf_theme = a.split("=", 1)[1]
        elif a == "--tolerance":
            tolerance = int(args[i + 1])
            i += 1
        elif a.startswith("--tolerance="):
            tolerance = int(a.split("=", 1)[1])
        elif a in ("-h", "--help"):
            print(__doc__)
            raise SystemExit(0)
        else:
            files.append(a)
        i += 1

    if not files:
        print(__doc__)
        raise SystemExit(2)

    try:
        import playwright  # noqa: F401
    except ImportError:
        print(
            "check_overflow needs Playwright:\n"
            "  pip install playwright\n"
            "  playwright install chromium",
            file=sys.stderr,
        )
        raise SystemExit(2)

    all_clean = True
    for f in files:
        if not _check_one(f, pdf_theme, tolerance):
            all_clean = False
    raise SystemExit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
