"""Palette guard — reject banned colors before a document is exported.

House rule (owner directive 2026-07-13):
    NO brown. NO mustard. NO puke/lime green.
    Yellow and orange are allowed ONLY as bright, clean tones (high lightness).
    Any other green is fine — just not lime or puke.

Why this exists: darkening amber/gold for white paper turns it brown. That is a
color-space fact, not a mistake anyone made on purpose, so it will keep happening
unless something checks. This module is that check.

Usage:
    python -m pdf_tool.check_palette <file.html> [more.html ...]
    python -m pdf_tool.check_palette --scan storage/          # walk a tree

Exits non-zero if any banned color is found, and prints the offending hex,
what it is, the file, and the line.
"""

import colorsys
import re
import sys
from pathlib import Path

HEX_RE = re.compile(r"#([0-9a-fA-F]{6})\b")


def classify(hex6: str):
    """Return (verdict, label) for a 6-digit hex. verdict: 'ok' | 'banned'."""
    r, g, b = (int(hex6[i : i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue = h * 360

    # Near-neutral (very low saturation) is always fine — greys, near-blacks, paper white.
    if s < 0.18:
        return "ok", "neutral"

    # --- BROWN / MUSTARD -----------------------------------------------------
    # Orange-to-yellow hues that are too DARK read as brown or mustard on paper.
    # A clean amber must stay bright; once lightness drops it goes muddy.
    if 20 <= hue <= 65:
        if l < 0.50:
            return "banned", "BROWN/MUSTARD (dark orange-yellow)"
        if l < 0.58 and s < 0.60:
            return "banned", "MUSTARD (dull yellow)"
        return "ok", "bright amber/gold/orange"

    # --- PUKE / LIME GREEN ---------------------------------------------------
    # Yellow-green through chartreuse. Lime = bright + saturated; puke = dark + dull.
    if 65 < hue <= 100:
        return "banned", "LIME/PUKE GREEN (yellow-green)"

    # Olive: green hue but dark and desaturated -> reads as puke.
    if 100 < hue <= 150 and l < 0.35 and s < 0.55:
        return "banned", "OLIVE/PUKE GREEN"

    # Everything else (reds, magentas, blues, teals, purples, clean greens) is fine.
    return "ok", "allowed"


def check_file(path: Path):
    """Yield (line_no, hex, label) for each banned color in the file."""
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for n, line in enumerate(text.splitlines(), 1):
        for m in HEX_RE.finditer(line):
            hx = m.group(1)
            verdict, label = classify(hx)
            if verdict == "banned":
                hits.append((n, "#" + hx, label))
    return hits


def main(argv):
    args = [a for a in argv if a != "--scan"]
    scan = "--scan" in argv
    if not args:
        print(__doc__)
        return 2

    targets = []
    for a in args:
        p = Path(a)
        if scan or p.is_dir():
            targets += [
                f
                for f in p.rglob("*")
                if f.suffix.lower() in (".html", ".css", ".json") and "_exports" not in f.parts
            ]
        else:
            targets.append(p)

    total = 0
    for f in sorted(set(targets)):
        for n, hx, label in check_file(f):
            total += 1
            print(f"{f}:{n}: {hx}  <-  {label}")

    if total:
        print(f"\nFAIL: {total} banned color(s). House rule: no brown, no mustard, no lime/puke green.")
        print("Fix: on WHITE, amber has no readable dark form — use another hue from the palette instead.")
        return 1

    print("PASS: no banned colors.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
