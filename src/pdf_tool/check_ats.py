"""ATS text-layer guard — show what a PDF parser actually reads.

Usage:
    python -m pdf_tool.check_ats <resume.pdf>
    python -m pdf_tool.check_ats <resume.pdf> --json

Exits 1 if word count < 40, or if required section cues are missing / split
(Jobright / Indeed style parsers). Exits 2 on bad args. Exits 0 when healthy.

How to know a résumé is parseable (SSOT: docs/JOB-ASSESSMENT.md § ATS PARSE SAFETY):
  1. Export the LIGHT PDF.
  2. Run this command — read the text layer + the cue checklist.
  3. If YOU cannot find Job Title / Work Experience / Education as contiguous
     phrases in the dump, neither can the board.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Soft cues — reported when present (do not fail the gate alone).
_SECTION_CUES = (
    "work experience",
    "experience",
    "education",
    "skills",
    "summary",
    "objective",
    "employment",
    "job title",
    "projects",
    "certifications",
    "contact",
)

# Hard cues — Jobright / board upload parsers look for these as real fields.
# "work experience" preferred over bare "experience".
_REQUIRED_CUES = (
    "job title",
    "work experience",
    "education",
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


def _collapsed(s: str) -> str:
    return re.sub(r"\s+", "", s.lower())


def extract_ats_text(pdf_path: Path):
    """Return (pages, full_text, word_count, section_cues, cue_report)."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        pages.append({"page": i, "text": text, "words": len(re.findall(r"\b\w+\b", text))})

    full_text = "\n".join(p["text"] for p in pages)
    word_count = len(re.findall(r"\b\w+\b", full_text))
    lower = full_text.lower()
    collapsed = _collapsed(full_text)
    cues = [c for c in _SECTION_CUES if c in lower]

    cue_report = {}
    for cue in _SECTION_CUES:
        contiguous = cue in lower
        collapsed_hit = _collapsed(cue) in collapsed
        if contiguous:
            status = "ok"
        elif collapsed_hit:
            status = "split"  # glyphs have spaces (e.g. "W ORK EXPERIENCE")
        else:
            status = "missing"
        cue_report[cue] = status

    return pages, full_text, word_count, cues, cue_report


def check_ats(pdf_path: Path, as_json: bool = False) -> int:
    if not pdf_path.exists():
        _out(f"file not found: {pdf_path}")
        return 2

    try:
        pages, full_text, word_count, cues, cue_report = extract_ats_text(pdf_path)
    except Exception as e:
        _out(f"cannot read PDF: {e}")
        return 2

    missing_required = [c for c in _REQUIRED_CUES if cue_report.get(c) != "ok"]
    # Bare "experience" does NOT satisfy Jobright — require the contiguous phrase.
    split_required = [c for c in _REQUIRED_CUES if cue_report.get(c) == "split"]

    if as_json:
        payload = {
            "path": str(pdf_path),
            "pages": len(pages),
            "word_count": word_count,
            "section_cues": cues,
            "cue_report": cue_report,
            "required_cues": list(_REQUIRED_CUES),
            "missing_required": missing_required,
            "split_required": split_required,
            "text": full_text,
            "per_page": pages,
        }
        _out(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        _out(f"\n{'=' * 78}")
        _out(f"  ATS TEXT LAYER  ·  {pdf_path.name}")
        _out(f"{'=' * 78}")
        _out(f"  Pages: {len(pages)}  ·  Words: {word_count}")
        _out("  Required cues (Jobright / board parsers):")
        for cue in _REQUIRED_CUES:
            st = cue_report.get(cue, "missing")
            mark = {"ok": "OK ", "split": "SPLIT", "missing": "MISS"}.get(st, st)
            _out(f"    [{mark}] {cue}")
        soft = [c for c in cues if c not in _REQUIRED_CUES]
        if soft:
            _out(f"  Also found: {', '.join(soft)}")
        _out(f"\n{'-' * 78}")
        for p in pages:
            preview = p["text"].strip().replace("\n", " ")[:200]
            _out(f"  Page {p['page']} ({p['words']} words): {preview or '(empty)'}")
        _out(f"{'-' * 78}")
        _out("  Read the dump above. If Job Title / Work Experience / Education are not")
        _out("  contiguous phrases a human can find, fix the HTML — not the board.")
        _out(f"{'-' * 78}\n")

    if word_count < 40:
        _out(f"FAIL: only {word_count} words — ATS parsers may see an empty document.")
        return 1

    if missing_required:
        parts = []
        for c in missing_required:
            st = cue_report.get(c, "missing")
            if st == "split":
                parts.append(
                    f"{c!r} is SPLIT in the text layer (e.g. 'W ORK EXPERIENCE') — "
                    "use a system font on section h2 / reduce letter-spacing (docs/JOB-ASSESSMENT.md)"
                )
            else:
                parts.append(
                    f"{c!r} missing — use the exact heading (Job Title · Work Experience · Education)"
                )
        _out("FAIL: required ATS section cues not parseable:")
        for p in parts:
            _out(f"  - {p}")
        return 1

    _out("PASS: text layer looks readable + required section cues are contiguous.")
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
