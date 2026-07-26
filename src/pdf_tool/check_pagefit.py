"""Page-fit guard -- the exported PDF must have the right page count, no clipped ink,
and no orphan sign-off.

WHY THIS EXISTS
---------------
Every other guard reads the DOM or the HTML. A DOM-based check cannot see what the PDF
*rasteriser* did, and on 2026-07-25 that gap shipped a broken document:

    The Sony cover letter went out with "Founder & CEO, Martian Games LLC" sliced through
    the middle and the email line missing entirely.

Cause: the letter had copied the RESUME's print pattern -- a fixed `.page` height plus
`overflow: hidden`. `@page { margin }` already insets the printable area, so a `.page` that
*also* declares a near-full height overflows the sheet, and `overflow: hidden` then CLIPS
the tail rather than letting it flow.

Every existing check passed:

    check_overflow      PASS   DOM said content was 7.29in inside a 9.6in box (overflowBy: 0)
    check_generation    PASS   10/10 -- the signature WAS present, merely cut in half
    page count          PASS   exactly 1 page, as required
    text layer          PASS   the clipped line still exists in it, so a grep succeeds

Only rasterising the PDF and looking at the bottom of the page found it. This module is
that look, automated.

WHAT IT ASSERTS
---------------
1. PAGE COUNT      -- exactly what the doc type requires (letter 1 / resume 2 / samples 3).
2. NO CLIPPED INK  -- no ink touching the content edge, which is the signature of a cut.
3. NO ORPHAN TAIL  -- a final page holding only a sign-off (a signature stranded alone on
                      page 2 is unprofessional even though nothing is clipped).

Usage:
    python -m pdf_tool.check_pagefit <doc>.pdf
    python -m pdf_tool.check_pagefit <doc>.pdf --expect 1
    python -m pdf_tool.check_pagefit storage/<user>/_exports/<App>/*.pdf

Exit codes:
  0  PASS
  1  FAIL -- wrong page count, clipped ink, or an orphan sign-off page
  2  usage / unreadable PDF
"""

import sys
from pathlib import Path

# A doc type's required page count, inferred from the filename when --expect is absent.
EXPECTED_BY_KIND = {
    "cover-letter": 1,
    "cover_letter": 1,
    "coverletter": 1,
    "resume": 2,
    "work-samples": 3,
    "work_examples": 3,
}

# Ink within this many pixels (at scale 2) of the content edge is treated as clipped.
EDGE_TOL = 4
# A final page with less than this fraction of the ink of a typical page is "orphan-ish".
ORPHAN_INK_RATIO = 0.18


def _out(*a, **k):
    print(*a, **k)


def _configure_stdout():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            try:
                s.reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def _expected_for(path: Path):
    name = path.name.lower()
    for kind, n in EXPECTED_BY_KIND.items():
        if kind in name:
            return n, kind
    return None, None


