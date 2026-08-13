"""Vault guard -- make sure a resume gets everything the vault can honestly give it.

The vault is the single source of truth for what a person may truthfully claim. The
danger is not that it says something false. The danger is that a claim is SILENTLY
INVISIBLE -- tagged with a track that doesn't exist, or with no track that matches the
job -- so the resume is quietly built without the best evidence its owner has.

Nobody sees an error. They just get a worse resume, and never find out why.

THE FOUR GUARD MODES
  1. VALIDATE  -- schema check on every tracked section (not just skills). A track typo
                  anywhere is an error. Thin tracks and unverified tools are warnings.
  2. EXPLAIN   -- print exactly what a resume WILL contain, ranked, BEFORE you build it.
                  You should never have to render a PDF to find out what it says.
  3. LISTING-COVERAGE -- mechanical gap-check: listing requirements vs vault claims on
                  a track. Unbacked rows are questions (ASK BEFORE GAPS), not failures.
  4. SUSPECT   -- which entries look WRONG or STALE and should be RE-CONFIRMED? The other
                  three ask "is the vault well-formed / does it cover this listing?".
                  This one asks "is what it says still TRUE?" -- the question that actually
                  bit us. Substance Painter sat `unverified` in BOTH vaults for months while
                  both founders had 5 years with it; nothing was malformed, so nothing
                  complained. With a listing, tools the EMPLOYER names are promoted to
                  URGENT (exit 1) so the build stops until someone asks.

Usage:
    python -m pdf_tool.check_vault --all                     # VALIDATE all vaults
    python -m pdf_tool.check_vault --explain shade ai        # ranked claims for track
    python -m pdf_tool.check_vault --explain jenni 3d-viz --verbose
    python -m pdf_tool.check_vault --coverage shade 3d-viz examples/_job-listings/example-application/Company.example.md
    python -m pdf_tool.check_vault --suspect shade                     # what should be re-confirmed?
    python -m pdf_tool.check_vault --suspect shade <listing>.md        # + urgent for THIS listing
    python -m pdf_tool.check_vault vaults/shade.json
    python -m pdf_tool.check_vault storage/shade/resume-source.json

Exit codes:
  0  PASS
  1  FAIL -- VALIDATE: schema errors; EXPLAIN: schema errors OR thin TARGET track;
             COVERAGE: schema errors OR thin target track;
             SUSPECT: an UNVERIFIED tool that THIS LISTING NAMES (ask before building)
  2  usage / missing vault / unknown track / unreadable listing

VALIDATE warnings (unverified tools, thin tracks on sibling tracks) do NOT fail --all.
EXPLAIN / COVERAGE treat a thin *target* track as exit 1 so you never build on an empty story.
COVERAGE unbacked listing rows return 0 -- they are questions, not hard fails.
"""

import json
import re
import sys
from pathlib import Path

from .paths import iter_vault_paths, resolve_rel, vault_path

STRENGTHS = {"lead", "solid", "supporting"}
STATUSES = {"unverified", "confirmed-absent", "confirmed-have"}
RANK = {"lead": 0, "solid": 1, "supporting": 2}

# Every section whose entries carry `tracks` and therefore feed a resume.
TRACKED_SECTIONS = ("skills", "employment", "credits", "education", "clients")

# A track with fewer than this many track-specific claims will produce a thin,
# generic resume. Not an error -- but you should know before you build.
THIN_TRACK = 5

_REQ_HEADER = re.compile(
    r"^(?:#+\s*)?(?:requirements?|qualifications?|what you.ll need|what we.re looking for)\b",
    re.I,
)
_VERBATIM_HEADER = re.compile(r"listing.*verbatim|verbatim.*listing", re.I)
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+(.+)")
_TOKEN = re.compile(r"[a-z0-9]{3,}", re.I)
_STOP = frozenset(
    "the and for with you our are will have this that from your experience years ability".split()
)


