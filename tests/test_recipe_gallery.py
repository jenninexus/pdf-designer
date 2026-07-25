"""recipe_gallery — Hub surface over layouts/ + themes/presets/."""

from __future__ import annotations

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
    slate = next(p for p in data["palettePresets"] if p["id"] == "slate-ink")
    assert slate["modes"]["dark"]["hubUrl"] == "/?palette=slate-ink&mode=dark"
    assert slate["modes"]["dark"]["swatches"].get("--primary")
