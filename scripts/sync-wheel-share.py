#!/usr/bin/env python3
"""Copy public themes/layouts/examples into pdf_tool/share/ for wheel builds.

SSOT remains at the repo root. This tree exists only so an installed package
can find assets without a git checkout. See docs/PACKAGING.md.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARE = ROOT / "src" / "pdf_tool" / "share"

# (repo-relative source, share-relative dest)
COPIES = (
    ("themes", "themes"),
    ("layouts", "layouts"),
    ("examples/profiles/default-resume", "examples/profiles/default-resume"),
    ("profiles/you-resume.example.json", "profiles/you-resume.example.json"),
)

EXCLUDED_PARTS = {"_exports", "output", "_variants", "__pycache__"}


def public_sources() -> list[Path]:
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "--", *(src for src, _ in COPIES)],
        check=True,
        capture_output=True,
    )
    return [Path(path) for path in tracked.stdout.decode("utf-8").split("\0") if path]


def main() -> int:
    if not (ROOT / "themes" / "default-resume.json").is_file():
        print("FAIL: themes/default-resume.json missing — run from a full checkout", file=sys.stderr)
        return 1

    SHARE.mkdir(parents=True, exist_ok=True)
    sources = public_sources()
    for src_rel, dest_rel in COPIES:
        dest = SHARE / dest_rel
        prefix = Path(src_rel)
        selected = [
            source for source in sources
            if (source == prefix or prefix in source.parents)
            and not EXCLUDED_PARTS.intersection(source.parts)
            and source.suffix.lower() not in {".pyc", ".pdf", ".png"}
        ]
        if not selected:
            print(f"FAIL: no tracked public sources in {src_rel}", file=sys.stderr)
            return 1
        if dest.is_dir():
            shutil.rmtree(dest)
        for source in selected:
            target = dest if source == prefix else dest / source.relative_to(prefix)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)
        print(f"[ok] {src_rel} -> src/pdf_tool/share/{dest_rel}")

    marker = SHARE / "themes" / "default-resume.json"
    if not marker.is_file():
        print("FAIL: share sync incomplete", file=sys.stderr)
        return 1
    print(f"PASS - wheel share ready at {SHARE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
