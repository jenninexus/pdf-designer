#!/usr/bin/env python3
"""TestPyPI / local-wheel dry-run for pdf-designer.

Steps (from repo root):
  1. python scripts/check-wheel-assets.py   (gate — themes/layouts in wheel)
  2. build sdist+wheel into dist/
  3. if TESTPYPI_TOKEN or TWINE_PASSWORD is set → twine upload --repository testpypi
  4. fresh venv → pip install from TestPyPI (if uploaded) or from the local wheel
  5. prove pdf_tool.paths.repo_root() sees bundled share/ + run check_generation
     on the packaged default-resume HTML

Env (optional upload):
  TESTPYPI_TOKEN   API token from https://test.pypi.org/manage/account/token/
                   (username is always __token__)
  TWINE_PASSWORD   same token (TWINE_USERNAME defaults to __token__)
  TWINE_REPOSITORY testpypi (default when uploading)

Usage:
  python scripts/testpypi-dry-run.py              # local wheel proof (no upload)
  python scripts/testpypi-dry-run.py --upload     # require token + upload TestPyPI
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict | None = None,
    capture: bool = False,
) -> str:
    print("+", " ".join(cmd), f"(cwd={cwd or ROOT})")
    completed = subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        check=True,
        env=env,
        capture_output=capture,
        text=True,
    )
    return completed.stdout if capture else ""


def token() -> str | None:
    return os.environ.get("TESTPYPI_TOKEN") or os.environ.get("TWINE_PASSWORD")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--upload",
        action="store_true",
        help="Upload to TestPyPI (requires TESTPYPI_TOKEN / TWINE_PASSWORD)",
    )
    ap.add_argument(
        "--skip-gate",
        action="store_true",
        help="Skip check-wheel-assets.py (already ran this session)",
    )
    args = ap.parse_args()

    if not args.skip_gate:
        run([sys.executable, str(ROOT / "scripts" / "check-wheel-assets.py")])

    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    run([sys.executable, "-m", "build", "--outdir", str(dist)])
    wheels = sorted(dist.glob("*.whl"))
    if not wheels:
        print("FAIL: no wheel in dist/", file=sys.stderr)
        return 1
    wheel = wheels[-1]
    print(f"built: {wheel.name}")

    uploaded = False
    if args.upload:
        tok = token()
        if not tok:
            print(
                "FAIL: --upload needs TESTPYPI_TOKEN (or TWINE_PASSWORD).\n"
                "  Create at https://test.pypi.org/manage/account/token/\n"
                "  Store in sys-admin userdata.db (category=API Keys, service=TestPyPI)\n"
                "  or export TESTPYPI_TOKEN for this shell.",
                file=sys.stderr,
            )
            return 2
        run([sys.executable, "-m", "pip", "install", "-q", "twine"])
        env = os.environ.copy()
        env["TWINE_USERNAME"] = env.get("TWINE_USERNAME") or "__token__"
        env["TWINE_PASSWORD"] = tok
        run(
            [
                sys.executable,
                "-m",
                "twine",
                "upload",
                "--repository",
                "testpypi",
                "--non-interactive",
                str(wheel),
            ],
            env=env,
        )
        uploaded = True

    with tempfile.TemporaryDirectory(prefix="pdf-designer-venv-") as tmp:
        vdir = Path(tmp) / "venv"
        venv.create(vdir, with_pip=True)
        py = vdir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"])
        if uploaded:
            # TestPyPI often lacks mirrored deps — allow PyPI for playwright/pypdf/Pillow
            run(
                [
                    str(py),
                    "-m",
                    "pip",
                    "install",
                    "-q",
                    "--index-url",
                    "https://test.pypi.org/simple/",
                    "--extra-index-url",
                    "https://pypi.org/simple/",
                    f"pdf-designer=={wheel.name.split('-')[1]}",
                ]
            )
            source = "TestPyPI"
        else:
            run([str(py), "-m", "pip", "install", "-q", str(wheel)])
            source = f"local wheel {wheel.name}"

        # CRITICAL: paths.repo_root() prefers a checkout over share/ when cwd (or
        # parents) looks like the repo. Prove from a directory OUTSIDE the checkout
        # so we exercise the wheel payload a stranger would get.
        outside = Path(tmp) / "outside-cwd"
        outside.mkdir()
        prove = r"""
import pdf_tool
from pdf_tool.paths import repo_root
from pathlib import Path
root = repo_root()
theme = root / "themes" / "default-resume.json"
layout = root / "layouts" / "collage"
ex = root / "examples" / "profiles" / "default-resume" / "default-resume.html"
assert theme.is_file(), theme
assert layout.is_dir(), layout
assert ex.is_file(), ex
share = Path(pdf_tool.__file__).resolve().parent / "share"
assert root == share.resolve(), (root, share)
assert "site-packages" in str(root).replace("\\", "/"), root
print("repo_root=", root)
print("theme_ok", theme)
print("example_ok", ex)
print("pdf_tool=", Path(pdf_tool.__file__).resolve())
"""
        run([str(py), "-c", prove], cwd=outside)

        # Chromium is a post-install step (never bundled in the wheel)
        run([str(py), "-m", "playwright", "install", "chromium"], cwd=outside)

        html_path = run(
            [
                str(py),
                "-c",
                "from pdf_tool.paths import repo_root; "
                "print(repo_root() / 'examples' / 'profiles' / 'default-resume' / 'default-resume.html')",
            ],
            cwd=outside,
            capture=True,
        ).strip()
        print(f"check_generation on {html_path}")
        cg = vdir / (
            "Scripts/pdf-designer-check-generation.exe"
            if os.name == "nt"
            else "bin/pdf-designer-check-generation"
        )
        if cg.exists():
            run([str(cg), html_path], cwd=outside)
        else:
            run([str(py), "-m", "pdf_tool.check_generation", html_path], cwd=outside)

    print(f"PASS - fresh-venv install proof via {source}")
    if not uploaded:
        print(
            "NOTE: upload skipped (no --upload or no token). "
            "Local wheel proof is green; TestPyPI publish still needs an account token."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as e:
        print(f"FAIL: command exited {e.returncode}", file=sys.stderr)
        raise SystemExit(e.returncode or 1)
