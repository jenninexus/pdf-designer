"""Design Hub workspace discovery stays aligned with the dual-path resolver."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_tool.paths import workspace_rel_info
from pdf_tool.preview import (
    APP_HTML,
    _hyphen_token_in_rel,
    available_profile_ids,
    classify_document,
    load_palettes,
    profile_options,
    pdf_preview_info,
    render_pdf_preview_page,
    resolve_preview_file,
    scan_documents,
    workspace_profile_ids,
)


def test_workspace_profiles_drive_document_tags_and_header_options(tmp_path: Path):
    users = tmp_path / "storage" / "users"
    users.mkdir(parents=True)
    (users / "alex.json").write_text(json.dumps({"id": "alex"}), encoding="utf-8")
    applications = tmp_path / "storage" / "_job-listings" / "Example"
    applications.mkdir(parents=True)
    (applications / "alex-role-resume.html").write_text("<p>Alex</p>", encoding="utf-8")

    assert workspace_profile_ids(tmp_path) == ["alex"]
    docs = scan_documents(tmp_path)
    assert docs[0]["profile"] == "alex"
    assert available_profile_ids(tmp_path, docs) == ["alex"]
    assert profile_options(["alex"]) == '<option value="alex">alex</option>'


def test_custom_preview_root_contributes_its_private_brand_palette(tmp_path: Path):
    brand_dir = tmp_path / "brands"
    brand_dir.mkdir()
    (brand_dir / "alex.json").write_text(
        json.dumps({"tokens": {"dark": {"--primary": "#123456"}}}), encoding="utf-8"
    )

    palettes = load_palettes(tmp_path)
    assert ("alex", "dark") in {(palette["id"], palette["mode"]) for palette in palettes}


def test_hyphen_token_matches_meet_jenni_bot_not_jennifer():
    assert _hyphen_token_in_rel(
        "storage/collages/meet-jenni-bot/images/_candidates/uniform-grid.html",
        "uniform-grid",
        "jenni",
    )
    assert _hyphen_token_in_rel("storage/jenni/defaults/jenni-default-resume.html", "jenni-default-resume", "jenni")
    assert not _hyphen_token_in_rel("examples/jennifer-letter.html", "jennifer-letter", "jenni")


def test_collage_project_token_tags_workspace_profile(tmp_path: Path):
    users = tmp_path / "storage" / "users"
    users.mkdir(parents=True)
    (users / "jenni.json").write_text(json.dumps({"id": "jenni"}), encoding="utf-8")
    collage = tmp_path / "storage" / "collages" / "meet-jenni-bot" / "_candidates"
    collage.mkdir(parents=True)
    (collage / "uniform-grid.html").write_text("<p>grid</p>", encoding="utf-8")
    resume = tmp_path / "storage" / "jenni" / "defaults"
    resume.mkdir(parents=True)
    (resume / "jenni-default-resume.html").write_text("<p>resume</p>", encoding="utf-8")

    docs = {doc["path"].replace("\\", "/"): doc for doc in scan_documents(tmp_path)}
    assert docs["storage/jenni/defaults/jenni-default-resume.html"]["profile"] == "jenni"
    assert docs["storage/collages/meet-jenni-bot/_candidates/uniform-grid.html"]["profile"] == "jenni"


def test_classify_fallback_tokens_without_workspace_card():
    tagged = classify_document(
        "storage/collages/meet-jenni-bot/_candidates/uniform-grid.html",
        "uniform-grid",
        (),
    )
    assert tagged["profile"] == "jenni"
    assert tagged["root"] == "storage"


def test_profile_card_without_html_still_appears_in_header(tmp_path: Path):
    profiles = tmp_path / "storage" / "profiles"
    profiles.mkdir(parents=True)
    (profiles / "studio-resume.json").write_text(json.dumps({"id": "studio-resume"}), encoding="utf-8")
    assert workspace_profile_ids(tmp_path) == ["studio"]
    assert available_profile_ids(tmp_path, []) == ["studio"]


def test_hub_js_restores_profile_before_folder_rebuild():
    assert "function applyProfileChange()" in APP_HTML
    assert 'personFilter").addEventListener("change", applyProfileChange)' in APP_HTML
    assert "docsForProfile(activeProfile())" in APP_HTML
    assert 'id="hubHomeLink"' in APP_HTML
    assert 'const cur = sel ? sel.value : "";' in APP_HTML
    boot = APP_HTML.split("if (!openFromQuery())", 1)[0]
    assert boot.rfind("restoreHubPrefs") < boot.rfind("buildFolderSelect();")


def test_stagebar_badges_filter_kind_profile_and_root():
    assert 'function stageFilterButton(label, type, value, className, pressed)' in APP_HTML
    assert 'button.className = "badge stage-filter"' in APP_HTML
    assert 'function applyStageFilter(type, value)' in APP_HTML
    assert 'setFolderFilterValue(value);' in APP_HTML
    assert 'new Set(pool.flatMap(d => [d.root, d.group]).filter(Boolean))' in APP_HTML
    assert 'if (folder === "_exports") return "Exports";' in APP_HTML
    assert 'folderDisplayName(root)' in APP_HTML
    assert 'const label = folderDisplayName(v);' in APP_HTML
    assert 'placeholder="_exports/<profile>/<kind> (default)"' in APP_HTML


def test_hub_offcanvas_controls_are_in_the_header_and_close_from_the_backdrop():
    """The drawer has header actions; both overlays also close from their backdrop."""
    css = (Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static" / "hub.css").read_text(
        encoding="utf-8"
    )
    assert 'if (backdrop) backdrop.addEventListener("click", closeDrawer);' in APP_HTML
    assert 'searchOvl.addEventListener("pointerdown", (e) => {' in APP_HTML
    assert 'if (!searchCard?.contains(e.target)) closeSearchOvl();' in APP_HTML
    assert '<kbd>Esc</kbd> or click outside closes' in APP_HTML
    assert ".hub-bar-scroll > .hub-group:not(.hub-brand-group):not(.spacer)" in css
    assert 'class="hub-drawer-head-actions"' in APP_HTML
    assert APP_HTML.index('id="drawerRefresh"') < APP_HTML.index('id="drawerClose"')
    assert '<div class="hub-drawer-foot"><kbd>Esc</kbd> closes</div>' not in APP_HTML
    assert ".hub-drawer-head-actions {" in css
    assert "grid-template-columns: repeat(auto-fit, minmax(116px, 1fr))" in css
    assert ".hub-drawer .hub-select-menu {" in css
    assert "position: static;" in css
    assert 'folders.add("_exports")' in APP_HTML
    assert "selected.exportable === false" in APP_HTML
    assert 'class="frame artifact-frame"' in APP_HTML
    assert 'id="compareFocusBtn"' in APP_HTML
    assert 'id="compareResetBtn"' in APP_HTML
    assert "compareExcluded" in APP_HTML
    assert '"/pdf-viewer?doc="' in APP_HTML


def test_recipes_and_vault_share_the_mobile_drawer_contract():
    root = Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static"
    for name in ("recipes.html", "vault.html"):
        html = (root / name).read_text(encoding="utf-8")
        assert 'id="drawerToggle"' in html
        assert 'id="hubDrawerBackdrop"' in html
        assert 'id="drawerClose"' in html
        assert 'id="drawerRefresh"' in html
        assert 'src="/_hub/hub-chrome.js"' in html
    chrome = (root / "hub-chrome.js").read_text(encoding="utf-8")
    select_script = (root / "hub-select.js").read_text(encoding="utf-8")
    css = (root / "hub.css").read_text(encoding="utf-8")
    assert 'btn.id = "hubToTop"' in chrome
    assert "hub-page" in chrome
    assert ".hub-to-top" in css
    assert "window.hubCloseContainedSelects?.();" in chrome
    assert "MutationObserver" not in select_script
    assert 'src="/_hub/hub-chrome.js"' not in APP_HTML


def test_drawer_resize_and_compact_mobile_controls_are_shared_across_hub_routes():
    root = Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static"
    css = (root / "hub.css").read_text(encoding="utf-8")
    resize_script = (root / "drawer-resize.js").read_text(encoding="utf-8")
    assert 'id="drawerResize"' in APP_HTML
    assert 'id="libraryResize"' in APP_HTML
    assert 'src="/_hub/drawer-resize.js"' in APP_HTML
    assert "pdf-designer.hub.drawerWidth" in resize_script
    assert "pdf-designer.hub.libraryWidth" in resize_script
    assert "hideWhenPhoneSheet" in resize_script
    assert "min(92vw" in css
    assert "aspect-ratio: 1 / 1" in css
    assert "--hub-drawer-min: 280px" in css
    assert "--hub-library-w: 300px" in css
    assert "grid-template-columns: repeat(auto-fit, minmax(116px, 1fr))" in css
    assert "@media (max-width: 575.98px)" in css
    assert "@media (max-width: 1399.98px)" in css
    assert "pointerdown" in resize_script
    assert "localStorage.setItem(opts.key" in resize_script or "localStorage.setItem(key" in resize_script
    for name in ("recipes.html", "vault.html"):
        html = (root / name).read_text(encoding="utf-8")
        assert 'id="drawerResize"' in html
        assert 'src="/_hub/drawer-resize.js"' in html
        assert html.index('id="drawerRefresh"') < html.index('id="drawerClose"')
        assert '<div class="hub-drawer-actions" hidden aria-hidden="true">' in html


def test_hub_icons_are_local_font_awesome_assets_with_attribution():
    root = Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static"
    css = (root / "hub.css").read_text(encoding="utf-8")
    assert "Font Awesome Free 6.7.2" in css
    assert (root / "FONT-AWESOME-LICENSE.txt").is_file()
    for icon in (
        "xmark", "arrows-rotate", "magnifying-glass",
        "download", "ellipsis", "chevron-down", "chevron-up", "star",
        "patreon", "paypal",
    ):
        assert (root / f"fa-{icon}.svg").is_file()
        assert f".fa-{icon}" in css

    for html in (APP_HTML, *((root / name).read_text(encoding="utf-8") for name in ("recipes.html", "vault.html", "wizard.html"))):
        assert 'class="hub-icon hub-menu-icon"' in html
        assert 'viewBox="0 0 512 512"' in html
        assert 'class="hub-fa-icon fa-patreon"' in html
        assert 'class="hub-fa-icon fa-paypal"' in html
        assert ">Wizard</a>" in html


def test_public_example_rel_tags_examples_profile():
    tagged = classify_document(
        "examples/profiles/default-resume/default-resume.html",
        "default-resume",
        (),
    )
    assert tagged["profile"] == "examples"
    assert tagged["kind"] == "resume"
    assert tagged["bucket"] == "examples"
    assert tagged["root"] == "examples"
    work = classify_document(
        "profiles/default-work-examples/default-work-examples.html",
        "default-work-examples",
        (),
    )
    assert work["profile"] == "examples"
    assert work["kind"] == "work-samples"


def test_examples_profile_sorts_first(tmp_path: Path):
    users = tmp_path / "users"
    users.mkdir()
    (users / "alex.json").write_text(json.dumps({"id": "alex"}), encoding="utf-8")
    (users / "examples.json").write_text(json.dumps({"id": "examples"}), encoding="utf-8")
    assert workspace_profile_ids(tmp_path) == ["examples", "alex"]


def test_scan_skips_archive_and_template_html(tmp_path: Path):
    (tmp_path / "resumes" / "alex" / "defaults").mkdir(parents=True)
    (tmp_path / "resumes" / "alex" / "defaults" / "alex-resume.html").write_text("<p>ok</p>", encoding="utf-8")
    (tmp_path / "resumes" / "alex" / "defaults" / "alex-resume.template.html").write_text("<p>tmpl</p>", encoding="utf-8")
    archived = tmp_path / "_archive" / "old"
    archived.mkdir(parents=True)
    (archived / "ghost-resume.html").write_text("<p>ghost</p>", encoding="utf-8")
    nested = tmp_path / "storage" / "_archive" / "dupes"
    nested.mkdir(parents=True)
    (nested / "ghost-cover.html").write_text("<p>ghost</p>", encoding="utf-8")

    docs = {doc["path"].replace("\\", "/") for doc in scan_documents(tmp_path)}
    assert docs == {"resumes/alex/defaults/alex-resume.html"}


def test_scan_skips_generated_desktop_and_package_mirrors(tmp_path: Path):
    canonical = tmp_path / "examples" / "profiles" / "default-resume"
    canonical.mkdir(parents=True)
    (canonical / "default-resume.html").write_text("<p>source</p>", encoding="utf-8")

    generated_paths = (
        tmp_path / "desktop" / "runtime" / "pdf-designer-runtime" / "_internal" / "pdf_tool" / "share",
        tmp_path / "desktop" / "workspace-seed",
        tmp_path / "src" / "pdf_tool" / "share",
    )
    for generated in generated_paths:
        mirror = generated / "examples" / "profiles" / "default-resume"
        mirror.mkdir(parents=True)
        (mirror / "default-resume.html").write_text("<p>generated</p>", encoding="utf-8")

    docs = {doc["path"].replace("\\", "/") for doc in scan_documents(tmp_path)}
    assert docs == {"examples/profiles/default-resume/default-resume.html"}


def test_scan_includes_private_exports_as_read_only_preview_artifacts(tmp_path: Path):
    exports = tmp_path / "_exports" / "alex" / "resumes" / "Example-Role"
    exports.mkdir(parents=True)
    (exports / "alex-example-resume-light.pdf").write_bytes(b"%PDF-1.4\n")
    (exports / "alex-example-cover-letter-dark.png").write_bytes(b"png")
    archived = exports / "_archive"
    archived.mkdir()
    (archived / "old-resume.pdf").write_bytes(b"%PDF-1.4\n")

    docs = {doc["path"].replace("\\", "/"): doc for doc in scan_documents(tmp_path)}
    resume = docs["_exports/alex/resumes/Example-Role/alex-example-resume-light.pdf"]
    cover = docs["_exports/alex/resumes/Example-Role/alex-example-cover-letter-dark.png"]
    assert resume["kind"] == "resume"
    assert cover["kind"] == "cover-letter"
    assert resume["profile"] == cover["profile"] == "alex"
    assert resume["bucket"] == cover["bucket"] == "exports"
    assert resume["artifact"] is True and resume["exportable"] is False
    assert resume["format"] == "pdf"
    assert not any("_archive" in path for path in docs)


def test_dark_pdf_viewer_renders_the_real_pdf_pages(tmp_path: Path):
    from pypdf import PdfWriter

    source = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)
    with source.open("wb") as stream:
        writer.write(stream)

    info = pdf_preview_info(source)
    assert info["pageCount"] == 2
    assert info["pages"][0]["widthPt"] == 612
    png = render_pdf_preview_page(source, 0, scale=1)
    assert png.startswith(b"\x89PNG\r\n\x1a\n")


def test_pdf_viewer_assets_use_dark_canvas_and_matching_scrollbar():
    root = Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static"
    html = (root / "pdf-viewer.html").read_text(encoding="utf-8")
    css = (root / "pdf-viewer.css").read_text(encoding="utf-8")
    js = (root / "pdf-viewer.js").read_text(encoding="utf-8")
    assert 'id="pdfCanvas"' in html
    assert "--viewer-bg: #12151c" in css
    assert "--viewer-scroll-thumb: rgba(66, 244, 200, 0.55)" in css
    assert "/api/pdf-info?doc=" in js
    assert "/api/pdf-page?doc=" in js


def test_export_workspace_info_tags_profile_without_exposing_payload():
    info = workspace_rel_info("_exports/shade/resumes/Example/shade-resume-light.pdf")
    assert info.bucket == "exports"
    assert info.profile == "shade"


def test_resolve_preview_file_follows_storage_alias(tmp_path: Path):
    live = tmp_path / "resumes" / "alex" / "defaults"
    live.mkdir(parents=True)
    (live / "alex-resume.html").write_text("<p>live</p>", encoding="utf-8")
    got = resolve_preview_file(tmp_path, "storage/alex/defaults/alex-resume.html")
    assert got == (live / "alex-resume.html").resolve()
    assert resolve_preview_file(tmp_path, "missing.html") is None


def test_public_examples_cover_each_hub_kind():
    root = Path(__file__).resolve().parents[1]
    docs = scan_documents(root / "examples")
    by_kind: dict[str, list[str]] = {}
    for doc in docs:
        by_kind.setdefault(doc["kind"], []).append(doc["path"].replace("\\", "/"))
    assert any("default-resume" in path for path in by_kind.get("resume", []))
    assert any("cover-letter" in path for path in by_kind.get("cover-letter", []))
    assert any("letter" in path.lower() for path in by_kind.get("letter", []))
    assert any("work-example" in path for path in by_kind.get("work-samples", []))
    assert any("collage" in path for path in by_kind.get("collage", []))
    assert any(path.endswith("_candidates/index.html") for path in by_kind.get("gallery", []))
    assert all(doc.get("profile") == "examples" for doc in docs)
