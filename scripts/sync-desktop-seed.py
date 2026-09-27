#!/usr/bin/env python3
"""Build the clone-safe first-run workspace bundled by the Windows installer.

The seed is generated only from Git-tracked public source files.  That makes a
local vault, résumé, brand map, or export impossible to sweep into a desktop
installer merely because it happens to exist beside the source checkout.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "desktop" / "workspace-seed"
PUBLIC_PREFIXES = ("themes/", "layouts/", "examples/")
PUBLIC_FILES = (
    "users/README.md",
    "users/examples.json",
    "vaults/README.md",
    "vaults/examples.json",
    "profiles/README.md",
    "profiles/examples.json",
    "resumes/README.md",
    "_job-apps/README.md",
    "collages/README.md",
    "brands/README.md",
)
EXCLUDED_PARTS = {"_exports", "output", "_variants", "__pycache__"}
EXCLUDED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pyc"}


def tracked_public_paths(root: Path = ROOT) -> list[Path]:
    """Return only allowed, tracked source files for the customer workspace."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", *PUBLIC_PREFIXES, *PUBLIC_FILES],
        check=True,
        capture_output=True,
    )
    paths: list[Path] = []
    for raw in result.stdout.decode("utf-8").split("\0"):
        if not raw:
            continue
        rel = Path(raw)
        if any(part in EXCLUDED_PARTS for part in rel.parts) or rel.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if raw.startswith(PUBLIC_PREFIXES) or raw in PUBLIC_FILES:
            paths.append(rel)
    return sorted(paths)


def sync(output: Path, root: Path = ROOT) -> int:
    """Replace ``output`` with the exact clone-safe workspace seed."""
    output = output.resolve()
    if output == root.resolve():
        raise ValueError("desktop seed output must not be the repository root")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copied = 0
    for rel in tracked_public_paths(root):
        src = root / rel
        if not src.is_file():
            raise FileNotFoundError(src)
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
    required = output / "themes" / "default-resume.json"
    if not required.is_file():
        raise RuntimeError("desktop seed is missing themes/default-resume.json")
    print(f"PASS - desktop workspace seed: {copied} public files -> {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    return sync(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
