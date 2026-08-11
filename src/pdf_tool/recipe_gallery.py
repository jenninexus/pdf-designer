"""Design Hub recipe gallery — browse layouts/ + themes/presets/.

Read-only. Structure (layouts) and public audition palettes (themes/presets)
already exist as registries; this surfaces them in the Hub for humans and
agents without parsing JSON by hand. Not a second renderer.
"""

from __future__ import annotations

import json
from pathlib import Path

_SWATCH_KEYS = ("--bg", "--primary", "--secondary", "--accent", "--support")

# Document layout categories (structure recipes). Collage stays separate.
_DOC_LAYOUT_DIRS = ("cover-letter", "letter", "resume", "work-examples")


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def _swatches(token_map: dict | None) -> dict:
    if not isinstance(token_map, dict):
        return {}
    out = {}
    for key in _SWATCH_KEYS:
        val = token_map.get(key)
        if isinstance(val, str) and val.startswith("#"):
            out[key] = val
    return out


def _collage_recipes(root: Path) -> list[dict]:
    layouts_dir = root / "layouts" / "collage"
    if not layouts_dir.is_dir():
        return []
    out = []
    for path in sorted(layouts_dir.glob("*.json")):
        data = _read_json(path)
        if not isinstance(data, dict):
            continue
        rid = data.get("id") or path.stem
        out.append(
            {
                "id": rid,
                "kind": "collage",
                "family": data.get("family"),
                "canvas": data.get("canvas"),
                "px": data.get("px"),
                "fit": data.get("fit"),
                "background": data.get("background"),
                "bestFor": data.get("bestFor") or "",
                "notes": data.get("notes") or "",
                "path": _rel(root, path),
                "cli": f"python -m pdf_tool.collage <imagesDir> --recipe {rid} --png",
            }
        )
    return out


def _document_layouts(root: Path) -> list[dict]:
    """Document page models under layouts/<category>/*.json (+ legacy top-level).

    Categories: cover-letter · letter · resume · work-examples.
    Collage recipes stay under layouts/collage/ (see _collage_recipes).
    """
    layouts_root = root / "layouts"
    if not layouts_root.is_dir():
        return []
    paths: list[Path] = []
    for cat in _DOC_LAYOUT_DIRS:
        cat_dir = layouts_root / cat
        if cat_dir.is_dir():
            paths.extend(sorted(cat_dir.glob("*.json")))
    # Legacy flat layouts/*.json (pre-category) — keep discoverable if any remain
    paths.extend(sorted(layouts_root.glob("*.json")))

    seen: set[str] = set()
    out = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        data = _read_json(path)
        if not isinstance(data, dict):
            continue
        page = data.get("page") if isinstance(data.get("page"), dict) else {}
        box = data.get("contentBox") if isinstance(data.get("contentBox"), dict) else {}
        rid = data.get("id") or path.stem
        category = path.parent.name if path.parent != layouts_root else "document"
        out.append(
            {
                "id": rid,
                "kind": "document",
                "category": category,
                "docType": data.get("docType") or category,
                "bestFor": data.get("bestFor") or "",
                "pageSize": page.get("size"),
                "margin": page.get("margin"),
                "contentHeightIn": box.get("heightIn"),
                "expectedPages": data.get("expectedPages"),
                "guards": data.get("guards") or [],
                "spec": data.get("spec"),
                "path": _rel(root, path),
            }
        )
    return out


# Back-compat alias for callers that still say "resume layouts"
_resume_layouts = _document_layouts


def _palette_presets(root: Path) -> list[dict]:
    presets_dir = root / "themes" / "presets"
    if not presets_dir.is_dir():
        return []
    out = []
    for path in sorted(presets_dir.glob("*.json")):
        data = _read_json(path)
        if not isinstance(data, dict):
            continue
        meta = data.get("_meta") if isinstance(data.get("_meta"), dict) else {}
        tokens = data.get("tokens") if isinstance(data.get("tokens"), dict) else {}
        pid = meta.get("id") or path.stem
        modes = {}
        for mode in ("dark", "light"):
            block = tokens.get(mode) if isinstance(tokens.get(mode), dict) else None
            if not block:
                nested = data.get(mode)
                block = nested if isinstance(nested, dict) else None
            modes[mode] = {
                "swatches": _swatches(block),
                "hubUrl": f"/?palette={pid}&mode={mode}",
            }
        out.append(
            {
                "id": pid,
                "name": meta.get("name") or pid,
                "description": meta.get("description") or "",
                "aesthetic": meta.get("aesthetic") or "",
                "path": _rel(root, path),
                "modes": modes,
            }
        )
    return out


def build_recipe_gallery(root: Path) -> dict:
    """Return a JSON-serializable gallery of public layouts + palette presets."""
    collage = _collage_recipes(root)
    documents = _document_layouts(root)
    palettes = _palette_presets(root)
    return {
        "ok": True,
        "collageRecipes": collage,
        "resumeLayouts": documents,  # legacy key — all document page models
        "documentLayouts": documents,
        "palettePresets": palettes,
        "counts": {
            "collage": len(collage),
            "resume": len(documents),
            "document": len(documents),
            "palettes": len(palettes),
        },
        "cli": {
            "listRecipes": "python -m pdf_tool.collage --list-recipes",
            "renderRecipe": "python -m pdf_tool.collage <imagesDir> --recipe <id> --png",
            "screenshots": "add --fit contain (or use a recipe that already sets it)",
        },
        "hubHint": (
            "Palette 'Try in Hub' uses /?palette=<id>&mode=dark|light on the library. "
            "Document recipes live under layouts/{cover-letter,letter,resume,work-examples}/. "
            "Collage recipes stay CLI (--recipe); this page is discovery, not a second engine."
        ),
    }
