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
import shutil
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

    # setuptools reuses build/lib and does not remove files that disappeared from
    # the source tree. A prior build can therefore smuggle ignored _variants/
    # PDFs into a later wheel even though sync-wheel-share.py excludes them.
    build_tree = ROOT / "build"
    if build_tree.exists():
        shutil.rmtree(build_tree)

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

    forbidden = [
        name
        for name in names
        if (
            "/_exports/" in name
            or "/_variants/" in name
            or (
                name.startswith("pdf_tool/share/")
                and name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif"))
            )
        )
    ]

    print(f"wheel: {wheel.name} ({len(names)} files)")
    if missing:
        print("FAIL: wheel missing required public assets:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    if forbidden:
        print("FAIL: wheel contains generated/private-style artifacts:", file=sys.stderr)
        for item in forbidden:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("PASS - wheel includes public source assets and no generated image/PDF artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
