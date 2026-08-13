"""Omission audit -- what did the vault have that the resume left out?

`check_vault --explain` tells you what a resume COULD say, before you build it.
This tells you what it actually DIDN'T say, after you build it.

They catch different failures:

    --explain   catches a claim that is INVISIBLE (tagged wrong -> never selectable)
    audit       catches a claim that was VISIBLE and simply got FORGOTTEN

The second one is the quiet one. Nothing errors. The resume renders, the page count is
right, the palette passes -- and a `lead`-strength claim the applicant spent fifteen
years earning just isn't on the page, because whoever wrote it didn't scroll far enough.

This diffs the rendered document against the vault and reports every claim that was
available for that track and does not appear.

    python -m pdf_tool.audit_resume shade ai storage/shade/shade-ai-resume.html

Not every omission is a bug -- a resume is a SELECTION, and cutting is the whole craft.
A `supporting` claim left off a two-page resume is a judgment call. But a **lead**
claim missing from the document is almost always a mistake, and you should have to look
at it and decide, rather than never learn it happened.

Exit codes:  0 = no lead-strength omissions   1 = a lead claim is missing
"""

import json
import re
import sys
from pathlib import Path

from .check_vault import TRACKED_SECTIONS, collect
from .paths import vault_path

# Words too generic to prove a claim is present -- matching on these gives false
# "it's covered" readings and defeats the audit.
STOP = {
    "and", "the", "for", "with", "a", "an", "of", "in", "to", "on", "at", "is", "it",
    "as", "by", "or", "from", "that", "this", "real", "work", "years", "year", "not",
    "new", "own", "own", "into", "across", "every", "all", "more", "most", "than",
    "production", "design", "designer", "development", "experience", "skills", "tools",
}


def _keywords(text, n=10):
    """The distinctive words in a claim -- the ones that would prove it's on the page.

    Take MORE of them (10, not 6) and stem lightly. A resume RESTATES a claim in the
    employer's vocabulary rather than pasting it, so a narrow keyword set produces false
    "missing" reports: this audit first flagged a claim as absent while the document said
    "generative asset and audio pipelines" three separate times. A noisy guard gets
    ignored, and an ignored guard is worse than none.
    """
    words = re.findall(r"[A-Za-z0-9+#]{3,}", text.lower())
    seen, out = set(), []
    for w in words:
        # light stem: creative/creatives, tool/tools, pipeline/pipelines all match
        stem = w[:-1] if w.endswith("s") and len(w) > 4 else w
        if stem in STOP or stem in seen or len(stem) < 3:
            continue
        seen.add(stem)
        out.append(stem)
        if len(out) >= n:
            break
    return out


def _present(claim, page_text, threshold=0.34):
    """Is this claim represented on the page?

    Overlap, not exact match. The threshold is deliberately LOW (a third of the keywords):
    the cost of a false "missing" is that a real signal gets buried in noise and the whole
    audit stops being read. The cost of a false "present" is that one claim slips through
    -- and `--explain` already covers that case before the build. So: bias toward quiet.
    """
    kws = _keywords(claim)
    if not kws:
        return True
    hits = sum(1 for k in kws if k in page_text)
    return hits / len(kws) >= threshold


def audit(user: str, track: str, html_path: str):
    vault_p = vault_path(user)
    doc_p = Path(html_path)
    if not vault_p.exists():
        print(f"no vault: {vault_p}")
        return 2
    if not doc_p.exists():
        print(f"no document: {doc_p}")
        return 2

    v = json.loads(vault_p.read_text(encoding="utf-8"))
    raw = doc_p.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<[^>]+>", " ", raw)          # strip tags
    text = re.sub(r"\s+", " ", text).lower()     # normalize

    got = collect(v, track)

    missing_lead, missing_solid, missing_supp = [], [], []
    total = present = 0

    for sec in TRACKED_SECTIONS:
        for is_any, _, _group, e in got[sec]:
            claim = e.get("claim") or e.get("summary") or e.get("name") or e.get("org") or ""
            if not claim:
                continue
            total += 1
            if _present(claim, text):
                present += 1
                continue
            row = (e.get("id") or e.get("name") or "?", sec, "any" if is_any else "**", claim)
            st = e.get("strength", "supporting")
            (missing_lead if st == "lead" else
             missing_solid if st == "solid" else missing_supp).append(row)

    print(f"\n{'=' * 78}")
    print(f"  OMISSION AUDIT   {user} / {track}   ->   {doc_p.name}")
    print(f"{'=' * 78}")
    print(f"\n  {present}/{total} available claims are represented in the document.\n")

    def show(title, rows, note):
        if not rows:
            return
        print(f"{title}  ({len(rows)})")
        print(f"   {note}")
        for cid, sec, tag, claim in rows:
            print(f"   {tag} {cid[:22]:22} [{sec[:9]:9}] {claim[:44]}")
        print()

    show("!! MISSING **LEAD** CLAIMS", missing_lead,
         "These are the strongest things this person can say for this track.\n"
         "   A lead claim missing from the page is almost always a mistake.")
    show("-- missing solid claims", missing_solid,
         "Worth a look. Did you cut these deliberately, or lose them?")
    show("   missing supporting claims", missing_supp,
         "Usually fine -- a two-page resume cannot carry everything.")

    if missing_lead:
        print(f"{'=' * 78}")
        print(f"  {len(missing_lead)} LEAD claim(s) are missing. Either put them on the page,")
        print("  or be able to say why not. Do not let them vanish silently.")
        print(f"{'=' * 78}\n")
        return 1

    print("  No lead-strength claims omitted. The resume carries this person's best evidence.\n")
    return 0


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    if len(args) < 3:
        print(__doc__)
        return 2
    return audit(args[0], args[1], args[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
