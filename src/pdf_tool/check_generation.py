"""check_generation — the ONE QA pass for a generated document (resume / cover letter / work-samples).

Runs every house rule against an .html source in one shot, so a generation can't ship with a
brown wash, a magenta Shade doc, an all-lowercase name, a drifting margin, an unpinned signature,
or a neon color painted over a photo. Composes the existing single-purpose guards
(check_palette, check_overflow) and adds the checks they don't cover.

    python -m pdf_tool.check_generation <doc>.html                  # auto-detect user from filename/content
    python -m pdf_tool.check_generation <doc>.html --user shade     # force per-user rules (no-magenta)
    python -m pdf_tool.check_generation --scan storage/shade/defaults  # sweep a dir of .html
    python -m pdf_tool.check_generation <doc>.html --json           # machine-readable

Exit 0 = all checks pass. Exit 1 = one or more FAIL. Exit 2 = bad usage / file not found.

The rules (SSOT: themes/GENERATION-RULES.md + themes/PALETTE-RULES.md):
  1. palette      no brown / mustard / lime  (+ no magenta/pink for shade & martian)
  2. rgba-magenta magenta/pink smuggled in as rgba()/hsl() (invisible to the hex-only palette guard)
  3. casing       names & company names never all-lowercase in display text
  4. overlay      no bright/neon/primary fill washed over a banner/hero/photo (dark scrim only)
  5. signature    a bottom-pinned bottom-right signature block is present
  6. margins      @page margins are equal on all four edges (consistent padding)
  7. overflow     no page overflows its print box (pinned footer won't collide) — needs render
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import check_palette

# Windows consoles default to cp1252 and choke on → / ⭐ etc. Force UTF-8 for our output.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ helpers

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _detect_user(path: Path, html: str) -> str | None:
    """shade / jenni / martian / studio / None, from the path then the content."""
    p = str(path).lower()
    for u in ("shade", "jenni", "martian", "studio"):
        if f"/{u}" in p.replace("\\", "/") or path.name.lower().startswith(u):
            return u
    # content fallback — signature name / studio line
    low = html.lower()
    if "shade@martiangames" in low or ">shade<" in low:
        return "shade"
    if "jenni@jenninexus" in low or "jennifer sylvester" in low:
        return "jenni"
    return None


def _no_magenta_for(user: str | None) -> bool:
    return user in ("shade", "martian")


# ------------------------------------------------------------------ checks
# Each check returns (ok: bool, list[str] messages).

def check_palette_hex(path: Path, no_magenta: bool):
    hits = check_palette.check_file(path, no_magenta=no_magenta)
    msgs = [f"line {n}: {hx} <- {label}" for n, hx, label in hits]
    return (not hits), msgs


# magenta/pink as rgba()/hsl() — the palette guard is hex-only, so these slip past it.
_RGBA_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", re.I)


def _rgb_is_magenta(r: int, g: int, b: int) -> bool:
    import colorsys
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hue = h * 360
    return 290 <= hue <= 345 and s >= 0.25 and 0.18 <= l <= 0.85


def check_rgba_magenta(path: Path, no_magenta: bool):
    if not no_magenta:
        return True, []
    html = _read(path)
    msgs = []
    for n, line in enumerate(html.splitlines(), 1):
        # skip comment lines that document a past fix ("was rgba(...)")
        low = line.lower()
        if "was rgba" in low or "magenta-free" in low or "(was " in low:
            continue
        for m in _RGBA_RE.finditer(line):
            r, g, b = (int(x) for x in m.groups())
            if _rgb_is_magenta(r, g, b):
                msgs.append(f"line {n}: rgba({r},{g},{b}) is magenta/pink (banned for shade/martian)")
    return (not msgs), msgs


# NAMES + company names must never be all-lowercase in DISPLAY (body) text.
# NOTE: 'jenninexus' is EXCLUDED — it is Jenni's brand wordmark, deliberately styled lowercase
# (like a logo). GENERATION-RULES allows a stylized wordmark; the ban targets the NAMES below.
_LOWER_TOKENS = ["jenni", "shade", "martian games", "synagen", "synabrain", "agency"]
# lowercase forms that are legitimate (urls, emails, handles, file paths) — ignore them.
_LOWER_OK_CONTEXT = re.compile(
    r"(mailto:|https?://|@|\.com|\.us|\.io|github\.com|linkedin|/in/|\.json|\.html|\.css|\.pdf"
    r"|src=|href=|url\(|storage/|resources/|\{\{img)", re.I)


def check_casing(path: Path):
    html = _read(path)
    msgs = []
    # remove non-display regions so we only test VISIBLE body text (correct line numbers preserved
    # by blanking each region in place rather than deleting it).
    def _blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    body = re.sub(r"<style.*?</style>", _blank, html, flags=re.S | re.I)
    body = re.sub(r"<script.*?</script>", _blank, body, flags=re.S | re.I)
    body = re.sub(r"<head.*?</head>", _blank, body, flags=re.S | re.I)   # title/meta live here
    body = re.sub(r"<!--.*?-->", _blank, body, flags=re.S)

    for n, line in enumerate(body.splitlines(), 1):
        for chunk in re.findall(r">([^<]+)<", line):      # text nodes only
            if _LOWER_OK_CONTEXT.search(chunk):
                continue
            for tok in _LOWER_TOKENS:
                for mt in re.finditer(r"(?<![\w./@-])" + re.escape(tok) + r"(?![\w./@-])", chunk):
                    seg = chunk[max(0, mt.start() - 12): mt.end() + 12]
                    if _LOWER_OK_CONTEXT.search(seg):
                        continue
                    msgs.append(f"line {n}: all-lowercase '{tok}' in display text: …{seg.strip()}…")
    seen, out = set(), []
    for m in msgs:
        if m not in seen:
            seen.add(m); out.append(m)
    return (not out), out


# no bright/neon/primary FILL over an image. Approved on-image overlay = a dark (near-black) scrim.
def check_image_overlay(path: Path):
    html = _read(path)
    msgs = []
    # find .hero .cap / caption overlays and any element that sits over an <img> with a colored bg.
    # Heuristic: a gradient/solid background inside a rule whose selector also styles an image caption,
    # where the color is NOT near-black. We scan the <style> for caption/overlay rules.
    style = "\n".join(re.findall(r"<style.*?>(.*?)</style>", html, flags=re.S | re.I))
    # rules that look like image overlays
    for m in re.finditer(r"\.(hero|cap|overlay|banner)[^{]*\{([^}]*)\}", style, re.I):
        block = m.group(2)
        for bg in re.finditer(r"background(?:-image)?\s*:\s*([^;]+);", block, re.I):
            val = bg.group(1)
            # collect rgb(a) colors in the overlay
            for cm in _RGBA_RE.finditer(val):
                r, g, b = (int(x) for x in cm.groups())
                # a scrim is near-black: all channels low. Flag a bright/saturated fill.
                if max(r, g, b) > 90 and (max(r, g, b) - min(r, g, b)) > 40:
                    msgs.append(
                        f".{m.group(1)} overlay uses a colored fill rgba({r},{g},{b}) over an image "
                        f"— use a black→transparent scrim (GENERATION-RULES.md)")
    seen, out = set(), []
    for x in msgs:
        if x not in seen:
            seen.add(x); out.append(x)
    return (not out), out


def _doc_type(path: Path, html: str) -> str:
    """resume | cover-letter | work-samples — from the filename/content."""
    name = path.name.lower()
    if "cover" in name or "letter" in name:
        return "cover-letter"
    if "work-sample" in name or "work-example" in name or "portfolio" in name:
        return "work-samples"
    low = html.lower()
    if "re:" in low and "dear" in low:
        return "cover-letter"
    return "resume"


# Signature rule is DOC-TYPE aware (GENERATION-RULES / LAYOUT-SYSTEM):
#   resume + work-samples → signature/footer PINNED to the bottom (margin-top:auto), bottom-RIGHT.
#   cover letter          → signoff flows after the body (natural), not pinned. Just must exist.
def check_signature(path: Path):
    html = _read(path)
    style = "\n".join(re.findall(r"<style.*?>(.*?)</style>", html, flags=re.S | re.I))
    dt = _doc_type(path, html)

    has_sig_el = bool(re.search(r'class="[^"]*\b(page-sig|signature|signoff|footer|page-foot)\b', html))
    if not has_sig_el:
        return False, [f"[{dt}] no signature/sign-off element "
                       f"(.page-sig / .signature / .signoff / .footer)"]

    if dt == "cover-letter":
        # a signoff just needs to be present (natural flow is correct for a 1-page letter)
        return True, []

    # resume / work-samples: must be bottom-pinned
    pinned = bool(re.search(r"(page-sig|signature|signoff|footer|page-foot)[^{]*\{[^}]*margin-top:\s*auto",
                            style, re.I | re.S))
    if not pinned:
        return False, [f"[{dt}] signature/footer is not bottom-pinned "
                       f"(needs margin-top:auto on its rule — LAYOUT-SYSTEM.md)"]
    # bottom-RIGHT alignment for resume/work-samples (align-self:flex-end or a right-aligned footer)
    right = bool(re.search(r"(page-sig|signature)[^{]*\{[^}]*(align-self:\s*flex-end|text-align:\s*right)",
                           style, re.I | re.S)) or "footer" in html.lower()
    if not right:
        return False, [f"[{dt}] signature is pinned but not bottom-RIGHT "
                       f"(needs align-self:flex-end / text-align:right)"]
    return True, []


# @page margins equal on all four edges (consistent padding).
# The @page background paints the PDF's MARGIN/BORDER area. If sibling docs in one application
# disagree (e.g. 0B0B0D on the letter vs 000000 on the samples), the set looks mismatched when the
# PDFs sit side by side — the reader sees a different-coloured border on one file. Caught 2026-07-21.
def check_page_bg(path: Path):
    html = _read(path)
    msgs = []
    bgs = re.findall(r"@page[^{]*\{[^}]*background:\s*(#[0-9a-fA-F]{3,8})", html)
    uniq = {b.lower() for b in bgs}
    if len(uniq) > 1:
        msgs.append(f"@page backgrounds disagree inside this file: {sorted(uniq)}")
    # Cross-document consistency, scoped to the SAME APPLICANT. Two applicants applying to one
    # company legitimately render different palettes (split accent runs), so only compare files
    # that share this doc's user prefix (e.g. shade-* vs shade-*).
    stem = path.name.split("-")[0].lower()
    sibs = [p for p in path.parent.glob("*.html")
            if p != path and not p.name.endswith(".template.html")
            and p.name.split("-")[0].lower() == stem]
    for s in sibs:
        try:
            sb = re.findall(r"@page[^{]*\{[^}]*background:\s*(#[0-9a-fA-F]{3,8})", _read(s))
        except OSError:
            continue
        su = {b.lower() for b in sb}
        if su and uniq and su != uniq:
            msgs.append(f"page background {sorted(uniq)} differs from {s.name} {sorted(su)} "
                        f"— sibling docs in one application must share the PDF border colour")
    return (not msgs), msgs


def check_margins(path: Path):
    html = _read(path)
    msgs = []
    for m in re.finditer(r"@page[^{]*\{[^}]*?margin:\s*([^;]+);", html, re.I | re.S):
        val = m.group(1).strip()
        parts = val.split()
        if len(parts) == 1:
            continue  # single value = equal on all four, fine
        if len(parts) in (2, 3, 4):
            # 2 = vert/horiz (equal per-axis, acceptable if both axes match is NOT required;
            # the house rule is "equal on all four edges" — 2-value v/h is the common cover-letter form
            # and is allowed as long as it's symmetric per axis). 3/4 asymmetric values are the drift.
            uniq = set(parts)
            if len(parts) >= 3 and len(uniq) > 1:
                msgs.append(f"@page margin '{val}' is asymmetric (drift) — use equal margins "
                            f"(one value, or a symmetric v/h pair). See GENERATION-RULES/LAYOUT-SYSTEM.")
    return (not msgs), msgs


def check_footer_collision(path: Path):
    """GROUND TRUTH: export the PDF and look for content colliding with the pinned signature.

    DOM measurement (check_overflow) sums heights and can still miss a real collision — it did on
    2026-07-21, when a Toolbelt line rendered *through* the "Shade Muse" signature on page 1 while
    the guard reported PASS. This renders the actual PDF and inspects the signature band: if
    non-background pixels appear to the LEFT of the right-aligned signature on the same rows, body
    text is running into it.
    """
    try:
        import tempfile
        import pypdfium2 as pdfium
        from . import html_to_pdf  # noqa: F401  (ensures the export deps exist)
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return True, [f"(skipped — {e})"]

    msgs = []
    try:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "probe.pdf"
            with sync_playwright() as p:
                b = p.chromium.launch()
                pg = b.new_page()
                pg.goto(path.resolve().as_uri())
                pg.evaluate("() => document.documentElement.setAttribute('data-pdf-theme','dark')")
                pg.emulate_media(media="print")
                pg.wait_for_timeout(400)
                # Match html_to_pdf: CSS @page size + painted backgrounds.
                pg.pdf(
                    path=str(out),
                    format="Letter",
                    print_background=True,
                    prefer_css_page_size=True,
                )
                b.close()

            pdf = pdfium.PdfDocument(str(out))
            try:
                for i in range(len(pdf)):
                    im = pdf[i].render(scale=2).to_pil().convert("RGB")
                    W, H = im.size
                    # Sample INSIDE the content box — edge pixels are often @page
                    # chrome (or white margin) and make the whole sheet look "lit".
                    # 0.65in ≈ 94px at scale 2; use a safe inset past equal margins.
                    inset = max(120, int(min(W, H) * 0.12))
                    bg = im.getpixel((inset, H // 2))

                    def lit(px):  # noticeably different from the page background
                        return sum(abs(a - c) for a, c in zip(px, bg)) > 90

                    # Signature is the BOTTOM-MOST contiguous lit cluster in the far-right column.
                    # Do NOT take every right-column lit row in the bottom 22% — a 2-col Tools
                    # block also paints there and would inflate the band (false positive). The
                    # 2026-07-20 jenni miss was the opposite: Tools col-2 under the glyphs with
                    # a left-only intrusion window that stopped at 0.62 and reported PASS.
                    sig_x0 = int(W * 0.72)
                    search_lo = int(H * 0.70)
                    right_rows = [y for y in range(search_lo, H - 2, 2)
                                  if any(lit(im.getpixel((x, y))) for x in range(sig_x0, W - 4, 3))]
                    if not right_rows:
                        continue
                    # Walk up from the bottom-most lit row. Allow a short empty run so the
                    # script name + email line stay one cluster (they often have ~10–16px
                    # between them). Stop only after a larger gap — that is body content above.
                    bot = max(right_rows)
                    top = bot
                    gap = 0
                    for y in range(bot, search_lo - 1, -2):
                        if any(lit(im.getpixel((x, y))) for x in range(sig_x0, W - 4, 3)):
                            top = y
                            gap = 0
                        else:
                            gap += 1
                            if gap >= 8:  # ≥16 px empty at scale 2 → above the signature cluster
                                break
                    # Body text on those same signature rows, including mid/right columns
                    # up to the signature (catches col-2 sitting under the script).
                    intruding = sum(
                        1 for y in range(top, bot + 1, 2)
                        for x in range(int(W * 0.08), sig_x0, 3)
                        if lit(im.getpixel((x, y)))
                    )
                    if intruding > 40:
                        msgs.append(
                            f"page {i + 1}: body content overlaps the pinned signature band "
                            f"(rows {top}-{bot}, {intruding} intruding pixels). Move a section to the "
                            f"next page — see docs/LAYOUT-SYSTEM.md content-fit rule.")
            finally:
                pdf.close()
    except Exception as e:
        return True, [f"(skipped — {e})"]
    return (not msgs), msgs


def check_overflow_render(path: Path):
    """Render-based: import lazily (playwright/pypdfium2) so the other checks work without them."""
    try:
        from . import check_overflow
    except Exception as e:  # pragma: no cover
        return True, [f"(skipped overflow — {e})"]
    msgs = []
    for theme in (None, "dark"):
        try:
            over = check_overflow.check_overflow(str(path), pdf_theme=theme)
        except Exception as e:
            return True, [f"(skipped overflow render — {e})"]
        for o in over:
            msgs.append(f"[{theme or 'light'}] page {o.get('index')}: content {o.get('content')}px "
                        f"> box {o.get('box')}px")
    return (not msgs), msgs


def check_rendered(path: Path):
    """RENDERED-PIXEL brown + large-area warm cast — catches brown the hex guard cannot see.

    A red-tinted dark grey background is 'neutral' per-pixel but reads BROWN over a large area;
    alpha layers over warm darks manufacture real brown pixels that appear in no stylesheet.
    """
    try:
        from . import check_rendered_color
    except Exception as e:
        return True, [f"(skipped — {e})"]
    msgs = []
    try:
        rep = check_rendered_color.analyze(path)
    except Exception as e:
        return True, [f"(skipped render — {e})"]
    if rep["brown_pct"] > rep["thresholds"]["max_brown_pct"]:
        msgs.append(f"{rep['brown_pixels']} brown/mustard px ({rep['brown_pct']}%) "
                    f"> {rep['thresholds']['max_brown_pct']}%")
        msgs += [f"  {s}" for s in rep["pixel_samples"][:4]]
    for c in rep["cast_violations"][:4]:
        msgs.append(c)
    if rep["cast_violations"]:
        msgs.append("FIX: remove warm/red tint from the BASE background; red only as saturated accents.")
    return (not msgs), msgs


CHECKS = [
    ("palette", "no brown/mustard/lime (+ no magenta for shade/martian)", check_palette_hex, True),
    ("rgba-magenta", "no magenta/pink smuggled via rgba()/hsl()", check_rgba_magenta, True),
    ("casing", "names/company never all-lowercase in display text", check_casing, False),
    ("overlay", "no neon/color fill over images (dark scrim only)", check_image_overlay, False),
    ("signature", "signature block present + bottom-pinned", check_signature, False),
    ("margins", "equal/consistent @page margins", check_margins, False),
    ("page-bg", "PDF border colour matches sibling docs in the same application", check_page_bg, False),
    ("rendered-color", "⭐ no brown in the RENDERED pixels / no large-area warm cast", check_rendered, False),
    ("overflow", "no page overflows its print box (render)", check_overflow_render, False),
    ("footer-collision", "⭐ PDF ground truth: nothing overlaps the pinned signature",
     check_footer_collision, False),
]


def run_file(path: Path, user: str | None = None, do_render: bool = True) -> dict:
    html = _read(path)
    if user is None:
        user = _detect_user(path, html)
    no_mag = _no_magenta_for(user)
    results = []
    for key, desc, fn, needs_nomag in CHECKS:
        if key in ("overflow", "rendered-color", "footer-collision") and not do_render:
            results.append({"check": key, "ok": True, "skipped": True, "messages": ["(render skipped)"]})
            continue
        if needs_nomag:
            ok, msgs = fn(path, no_mag)
        else:
            ok, msgs = fn(path)
        results.append({"check": key, "desc": desc, "ok": ok, "messages": msgs})
    passed = all(r["ok"] for r in results)
    return {"file": str(path), "user": user, "no_magenta": no_mag, "passed": passed, "checks": results}


def _print_report(rep: dict) -> None:
    mark = "PASS" if rep["passed"] else "FAIL"
    u = rep["user"] or "?"
    print(f"\n{'='*76}\n{mark}  {rep['file']}   (user={u}, no-magenta={rep['no_magenta']})")
    for r in rep["checks"]:
        if r.get("skipped"):
            print(f"  ~ {r['check']:<13} skipped")
            continue
        icon = "OK " if r["ok"] else "XX "
        print(f"  {icon}{r['check']:<13} {r.get('desc','')}")
        if not r["ok"]:
            for m in r["messages"]:
                print(f"        - {m}")


def main(argv) -> int:
    args = [a for a in argv if not a.startswith("--")]
    flags = [a for a in argv if a.startswith("--")]
    as_json = "--json" in flags
    scan = "--scan" in flags
    do_render = "--no-render" not in flags
    user = None
    if "--user" in argv:
        i = argv.index("--user")
        if i + 1 < len(argv):
            user = argv[i + 1]
            args = [a for a in args if a != user]

    if not args:
        print(__doc__)
        return 2

    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if scan or p.is_dir():
            targets += [f for f in p.rglob("*.html") if not f.name.endswith(".template.html")]
        elif p.exists():
            targets.append(p)
        else:
            print(f"not found: {a}")
            return 2

    reports = [run_file(p, user=user, do_render=do_render) for p in sorted(set(targets))]

    if as_json:
        print(json.dumps(reports, indent=2))
    else:
        for rep in reports:
            _print_report(rep)
        n_fail = sum(1 for r in reports if not r["passed"])
        print(f"\n{'='*76}\n{len(reports)} file(s) checked · {n_fail} FAIL · {len(reports)-n_fail} PASS")

    return 1 if any(not r["passed"] for r in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
