"""Resolve public assets and the private workspace tree.

Editable checkouts keep ``themes/`` + ``layouts/`` at the **repo root**. A wheel
bundles a copy under ``pdf_tool/share/`` (see ``scripts/sync-wheel-share.py``
and ``docs/PACKAGING.md``). Callers must not hard-code ``Path(__file__).parents[2]``.

Checkout wins over ``share/`` so a local ``sync-wheel-share`` run cannot shadow
live edits to repo-root ``themes/`` / ``layouts/``.

Workspace nouns (``users/`` · ``vaults/`` · ``_job-apps/`` · …) are the product
layout — see ``docs/WORKSPACE-LAYOUT.md``. Live data uses the root nouns;
``storage/`` is retained only as ignored legacy residue. Every helper here
accepts **both** trees: an existing new-noun file wins; otherwise the
``storage/`` alias. Job folders: ``_job-apps/`` (canonical) ·
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
            "Pass a real directory (for example resumes/jenni or resumes/jenni/<App>)."
        )


OUTPUT_KIND_RESUMES = "resumes"
OUTPUT_KIND_COLLAGES = "collages"
OUTPUT_KIND_EXAMPLES = "examples"

# Collage *projects* are not users. Map known local sets so Jenni's renders
# land under output/jenni/collages/ instead of a kind-only root folder.
COLLAGE_PROJECT_USERS = {
    "meet-jenni-bot": "jenni",
    "agency-patreon-desks": "jenni",
    "syn-themes": "jenni",
    "martian-collage": "studio",
    "martian-discord": "studio",
}


def output_root(*, root: Path | None = None) -> Path:
    """Repo-root ``output/`` — disposable automation/test scratch only."""
    return _root(root) / "output"


def export_root(*, root: Path | None = None) -> Path:
    """Repo-root ``_exports/`` — fallback library for examples and unfiled exports.

    Personal documents export beside their family instead: ``resumes/<user>/`` and
    ``collages/<project>/`` (see :func:`default_output_dir`).
    """
    return _root(root) / "_exports"


def _strip_output_prefixes(parts: tuple[str, ...]) -> tuple[str, ...]:
    if parts and parts[0] in {"output", "_exports"}:
        return parts[1:]
    return parts


def collage_project_user(project: str) -> str | None:
    if project in COLLAGE_PROJECT_USERS:
        return COLLAGE_PROJECT_USERS[project]
    low = project.lower()
    if "jenni" in low:
        return "jenni"
    if "shade" in low or "synagen" in low:
        return "shade"
    if "martian" in low:
        return "studio"
    return None


def infer_output_user_kind(
    source: Path | str,
    *,
    kind: str | None = None,
    root: Path | None = None,
) -> tuple[str | None, str | None]:
    """Return ``(user_or_none, kind_or_none)`` for a source file or folder."""
    root_path = _root(root).resolve()
    source_path = Path(source).resolve()
    try:
        parts = source_path.relative_to(root_path).parts
    except ValueError:
        return None, kind

    parts = _strip_output_prefixes(parts)
    if not parts:
        return None, kind

    first = parts[0]
    if first == "resumes" and len(parts) >= 2:
        return parts[1], kind or OUTPUT_KIND_RESUMES
    if first == "collages" and len(parts) >= 2:
        return collage_project_user(parts[1]), kind or OUTPUT_KIND_COLLAGES
    if first == "examples":
        return None, kind or OUTPUT_KIND_EXAMPLES
    if first == "storage" and len(parts) >= 2:
        second = parts[1]
        if second == "collages" and len(parts) >= 3:
            return collage_project_user(parts[2]), kind or OUTPUT_KIND_COLLAGES
        if second not in _RESERVED_STORAGE:
            return second, kind or OUTPUT_KIND_RESUMES
    # Already-migrated output/jenni/resumes/...
    if len(parts) >= 2 and parts[1] in {
        OUTPUT_KIND_RESUMES,
        OUTPUT_KIND_COLLAGES,
        OUTPUT_KIND_EXAMPLES,
    }:
        return parts[0], kind or parts[1]
    if first in {OUTPUT_KIND_RESUMES, OUTPUT_KIND_COLLAGES, OUTPUT_KIND_EXAMPLES}:
        nested = parts[1] if len(parts) >= 2 else None
        if first == OUTPUT_KIND_COLLAGES and nested:
            return collage_project_user(nested), kind or first
        return nested, kind or first
    return None, kind


_RESERVED_USER_DIRS = {
    "defaults",
    "resources",
    "templates",
    "_archive",
    "_submitted",
    "_exports",
}


def output_job_leaf(source: Path | str, *, root: Path | None = None) -> str | None:
    """Per-job folder name (Netflix-App, CZI, …) when the source is not a go-to pack."""
    root_path = _root(root).resolve()
    source_path = Path(source).resolve()
    try:
        parts = list(source_path.relative_to(root_path).parts)
    except ValueError:
        return None
    parts = list(_strip_output_prefixes(tuple(parts)))
    if "_exports" in parts:
        idx = parts.index("_exports")
        if idx + 1 < len(parts) and parts[idx + 1] not in _RESERVED_USER_DIRS:
            return parts[idx + 1]
    # resumes/<user>/<App>/doc.html  (len>=4) — not a file sitting in the user folder
    if parts[:1] == ["resumes"] and len(parts) >= 4 and parts[2] not in _RESERVED_USER_DIRS:
        return parts[2]
    if len(parts) >= 4 and parts[1] == OUTPUT_KIND_RESUMES and parts[2] not in _RESERVED_USER_DIRS:
        return parts[2]
    return None


def _workspace_user_ids(root: Path) -> set[str]:
    """Person ids known to this workspace: ``users/<id>.json`` plus ``resumes/<id>/`` folders."""
    ids: set[str] = set()
    users = root / "users"
    if users.is_dir():
        ids.update(p.stem for p in users.glob("*.json") if _is_workspace_json(p) and p.stem != "examples")
    resumes = root / "resumes"
    if resumes.is_dir():
        ids.update(d.name for d in resumes.iterdir() if d.is_dir() and not d.name.startswith(("_", ".")))
    return ids


def _job_app_user_and_leaf(source: Path, root: Path) -> tuple[str | None, str | None]:
    """``_job-apps/<App>/<user>-….html`` → ``(user, App)``; the user is the filename prefix."""
    try:
        parts = source.resolve().relative_to(root.resolve()).parts
    except ValueError:
        return None, None
    rel = "/".join(parts)
    for prefix in _JOB_APP_PREFIXES:
        if not rel.startswith(prefix + "/"):
            continue
        rest = rel[len(prefix) + 1 :].split("/")
        if len(rest) < 2:
            return None, None
        app, name = rest[0], rest[-1].lower()
        users = sorted(_workspace_user_ids(root), key=len, reverse=True)
        user = next((u for u in users if name.startswith(u.lower() + "-")), None)
        return user, app
    return None, None


def default_output_dir(
    source: Path | str,
    *,
    kind: str | None = None,
    root: Path | None = None,
    leaf: str | None = None,
) -> Path:
    """Where a deliberate export goes when the caller omits ``--output-dir``.

    Exports live WITH their document family (owner directive 2026-09-27):

    * ``resumes/<user>/…`` and ``_job-apps/<App>/<user>-….html`` → ``resumes/<user>/``
      (plus the job folder, e.g. ``resumes/<user>/<App>/``);
    * ``collages/<project>/…`` → ``collages/<project>/`` (beside ``images/`` and
      ``_candidates/``);
    * anything else — public ``examples/`` or an unrecognised source — falls back to
      ``_exports/<kind>/`` or ``_exports/unfiled/`` so a fresh clone still works.

    Optional ``leaf`` nests one more folder (a job name, or ``<stem>-png``).
    ``output/`` stays reserved for callers that explicitly choose disposable scratch.
    """
    root_path = _root(root)
    source_path = Path(source)
    job_user, job_app = _job_app_user_and_leaf(source_path, root_path)
    if job_user:
        dest = root_path / "resumes" / job_user
        job = leaf if leaf is not None else job_app
        return dest / job if job else dest
    try:
        parts = source_path.resolve().relative_to(root_path.resolve()).parts
    except ValueError:
        parts = ()
    parts = _strip_output_prefixes(parts)
    if len(parts) >= 2 and parts[0] == "collages":
        dest = root_path / "collages" / parts[1]
        return dest / leaf if leaf else dest
    user, inferred_kind = infer_output_user_kind(source, kind=kind, root=root)
    if parts[:1] == ("resumes",) and len(parts) >= 2:
        dest = root_path / "resumes" / parts[1]
    elif inferred_kind:
        dest = export_root(root=root) / inferred_kind
    else:
        dest = export_root(root=root) / "unfiled"
    job = leaf if leaf is not None else output_job_leaf(source, root=root)
    if job:
        dest = dest / job
    return dest


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
    if low.startswith("_exports/") and len(parts) >= 2:
        return RelInfo(bucket="exports", profile=parts[1])
    if low.startswith("resumes/") and len(parts) >= 2:
        return RelInfo(bucket="vault-renders", profile=parts[1])
    if low.startswith("storage/") and len(parts) >= 2 and parts[1] not in _RESERVED_STORAGE:
        return RelInfo(bucket="vault-renders", profile=parts[1])
    return RelInfo()
