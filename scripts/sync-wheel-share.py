#!/usr/bin/env python3
"""Copy public themes/layouts/examples into pdf_tool/share/ for wheel builds.

SSOT remains at the repo root. This tree exists only so an installed package
can find assets without a git checkout. See docs/PACKAGING.md.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARE = ROOT / "src" / "pdf_tool" / "share"

# (repo-relative source, share-relative dest)
COPIES = (
    ("themes", "themes"),
    ("layouts", "layouts"),
    ("examples/profiles/default-resume", "examples/profiles/default-resume"),
)


def main() -> int:
    if not (ROOT / "themes" / "default-resume.json").is_file():
        print("FAIL: themes/default-resume.json missing — run from a full checkout", file=sys.stderr)
        return 1

    SHARE.mkdir(parents=True, exist_ok=True)
    for src_rel, dest_rel in COPIES:
        src = ROOT / src_rel
        dest = SHARE / dest_rel
        if not src.exists():
            print(f"FAIL: missing {src}", file=sys.stderr)
            return 1
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            src,
            dest,
            ignore=shutil.ignore_patterns(
                "_exports",
                "_variants",
                "__pycache__",
                "*.pyc",
                "*.pdf",
                "*.png",
            ),
        )
        print(f"[ok] {src_rel} -> src/pdf_tool/share/{dest_rel}")

    marker = SHARE / "themes" / "default-resume.json"
    if not marker.is_file():
        print("FAIL: share sync incomplete", file=sys.stderr)
        return 1
    print(f"PASS - wheel share ready at {SHARE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
