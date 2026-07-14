"""Render a document's pages to PNG images -- one PNG per page.

    python -m pdf_tool.pdf_to_png resume.html
    python -m pdf_tool.pdf_to_png resume.html out-dir --scale 2

This is how an agent SEES its own output. Export, render, then *read the PNGs* --
that is the verification loop, and it is the whole reason this module exists.

WHY IT TAKES HTML, NOT PDF
--------------------------
It used to rasterize the exported PDF with PyMuPDF. PyMuPDF is **AGPL-3.0**, and this
project is MIT -- an MIT package cannot carry a mandatory AGPL dependency without the
license claim becoming incoherent. So PyMuPDF is gone.

The replacement is not a workaround; it is better. Every document in this repo wraps
each printed page in a `.page` element (that is the pagination contract -- see
docs/EXPORTS.md). So we screenshot **each `.page` element** in the *same* headless
Chromium, in the *same* print media mode, that html_to_pdf uses to print. The image is
the exact element the PDF renders. No PDF round-trip, no second rasterizer, no
approximation, and no new dependency -- Playwright was already here.

Fallback: a document with no `.page` wrappers is sliced into Letter-height viewport
screenshots. That is approximate (it cannot see CSS page breaks), and it says so.

Setup: pip install -e .   (Playwright only -- Apache-2.0)
"""

from pathlib import Path
import sys

# US Letter at 96 CSS px/in.
_PAGE_W = 816
_PAGE_H = 1056


def render_to_png(
    source: str,
    output_dir: str | None = None,
    scale: float = 2.0,
    pdf_theme: str | None = None,
) -> list[Path]:
    """Render each page of an HTML document to a PNG. Returns the output paths."""
    from playwright.sync_api import sync_playwright

    src = Path(source).resolve()
    if not src.exists():
        raise FileNotFoundError(src)

    if src.suffix.lower() == ".pdf":
        raise SystemExit(
            f"\n{src.name} is a PDF.\n\n"
            "This module renders the HTML SOURCE, not the exported PDF -- it screenshots the\n"
            "same DOM, in the same browser, that html_to_pdf prints, so the image is exact.\n"
            "(The old PDF rasterizer was PyMuPDF, which is AGPL and incompatible with this\n"
            "project's MIT license. See docs/LICENSING-NOTES.md.)\n\n"
            f"Try:  python -m pdf_tool.pdf_to_png {src.with_suffix('.html').name}\n"
        )

    out_dir = (
        Path(output_dir).resolve()
        if output_dir
        else src.parent / "_exports" / f"{src.stem}-png"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": _PAGE_W, "height": _PAGE_H},
            device_scale_factor=scale,
        )
        page.goto(src.as_uri(), wait_until="networkidle")

        if pdf_theme:
            page.evaluate(
                "t => document.documentElement.setAttribute('data-pdf-theme', t)",
                pdf_theme,
            )

        # Print media, so @media print rules apply -- exactly as in html_to_pdf.
        page.emulate_media(media="print")

        sheets = page.query_selector_all(".page")
        if sheets:
            # The faithful path: one screenshot per printed page element.
            for index, sheet in enumerate(sheets, 1):
                out = out_dir / f"{src.stem}-page-{index}.png"
                sheet.screenshot(path=str(out))
                outputs.append(out)
        else:
            # No .page wrappers -- slice the viewport. Approximate: this cannot see CSS
            # page breaks, so a section may be cut where the real PDF would not cut it.
            height = page.evaluate("document.documentElement.scrollHeight")
            count = max(1, -(-height // _PAGE_H))
            print(
                f"note: {src.name} has no .page wrappers, so pages are approximated by "
                f"slicing at {_PAGE_H}px. Real page breaks may differ. "
                "Wrap each page in a .page element for exact output.",
                file=sys.stderr,
            )
            for index in range(count):
                out = out_dir / f"{src.stem}-page-{index + 1}.png"
                page.screenshot(
                    path=str(out),
                    clip={
                        "x": 0,
                        "y": index * _PAGE_H,
                        "width": _PAGE_W,
                        "height": min(_PAGE_H, height - index * _PAGE_H),
                    },
                )
                outputs.append(out)

        browser.close()

    return outputs


# Back-compat: the old name, used by preview.py.
render_pdf_to_png = render_to_png


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        raise SystemExit(1)

    scale = 2.0
    pdf_theme = None
    cleaned: list[str] = []
    skip_next = False
    for index, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg == "--scale":
            if index + 1 >= len(args):
                raise SystemExit("--scale requires a numeric value")
            scale = float(args[index + 1])
            skip_next = True
            continue
        if arg.startswith("--scale="):
            scale = float(arg.split("=", 1)[1])
            continue
        if arg == "--pdf-theme":
            if index + 1 >= len(args):
                raise SystemExit("--pdf-theme requires a value, e.g. dark")
            pdf_theme = args[index + 1]
            skip_next = True
            continue
        if arg.startswith("--pdf-theme="):
            pdf_theme = arg.split("=", 1)[1]
            continue
        cleaned.append(arg)

    source = cleaned[0]
    output_dir = cleaned[1] if len(cleaned) > 1 else None

    try:
        outputs = render_to_png(source, output_dir, scale=scale, pdf_theme=pdf_theme)
    except ModuleNotFoundError:
        print(
            "Playwright is not installed yet. Run:\n"
            "  pip install -e .\n"
            "  playwright install chromium"
        )
        raise SystemExit(1)

    for path in outputs:
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
