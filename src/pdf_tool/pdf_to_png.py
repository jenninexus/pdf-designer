"""Render PDF pages to PNG images.

Usage:
    python -m pdf_tool.pdf_to_png path/to/document.pdf
    python -m pdf_tool.pdf_to_png path/to/document.pdf path/to/output-dir --scale 2

This is intended for resume/cover-letter preview exports after HTML -> PDF.
It writes one PNG per page using PyMuPDF. Without an explicit output dir,
PNGs go under an _exports directory next to the source PDF.

Setup:
    pip install pymupdf
"""

from pathlib import Path
import sys


def render_pdf_to_png(pdf_path: str, output_dir: str | None = None, scale: float = 2.0) -> list[Path]:
    """Render each PDF page to a PNG and return the output paths."""
    import fitz

    pdf = Path(pdf_path).resolve()
    if not pdf.exists():
        raise FileNotFoundError(pdf)

    out_dir = Path(output_dir).resolve() if output_dir else pdf.parent / "_exports" / f"{pdf.stem}-png"
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    outputs: list[Path] = []
    matrix = fitz.Matrix(scale, scale)
    for index, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = out_dir / f"{pdf.stem}-page-{index}.png"
        pix.save(out)
        outputs.append(out)
    return outputs


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        raise SystemExit(1)

    scale = 2.0
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
        cleaned.append(arg)

    pdf = cleaned[0]
    output_dir = cleaned[1] if len(cleaned) > 1 else None

    try:
        outputs = render_pdf_to_png(pdf, output_dir, scale=scale)
    except ModuleNotFoundError:
        print("PyMuPDF is not installed yet. Run:\n  pip install pymupdf")
        raise SystemExit(1)

    for path in outputs:
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
