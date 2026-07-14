"""Vault guard -- make sure a resume gets everything the vault can honestly give it.

The vault is the single source of truth for what a person may truthfully claim. The
danger is not that it says something false. The danger is that a claim is SILENTLY
INVISIBLE -- tagged with a track that doesn't exist, or with no track that matches the
job -- so the resume is quietly built without the best evidence its owner has.

Nobody sees an error. They just get a worse resume, and never find out why.

That has now happened three times:
  * Five claims (Photoshop, Figma, Affinity, Adobe CS, UX/UI) were tagged `ui-ux` on a
    vault that had no `ui-ux` track. A UI/UX resume would have shipped without her
    entire design toolkit.
  * Five engine claims (WebGPU, multiplayer, WWISE, Unreal/Unity, platforms) were
    tagged `game-dev` only -- so an ENGINE-RESEARCH resume built on the `ai` track
    couldn't see any of them.
  * Two industry-standard tools sat in `doNotClaim` for months while both applicants
    had years of experience with each.

The lesson each time: you cannot fix this with discipline. "Remember to check the
vault" is exactly the instruction that already failed. It has to be a GUARD.

THE THREE LAYERS
  1. VALIDATE  -- every section, not just skills. A track typo anywhere is now an error.
  2. COVERAGE  -- warn when a track is THIN (few claims reachable). A thin track means
                  a weak resume, and it is invisible without this check.
  3. EXPLAIN   -- print exactly what a resume WILL contain, ranked, BEFORE you build it.
                  You should never have to render a PDF to find out what it says.

Usage:
    python -m pdf_tool.check_vault --all                     # validate + coverage
    python -m pdf_tool.check_vault --explain shade ai        # what an `ai` resume gets
    python -m pdf_tool.check_vault --explain jenni 3d-viz --verbose
    python -m pdf_tool.check_vault storage/shade/resume-source.json

Exit non-zero on any error. Warnings (unverified tools, thin tracks) do not fail the
run -- they are reported so you know what to ask about.
"""

import json
import sys
from pathlib import Path

STRENGTHS = {"lead", "solid", "supporting"}
STATUSES = {"unverified", "confirmed-absent", "confirmed-have"}
RANK = {"lead": 0, "solid": 1, "supporting": 2}

# Every section whose entries carry `tracks` and therefore feed a resume.
# `skills` used to be the only one validated -- which meant a typo'd track on a CREDIT
# or an EMPLOYMENT entry failed just as silently, and nothing ever caught it.
TRACKED_SECTIONS = ("skills", "employment", "credits", "education", "clients")

# A track with fewer than this many track-specific claims will produce a thin,
# generic resume. Not an error -- but you should know before you build.
THIN_TRACK = 5


def _iter_entries(node):
    """Yield (label, entry) for every dict entry in a vault section, whatever its shape.

    Sections are inconsistent by design (skills is grouped by domain, employment is a
    flat list, credits nests titles/outsourcerCredits/ownTitles). Walk them all rather
    than special-casing, so a new section can't quietly escape validation.
    """
    if isinstance(node, list):
        for e in node:
            if isinstance(e, dict):
                yield "", e
    elif isinstance(node, dict):
        for key, val in node.items():
            if key.startswith("_"):
                continue
            if isinstance(val, list):
                for e in val:
                    if isinstance(e, dict):
                        yield key, e
            elif isinstance(val, dict) and ("tracks" in val or "claim" in val or "name" in val):
                yield key, val


def _label(entry, group=""):
    return entry.get("id") or entry.get("name") or entry.get("org") or entry.get("claim", "?")[:40] or group


def collect(vault, track):
    """Every entry a resume on `track` may draw on, correctly ranked.

    RANKING (this is the whole game):
        1. track-specific claims BEFORE `any` claims
        2. then by strength (lead -> solid -> supporting)

    Do NOT sort by strength alone. An `any`+`lead` claim (the AI-pipeline one) will
    otherwise outrank every claim that is actually ABOUT THE JOB -- sorted naively, an
    audio resume opens with AI tooling.
    """
    out = {}
    for sec in TRACKED_SECTIONS:
        hits = []
        for group, e in _iter_entries(vault.get(sec, {})):
            tr = e.get("tracks") or []
            if track in tr or "any" in tr:
                hits.append((track not in tr, RANK.get(e.get("strength", "supporting"), 2), group, e))
        hits.sort(key=lambda h: (h[0], h[1]))
        out[sec] = hits
    return out


