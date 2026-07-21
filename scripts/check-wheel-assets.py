#!/usr/bin/env python3
"""Prove a built wheel includes public themes/ + layouts/ (PyPI gate).

A wheel that only ships ``pdf_tool/*.py`` is broken for non-checkout users —
variants, collage, and the Design Hub all need those trees. Run before any
TestPyPI / PyPI upload.

Usage (from repo root):
    python scripts/check-wheel-assets.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync-wheel-share.py")],
        cwd=ROOT,
    )
    if sync.returncode != 0:
        return sync.returncode

    with tempfile.TemporaryDirectory(prefix="pdf-designer-wheel-") as tmp:
        out = Path(tmp)
        build = subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", str(out)],
            cwd=ROOT,
        )
        if build.returncode != 0:
            print("FAIL: python -m build --wheel (pip install build)", file=sys.stderr)
            return build.returncode

        wheels = sorted(out.glob("*.whl"))
        if not wheels:
            print("FAIL: no wheel produced", file=sys.stderr)
            return 1
        wheel = wheels[0]
        with zipfile.ZipFile(wheel) as zf:
            names = zf.namelist()

    need = (
        "pdf_tool/share/themes/default-resume.json",
        "pdf_tool/share/themes/default-resume.css",
        "pdf_tool/share/layouts/collage/",
        "pdf_tool/paths.py",
    )
    missing = []
    for item in need:
        if item.endswith("/"):
            ok = any(n.startswith(item) for n in names)
        else:
            ok = item in names
        if not ok:
            missing.append(item)

    print(f"wheel: {wheel.name} ({len(names)} files)")
    if missing:
        print("FAIL: wheel missing required public assets:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print("PASS - wheel includes themes/ + layouts/ under pdf_tool/share/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
