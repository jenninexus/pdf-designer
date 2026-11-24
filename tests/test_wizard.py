"""Verify the first-run wizard against the actual loopback Hub."""

from __future__ import annotations

import json
import threading
from html import escape
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

import pytest
from pypdf import PdfReader

from tests.test_seed_from_resume import RESUME
from pdf_tool.preview import APP_HTML, load_palettes, make_handler, scan_documents


def test_wizard_is_a_design_hub_route_and_navigation_target():
    root = Path(__file__).resolve().parents[1]
    handler = make_handler(root, scan_documents(root), load_palettes(root))
    assert 'href="/wizard"' in APP_HTML
    assert ">Wizard</a>" in APP_HTML
    assert 'class="hub-fa-icon fa-patreon"' in APP_HTML
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/wizard") as response:
            assert response.status == 200
            html = response.read().decode("utf-8")
            assert "Start wizard" in html
            assert ">Wizard</a>" in html
            assert 'class="hub-fa-icon fa-patreon"' in html
            assert 'class="hub-fa-icon fa-paypal"' in html
        with urlopen(f"http://127.0.0.1:{server.server_port}/api/voice-card") as response:
            payload = json.loads(response.read())
            assert payload["ok"] is True
            assert payload["card"]["displayName"] == "Jane Example"
        req = Request(
            f"http://127.0.0.1:{server.server_port}/api/import-resume",
            data=json.dumps({"files": [{"name": "alex-resume.txt", "text": RESUME}]}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req) as response:
            imported = json.loads(response.read())
            assert imported["ok"] is True
            assert imported["draft"]["displayName"] == "Alex Rivera"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
    for page in ("vault.html", "recipes.html", "wizard.html"):
        html = (root / "src" / "pdf_tool" / "static" / page).read_text(encoding="utf-8")
        assert 'href="/wizard"' in html
        assert ">Wizard</a>" in html


def test_compact_wizard_imports_reviews_styles_and_exports(tmp_path):
    playwright = pytest.importorskip("playwright.sync_api")
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(tmp_path, [], load_palettes(tmp_path)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    try:
        with playwright.sync_playwright() as runtime:
            browser = runtime.chromium.launch()
            source = browser.new_page()
            source.set_content(f'<meta charset="utf-8"><pre>{escape(RESUME)}</pre>')
            original_pdf = source.pdf()
            source.close()
            page = browser.new_page(viewport={"width": 320, "height": 568}, has_touch=True, reduced_motion="reduce")
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(f"{origin}/wizard?no-splash")
            page.get_by_role("button", name="Read résumé").click()
            assert "Choose a résumé" in page.locator("#importStatus").inner_text()
            page.locator("#starterFiles").set_input_files({
                "name": "alex-resume.pdf", "mimeType": "application/pdf", "buffer": original_pdf
            })
            page.get_by_role("button", name="Read résumé").click()
            playwright.expect(page.locator("#wizard-review")).to_be_focused()
            assert page.get_by_label("Name", exact=True).input_value() == "Alex Rivera"
            assert page.get_by_label("Dates").input_value() == "2022 – Present"
            assert page.get_by_label("Education").input_value() == "B.A. Design, Example University"
            assert not (tmp_path / "vaults/alex-rivera.json").exists()
            page.get_by_label("Skills").fill("HTML\nPython")
            for width in (320, 390, 576, 992):
                page.set_viewport_size({"width": width, "height": 568})
                assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
            page.set_viewport_size({"width": 320, "height": 568})
            page.get_by_role("button", name="Choose a style").click()
            page.locator("#starterLayout").select_option("skills-first")
            page.locator("#starterPalette").select_option("slate-ink")
            page.get_by_role("button", name="Review and save").click()
            save = page.get_by_role("button", name="Save résumé and vault")
            assert save.is_disabled()
            page.get_by_role("checkbox").check()
            save.click()
            page.get_by_role("link", name="Open my résumé").click()
            preview = page.frame_locator("#main")
            playwright.expect(preview.get_by_role("heading", name="Alex Rivera", level=1)).to_be_visible()
            assert preview.locator(".page").first.get_by_text("Skills", exact=True).is_visible()
            assert not preview.locator(".page").first.get_by_text("Work experience", exact=True).count()
            assert not errors
            profile = json.loads((tmp_path / "profiles/alex-rivera-resume.json").read_text(encoding="utf-8"))
            assert profile["theme"]["preset"] == "slate-ink"
            assert profile["layout"]["variant"] == "skills-first"
            vault = json.loads((tmp_path / "vaults/alex-rivera.json").read_text(encoding="utf-8"))
            assert [skill["claim"] for skill in vault["skills"]["imported"]] == ["HTML", "Python"]
            assert all(skill["confidence"] == "inferred" for skill in vault["skills"]["imported"])
            for theme in ("light", "dark"):
                response = page.request.post(f"{origin}/api/export", data={
                    "doc": "resumes/alex-rivera/alex-rivera-resume.html", "format": f"pdf-{theme}"
                })
                result = response.json()
                assert result["ok"], result
                pdf = PdfReader(result["outputs"][0])
                assert len(pdf.pages) == 2
                assert float(pdf.pages[0].mediabox.width) == 612
                assert float(pdf.pages[0].mediabox.height) == 792
                assert "Python" in pdf.pages[0].extract_text()
                assert "Example Studio" in pdf.pages[1].extract_text()
            browser.close()
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
