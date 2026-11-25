"""recipe_gallery — Hub surface over layouts/ + themes/presets/."""

from __future__ import annotations

import json

from pdf_tool.paths import repo_root
from pdf_tool.recipe_gallery import build_recipe_gallery


def test_recipe_gallery_lists_public_registries():
    data = build_recipe_gallery(repo_root())
    assert data["ok"] is True
    assert data["counts"]["collage"] >= 1
    assert data["counts"]["resume"] >= 1
    assert data["counts"]["palettes"] >= 1

    collage_ids = {r["id"] for r in data["collageRecipes"]}
    assert "scatter-showcase-16x9" in collage_ids
    scatter = next(r for r in data["collageRecipes"] if r["id"] == "scatter-showcase-16x9")
    assert scatter["family"] == "frame-scatter"
    assert "--recipe scatter-showcase-16x9" in scatter["cli"]

    resume_ids = {r["id"] for r in data["resumeLayouts"]}
    assert "two-page-standard" in resume_ids

    palette_ids = {p["id"] for p in data["palettePresets"]}
    assert "slate-ink" in palette_ids
    assert {"aesyna", "aesyna-harmony"} <= palette_ids
    for palette_id in ("aesyna", "aesyna-harmony"):
        preset = next(p for p in data["palettePresets"] if p["id"] == palette_id)
        for mode in ("dark", "light"):
            assert preset["modes"][mode]["hubUrl"] == f"/?palette={palette_id}&mode={mode}"
            assert preset["modes"][mode]["swatches"].get("--accent")
    slate = next(p for p in data["palettePresets"] if p["id"] == "slate-ink")
    assert slate["modes"]["dark"]["hubUrl"] == "/?palette=slate-ink&mode=dark"
    assert slate["modes"]["dark"]["swatches"].get("--primary")


def test_gallery_uses_the_public_packet_recipe_when_local_copy_exists(tmp_path):
    layouts = tmp_path / "layouts"
    layouts.mkdir()
    for filename in ("application-packet.json", "application-packet.example.json"):
        (layouts / filename).write_text(json.dumps({"id": "application-packet"}), encoding="utf-8")

    recipes = build_recipe_gallery(tmp_path)["resumeLayouts"]

    assert [recipe["path"] for recipe in recipes] == ["layouts/application-packet.example.json"]
