"""Tests for the collage layout registry (layouts/collage/) and grid fitting."""

import json

import pytest

from pdf_tool import collage as collage_mod
from pdf_tool.collage import (
    BACKGROUNDS,
    _LAYOUTS_DIR,
    _grid_cols,
    archive_recipe,
    list_recipes,
    load_recipe,
    promote_recipe,
    resolve_background,
    resolve_frame,
    shelve_renders,
    variant_stem,
)

_MODE = {"bg": "#0b0d12", "border": "rgba(79,209,201,0.14)"}


# ---------------------------------------------------------------- recipes

def test_every_shipped_recipe_is_valid():
    """Each tracked recipe parses and declares the fields the CLI relies on."""
    paths = sorted(_LAYOUTS_DIR.glob("*.json"))
    assert paths, "no layout recipes found — layouts/collage/ should ship some"
    for path in paths:
        rec = json.loads(path.read_text(encoding="utf-8"))
        assert rec["id"] == path.stem, f"{path.name}: id must match filename stem"
        assert rec["family"], f"{path.name}: needs a family"
        assert rec["canvas"], f"{path.name}: needs a canvas"
        if "fit" in rec:
            assert rec["fit"] in ("cover", "contain")
        if "background" in rec:
            # Raw CSS is allowed, but a bare word must be a real preset.
            bg = rec["background"]
            if " " not in bg and not bg.startswith("#"):
                assert bg in BACKGROUNDS, f"{path.name}: unknown background {bg!r}"


def test_screenshot_recipes_never_crop():
    """A recipe aimed at screenshots must use contain — cover cuts off content."""
    for path in _LAYOUTS_DIR.glob("*.json"):
        rec = json.loads(path.read_text(encoding="utf-8"))
        blurb = f"{rec.get('bestFor', '')} {rec.get('notes', '')}".lower()
        if "screenshot" in blurb:
            assert rec.get("fit") == "contain", f"{path.name}: screenshot recipe must set fit=contain"


def test_list_recipes_reports_shipped_files():
    ids = {row[0] for row in list_recipes()}
    assert "screenshot-grid-16x9" in ids


def test_unknown_recipe_raises_with_guidance():
    with pytest.raises(SystemExit) as exc:
        load_recipe("definitely-not-a-recipe")
    assert "Available:" in str(exc.value)


# ---------------------------------------------------------------- backgrounds

def test_named_background_resolves_to_css():
    assert resolve_background("discord-slate", _MODE).startswith("linear-gradient")


def test_raw_css_background_passes_through():
    raw = "linear-gradient(90deg,#000,#fff)"
    assert resolve_background(raw, _MODE) == raw


def test_no_background_falls_back_to_mode():
    assert resolve_background(None, _MODE) == _MODE["bg"]


def test_frame_never_defaults_to_white():
    """The polaroid frame must come from the palette, not a hardcoded #fff."""
    assert resolve_frame("discord-slate", _MODE).lower() != "#ffffff"
    # An unknown/raw background still gets a palette-consistent frame.
    assert resolve_frame(None, _MODE) == _MODE["border"]


# ---------------------------------------------------------------- grid fit

