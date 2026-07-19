"""Render any HTML file to PDF using a real headless browser.

Why a headless browser and not reportlab/wkhtmltopdf: real documents (resumes,
letters, forms) rely on real CSS - grid/flex layout, @media print rules,
web fonts. Only a browser engine renders that correctly. Playwright's
page.pdf() drives headless Chromium, so the output matches exactly what a
human gets from "Print -> Save as PDF" in a real browser, without a human
doing it by hand every time.

One-time setup (not run automatically by this module):
    pip install playwright
    playwright install chromium

Usage:
    python -m pdf_tool.html_to_pdf path/to/document.html
    python -m pdf_tool.html_to_pdf path/to/document.html path/to/output.pdf
    python -m pdf_tool.html_to_pdf path/to/document.html --output-dir path/to/_exports
    python -m pdf_tool.html_to_pdf path/to/document.html --force
    python -m pdf_tool.html_to_pdf path/to/document.html --pdf-theme dark
    python -m pdf_tool.html_to_pdf path/to/document.html --variants

By default, re-running against the same document.html does NOT overwrite a
previous export - it writes document-v2.pdf, document-v3.pdf, etc., so you
always keep the last version you sent somewhere. Default exports go under an
_exports directory next to the source HTML. Pass an explicit output path
(second positional arg), --output-dir, or --force to control that behavior.

``--variants`` exports a light PDF for each public palette (default-resume +
``themes/presets/``) into ``_variants/<stem>/`` — same as
``python -m pdf_tool.variants <doc>.html``.
"""

import sys
from pathlib import Path


