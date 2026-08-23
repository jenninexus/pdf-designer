#!/usr/bin/env python3
"""One-shot: restore resumes/ + collages/ source, send generated files to output/.

Safe to re-run: skips moves when the destination already exists.
Does not touch storage/. Leaves a retired _exports/README.md pointer.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from pdf_tool.paths import collage_project_user, repo_root

GENERATED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg"}
# WebP in resources/ is source art. Root-level collage PNG/PDF is generated.
KEEP_COLLAGE_DIRS = {"images", "_raw", "_candidates", "_picker", "faves"}


def _move(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  skip exists: {dest}")
        return
    print(f"  {src} -> {dest}")
    shutil.move(str(src), str(dest))


def _rm_empty(path: Path) -> None:
    if path.is_dir() and not any(path.iterdir()):
        path.rmdir()
        print(f"  rmdir empty {path}")


def restore_resume_users(root: Path) -> None:
    src_root = root / "_exports" / "resumes"
    if not src_root.is_dir():
        return
    readme = src_root / "README.md"
    if readme.is_file():
        _move(readme, root / "resumes" / "README.md")
    names = sorted(p.name for p in src_root.iterdir() if p.is_dir())
    if "studio" in names:
        names.remove("studio")
        names.insert(0, "studio")
    for name in names:
        src = src_root / name
        dest = root / "resumes" / name
        _move(src, dest)

    for user_dir in sorted((root / "resumes").iterdir()):
        if not user_dir.is_dir():
            continue
        name = user_dir.name
        nested = user_dir / "_exports"
        if nested.is_dir():
            for job in sorted(nested.iterdir()):
                if not job.is_dir():
                    continue
                out = root / "output" / name / "resumes" / job.name
                leftover = user_dir / job.name
                for item in sorted(job.iterdir()):
                    if item.is_file() and item.suffix.lower() in GENERATED_SUFFIXES:
                        _move(item, out / item.name)
                    else:
                        _move(item, leftover / item.name)
                _rm_empty(job)
            _rm_empty(nested)

        for pdf in sorted(user_dir.rglob("*")):
            if not pdf.is_file() or pdf.suffix.lower() not in GENERATED_SUFFIXES:
                continue
            if "resources" in pdf.parts:
                continue
            rel = pdf.relative_to(user_dir)
            if rel.parts[0] == "defaults" or len(rel.parts) == 1:
                _move(pdf, root / "output" / name / "resumes" / pdf.name)


def restore_collages(root: Path) -> None:
    src_root = root / "_exports" / "collages"
    if not src_root.is_dir():
        return
    readme = src_root / "README.md"
    if readme.is_file():
        _move(readme, root / "collages" / "README.md")
    for src in sorted(src_root.iterdir()):
        if not src.is_dir():
            continue
        dest = root / "collages" / src.name
        _move(src, dest)
        user = collage_project_user(src.name)
        out = (
            root / "output" / user / "collages" / src.name
            if user
            else root / "output" / "collages" / src.name
        )
        for item in sorted(dest.iterdir()):
            if item.is_file() and item.suffix.lower() in GENERATED_SUFFIXES:
                _move(item, out / item.name)


def write_retired_pointer(root: Path) -> None:
    leftover = root / "_exports"
    leftover.mkdir(exist_ok=True)
    for empty in (leftover / "resumes", leftover / "collages"):
        _rm_empty(empty)
    pointer = leftover / "README.md"
    pointer.write_text(
        "# `_exports/` is retired (2026-08-22)\n\n"
        "Generated PDFs and PNGs now live at repo-root "
        "`output/<user>/<kind>/` (or `output/<kind>/` / `output/` when "
        "there is no profile). Source HTML stays in `resumes/` and "
        "`collages/`.\n\n"
        "The engine default (no `--output-dir`) is `pdf_tool.paths.default_output_dir`.\n",
        encoding="utf-8",
    )
    print(f"  wrote {pointer}")


def main() -> None:
    root = repo_root()
    print(f"root: {root}")
    (root / "resumes").mkdir(exist_ok=True)
    (root / "collages").mkdir(exist_ok=True)
    (root / "output").mkdir(exist_ok=True)
    restore_resume_users(root)
    restore_collages(root)
    write_retired_pointer(root)
    print("done")


if __name__ == "__main__":
    main()