def check_vault(path: Path):
    """Return (errors, warnings) for one vault file."""
    errors, warnings = [], []
    try:
        v = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot parse: {e}"], []

    tracks = {k for k in v.get("roleTracks", {}) if not k.startswith("_")}
    if not tracks:
        errors.append("roleTracks: no tracks defined")
        return errors, warnings

    # Every track needs an angle -- the framing /make-resume reads.
    for t in sorted(tracks):
        spec = v["roleTracks"][t]
        if not isinstance(spec, dict):
            errors.append(f"roleTracks.{t}: must be an object with `covers` + `angle`")
        elif "angle" not in spec and "clusters" not in spec:
            errors.append(f"roleTracks.{t}: no `angle` -- /make-resume has no framing for this track")

    # --- validate EVERY tracked section, not just skills ---------------------
    seen_ids = {}
    for sec in TRACKED_SECTIONS:
        for group, e in _iter_entries(v.get(sec, {})):
            where = f"{sec}.{group + '.' if group else ''}{_label(e, group)}"

            cid = e.get("id")
            if cid:
                if cid in seen_ids:
                    errors.append(f"{where}: duplicate id (also {seen_ids[cid]})")
                seen_ids[cid] = where

            tr = e.get("tracks")
            if not tr:
                # credits/clients sometimes legitimately carry no tracks (they're cited
                # via a parent rule) -- only skills/employment MUST be reachable.
                if sec in ("skills", "employment"):
                    errors.append(f"{where}: no `tracks` -- this can NEVER be selected. It is invisible.")
                continue

            for t in tr:
                if t != "any" and t not in tracks:
                    errors.append(
                        f"{where}: tracks has {t!r}, which is NOT A REAL TRACK -- this entry is "
                        f"INVISIBLE and will never appear on any resume. Real tracks: {sorted(tracks)}"
                    )

            if sec == "skills":
                if not e.get("source"):
                    errors.append(f"{where}: no `source` -- source-backed only")
                if not e.get("confidence"):
                    errors.append(f"{where}: no `confidence`")
                if e.get("strength") not in STRENGTHS:
                    errors.append(f"{where}: strength {e.get('strength')!r} not in {sorted(STRENGTHS)}")

    # --- COVERAGE: is any track too thin to build a good resume from? --------
    for t in sorted(tracks):
        got = collect(v, t)
        specific = sum(1 for h in got["skills"] if not h[0])
        total = len(got["skills"])
        if specific < THIN_TRACK:
            warnings.append(
                f"THIN TRACK `{t}`: only {specific} track-specific skill claim(s) "
                f"({total} incl. `any`). A resume on this track will be generic. "
                f"Either tag more claims with `{t}`, or don't use this track."
            )

    # --- the verification ledger (the Maya/ZBrush check) ---------------------
    dnc = v.get("doNotClaim", {})
    unverified = []
    for t in dnc.get("tools", []):
        if isinstance(t, str):
            errors.append(
                f"doNotClaim.tools: {t!r} is a bare string. It MUST be an object with a `status` -- "
                f"a flat blocklist cannot tell 'we asked and they don't have it' from 'nobody ever "
                f"checked', which is exactly how two tools they DO have got wrongly forbidden."
            )
            continue
        name, status = t.get("name", "?"), t.get("status")
        if status not in STATUSES:
            errors.append(f"doNotClaim.tools.{name}: status {status!r} not in {sorted(STATUSES)}")
        elif status == "unverified":
            unverified.append(name)
        elif status == "confirmed-have":
            errors.append(f"doNotClaim.tools.{name}: `confirmed-have` -- move it to `skills`")

    if unverified:
        warnings.append(
            f"{len(unverified)} tool(s) UNVERIFIED -- nobody has asked. NOT gaps; do not write them "
            f"off in an application: {', '.join(unverified)}"
        )

    return errors, warnings