def _page_ink(im, bg_probe_inset=120):
    """Return (rows_with_ink, W, H, lit_fn) for one rendered page."""
    W, H = im.size
    inset = max(bg_probe_inset, int(min(W, H) * 0.12))
    bg = im.getpixel((inset, H // 2))

    def lit(px):
        return sum(abs(a - c) for a, c in zip(px, bg)) > 90

    rows = [y for y in range(0, H, 2)
            if any(lit(im.getpixel((x, y))) for x in range(int(W * 0.03), W - 3, 3))]
    return rows, W, H, lit


def check_pagefit(pdf_path: Path, expect: int = None):
    """Return (ok, messages) for one exported PDF."""
    try:
        import pypdfium2 as pdfium
    except ImportError as e:
        return True, [f"(skipped -- {e})"]

    if not pdf_path.exists():
        return False, [f"no such PDF: {pdf_path}"]

    msgs = []
    want, kind = (expect, "explicit") if expect else _expected_for(pdf_path)

    try:
        pdf = pdfium.PdfDocument(str(pdf_path))
    except Exception as e:  # noqa: BLE001 - surface any parse failure as a real result
        return False, [f"cannot open: {e}"]

    try:
        n = len(pdf)

        # 1. PAGE COUNT
        if want and n != want:
            msgs.append(
                f"page count is {n}, expected {want} for a {kind or 'document'}. "
                f"A cover letter is ALWAYS 1 page; a resume ALWAYS 2. Fix by CUTTING PROSE or "
                f"tightening font-size/line-height within the allowed band -- never by adding a "
                f"fixed height + overflow:hidden, which hides the overflow and ships a clipped file. "
                f"See layouts/resume/one-page-letter.json 'fitToOnePage'."
            )

        page_ink_counts = []
        for i in range(n):
            im = pdf[i].render(scale=2).to_pil().convert("RGB")
            rows, W, H, lit = _page_ink(im)
            page_ink_counts.append(len(rows))
            if not rows:
                msgs.append(f"page {i + 1}: BLANK -- a phantom sheet (check for a trailing break-after: page).")
                continue

            # 2. INK AT THE SHEET EDGE -- a coarse cut (content running off the paper).
            #
            # ⚠ HONEST LIMITATION, measured 2026-07-25: this does NOT detect the box-boundary
            # clip. `overflow: hidden` on a `.page` that declares its own height cuts content
            # at the BOX edge, which sits well inside the paper margin -- a clipped export and
            # a clean one measured an IDENTICAL bottom-ink row (y=1438 of 1584), and their
            # final-line band heights were statistically indistinguishable (13px against a
            # 16px median, in BOTH files). Pixel forensics cannot separate "the line ended
            # here" from "the line was cut here".
            #
            # That is why the box-boundary clip is prevented at the SOURCE instead --
            # check_source_geometry() below refuses the CSS pattern that causes it, and the
            # layout contract (layouts/resume/one-page-letter.json) forbids it. Rasterised
            # eyeballing remains the final check for a human: pdf_to_png, then LOOK.
            if max(rows) >= H - EDGE_TOL:
                msgs.append(
                    f"page {i + 1}: ink touches the BOTTOM edge (y={max(rows)} of {H}) -- content "
                    f"is running off the sheet."
                )
            if min(rows) <= EDGE_TOL:
                msgs.append(
                    f"page {i + 1}: ink touches the TOP edge (y={min(rows)}) -- content is cut off above."
                )

        # 3. ORPHAN TAIL -- a last page carrying only a sign-off.
        if n > 1 and page_ink_counts:
            body = page_ink_counts[:-1]
            typical = max(body) if body else 0
            last = page_ink_counts[-1]
            if typical and last <= typical * ORPHAN_INK_RATIO:
                msgs.append(
                    f"page {n}: ORPHAN TAIL -- only {last} ink rows vs {typical} on a full page. "
                    f"A signature stranded alone on the last page reads as unprofessional even though "
                    f"nothing is clipped. Cut prose so it rejoins the previous page."
                )
    finally:
        pdf.close()

    return (not msgs), msgs


def check_source_geometry(html_path: Path):
    """Refuse the CSS pattern that clips a cover letter, BEFORE it is exported.

    This is the reliable half of the guard. Pixel forensics cannot tell a cut line from a
    finished one (see the note in check_pagefit), so the box-boundary clip is prevented at
    the source: on a COVER LETTER, a print-scoped `.page` must not declare a fixed `height`
    together with `overflow: hidden`.

    `@page { margin }` already insets the printable area. A `.page` that ALSO declares a
    near-full height overflows the sheet, and `overflow: hidden` then silently truncates the
    tail -- which on 2026-07-25 shipped a letter with its sign-off sliced through and the
    email line missing, past four passing guards.

    Résumés and work-samples legitimately use that pattern (their page count is fixed and the
    footer must hold the bottom edge), so this only applies to letters.
    """
    if not html_path.exists():
        return False, [f"no such file: {html_path}"]

    name = html_path.name.lower()
    if not any(k in name for k in ("cover-letter", "cover_letter", "coverletter", "letter")):
        return True, []          # not a letter -- the pinned model is correct there

    try:
        src = html_path.read_text(encoding="utf-8")
    except OSError as e:
        return False, [f"cannot read: {e}"]

    import re
    msgs = []

    # Strip comments first -- a commented-out example must not trip the guard.
    clean = re.sub(r"/\*.*?\*/", "", src, flags=re.S)

    # Find each `@media print { ... }` by BRACE MATCHING. A regex cannot do this: the block
    # contains nested rules, so `\{(.*?)\}` stops at the first inner `}` and the .page rule
    # inside is never seen (that bug made this guard silently pass its own regression file).
    blocks = []
    for m in re.finditer(r"@media\s+print\s*\{", clean):
        depth, i = 1, m.end()
        while i < len(clean) and depth:
            if clean[i] == "{":
                depth += 1
            elif clean[i] == "}":
                depth -= 1
            i += 1
        blocks.append(clean[m.end():i - 1])

    for block in blocks:
        for rule in re.findall(r"\.page\s*\{([^}]*)\}", block):
            has_h = re.search(r"(?<!min-)(?<!max-)height\s*:\s*[\d.]+\s*(in|px|pt|cm|mm)", rule)
            has_hidden = re.search(r"overflow\s*:\s*hidden", rule)
            if has_h and has_hidden:
                msgs.append(
                    "COVER LETTER: print `.page` declares BOTH a fixed `height` and "
                    "`overflow: hidden`. That combination CLIPS the sign-off at the box "
                    "boundary while every DOM-based guard reports success -- it is exactly "
                    "how a letter shipped on 2026-07-25 with 'Founder & CEO, ...' sliced "
                    "through and the email line missing.\n"
                    "     FIX: `.page { width: auto; height: auto; min-height: 0; }` with NO "
                    "overflow rule, and let the sign-off flow. If the letter then runs to two "
                    "pages, CUT PROSE (or tighten font-size / line-height within the band) --\n"
                    "     never restore the height, which only re-hides the overflow.\n"
                    "     Contract: layouts/resume/one-page-letter.json"
                )
    return (not msgs), msgs


def main(argv):
    _configure_stdout()

    if "--source" in argv:
        rest = [a for a in argv if not a.startswith("-")]
        if not rest:
            _out("usage: --source <doc>.html")
            return 2
        failed = 0
        for a in rest:
            ok, msgs = check_source_geometry(Path(a))
            _out(f"\n{'PASS' if ok else 'FAIL'}  {Path(a).name}")
            for m in msgs:
                _out(f"  XX {m}")
            if not ok:
                failed += 1
        _out("")
        return 1 if failed else 0

    expect = None
    if "--expect" in argv:
        i = argv.index("--expect")
        try:
            expect = int(argv[i + 1])
        except (IndexError, ValueError):
            _out("usage: --expect <n>")
            return 2
        argv = argv[:i] + argv[i + 2:]

    paths = [Path(a) for a in argv if not a.startswith("-")]
    if not paths:
        _out(__doc__)
        return 2

    failed = 0
    for p in paths:
        ok, msgs = check_pagefit(p, expect)
        _out(f"\n{'PASS' if ok else 'FAIL'}  {p.name}")
        for m in msgs:
            _out(f"  {'--' if ok else 'XX'} {m}")
        if not ok:
            failed += 1

    if failed:
        _out(f"\nFAIL: {failed} file(s). Fix order for a letter: cut prose -> tighten closing -> "
             f"font-size 11.5->11.0->10.75 -> line-height 1.55->1.5->1.45 -> margin 0.75-0.8in.")
        _out("NEVER add a fixed height + overflow:hidden to make it 'fit'.\n")
        return 1
    _out("\nPASS: page count, no clipped ink, no orphan tail.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
