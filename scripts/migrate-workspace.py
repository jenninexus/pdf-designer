"""Copy live ``storage/`` payloads into root nouns. Keep ``storage/`` as the alias.

Does **not** delete ``storage/``. Dual-run until Hub + tracker + vault smoke is green
on the new tree, then a human can drop the alias.

Usage (from repo root):

    python scripts/migrate-workspace.py           # copy missing files
    python scripts/migrate-workspace.py --dry-run # print the plan
    python scripts/migrate-workspace.py --force   # overwrite dest files that already exist

Junctions under ``storage/{jenni,shade}/resources/images/martiangames`` are recreated
under ``resumes/`` pointing at ``resumes/studio/resources/images/martiangames`` — never
copied as real trees.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORAGE = ROOT / "storage"
SKIP_NAMES = frozenset({"README.md", ".gitkeep"})
PERSON_FOLDERS = ("studio", "jenni", "shade")  # studio first — junction target
RESERVED = frozenset(
    {
        "users",
        "profiles",
        "brand-design",
        "collages",
        "_job-listings",
        "docs",
        "brands",
    }
)


def _is_junction(path: Path) -> bool:
    """True for Windows directory junctions and POSIX/Windows symlinks.

    ``Path.is_junction()`` is 3.12+; ``is_symlink()`` is False for junctions on
    3.10, which would follow them and duplicate the MG gallery.
    """
    try:
        st = os.lstat(path)
    except OSError:
        return False
    # FILE_ATTRIBUTE_REPARSE_POINT
    if getattr(st, "st_file_attributes", 0) & 0x400:
        return True
    return path.is_symlink()


def _junction_target(path: Path) -> Path:
    raw = os.readlink(path)
    target = Path(raw)
    if not target.is_absolute():
        target = (path.parent / target).resolve()
    return target


def _ensure_junction(link: Path, target: Path, *, dry_run: bool) -> str:
    """Create a Windows directory junction (or POSIX symlink)."""
    if link.exists() or link.is_symlink() or _is_junction(link):
        try:
            if _is_junction(link) or link.is_symlink():
                existing = _junction_target(link)
                if existing.resolve() == target.resolve():
                    return f"keep junction {link.relative_to(ROOT)} -> {target.relative_to(ROOT)}"
        except OSError:
            pass
        return f"skip existing {link.relative_to(ROOT)}"
    if dry_run:
        return f"junction {link.relative_to(ROOT)} -> {target.relative_to(ROOT)}"
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        import subprocess

        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            check=True,
            capture_output=True,
            text=True,
        )
    else:
        link.symlink_to(target, target_is_directory=True)
    return f"junction {link.relative_to(ROOT)} -> {target.relative_to(ROOT)}"


def _copy_file(src: Path, dst: Path, *, dry_run: bool, force: bool) -> str:
    rel = dst.relative_to(ROOT)
    if dst.exists() and not force:
        return f"skip {rel}"
    if dry_run:
        return f"copy {src.relative_to(ROOT)} -> {rel}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"copy {rel}"


def _copy_tree(src: Path, dst: Path, *, dry_run: bool, force: bool, notes: list[str]) -> None:
    if not src.is_dir():
        return
    for child in sorted(src.iterdir()):
        if child.name in SKIP_NAMES or child.name.endswith(".example.json"):
            continue
        dest_child = dst / child.name
        if _is_junction(child) or child.is_symlink():
            # Remap later; skip follow-copy.
            notes.append(f"defer junction {child.relative_to(ROOT)}")
            continue
        if child.is_dir():
            _copy_tree(child, dest_child, dry_run=dry_run, force=force, notes=notes)
        elif child.is_file():
            notes.append(_copy_file(child, dest_child, dry_run=dry_run, force=force))


def migrate(*, dry_run: bool, force: bool) -> int:
    if not STORAGE.is_dir():
        print("No storage/ directory — nothing to copy.", file=sys.stderr)
        return 1

    notes: list[str] = []

    users_src = STORAGE / "users"
    if users_src.is_dir():
        for path in sorted(users_src.glob("*.json")):
            if path.name.endswith(".example.json"):
                continue
            notes.append(_copy_file(path, ROOT / "users" / path.name, dry_run=dry_run, force=force))

    profiles_src = STORAGE / "profiles"
    if profiles_src.is_dir():
        for path in sorted(profiles_src.glob("*.json")):
            if path.name.endswith(".example.json"):
                continue
            notes.append(
                _copy_file(path, ROOT / "profiles" / path.name, dry_run=dry_run, force=force)
            )

    for path in sorted(STORAGE.glob("*/resume-source.json")):
        user = path.parent.name
        if user in RESERVED:
            continue
        notes.append(_copy_file(path, ROOT / "vaults" / f"{user}.json", dry_run=dry_run, force=force))

    _copy_tree(
        STORAGE / "_job-listings",
        ROOT / "_job-apps",
        dry_run=dry_run,
        force=force,
        notes=notes,
    )
    _copy_tree(
        STORAGE / "collages",
        ROOT / "collages",
        dry_run=dry_run,
        force=force,
        notes=notes,
    )
    _copy_tree(
        STORAGE / "brand-design",
        ROOT / "brands",
        dry_run=dry_run,
        force=force,
        notes=notes,
    )

    for person in PERSON_FOLDERS:
        src = STORAGE / person
        if not src.is_dir():
            continue
        _copy_tree(src, ROOT / "resumes" / person, dry_run=dry_run, force=force, notes=notes)

    studio_gallery = ROOT / "resumes" / "studio" / "resources" / "images" / "martiangames"
    for person in ("jenni", "shade"):
        link = ROOT / "resumes" / person / "resources" / "images" / "martiangames"
        if studio_gallery.exists() or dry_run:
            notes.append(_ensure_junction(link, studio_gallery, dry_run=dry_run))

    copied = sum(1 for n in notes if n.startswith("copy "))
    skipped = sum(1 for n in notes if n.startswith("skip "))
    junctions = [n for n in notes if n.startswith("junction ") or n.startswith("keep junction") or n.startswith("defer junction")]
    print(f"{'[dry-run] ' if dry_run else ''}copy={copied} skip={skipped} junctions={len(junctions)}")
    for line in junctions:
        print(f"  {line}")
    print("storage/ left in place as the dual-run alias. Do not delete it yet.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    return migrate(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
