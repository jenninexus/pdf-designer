"""check_overflow — the pinned-footer overlap guard.

The layout system pins the footer/signature to the bottom of a FIXED-HEIGHT
`.page` (via `margin-top:auto`). If a page's content is TALLER than that box,
the content overflows and the pinned signature lands on top of the last lines —
the 2026-07-19 overlap bug. A page-count check does NOT catch this (the PDF still
has the right number of pages; the last one just has garbage stacked on it).

This guard renders the document in the SAME headless Chromium the exporter uses,
in `print` media, and for every `.page` / `.page-sheet` compares the content's
`scrollHeight` to the box's `clientHeight`. Any page whose content overflows is
reported; the command exits non-zero so it can gate an export in CI or a script.

Usage:
    python -m pdf_tool.check_overflow document.html
    python -m pdf_tool.check_overflow document.html --pdf-theme dark
    python -m pdf_tool.check_overflow document.html --tolerance 4
    python -m pdf_tool.check_overflow a.html b.html            # several at once
"""

from __future__ import annotations

import sys
from pathlib import Path

# JS run inside the print-media page. Returns one record per .page element with
# the box height (clientHeight) and the content height (scrollHeight). A page
# overflows when scrollHeight > clientHeight + tolerance.
_MEASURE_JS = r"""
() => {
  const pages = Array.from(document.querySelectorAll('.page, .page-sheet'));
  return pages.map((el, i) => {
    // Height of the fixed print box vs. the height the content actually needs.
    const box = el.clientHeight;
    const content = el.scrollHeight;
    // Also detect a pinned footer sitting visually on top of prior content:
    // if the last-child footer's top is above the previous element's bottom.
    let footerCollision = false;
    const footer = el.querySelector(':scope > .page-sig, :scope > .page-foot, :scope > .letter-sign, :scope > .signature');
    if (footer) {
      const fr = footer.getBoundingClientRect();
      // previous meaningful sibling (the last content block)
      let prev = footer.previousElementSibling;
      while (prev && prev.getBoundingClientRect().height === 0) prev = prev.previousElementSibling;
      if (prev) {
        const pr = prev.getBoundingClientRect();
        if (fr.top < pr.bottom - 1) footerCollision = true;
      }
    }
    return { index: i + 1, box: Math.round(box), content: Math.round(content), footerCollision };
  });
}
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
        page = browser.new_page()
        page.goto(p_html.as_uri())
        if pdf_theme:
            page.evaluate(
                "theme => { document.documentElement.dataset.pdfTheme = theme; }",
                pdf_theme,
            )
        page.emulate_media(media="print")
        # Force layout to settle in print media before measuring.
        page.evaluate("() => document.body.getBoundingClientRect().height")
        records = page.evaluate(_MEASURE_JS)
        browser.close()

    problems = []
    for r in records:
        overflow_px = r["content"] - r["box"]
        if overflow_px > tolerance or r["footerCollision"]:
            problems.append({**r, "overflow_px": overflow_px})
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
