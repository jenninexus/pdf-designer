"""ATS text-layer guard — show what a PDF parser actually reads.

Usage:
    python -m pdf_tool.check_ats <resume.pdf>
    python -m pdf_tool.check_ats <resume.pdf> --json

Exits 1 if word count < 40 (likely image-only or broken text layer).
Exits 2 on bad args. Exits 0 when the text layer looks healthy.
"""

import json
import re
import sys
from pathlib import Path

_SECTION_CUES = (
    "experience",
    "education",
    "skills",
    "summary",
    "objective",
    "employment",
    "projects",
    "certifications",
    "contact",
)


def _configure_stdout():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def _out(*args, **kwargs):
    print(*args, **kwargs)


def extract_ats_text(pdf_path: Path):
    """Return (pages, full_text, word_count, section_cues)."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        pages.append({"page": i, "text": text, "words": len(re.findall(r"\b\w+\b", text))})

    full_text = "\n".join(p["text"] for p in pages)
    word_count = len(re.findall(r"\b\w+\b", full_text))
    lower = full_text.lower()
    cues = [c for c in _SECTION_CUES if c in lower]
    return pages, full_text, word_count, cues


def check_ats(pdf_path: Path, as_json: bool = False) -> int:
    if not pdf_path.exists():
        _out(f"file not found: {pdf_path}")
        return 2

    try:
        pages, full_text, word_count, cues = extract_ats_text(pdf_path)
    except Exception as e:
        _out(f"cannot read PDF: {e}")
        return 2

    if as_json:
        payload = {
            "path": str(pdf_path),
            "pages": len(pages),
            "word_count": word_count,
            "section_cues": cues,
            "text": full_text,
            "per_page": pages,
        }
        _out(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        _out(f"\n{'=' * 78}")
        _out(f"  ATS TEXT LAYER  ·  {pdf_path.name}")
        _out(f"{'=' * 78}")
        _out(f"  Pages: {len(pages)}  ·  Words: {word_count}")
        if cues:
            _out(f"  Section cues: {', '.join(cues)}")
        else:
            _out("  Section cues: (none detected)")
        _out(f"\n{'-' * 78}")
        for p in pages:
            preview = p["text"].strip().replace("\n", " ")[:200]
            _out(f"  Page {p['page']} ({p['words']} words): {preview or '(empty)'}")
        _out(f"{'-' * 78}\n")

    if word_count < 40:
        _out(f"FAIL: only {word_count} words — ATS parsers may see an empty document.")
        return 1

    _out("PASS: text layer looks readable.")
    return 0


def main(argv):
    _configure_stdout()
    args = [a for a in argv if a != "--json"]
    as_json = "--json" in argv

    if len(args) != 1:
        _out(__doc__)
        return 2

    return check_ats(Path(args[0]), as_json=as_json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
