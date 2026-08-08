"""Design Hub recipe gallery — browse layouts/ + themes/presets/.

Read-only. Structure (layouts) and public audition palettes (themes/presets)
already exist as registries; this surfaces them in the Hub for humans and
agents without parsing JSON by hand. Not a second renderer.
"""

from __future__ import annotations

import json
from pathlib import Path

_SWATCH_KEYS = ("--bg", "--primary", "--secondary", "--accent", "--support")


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


def _resume_layouts(root: Path) -> list[dict]:
    """Document page models live at layouts/*.json (not layouts/resume/).

    Collage recipes stay under layouts/collage/; only top-level JSON here.
    """
    layouts_dir = root / "layouts"
    if not layouts_dir.is_dir():
        return []
    out = []
    for path in sorted(layouts_dir.glob("*.json")):
        data = _read_json(path)
        if not isinstance(data, dict):
            continue
        page = data.get("page") if isinstance(data.get("page"), dict) else {}
        box = data.get("contentBox") if isinstance(data.get("contentBox"), dict) else {}
        rid = data.get("id") or path.stem
        out.append(
            {
                "id": rid,
                "kind": "document",
                "docType": data.get("docType") or "resume",
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
                # Older nested shape (rare in presets)
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
    resume = _resume_layouts(root)
    palettes = _palette_presets(root)
    return {
        "ok": True,
        "collageRecipes": collage,
        "resumeLayouts": resume,
        "palettePresets": palettes,
        "counts": {
            "collage": len(collage),
            "resume": len(resume),
            "palettes": len(palettes),
        },
        "cli": {
            "listRecipes": "python -m pdf_tool.collage --list-recipes",
            "renderRecipe": "python -m pdf_tool.collage <imagesDir> --recipe <id> --png",
            "screenshots": "add --fit contain (or use a recipe that already sets it)",
        },
        "hubHint": (
            "Palette 'Try in Hub' uses /?palette=<id>&mode=dark|light on the library. "
            "Collage recipes stay CLI (--recipe); this page is discovery, not a second engine."
        ),
    }
