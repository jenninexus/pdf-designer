#!/usr/bin/env python3
"""White-label smoke — prove a fresh clone works from tracked files only.

No ``storage/`` required. Run from any checkout after::

    pip install -e ".[dev]" && playwright install chromium
    python scripts/smoke-white-label.py

Exits 0 only when check_generation, light+dark export, and ATS text-layer all pass.
PDFs land under ``examples/profiles/default-resume/_exports/`` (gitignored).

See docs/GETTING-STARTED.md and docs/PRODUCT.md.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples" / "profiles" / "default-resume" / "default-resume.html"
EXPORT_DIR = REPO / "examples" / "profiles" / "default-resume" / "_exports"
PUBLIC_TEXT_ROOTS = (
    REPO / ".claude" / "commands",
    REPO / ".config" / "mcp-pdf-designer.example.json",
    REPO / "examples",
)
PRIVATE_TRACKED_ROOTS = (
    ".codex",
    "storage",
    "users",
    "vaults",
    "profiles",
    "resumes",
    "_job-apps",
    "applications",
    "collages",
    "brands",
)
PRIVATE_MARKERS = (
    "jenninexus",
    "jenni",
    "shade",
    "synephi",
    "martian",
    "martian games",
    "hasbro",
    "halfbrick",
    "oddworld",
    "kixeye",
    "netflix",
    "alignerr",
    "sony",
    "segopc",
    "beethoven",
    "livphi",
    r"c:\github\pdf-designer",
)


def _run(label: str, argv: list[str]) -> None:
    print(f"\n==> {label}")
    print("    " + " ".join(argv))
    result = subprocess.run(argv, cwd=REPO)
    if result.returncode != 0:
        raise SystemExit(f"FAIL: {label} (exit {result.returncode})")


def _assert_public_path() -> None:
    if not EXAMPLE.is_file():
        raise SystemExit(f"FAIL: missing public example: {EXAMPLE.relative_to(REPO)}")
    # Soft check: smoke must not *require* storage/. Presence is fine (local workspaces).
    storage = REPO / "storage"
    if storage.is_dir():
        print(f"[ok] storage/ exists locally (ignored for smoke) - {storage}")
    else:
        print("[ok] no storage/ - pure public-path clone")


def _public_text_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_TEXT_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        if root.name == "commands":
            files.extend(sorted(root.glob("*.example.md")))
            continue
        files.extend(
            sorted(
                path
                for path in root.rglob("*")
                if path.is_file()
                and "_exports" not in path.parts
                and "_variants" not in path.parts
                and path.suffix.lower() in {".html", ".json", ".md", ".css"}
            )
        )
    return files


def _assert_public_privacy() -> None:
    offenders: list[str] = []
    for path in _public_text_files():
        text = path.read_text(encoding="utf-8").lower()
        for marker in PRIVATE_MARKERS:
            if marker in text:
                offenders.append(f"{path.relative_to(REPO)}: {marker}")
        normalized = text.replace("\\\\", "\\")
        if re.search(r"\b[a-z]:\\(?!\.\.\.)[a-z0-9_.-]+", normalized):
            offenders.append(f"{path.relative_to(REPO)}: absolute Windows path")

    if offenders:
        details = "\n  - ".join(offenders)
        raise SystemExit(f"FAIL: private workspace markers in public examples/seeds:\n  - {details}")

    if (REPO / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", *PRIVATE_TRACKED_ROOTS],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        unexpected = [
            path
            for path in tracked
            if not (
                Path(path).name == "README.md"
                or Path(path).name.endswith(".example.json")
            )
        ]
        if unexpected:
            details = "\n  - ".join(unexpected)
            raise SystemExit(f"FAIL: private paths are tracked:\n  - {details}")

    print(
        "[ok] Resume Studio/public-seed privacy boundary "
        f"({len(_public_text_files())} source files scanned)"
    )


def _export_light_dark(out: Path) -> tuple[Path, Path]:
    out.mkdir(parents=True, exist_ok=True)
    # Wipe prior smoke PDFs so --never-overwrite doesn't accumulate -v2/-v3 noise.
    for old in out.glob("default-resume-*.pdf"):
        old.unlink(missing_ok=True)

    _run(
        "export light (ATS)",
        [
            sys.executable,
            "-m",
            "pdf_tool.html_to_pdf",
            str(EXAMPLE),
            "--output-dir",
            str(out),
        ],
    )
    _run(
        "export dark (branded)",
        [
            sys.executable,
            "-m",
            "pdf_tool.html_to_pdf",
            str(EXAMPLE),
            "--output-dir",
            str(out),
            "--pdf-theme",
            "dark",
        ],
    )
    light = out / "default-resume-light.pdf"
    dark = out / "default-resume-dark.pdf"
    if not light.is_file() or not dark.is_file():
        raise SystemExit(f"FAIL: expected {light.name} and {dark.name} under {out}")
    return light, dark


def _assert_page_count(pdf: Path, expected: int) -> None:
    from pypdf import PdfReader

    n = len(PdfReader(str(pdf)).pages)
    if n != expected:
        raise SystemExit(f"FAIL: {pdf.name} has {n} pages (want {expected})")
    print(f"[ok] {pdf.name}: {n} page(s)")


def main() -> int:
    # Windows consoles are often cp1252 — keep status lines ASCII-only.
    print("White-label smoke - pdf-designer")
    print(f"repo: {REPO}")
    _assert_public_path()
    _assert_public_privacy()

    # Prefer a clean temp dir; also mirror into the example _exports for Hub browsing.
    with tempfile.TemporaryDirectory(prefix="pdf-designer-smoke-") as tmp:
        tmp_out = Path(tmp)
        _run(
            "QA gate (check_generation)",
            [sys.executable, "-m", "pdf_tool.check_generation", str(EXAMPLE)],
        )
        light, dark = _export_light_dark(tmp_out)
        _assert_page_count(light, 2)
        _assert_page_count(dark, 2)
        _run(
            "ATS text layer (light PDF)",
            [sys.executable, "-m", "pdf_tool.check_ats", str(light)],
        )

        # Leave a copy next to the example for Design Hub / human inspection.
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        for src in (light, dark):
            dest = EXPORT_DIR / src.name
            shutil.copy2(src, dest)
            print(f"[ok] copied -> {dest.relative_to(REPO)}")

    print("\nPASS - public path works without storage/")
    print("Next: python -m pdf_tool.preview  ->  http://127.0.0.1:8787/")
    print("Docs: docs/GETTING-STARTED.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
