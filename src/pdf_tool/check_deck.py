"""Acceptance for 16:9 presentations; Letter career-document gates remain separate.

Checks palette, real print DOM fit in both themes, PDF page geometry/order and
extractable slide titles. Usage: python -m pdf_tool.check_deck deck.html
"""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from playwright.sync_api import sync_playwright
from pypdf import PdfReader

from .check_palette import check_file
from .html_to_pdf import chromium_launch_kwargs


def check_deck(path: Path) -> list[str]:
    path = path.resolve()
    problems = [f"palette: {hit}" for hit in check_file(path)]
    with tempfile.TemporaryDirectory(prefix="pdf-deck-qa-") as scratch, sync_playwright() as pw:
        browser = pw.chromium.launch(**chromium_launch_kwargs())
        try:
            for theme in ("light", "dark"):
                page = browser.new_page(viewport={"width": 1184, "height": 624})
                try:
                    page.goto(path.as_uri(), wait_until="networkidle")
                    page.evaluate("theme => { document.documentElement.dataset.pdfTheme = theme; }", theme)
                    page.emulate_media(media="print", color_scheme=theme)
                    page.evaluate("document.fonts.ready")
                    margins = page.evaluate("""() => {
                      const rules = [];
                      function visit(list) { for (const rule of list) {
                        if (rule.type === CSSRule.PAGE_RULE) rules.push(rule);
                        else if (rule.cssRules && (!rule.conditionText || matchMedia(rule.conditionText).matches)) visit(rule.cssRules);
                      } }
                      for (const sheet of document.styleSheets) visit(sheet.cssRules);
                      const rule = rules.filter(r => !r.selectorText).at(-1);
                      if (!rule || rules.some(r => r.selectorText)) return [];
                      const probe = document.createElement('div');
                      for (const edge of ['Top','Right','Bottom','Left']) probe.style['margin' + edge] = rule.style['margin' + edge];
                      document.body.append(probe);
                      const computed = getComputedStyle(probe);
                      const values = ['Top','Right','Bottom','Left'].map(edge => parseFloat(computed['margin' + edge]));
                      probe.remove();
                      return values;
                    }""")
                    if len(margins) != 4 or any(value is None or abs(value - 48) > .1 for value in margins):
                        problems.append(f"{theme}: presentation requires equal 0.5-inch page margins")
                    metrics = page.evaluate("""() => [...document.querySelectorAll('.slide')].map((slide, i) => {
                      const box = slide.getBoundingClientRect();
                      const overflow = box.width > 1185 || box.height > 625 || [...slide.querySelectorAll('*')].some(el => {
                        const r = el.getBoundingClientRect();
                        return r.left < box.left - 1 || r.right > box.right + 1 ||
                          r.top < box.top - 1 || r.bottom > box.bottom + 1 ||
                          el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1;
                      });
                      return {index:i+1, title:slide.querySelector('h1,h2')?.textContent?.trim(), overflow};
                    })""")
                    if not metrics:
                        problems.append(f"{theme}: no presentation slides")
                        continue
                    for item in metrics:
                        if item["overflow"]:
                            problems.append(f"{theme}: slide {item['index']} exceeds its printable content box")
                        if not item["title"]:
                            problems.append(f"{theme}: slide {item['index']} has no title")
                    output = Path(scratch) / f"deck-{theme}.pdf"
                    page.pdf(path=str(output), print_background=True, prefer_css_page_size=True)
                    pdf = PdfReader(output)
                    if len(pdf.pages) != len(metrics):
                        problems.append(f"{theme}: {len(pdf.pages)} PDF pages for {len(metrics)} source slides")
                    for index, pdf_page in enumerate(pdf.pages):
                        if abs(float(pdf_page.mediabox.width) - 960) > 1 or abs(float(pdf_page.mediabox.height) - 540) > 1:
                            problems.append(f"{theme}: PDF page {index+1} is not 16:9 (960 x 540pt)")
                        if index < len(metrics):
                            expected = " ".join((metrics[index]["title"] or "").split())
                            text = " ".join((pdf_page.extract_text() or "").split())
                            if expected and expected not in text:
                                problems.append(f"{theme}: title missing or reordered on PDF page {index+1}")
                finally:
                    page.close()
        finally:
            browser.close()
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args(argv)
    if not args.html.is_file():
        parser.error("presentation source does not exist")
    problems = check_deck(args.html)
    for problem in problems:
        print(f"FAIL: {problem}")
    print("FAIL" if problems else "PASS: both themes, print fit, 16:9 PDF pages and slide text/order")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
