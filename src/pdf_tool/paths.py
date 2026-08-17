"""Resolve public assets and the private workspace tree.

Editable checkouts keep ``themes/`` + ``layouts/`` at the **repo root**. A wheel
bundles a copy under ``pdf_tool/share/`` (see ``scripts/sync-wheel-share.py``
and ``docs/PACKAGING.md``). Callers must not hard-code ``Path(__file__).parents[2]``.

Checkout wins over ``share/`` so a local ``sync-wheel-share`` run cannot shadow
live edits to repo-root ``themes/`` / ``layouts/``.

Workspace nouns (``users/`` · ``vaults/`` · ``_job-apps/`` · …) are the product
layout — see ``docs/WORKSPACE-LAYOUT.md``. Live data still sits under
``storage/`` until the alias is dropped. Every helper here accepts **both**
trees: an existing new-noun file wins; otherwise the ``storage/`` alias; if
neither file exists, prefer the legacy path while ``storage/`` is still present
so SEGO keeps working. Job folders: ``_job-apps/`` (canonical) ·
``applications/`` (brief 2026-08 name) · ``storage/_job-listings/`` (legacy).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_MARKER = Path("themes") / "default-resume.json"
_PKG_DIR = Path(__file__).resolve().parent
_SHARE_DIR = _PKG_DIR / "share"

# Directories under storage/ that are NOT a person's résumé working tree.
_RESERVED_STORAGE = frozenset(
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


def _is_asset_root(path: Path) -> bool:
    return (path / _MARKER).is_file() and (path / "layouts").is_dir()


@lru_cache(maxsize=1)
def repo_root() -> Path:
    """Return the directory that contains ``themes/`` and ``layouts/``.

    Search order:
    1. Walk from the package dir and cwd for a checkout-shaped tree (not ``share/``)
    2. Bundled ``pdf_tool/share/`` (installed wheel / no checkout above the package)
    3. Legacy editable fallback: ``src/pdf_tool`` → repo root (``parents[2]``)
    """
    share_resolved = _SHARE_DIR.resolve()
    for start in (_PKG_DIR, Path.cwd()):
        for candidate in (start, *start.parents):
            try:
                if candidate.resolve() == share_resolved:
                    continue
            except OSError:
                continue
            if _is_asset_root(candidate):
                return candidate

    if _is_asset_root(_SHARE_DIR):
        return _SHARE_DIR

    # Legacy editable: src/pdf_tool/paths.py → parents[2] is the checkout root
    return _PKG_DIR.parents[2]


def _root(root: Path | None) -> Path:
    return Path(root) if root is not None else repo_root()


def _posix(rel: str) -> str:
    return rel.replace("\\", "/").strip("/")


def _prefix_pair(rel: str, new_prefix: str, old_prefix: str) -> tuple[str, str] | None:
    """Map a path that is exactly ``new_prefix`` / ``old_prefix`` or a child of either."""
    if rel == new_prefix:
        return (new_prefix, old_prefix)
    if rel.startswith(new_prefix + "/"):
        rest = rel[len(new_prefix) + 1 :]
        return (rel, f"{old_prefix}/{rest}" if rest else old_prefix)
    if rel == old_prefix:
        return (new_prefix, old_prefix)
    if rel.startswith(old_prefix + "/"):
        rest = rel[len(old_prefix) + 1 :]
        return (f"{new_prefix}/{rest}" if rest else new_prefix, rel)
    return None


# Canonical job tree, then the brief 2026-08 name, then the storage alias.
_JOB_APP_PREFIXES = ("_job-apps", "applications", "storage/_job-listings")


def reject_flag_looking_path(path: str | None, *, flag: str = "--output-dir") -> None:
    """Refuse a path that is actually a leftover CLI flag (``--output-dir`` as a folder)."""
    if path and path.lstrip().startswith("-"):
        raise SystemExit(
            f"refusing {flag} path {path!r} — that looks like a CLI flag, not a folder.\n"
            "Pass a real directory (for example resumes/jenni/_exports or resumes/jenni/defaults)."
        )


def _job_app_aliases(rel: str) -> tuple[str, ...] | None:
    """Map any job-tree path onto ``(_job-apps/…, applications/…, storage/_job-listings/…)``."""
    rest: str | None = None
    for prefix in _JOB_APP_PREFIXES:
        if rel == prefix:
            rest = ""
            break
        if rel.startswith(prefix + "/"):
            rest = rel[len(prefix) + 1 :]
            break
    if rest is None:
        return None
    return tuple(f"{prefix}/{rest}" if rest else prefix for prefix in _JOB_APP_PREFIXES)


def _is_workspace_json(path: Path) -> bool:
    name = path.name
    if not name.endswith(".json") or name.startswith("_"):
        return False
    return not name.endswith(".example.json")


def _legacy_storage_present(root: Path) -> bool:
    return (root / "storage").is_dir()


def _has_payload(path: Path) -> bool:
    """True for a real file, or a directory that is more than a README scaffold."""
    if path.is_file():
        return True
    if not path.is_dir():
        return False
    try:
        for child in path.iterdir():
            name = child.name
            if name in {"README.md", ".gitkeep"} or name.endswith(".example.json"):
                continue
            return True
    except OSError:
        return False
    return False


def alias_rel_paths(rel: str) -> tuple[str, ...]:
    """Return (new-noun path, legacy storage path) when a mapping exists.

    Identity paths (``examples/…``, already-canonical with no pair) return a
    one-tuple. New-noun form is always first so callers that pick the first
    existing file prefer the product layout after migration.
    """
    rel = _posix(rel)
    if not rel:
        return (rel,)

    job_aliases = _job_app_aliases(rel)
    if job_aliases:
        return job_aliases

    for new_prefix, old_prefix in (
        ("users", "storage/users"),
        ("profiles", "storage/profiles"),
        ("collages", "storage/collages"),
        ("brands", "storage/brand-design"),
    ):
        paired = _prefix_pair(rel, new_prefix, old_prefix)
        if paired:
            return paired

    if rel == "vaults" or (rel.startswith("vaults/") and rel.endswith(".json")):
        if rel == "vaults":
            return (rel,)
        user = Path(rel).stem
        return (rel, f"storage/{user}/resume-source.json")
    if rel.startswith("resumes/"):
        return (rel, "storage/" + rel[len("resumes/") :])

    parts = rel.split("/")
    if (
        rel.startswith("storage/")
        and rel.endswith("/resume-source.json")
        and len(parts) == 3
        and parts[1] not in _RESERVED_STORAGE
    ):
        return (f"vaults/{parts[1]}.json", rel)
    if rel.startswith("storage/") and len(parts) >= 2 and parts[1] not in _RESERVED_STORAGE:
        return ("resumes/" + rel[len("storage/") :], rel)

    return (rel,)


def resolve_rel(rel: str, *, root: Path | None = None) -> Path:
    """Map a repo-relative path onto an existing file, accepting both trees.

    If neither alias exists: keep the ``storage/`` path while that directory
    is present (live SEGO tree); otherwise return the new-noun canonical path.
    """
    root = _root(root)
    aliases = alias_rel_paths(rel)
    for alias in aliases:
        candidate = root / alias
        if _has_payload(candidate):
            return candidate
    if len(aliases) > 1 and _legacy_storage_present(root):
        return root / aliases[-1]
    return root / aliases[0]


def user_path(user: str, *, root: Path | None = None) -> Path:
    return resolve_rel(f"users/{user}.json", root=root)


def vault_path(user: str, *, root: Path | None = None) -> Path:
    """``vaults/<user>.json`` or legacy ``storage/<user>/resume-source.json``."""
    return resolve_rel(f"vaults/{user}.json", root=root)


def profile_path(user: str, *, stem: str = "resume", root: Path | None = None) -> Path:
    return resolve_rel(f"profiles/{user}-{stem}.json", root=root)


def resume_dir(user: str, *, root: Path | None = None) -> Path:
    return resolve_rel(f"resumes/{user}", root=root)


def applications_dir(*, root: Path | None = None) -> Path:
    """Canonical job tree: ``_job-apps/`` (aliases: ``applications/``, ``storage/_job-listings/``)."""
    return resolve_rel("_job-apps", root=root)


job_apps_dir = applications_dir


def brands_dir(*, root: Path | None = None) -> Path:
    return resolve_rel("brands", root=root)


def collages_dir(*, root: Path | None = None) -> Path:
    return resolve_rel("collages", root=root)


def _iter_json_prefer_new(new_dir: Path, old_dir: Path, *, key=lambda p: p.stem):
    seen: set[str] = set()
    for folder in (new_dir, old_dir):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.json")):
            if not _is_workspace_json(path):
                continue
            ident = key(path)
            if ident in seen:
                continue
            seen.add(ident)
            yield path


def iter_user_paths(*, root: Path | None = None):
    root = _root(root)
    yield from _iter_json_prefer_new(root / "users", root / "storage" / "users")


def iter_profile_paths(*, root: Path | None = None):
    root = _root(root)
    yield from _iter_json_prefer_new(root / "profiles", root / "storage" / "profiles")


def iter_vault_paths(*, root: Path | None = None):
    """Yield vault JSON files, new nouns first, then unmatched legacy files."""
    root = _root(root)
    seen: set[str] = set()
    vaults = root / "vaults"
    if vaults.is_dir():
        for path in sorted(vaults.glob("*.json")):
            if not _is_workspace_json(path):
                continue
            seen.add(path.stem)
            yield path
    storage = root / "storage"
    if storage.is_dir():
        for path in sorted(storage.glob("*/resume-source.json")):
            user = path.parent.name
            if user in _RESERVED_STORAGE or user in seen:
                continue
            seen.add(user)
            yield path


def iter_application_json(*, root: Path | None = None):
    """Yield ``application.json`` files; prefer ``_job-apps/`` then aliases.

    Identity is the path *relative to that tree's root* (posix, casefolded), not the
    leaf folder name. ``_job-apps/Sony`` and ``storage/_job-listings/Sony`` are
    the same job; ``_job-apps/3d-art/Sony`` and ``storage/_job-listings/game-dev/Sony``
    are not.
    """
    root = _root(root)
    seen: set[str] = set()
    for base in (root / "_job-apps", root / "applications", root / "storage" / "_job-listings"):
        if not base.is_dir():
            continue
        for path in sorted(base.glob("**/application.json")):
            try:
                ident = path.parent.relative_to(base).as_posix().casefold()
            except ValueError:
                ident = path.parent.name.casefold()
            if ident in seen:
                continue
            seen.add(ident)
            yield path


def brand_dirs(*, root: Path | None = None) -> list[Path]:
    """Palette directories to scan (new first). Both may exist during dual-run."""
    root = _root(root)
    out: list[Path] = []
    seen: set[Path] = set()
    for folder in (root / "brands", root / "storage" / "brand-design"):
        if not folder.is_dir():
            continue
        resolved = folder.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(folder)
    return out


def has_private_workspace(*, root: Path | None = None) -> bool:
    root = _root(root)
    if next(iter_user_paths(root=root), None) is not None:
        return True
    if next(iter_vault_paths(root=root), None) is not None:
        return True
    if next(iter_profile_paths(root=root), None) is not None:
        return True
    return False


@dataclass(frozen=True)
class RelInfo:
    bucket: str | None = None
    profile: str | None = None


def workspace_rel_info(rel: str) -> RelInfo:
    """Hub classifier hints for a repo-relative document path."""
    low = _posix(rel).lower()
    parts = low.split("/")
    if (
        low.startswith("_job-apps/")
        or low.startswith("applications/")
        or low.startswith("storage/_job-listings/")
    ):
        return RelInfo(bucket="_job-listings")
    if low.startswith("collages/") or low.startswith("storage/collages/"):
        return RelInfo(bucket="collages")
    if low.startswith("resumes/") and len(parts) >= 2:
        return RelInfo(bucket="vault-renders", profile=parts[1])
    if low.startswith("storage/") and len(parts) >= 2 and parts[1] not in _RESERVED_STORAGE:
        return RelInfo(bucket="vault-renders", profile=parts[1])
    return RelInfo()