def _configure_stdout():
    """Avoid Windows cp1252 crashes on unicode (e.g. ≈) in vault text."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def _out(*args, **kwargs):
    """Safe print — utf-8 with replacement on broken consoles."""
    print(*args, **kwargs)


def _iter_entries(node):
    """Yield (label, entry) for every dict entry in a vault section, whatever its shape."""
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
    """Every entry a resume on `track` may draw on, correctly ranked."""
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


def track_depth(vault, track):
    """Return (narrative_depth, tool_count) for a track — shared by check_vault + explain."""
    got = collect(vault, track)
    narrative = [h for h in got["skills"] if h[3].get("kind") != "tool"]
    tools = len(got["skills"]) - len(narrative)
    depth = len(narrative) + len(got["employment"]) + len(got["credits"])
    return depth, tools


def _claim_text(entry):
    """Flatten one vault entry into searchable text."""
    parts = []
    for key in ("claim", "summary", "name", "org", "role", "yourRole", "id"):
        val = entry.get(key)
        if val:
            parts.append(str(val))
    bullets = entry.get("bullets")
    if isinstance(bullets, list):
        parts.extend(str(b) for b in bullets)
    return " ".join(parts).lower()


def _track_claim_corpus(vault, track):
    """All claim text reachable on `track`, with ids for reporting."""
    corpus = []
    for sec in TRACKED_SECTIONS:
        for _g, e in _iter_entries(vault.get(sec, {})):
            tr = e.get("tracks") or []
            if track in tr or "any" in tr:
                cid = e.get("id") or e.get("name") or _label(e)
                corpus.append((cid, _claim_text(e)))
    return corpus


def extract_requirements(text: str):
    """Pull requirement bullets from Requirements/Qualifications + verbatim listing sections."""
    lines = text.splitlines()
    reqs = []
    section = None
    in_fence = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            header = stripped.lstrip("#").strip()
            if _REQ_HEADER.search(header):
                section = "req"
                in_fence = False
                continue
            if _VERBATIM_HEADER.search(header):
                section = "verbatim"
                in_fence = False
                continue
            if section and stripped.startswith("##"):
                section = None
                in_fence = False
                continue

        if section == "verbatim" and stripped.startswith("```"):
            in_fence = not in_fence
            continue

        if section not in ("req", "verbatim"):
            continue

        m = _BULLET.match(line)
        if m:
            text = m.group(1).strip()
            if not text.endswith(":"):
                reqs.append(text)
            continue

        if section == "verbatim" and in_fence:
            continue  # verbatim section: bullets only (handled above)

    # De-dupe while preserving order
    seen = set()
    out = []
    for r in reqs:
        key = r.lower()
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def _tokens_align(req_t, claim_tokens):
    """True if req token matches any claim token (exact, substring, or 4-char prefix)."""
    for ct in claim_tokens:
        if req_t == ct:
            return True
        if len(req_t) >= 4 and len(ct) >= 4:
            if req_t[:4] == ct[:4]:
                return True
            if req_t in ct or ct in req_t:
                return True
    return False


def match_requirement(requirement: str, corpus):
    """Match one listing requirement against vault claim text (substring + token overlap)."""
    req_lower = requirement.lower()
    req_tokens = [t for t in _TOKEN.findall(req_lower) if t not in _STOP]
    if not req_tokens:
        return None

    best = None
    best_score = 0.0
    best_overlap = 0
    for cid, text in corpus:
        if req_lower in text or text in req_lower:
            return cid

        claim_tokens = list(_TOKEN.findall(text))
        if not claim_tokens:
            continue
        overlap = sum(1 for t in req_tokens if _tokens_align(t, claim_tokens))
        score = overlap / len(req_tokens)
        if overlap > best_overlap or (overlap == best_overlap and score > best_score):
            best_overlap = overlap
            best_score = score
            best = cid

    if best and (best_score >= 0.4 or best_overlap >= 2):
        return best
    return None


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

    for t in sorted(tracks):
        spec = v["roleTracks"][t]
        if not isinstance(spec, dict):
            errors.append(f"roleTracks.{t}: must be an object with `covers` + `angle`")
        elif "angle" not in spec and "clusters" not in spec:
            errors.append(f"roleTracks.{t}: no `angle` -- /make-resume has no framing for this track")

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

    for t in sorted(tracks):
        depth, tools = track_depth(v, t)
        if depth < THIN_TRACK:
            warnings.append(
                f"THIN TRACK `{t}`: only {depth} narrative claims + employment + credits "
                f"(tools excluded -- {tools} tools are selectable from every track by design). "
                f"A resume on this track would be a toolbelt with no story. Add "
                f"experience/capability claims tagged `{t}`."
            )
        if not v["roleTracks"].get(t, {}).get("toolbeltOrder"):
            warnings.append(
                f"track `{t}` has no `toolbeltOrder` -- nothing says which tools should LEAD "
                f"for this job family, so the resume may open its toolbelt with the wrong ones."
            )

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
    path = vault_path(user)
    if not path.exists():
        _out(f"no vault at {path}")
        return 2

    errors, warnings = check_vault(path)
    if errors:
        _out(f"\n{path}")
        for e in errors:
            _out(f"  ERROR  {e}")
        _out("\nFAIL: vault has schema errors -- fix before building.")
        return 1

    v = json.loads(path.read_text(encoding="utf-8"))
    tracks = {k for k in v.get("roleTracks", {}) if not k.startswith("_")}
    if track not in tracks:
        _out(f"'{track}' is not a track for {user}. Available: {sorted(tracks)}")
        return 2

    spec = v["roleTracks"][track]
    _out(f"\n{'=' * 78}")
    _out(f"  {user.upper()}  ·  track: {track}")
    _out(f"{'=' * 78}")
    _out(f"\n{spec.get('covers', '')}\n")

    angle = spec.get("angle", {})
    if angle.get("leadWith"):
        _out("LEAD WITH:")
        for x in angle["leadWith"]:
            _out(f"   * {x}")
    if angle.get("demote"):
        _out("\nDEMOTE:")
        for x in angle["demote"]:
            _out(f"   - {x}")
    if spec.get("clusters"):
        _out("\nCLUSTERS (reorder by what the listing names):")
        for cname, c in spec["clusters"].items():
            _out(f"   [{cname}] {', '.join(c.get('titles', [])[:3])}")

    got = collect(v, track)
    _out(f"\n{'-' * 78}")
    _out("  EVERY CLAIM THIS RESUME MAY DRAW ON, IN RANK ORDER")
    _out("  (track-specific first, THEN by strength -- never strength alone)")
    _out(f"{'-' * 78}")

    for sec in TRACKED_SECTIONS:
        hits = got[sec]
        if not hits:
            continue
        if sec == "skills":
            narrative = [h for h in hits if h[3].get("kind") != "tool"]
            tools = [h for h in hits if h[3].get("kind") == "tool"]
            specific = sum(1 for h in narrative if not h[0])
            _out(f"\nSKILLS — narrative  ({len(narrative)} available, {specific} track-specific)")
            _out("   what she DID and can DO. This is the story; lead with it.")
            for is_any, _, _g, e in narrative:
                tag = "any " if is_any else "**  "
                _out(f"   {tag}[{(e.get('strength') or '')[:4]:4}] {str(e.get('id'))[:22]:22} "
                     f"{(e.get('claim') or '')[:44]}")

            if tools:
                _out(f"\nTOOLBELT  ({len(tools)} tools — selectable from EVERY track)")
                order = spec.get("toolbeltOrder") or []
                if order:
                    _out(f"   LEAD WITH, on this track: {' · '.join(order)}")
                _out("   A tool you know is a tool you know. Every tool below is claimable on")
                _out("   this track — `toolbeltOrder` says which ones OPEN the section.")
                for _ia, _r, _g, e in tools:
                    _out(f"        [{(e.get('strength') or '')[:4]:4}] {str(e.get('id'))[:22]:22} "
                         f"{(e.get('claim') or '')[:44]}")
            continue

        specific = sum(1 for h in hits if not h[0])
        _out(f"\n{sec.upper()}  ({len(hits)} available, {specific} track-specific)")
        for is_any, _, group, e in hits:
            tag = "any " if is_any else "**  "
            st = (e.get("strength") or "")[:4]
            txt = e.get("claim") or e.get("summary") or e.get("name") or e.get("org") or ""
            cid = e.get("id") or e.get("name") or ""
            _out(f"   {tag}[{st:4}] {str(cid)[:22]:22} {txt[:44]}")

    total = sum(len(got[s]) for s in TRACKED_SECTIONS)
    depth, _tools = track_depth(v, track)
    narrative = [h for h in got["skills"] if h[3].get("kind") != "tool"]
    spec_n = sum(1 for h in narrative if not h[0])
    _out(f"\n{'-' * 78}")
    _out(f"  {total} entries available.  '**' = track-specific (lead with these).")
    _out(f"  '{track}' has {spec_n} track-specific NARRATIVE claims.", end="  ")
    _out("THIN -- toolbelt with no story." if depth < THIN_TRACK else "Healthy.")
    _out(f"{'-' * 78}")
    _out("\n  If something you EXPECT is missing from this list, it is tagged wrong in the")
    _out("  vault and WILL NOT appear on the resume. Fix the tags, not the resume.\n")

    if verbose and warnings:
        _out("  Vault warnings:")
        for w in warnings:
            _out(f"    warn  {w}")

    if depth < THIN_TRACK:
        return 1
    return 0


def coverage(user: str, track: str, listing_path: Path) -> int:
    """Mechanical gap-check: listing requirements vs vault claims on this track."""
    vpath = vault_path(user)
    if not vpath.exists():
        _out(f"no vault at {vpath}")
        return 2
    if not listing_path.exists():
        _out(f"no listing at {listing_path}")
        return 2

    errors, _warnings = check_vault(vpath)
    if errors:
        _out(f"\n{vpath}")
        for e in errors:
            _out(f"  ERROR  {e}")
        _out("\nFAIL: vault has schema errors -- fix before coverage check.")
        return 1

    try:
        listing_text = listing_path.read_text(encoding="utf-8")
    except OSError as e:
        _out(f"cannot read listing: {e}")
        return 2

    v = json.loads(vpath.read_text(encoding="utf-8"))
    tracks = {k for k in v.get("roleTracks", {}) if not k.startswith("_")}
    if track not in tracks:
        _out(f"'{track}' is not a track for {user}. Available: {sorted(tracks)}")
        return 2

    depth, _tools = track_depth(v, track)
    if depth < THIN_TRACK:
        _out(f"THIN TRACK `{track}`: only {depth} narrative claims -- tag more before applying.")
        return 1

    requirements = extract_requirements(listing_text)
    if not requirements:
        _out("no requirements found -- add bullets under Requirements/Qualifications or The listing, verbatim")
        return 2

    corpus = _track_claim_corpus(v, track)
    covered, unbacked = [], []

    _out(f"\n{'=' * 78}")
    _out(f"  COVERAGE  ·  {user}  ·  track: {track}")
    _out(f"  listing: {listing_path}")
    _out(f"{'=' * 78}\n")

    for req in requirements:
        match = match_requirement(req, corpus)
        if match:
            covered.append((req, match))
        else:
            unbacked.append(req)

    if covered:
        _out("COVERED (vault-backed):")
        for req, cid in covered:
            _out(f"  ✅  {req[:70]}")
            _out(f"      → {cid}")

    if unbacked:
        _out("\nUNBACKED — ASK BEFORE GAPS (not confirmed absent):")
        for req in unbacked:
            _out(f"  ⚠   {req}")

    _out(f"\n  {len(covered)} covered · {len(unbacked)} unbacked · {len(requirements)} total")
    _out("  Unbacked rows are questions, not failures. Ask the applicant before building.\n")
    return 0


def _employer_text(raw: str) -> str:
    """Return only the EMPLOYER's words from a listing doc.

    A finished `<Company>.md` is two documents in one: our assessment (evidence map, prep
    notes, and the explicit "Never claimed on this resume: Rhino, SketchUp, ..." line) and
    the verbatim listing below a `---` fence. Scanning the whole file to ask "does the
    employer want X?" is self-poisoning -- it finds every tool we wrote that we do NOT claim
    and reports it as a requirement.

    The convention (JOB-ASSESSMENT.md / make-resume step 6) is that the verbatim listing sits
    under a heading containing "verbatim" or "original listing", below a `---`. Use that when
    present; otherwise fall back to the whole text, minus the never-claimed line.
    """
    lower = raw.lower()
    for marker in ("## original listing", "## the listing, verbatim", "verbatim listing",
                   "listing (verbatim", "original listing (verbatim"):
        i = lower.find(marker)
        if i != -1:
            return raw[i:]
    # No verbatim fence -- strip the lines that enumerate what we deliberately do NOT claim.
    keep = [ln for ln in raw.splitlines()
            if "never claim" not in ln.lower() and "do not claim" not in ln.lower()
            and "donotclaim" not in ln.lower()]
    return "\n".join(keep)


def _tool_named_in(tool: str, text: str) -> bool:
    """Does the employer's text name this tool?

    Matches the tool's distinctive head word as well as its full name, because listings
    rarely write the product name in full: the Sony listing said "Substance", not
    "Substance Painter" -- which is precisely the entry that went unverified for months.
    A vault tool of "Substance Painter" must therefore match the bare word "Substance".
    """
    t = tool.lower().strip()
    if re.search(rf"\b{re.escape(t)}\b", text):
        return True
    head = t.split()[0]
    # Only trust a head word that is distinctive on its own (avoid 'after' from After Effects).
    GENERIC = {"after", "3d", "the", "adobe", "auto", "real"}
    if len(head) >= 5 and head not in GENERIC:
        return bool(re.search(rf"\b{re.escape(head)}\b", text))
    return False


def suspect(user: str, listing_path: Path = None) -> int:
    """SUSPECT: which vault entries look WRONG or STALE and should be re-confirmed?

    VALIDATE answers "is the vault well-formed?" and COVERAGE answers "does the vault cover
    THIS listing?" Neither asks the question that actually bit us: *is what the vault says
    still true?*

    Substance Painter sat `unverified` in BOTH vaults for months while both founders had five
    years of production experience with it. Nothing was malformed, so VALIDATE passed. It only
    surfaced on 2026-07-25 because a listing happened to name it and somebody asked. Maya and
    ZBrush were the same story in 2026-07-13, and the Colour X build surfaced four more.

    The pattern is always the same: a fact went stale, or was never confirmed, and there was no
    routine that would ever raise it again. This mode is that routine. It prints a ready-to-ask
    question list, ranked, so confirming is one message instead of an archaeology session.

    With a listing path, unverified tools the LISTING NAMES are promoted to URGENT -- that is
    exactly the Substance Painter case, caught mechanically instead of by luck.
    """
    vpath = vault_path(user)
    if not vpath.exists():
        _out(f"no vault at {vpath}")
        return 2

    errors, _w = check_vault(vpath)
    if errors:
        _out(f"\n{vpath}")
        for e in errors:
            _out(f"  ERROR  {e}")
        _out("\nFAIL: vault has schema errors -- fix those before auditing content.")
        return 1

    v = json.loads(vpath.read_text(encoding="utf-8"))
    listing_text = ""
    if listing_path:
        if not listing_path.exists():
            _out(f"no listing at {listing_path}")
            return 2
        raw = listing_path.read_text(encoding="utf-8")
        # ⚠ Match ONLY the employer's words. A finished listing doc also contains OUR analysis
        # -- the evidence map, the "Never claimed on this resume:" line, the prep notes -- which
        # name every tool we deliberately excluded. Scanning the whole file marks Houdini, Rhino,
        # and SketchUp as "the listing asks for this" purely because we wrote that we do NOT
        # claim them. Prefer the verbatim listing below the `---` fence when it is present.
        listing_text = _employer_text(raw).lower()

    urgent, unverified, undated, thin_note = [], [], [], []

    # 1. Unverified tools -- the Substance Painter class.
    for t in v.get("doNotClaim", {}).get("tools", []):
        if not isinstance(t, dict) or t.get("status") != "unverified":
            continue
        name = t.get("name", "?")
        if listing_text and _tool_named_in(name, listing_text):
            urgent.append(name)
        else:
            unverified.append(name)

    # 2. Claims with no date anywhere in `source` -- provenance we can no longer age.
    for sec in TRACKED_SECTIONS:
        for group, e in _iter_entries(v.get(sec, {})):
            src = str(e.get("source", ""))
            if not src:
                continue
            if not re.search(r"(19|20)\d{2}", src):
                undated.append(f"{sec}.{_label(e, group)}  (source: {src[:52]})")

    # 3. Tracks whose story is thin -- a resume there would be a toolbelt with no narrative.
    for t in sorted(k for k in v.get("roleTracks", {}) if not k.startswith("_")):
        depth, _tools = track_depth(v, t)
        if depth < THIN_TRACK:
            thin_note.append(f"{t} ({depth} narrative claims)")

    _out(f"\n{'=' * 78}")
    _out(f"  SUSPECT AUDIT  ·  {user}")
    if listing_path:
        _out(f"  listing: {listing_path}")
    _out(f"{'=' * 78}\n")
    _out("  Entries that may be WRONG or STALE. None of these are errors -- they are")
    _out("  QUESTIONS TO ASK before the next build. Confirming one permanently improves")
    _out("  every future application on that track.\n")

    if urgent:
        _out("!! URGENT -- THIS LISTING NAMES THESE, AND THEY ARE UNVERIFIED")
        _out("   Ask BEFORE building. This is the exact Substance Painter case:")
        _out("   'unverified' means NOBODY ASKED -- it does NOT mean they lack the skill.")
        for n in urgent:
            _out(f"   ??  {n}")
        _out("")

    if unverified:
        _out("-- UNVERIFIED TOOLS (nobody has asked; NOT gaps)")
        for n in unverified:
            _out(f"   ?   {n}")
        _out("")

    if undated:
        _out(f"-- UNDATED SOURCES ({len(undated)}) -- provenance cannot be aged")
        for u in undated[:12]:
            _out(f"   ·   {u}")
        if len(undated) > 12:
            _out(f"   ... and {len(undated) - 12} more")
        _out("")

    if thin_note:
        _out("-- THIN TRACKS (toolbelt, no story)")
        for t in thin_note:
            _out(f"   ·   {t}")
        _out("")

    total = len(urgent) + len(unverified)
    if not (urgent or unverified or undated or thin_note):
        _out("  Nothing suspect. Every tool has been asked about and every source is dated.\n")
        return 0

    _out(f"{'-' * 78}")
    if total:
        _out("  ASK THE APPLICANT, in one message:")
        names = ", ".join(urgent + unverified)
        _out(f'    "Do you have experience with any of these? {names}"')
        _out("")
        _out("  If YES -> write it into `skills` with source: \"owner directive <today>\",")
        _out("           move the ledger entry to `resolved` as `confirmed-have`, THEN use it.")
        _out("  If NO  -> set status `confirmed-absent` with an `askedOn` date. Only THEN")
        _out("           may it be treated as a gap.")
    _out(f"{'-' * 78}\n")

    # URGENT is a hard stop: the listing needs it and nobody has asked.
    return 1 if urgent else 0


def main(argv):
    _configure_stdout()

    if "--suspect" in argv:
        i = argv.index("--suspect")
        rest = [a for a in argv[i + 1:] if not a.startswith("-")]
        if not rest:
            _out("usage: --suspect <user> [listing.md]")
            return 2
        return suspect(rest[0], Path(rest[1]) if len(rest) > 1 else None)

    if "--explain" in argv:
        i = argv.index("--explain")
        rest = [a for a in argv[i + 1:] if not a.startswith("-")]
        if len(rest) < 2:
            _out("usage: --explain <user> <track>")
            return 2
        return explain(rest[0], rest[1], verbose="--verbose" in argv)

    if "--coverage" in argv:
        i = argv.index("--coverage")
        rest = [a for a in argv[i + 1:] if not a.startswith("-")]
        if len(rest) < 3:
            _out("usage: --coverage <user> <track> <listing.md>")
            return 2
        return coverage(rest[0], rest[1], Path(rest[2]))

    if "--all" in argv:
        vault_files = list(iter_vault_paths())
        if not vault_files:
            _out("no vaults under vaults/*.json or storage/*/resume-source.json")
            return 2
    else:
        vault_files = [resolve_rel(a) for a in argv if not a.startswith("-")]
    if not vault_files:
        _out(__doc__)
        return 2

    failed = 0
    for p in vault_files:
        errors, warnings = check_vault(p)
        _out(f"\n{p}")
        for e in errors:
            _out(f"  ERROR  {e}")
        for w in warnings:
            _out(f"  warn   {w}")
        if errors:
            failed += 1
        elif not warnings:
            _out("  OK")

    if failed:
        _out(f"\nFAIL: {failed} vault(s) have errors.")
        return 1
    _out("\nPASS: all vaults valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
