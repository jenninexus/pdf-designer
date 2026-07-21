"""Resolve the tree that owns public ``themes/`` + ``layouts/``.

Editable checkouts keep those directories at the **repo root**. A wheel bundles a
copy under ``pdf_tool/share/`` (see ``scripts/sync-wheel-share.py`` and
``docs/PACKAGING.md``). Callers must not hard-code ``Path(__file__).parents[2]``.

Checkout wins over ``share/`` so a local ``sync-wheel-share`` run cannot shadow
live edits to repo-root ``themes/`` / ``layouts/`` / ``storage/``.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_MARKER = Path("themes") / "default-resume.json"
_PKG_DIR = Path(__file__).resolve().parent
_SHARE_DIR = _PKG_DIR / "share"


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