@pytest.mark.parametrize("n", [1, 2, 3, 4, 6, 8, 9])
def test_grid_leaves_no_empty_cells_when_divisible(n):
    """4 images on 16:9 must be 2x2, not 3x2 with two dead cells."""
    canvas = {"px_w": 1920, "px_h": 1080}
    cols = _grid_cols(n, canvas)
    rows = -(-n // cols)
    assert cols * rows == n, f"n={n}: {cols}x{rows} leaves {cols * rows - n} empty"


# ---------------------------------------------------------------- filenames

def test_variant_stem_keeps_output_flat_and_distinct():
    canvas = {"id": "hd-landscape", "px_w": 1920, "px_h": 1080}
    slate = variant_stem(canvas, {"background": "discord-slate", "fit": "contain"})
    ember = variant_stem(canvas, {"background": "martian-ember", "fit": "contain"})
    assert slate != ember, "different backgrounds must not overwrite each other"
    assert "/" not in slate and "\\" not in slate, "stem must not introduce a subfolder"


def test_variant_stem_hashes_raw_css_to_a_safe_name():
    canvas = {"id": "square", "px_w": 1024, "px_h": 1024}
    stem = variant_stem(canvas, {"background": "linear-gradient(90deg,#000,#fff)"})
    for ch in '<>:"/\\|?*(),#':
        assert ch not in stem, f"raw CSS leaked {ch!r} into the filename"


# ---------------------------------------------------------------- promote / archive

@pytest.fixture
def temp_registry(tmp_path, monkeypatch):
    """Point the recipe registry at a temp dir so tests never touch layouts/."""
    reg = tmp_path / "collage"
    reg.mkdir()
    monkeypatch.setattr(collage_mod, "_LAYOUTS_DIR", reg)
    monkeypatch.setattr(collage_mod, "_ARCHIVE_DIR", reg / "_archive")
    return reg


_CANVAS = {"id": "hd-landscape", "px_w": 1920, "px_h": 1080, "preset_px": [1920, 1080]}


def test_promote_writes_a_loadable_recipe(temp_registry):
    promote_recipe("my-layout", _CANVAS, {"fit": "contain", "background": "discord-slate"},
                   "frame-scatter", best_for="Testing.")
    saved = json.loads((temp_registry / "my-layout.json").read_text(encoding="utf-8"))
    assert saved["id"] == "my-layout"
    assert saved["family"] == "frame-scatter"
    assert saved["fit"] == "contain"
    assert saved["bestFor"] == "Testing."


def test_promote_omits_px_when_it_is_just_the_preset_default(temp_registry):
    promote_recipe("preset-size", _CANVAS, {}, "uniform-grid")
    saved = json.loads((temp_registry / "preset-size.json").read_text(encoding="utf-8"))
    assert "px" not in saved, "a default canvas size should not be pinned into the recipe"


def test_promote_records_an_explicit_size_override(temp_registry):
    canvas = {"id": "hd-landscape", "px_w": 1280, "px_h": 720, "preset_px": [1920, 1080]}
    promote_recipe("smaller", canvas, {}, "uniform-grid")
    saved = json.loads((temp_registry / "smaller.json").read_text(encoding="utf-8"))
    assert saved["px"] == "1280x720"


def test_promote_refuses_auto_layout(temp_registry):
    with pytest.raises(SystemExit, match="ONE layout"):
        promote_recipe("nope", _CANVAS, {}, "auto")


def test_promote_refuses_to_clobber_an_existing_recipe(temp_registry):
    promote_recipe("taken", _CANVAS, {}, "masonry")
    with pytest.raises(SystemExit, match="already exists"):
        promote_recipe("taken", _CANVAS, {}, "filmstrip")


def test_archive_hides_the_recipe_but_keeps_the_file(temp_registry):
    promote_recipe("retire-me", _CANVAS, {}, "masonry")
    dest = archive_recipe("retire-me")
    assert dest.exists(), "archiving must never delete the file"
    assert not (temp_registry / "retire-me.json").exists()
    assert "retire-me" not in {row[0] for row in list_recipes()}


def test_archive_unknown_recipe_is_an_error(temp_registry):
    with pytest.raises(SystemExit, match="No active recipe"):
        archive_recipe("was-never-here")


def test_shelve_prefixes_by_project_into_one_flat_dir(tmp_path):
    out = tmp_path / "_candidates"
    out.mkdir()
    (out / "uniform-grid__hd-landscape-1920x1080.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (out / "hero-mosaic__hd-landscape-1920x1080.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    shelf = tmp_path / "layouts"

    copied = shelve_renders(out, "my-project", shelf)

    assert len(copied) == 2
    assert all(p.name.startswith("my-project__") for p in copied)
    assert not [p for p in shelf.iterdir() if p.is_dir()], "shelf must stay flat"