def _next_available_path(base: Path) -> Path:
    """Return base, or the next base-vN sibling that doesn't exist yet."""
    if not base.exists():
        return base
    n = 2
    while True:
        candidate = base.with_name(f"{base.stem}-v{n}{base.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def export_html_to_pdf(
    html_path: str,
    pdf_path: str | None = None,
    output_dir: str | None = None,
    page_format: str = "Letter",
    force: bool = False,
    pdf_theme: str | None = None,
    css_vars: dict | None = None,
) -> Path:
    """Render html_path to PDF and return the output path.

    Uses print media emulation and CSS @page sizing so @media print rules
    in the source HTML apply the same way they would in a browser's own
    print dialog. The default page_format is US Letter: 8.5 x 11 inches.
    For deterministic resume output, pair this with an explicit CSS rule:
    `@page { size: Letter; margin: ... }`.

    If pdf_theme is given, it is exposed to the document as:
    `document.documentElement.dataset.pdfTheme = "<value>"`.
    Templates can use selectors such as
    `@media print { html[data-pdf-theme="dark"] { ... } }` to keep Letter
    pagination while rendering a branded dark PDF variant.

    If pdf_path is not given, the default output lives under an _exports
    directory next to html_path, or under output_dir when provided. Unless
    force=True, an existing file at that default path is never overwritten -
    a -v2, -v3, ... suffix is used instead, so previously-sent PDFs are never
    silently replaced. Passing an explicit pdf_path always writes there
    exactly, overwrite or not - versioning only applies to generated output
    paths.
    """
    from playwright.sync_api import sync_playwright

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        raise FileNotFoundError(html_path)

    if pdf_path:
        out_path = Path(pdf_path).resolve()
    else:
        export_dir = Path(output_dir).resolve() if output_dir else html_path.parent / "_exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        # Dual-mode convention: stem-light.pdf (ATS) / stem-dark.pdf (branded).
        # Explicit pdf_path still wins when the caller wants a custom name.
        theme_label = (pdf_theme or "light").strip().lower() or "light"
        default_path = export_dir / f"{html_path.stem}-{theme_label}.pdf"
        out_path = default_path if force else _next_available_path(default_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        if pdf_theme:
            page.evaluate(
                "theme => { document.documentElement.dataset.pdfTheme = theme; }",
                pdf_theme,
            )
        if css_vars:
            # Palette override (e.g. from the preview server's palette swapper):
            # inline styles on <html> outrank :root rules, so the exported PDF
            # matches a palette-swapped screen preview exactly.
            page.evaluate(
                "vars => { for (const [k, v] of Object.entries(vars)) document.documentElement.style.setProperty(k, v); }",
                css_vars,
            )
        page.emulate_media(media="print")
        page.pdf(
            path=str(out_path),
            format=page_format,
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()

    return out_path


def _guard_palette(input_html: str) -> None:
    """Refuse to export a document that violates the house palette rule.

    This runs BY DEFAULT, on every export. It used to be a separate command the
    docs told you to remember -- and a brown light-mode accent shipped anyway,
    because "run the guard first" is not a guarantee, it is a hope. A rule that
    is only enforced when someone remembers it is not enforced.

    Escape hatch: --skip-palette-check (say why in the commit).
    """
    try:
        from .check_palette import check_file
    except ImportError:
        return  # guard unavailable -- never block an export on the guard's own bug

    hits = check_file(Path(input_html))
    if not hits:
        return

    print(f"\nBLOCKED: {input_html} uses banned colors.\n", file=sys.stderr)
    for line_no, hex6, label in hits:
        print(f"  line {line_no}: {hex6}  <-  {label}", file=sys.stderr)
    print(
        "\nHouse rule: no brown, no mustard, no lime/puke green.\n"
        "On WHITE, amber has no readable dark form -- it turns brown. Give the amber\n"
        "role to another hue from the palette instead. See themes/PALETTE-RULES.md.\n"
        "\nTo export anyway (rare, and say why): --skip-palette-check\n",
        file=sys.stderr,
    )
    raise SystemExit(2)


def _warn_overflow(input_html: str, pdf_theme: str | None) -> None:
    """Warn (do not block) if any .page overflows its fixed print box.

    A pinned footer sits at the bottom of a fixed-height .page; if the content
    is taller than the box it collides with the last lines (the 2026-07-19
    overlap bug). This is advisory — some templates legitimately differ — but a
    surprised author beats a shipped collision. Escape hatch: --skip-overflow-check.
    """
    try:
        from .check_overflow import check_overflow
    except ImportError:
        return
    try:
        problems = check_overflow(input_html, pdf_theme=pdf_theme)
    except Exception:
        return  # never fail an export on the guard's own error
    if not problems:
        return
    print(
        f"\n⚠ OVERFLOW: {len(problems)} page(s) exceed the print box — the pinned "
        "footer/signature may collide with the last lines.",
        file=sys.stderr,
    )
    for pr in problems:
        bits = []
        if pr.get("overflow_px", 0) > 0:
            bits.append(f"content {pr['content']}px > box {pr['box']}px")
        if pr.get("footerCollision"):
            bits.append("footer overlaps content")
        print(f"  • page {pr['index']}: " + "; ".join(bits), file=sys.stderr)
    print(
        "  Move a section to the next page or tighten this page's rhythm "
        "(docs/LAYOUT-SYSTEM.md § content-fit). "
        "python -m pdf_tool.check_overflow <doc>.html for detail.\n",
        file=sys.stderr,
    )


def main() -> None:
    raw_args = sys.argv[1:]
    force = any(a in ("--force", "-f") for a in raw_args)
    skip_palette = "--skip-palette-check" in raw_args
    skip_overflow = "--skip-overflow-check" in raw_args
    want_variants = "--variants" in raw_args
    pdf_theme = None
    output_dir = None
    args = []
    skip_next = False
    for index, arg in enumerate(raw_args):
        if skip_next:
            skip_next = False
            continue
        if arg in ("--force", "-f"):
            continue
        if arg == "--skip-palette-check":
            continue
        if arg == "--skip-overflow-check":
            continue
        if arg == "--variants":
            continue
        if arg == "--pdf-theme":
            if index + 1 >= len(raw_args):
                raise SystemExit("--pdf-theme requires a value, e.g. dark")
            pdf_theme = raw_args[index + 1]
            skip_next = True
            continue
        if arg.startswith("--pdf-theme="):
            pdf_theme = arg.split("=", 1)[1]
            continue
        if arg == "--output-dir":
            if index + 1 >= len(raw_args):
                raise SystemExit("--output-dir requires a path")
            output_dir = raw_args[index + 1]
            skip_next = True
            continue
        if arg.startswith("--output-dir="):
            output_dir = arg.split("=", 1)[1]
            continue
        args.append(arg)

    if len(args) < 1:
        print(__doc__)
        raise SystemExit(1)

    input_html = args[0]

    if want_variants:
        from .variants import export_variants

        try:
            export_variants(input_html, skip_palette=skip_palette)
        except ModuleNotFoundError:
            print(
                "Playwright is not installed yet. Run:\n"
                "  pip install playwright\n"
                "  playwright install chromium\n"
                "then re-run this command."
            )
            raise SystemExit(1)
        return

    output_pdf = args[1] if len(args) > 1 else None

    if not skip_palette:
        _guard_palette(input_html)

    try:
        result = export_html_to_pdf(
            input_html,
            output_pdf,
            output_dir=output_dir,
            force=force,
            pdf_theme=pdf_theme,
        )
    except ModuleNotFoundError:
        print(
            "Playwright is not installed yet. Run:\n"
            "  pip install playwright\n"
            "  playwright install chromium\n"
            "then re-run this command."
        )
        raise SystemExit(1)

    print(f"Saved: {result}")

    if not skip_overflow:
        _warn_overflow(input_html, pdf_theme)


if __name__ == "__main__":
    main()
