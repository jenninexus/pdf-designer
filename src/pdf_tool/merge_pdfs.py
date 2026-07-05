"""Merge multiple PDFs into one submission bundle.

Usage:
    python -m pdf_tool.merge_pdfs output.pdf input-1.pdf input-2.pdf
    python -m pdf_tool.merge_pdfs output.pdf cover-letter.pdf resume.pdf --require-letter
    python -m pdf_tool.merge_pdfs output.pdf cover-letter.pdf resume.pdf --title "Cover Letter and Resume"

By default, an existing output file is not overwritten. A -v2, -v3, ...
suffix is used unless --force is passed.
"""

from pathlib import Path
import sys


LETTER_WIDTH_PT = 612.0
LETTER_HEIGHT_PT = 792.0


def _next_available_path(base: Path) -> Path:
    if not base.exists():
        return base
    n = 2
    while True:
        candidate = base.with_name(f"{base.stem}-v{n}{base.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def _is_letter_page(page, tolerance: float = 0.5) -> bool:
    box = page.mediabox
    width = float(box.width)
    height = float(box.height)
    return (
        abs(width - LETTER_WIDTH_PT) <= tolerance
        and abs(height - LETTER_HEIGHT_PT) <= tolerance
    )


def merge_pdfs(
    output_pdf: str,
    input_pdfs: list[str],
    *,
    force: bool = False,
    require_letter: bool = False,
    title: str | None = None,
) -> Path:
    """Merge input_pdfs into output_pdf and return the written path."""
    from pypdf import PdfReader, PdfWriter

    if len(input_pdfs) < 2:
        raise ValueError("merge_pdfs requires at least two input PDFs")

    out_path = Path(output_pdf).resolve()
    if out_path.exists() and not force:
        out_path = _next_available_path(out_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()

    for pdf in input_pdfs:
        in_path = Path(pdf).resolve()
        if not in_path.exists():
            raise FileNotFoundError(in_path)

        reader = PdfReader(str(in_path))
        for index, page in enumerate(reader.pages, 1):
            if require_letter and not _is_letter_page(page):
                box = page.mediabox
                width = float(box.width) / 72
                height = float(box.height) / 72
                raise ValueError(
                    f"{in_path.name} page {index} is {width:.2f} x {height:.2f} in, "
                    "not US Letter 8.5 x 11"
                )
            writer.add_page(page)

    if title:
        writer.add_metadata({"/Title": title})

    with out_path.open("wb") as handle:
        writer.write(handle)

    return out_path


def main() -> None:
    raw_args = sys.argv[1:]
    force = any(arg in ("--force", "-f") for arg in raw_args)
    require_letter = "--require-letter" in raw_args
    title = None
    args: list[str] = []
    skip_next = False

    for index, arg in enumerate(raw_args):
        if skip_next:
            skip_next = False
            continue
        if arg in ("--force", "-f", "--require-letter"):
            continue
        if arg == "--title":
            if index + 1 >= len(raw_args):
                raise SystemExit("--title requires a value")
            title = raw_args[index + 1]
            skip_next = True
            continue
        if arg.startswith("--title="):
            title = arg.split("=", 1)[1]
            continue
        args.append(arg)

    if len(args) < 3:
        print(__doc__)
        raise SystemExit(1)

    try:
        result = merge_pdfs(
            args[0],
            args[1:],
            force=force,
            require_letter=require_letter,
            title=title,
        )
    except ModuleNotFoundError:
        print("pypdf is not installed yet. Run:\n  pip install pypdf")
        raise SystemExit(1)

    print(f"Saved: {result}")


if __name__ == "__main__":
    main()
