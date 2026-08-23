"""The first-resume wizard is a local Jane Example walkthrough, not a new renderer."""

from __future__ import annotations

import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

from pdf_tool.preview import APP_HTML, load_palettes, make_handler, scan_documents


def test_wizard_has_four_local_steps_and_uses_jane_example_export_path():
    root = Path(__file__).resolve().parents[1]
    wizard = (root / "src" / "pdf_tool" / "static" / "wizard.html").read_text(encoding="utf-8")
    for label in ("1 · Vault", "2 · Skills", "3 · Palette", "4 · Export"):
        assert label in wizard
    assert 'data-theme="dark"' in wizard
    assert '<meta name="color-scheme" content="dark">' in wizard
    assert 'class="hub-page wizard-page"' in wizard
    assert "Build the honest version first." in wizard
    assert "Hub is the default workspace" in wizard
    assert "Jane Example" in wizard
    assert "check_vault vaults/&lt;you&gt;.json" in wizard
    assert "check_generation examples/profiles/default-resume/default-resume.html" in wizard
    assert "--pdf-theme dark" in wizard
    assert "/api/export" not in wizard
    assert "creates no account" in wizard
    assert "second renderer" not in wizard.lower()
    assert "/api/voice-card" in wizard
    assert "saves nothing" in wizard
    assert "aria-current" in wizard
    assert "kind: \"tool\"" in wizard
    assert "résumé-file upload is not available" in wizard


def test_wizard_is_a_design_hub_route_and_navigation_target():
    root = Path(__file__).resolve().parents[1]
    handler = make_handler(root, scan_documents(root), load_palettes(root))
    assert 'href="/wizard"' in APP_HTML
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/wizard") as response:
            assert response.status == 200
            assert "Start a local résumé" in response.read().decode("utf-8")
        with urlopen(f"http://127.0.0.1:{server.server_port}/api/voice-card") as response:
            payload = __import__("json").loads(response.read())
            assert payload["ok"] is True
            assert payload["card"]["displayName"] == "Jane Example"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
    for page in ("vault.html", "recipes.html"):
        html = (root / "src" / "pdf_tool" / "static" / page).read_text(encoding="utf-8")
        assert 'href="/wizard"' in html
