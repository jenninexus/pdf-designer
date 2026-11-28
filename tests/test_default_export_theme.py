from pathlib import Path

import pytest
from PIL import ImageChops
from pypdf import PdfReader
from pypdfium2 import PdfDocument

from pdf_tool.html_to_pdf import export_html_to_pdf
from pdf_tool.pdf_to_png import render_to_png


class _FakeSheet:
    def screenshot(self, *, path: str) -> None:
        Path(path).write_bytes(b"png")


class _FakePage:
    def __init__(self) -> None:
        self.evaluations: list[tuple[str, object | None]] = []

    def goto(self, *_args, **_kwargs) -> None:
        return None

    def evaluate(self, expression: str, arg: object | None = None):
        self.evaluations.append((expression, arg))
        return 0

    def emulate_media(self, **_kwargs) -> None:
        return None

    def pdf(self, *, path: str, **_kwargs) -> None:
        Path(path).write_bytes(b"pdf")

    def query_selector_all(self, _selector: str) -> list[_FakeSheet]:
        return [_FakeSheet()]


class _FakeBrowser:
    def __init__(self, page: _FakePage) -> None:
        self.page = page

    def new_page(self, **_kwargs) -> _FakePage:
        return self.page

    def close(self) -> None:
        return None


class _FakeChromium:
    def __init__(self, page: _FakePage) -> None:
        self.page = page

    def launch(self, **_kwargs) -> _FakeBrowser:
        return _FakeBrowser(self.page)


class _FakePlaywright:
    def __init__(self, page: _FakePage) -> None:
        self.chromium = _FakeChromium(page)


class _FakePlaywrightContext:
    def __init__(self, page: _FakePage) -> None:
        self.playwright = _FakePlaywright(page)

    def __enter__(self) -> _FakePlaywright:
        return self.playwright

    def __exit__(self, *_args) -> None:
        return None


@pytest.fixture
def fake_page(monkeypatch: pytest.MonkeyPatch) -> _FakePage:
    page = _FakePage()
    monkeypatch.setattr(
        "playwright.sync_api.sync_playwright",
        lambda: _FakePlaywrightContext(page),
    )
    return page


def _source_with_dark_root(tmp_path: Path) -> Path:
    source = tmp_path / "letter.html"
    source.write_text('<html data-pdf-theme="dark"><div class="page">Hi</div></html>')
    return source


def test_default_pdf_export_forces_light_theme(
    tmp_path: Path, fake_page: _FakePage
) -> None:
    source = _source_with_dark_root(tmp_path)

    output = export_html_to_pdf(str(source), output_dir=str(tmp_path))

    assert output.name == "letter-light.pdf"
    assert fake_page.evaluations[0][1] == "light"


def test_explicit_dark_pdf_export_forces_dark_theme(
    tmp_path: Path, fake_page: _FakePage
) -> None:
    source = _source_with_dark_root(tmp_path)

    output = export_html_to_pdf(
        str(source), output_dir=str(tmp_path), pdf_theme="dark"
    )

    assert output.name == "letter-dark.pdf"
    assert fake_page.evaluations[0][1] == "dark"


def test_grayscale_pdf_keeps_searchable_text_and_neutral_art(tmp_path: Path) -> None:
    source = tmp_path / "color.html"
    source.write_text(
        '<p style="color:red;background:yellow">Searchable print text</p>'
        '<svg width="100" height="80"><rect width="100" height="80" fill="blue"/></svg>',
        encoding="utf-8",
    )
    output = export_html_to_pdf(str(source), output_dir=str(tmp_path), pdf_theme="grayscale")
    assert output.name == "color-grayscale.pdf"
    assert "Searchable print text" in PdfReader(output).pages[0].extract_text()
    with PdfDocument(str(output)) as pdf:
        page = pdf[0]
        bitmap = page.render()
        red, green, blue = bitmap.to_pil().convert("RGB").split()
        assert ImageChops.difference(red, green).getbbox() is None
        assert ImageChops.difference(green, blue).getbbox() is None


def test_default_png_render_forces_light_theme(
    tmp_path: Path, fake_page: _FakePage
) -> None:
    source = _source_with_dark_root(tmp_path)

    outputs = render_to_png(str(source), output_dir=str(tmp_path / "png"))

    assert len(outputs) == 1
    assert fake_page.evaluations[0][1] == "light"