def explain(user: str, track: str, verbose: bool = False) -> int:
    """Print exactly what a resume on this track WILL contain, ranked. Before you build it."""
    path = Path("storage") / user / "resume-source.json"
    if not path.exists():
        print(f"no vault at {path}")
        return 2
    v = json.loads(path.read_text(encoding="utf-8"))

    tracks = {k for k in v.get("roleTracks", {}) if not k.startswith("_")}
    if track not in tracks:
        print(f"'{track}' is not a track for {user}. Available: {sorted(tracks)}")
        return 2

    spec = v["roleTracks"][track]
    print(f"\n{'=' * 78}")
    print(f"  {user.upper()}  ·  track: {track}")
    print(f"{'=' * 78}")
    print(f"\n{spec.get('covers', '')}\n")

    angle = spec.get("angle", {})
    if angle.get("leadWith"):
        print("LEAD WITH:")
        for x in angle["leadWith"]:
            print(f"   * {x}")
    if angle.get("demote"):
        print("\nDEMOTE:")
        for x in angle["demote"]:
            print(f"   - {x}")
    if spec.get("clusters"):
        print("\nCLUSTERS (reorder by what the listing names):")
        for cname, c in spec["clusters"].items():
            print(f"   [{cname}] {', '.join(c.get('titles', [])[:3])}")

    got = collect(v, track)
    print(f"\n{'-' * 78}")
    print("  EVERY CLAIM THIS RESUME MAY DRAW ON, IN RANK ORDER")
    print("  (track-specific first, THEN by strength -- never strength alone)")
    print(f"{'-' * 78}")

    for sec in TRACKED_SECTIONS:
        hits = got[sec]
        if not hits:
            continue
        specific = sum(1 for h in hits if not h[0])
        print(f"\n{sec.upper()}  ({len(hits)} available, {specific} track-specific)")
        for is_any, _, group, e in hits:
            tag = "any " if is_any else "**  "
            st = (e.get("strength") or "")[:4]
            txt = e.get("claim") or e.get("summary") or e.get("name") or e.get("org") or ""
            cid = e.get("id") or e.get("name") or ""
            print(f"   {tag}[{st:4}] {str(cid)[:22]:22} {txt[:44]}")

    total = sum(len(got[s]) for s in TRACKED_SECTIONS)
    spec_n = sum(1 for h in got["skills"] if not h[0])
    print(f"\n{'-' * 78}")
    print(f"  {total} entries available.  '**' = track-specific (lead with these).")
    print(f"  '{track}' has {spec_n} track-specific SKILL claims.", end="  ")
    print("THIN -- resume will be generic." if spec_n < THIN_TRACK else "Healthy.")
    print(f"{'-' * 78}")
    print("\n  If something you EXPECT is missing from this list, it is tagged wrong in the")
    print("  vault and WILL NOT appear on the resume. Fix the tags, not the resume.\n")
    return 0


def main(argv):
    if "--explain" in argv:
        i = argv.index("--explain")
        rest = [a for a in argv[i + 1:] if not a.startswith("-")]
        if len(rest) < 2:
            print("usage: --explain <user> <track>")
            return 2
        return explain(rest[0], rest[1], verbose="--verbose" in argv)

    if "--all" in argv:
        paths = sorted(Path("storage").glob("*/resume-source.json"))
        if not paths:
            print("no vaults under storage/*/resume-source.json")
            return 2
    else:
        paths = [Path(a) for a in argv if not a.startswith("-")]
    if not paths:
        print(__doc__)
        return 2

    failed = 0
    for p in paths:
        errors, warnings = check_vault(p)
        print(f"\n{p}")
        for e in errors:
            print(f"  ERROR  {e}")
        for w in warnings:
            print(f"  warn   {w}")
        if errors:
            failed += 1
        elif not warnings:
            print("  OK")

    if failed:
        print(f"\nFAIL: {failed} vault(s) have errors.")
        return 1
    print("\nPASS: all vaults valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
