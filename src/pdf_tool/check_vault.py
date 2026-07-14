"""Vault guard -- validate a claim vault before anyone writes a resume from it.

The vault is the single source of truth for what a person may truthfully claim.
Nothing validated it, so a typo failed SILENTLY at resume-authoring time: a claim
tagged with a track that does not exist is simply never selected, and the resume
comes out quietly missing its best evidence. Nobody sees an error -- they just get
a worse resume.

What it checks
  1. Every claim has `source` and `confidence`  -- source-backed only, no exceptions.
  2. Every `tracks` entry names a track that actually exists in `roleTracks`.
     (Or `any`.)  A typo'd track is invisible, not loud -- this makes it loud.
  3. Every `strength` is lead | solid | supporting.
  4. Every role track carries an `angle` -- otherwise /make-resume has no framing.
  5. `doNotClaim.tools` is a VERIFICATION LEDGER, not a blocklist: every entry needs
     a `status`. Anything `unverified` is reported as MUST-ASK, never as a gap.
     (This is the Maya/ZBrush failure, encoded as a check.)
  6. No claim ID is duplicated.

Usage:
    python -m pdf_tool.check_vault storage/jenni/resume-source.json
    python -m pdf_tool.check_vault --all          # every vault under storage/

Exits non-zero on any error. Warnings (e.g. unverified tools) do not fail the run
-- they are reported so you know what to ask about.
"""

import json
import sys
from pathlib import Path

STRENGTHS = {"lead", "solid", "supporting"}
STATUSES = {"unverified", "confirmed-absent", "confirmed-have"}


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

    # (4) every track needs an angle -- the framing /make-resume reads
    for t in sorted(tracks):
        spec = v["roleTracks"][t]
        if not isinstance(spec, dict):
            errors.append(f"roleTracks.{t}: must be an object with `covers` + `angle`")
        elif "angle" not in spec:
            errors.append(f"roleTracks.{t}: missing `angle` (leadWith/demote) -- /make-resume has no framing for this track")

    # (1)(2)(3)(6) claims
    seen_ids = {}
    for group, claims in v.get("skills", {}).items():
        if group.startswith("_") or not isinstance(claims, list):
            continue
        for c in claims:
            cid = c.get("id", "<no id>")
            where = f"skills.{group}.{cid}"

            if cid in seen_ids:
                errors.append(f"{where}: duplicate claim id (also in {seen_ids[cid]})")
            seen_ids[cid] = where

            if not c.get("source"):
                errors.append(f"{where}: missing `source` -- source-backed only")
            if not c.get("confidence"):
                errors.append(f"{where}: missing `confidence`")

            st = c.get("strength")
            if st not in STRENGTHS:
                errors.append(f"{where}: strength {st!r} not in {sorted(STRENGTHS)}")

            ct = c.get("tracks")
            if not ct:
                errors.append(f"{where}: missing `tracks` -- it will never be selected")
            else:
                for t in ct:
                    if t != "any" and t not in tracks:
                        errors.append(
                            f"{where}: tracks has {t!r}, which is not a real track "
                            f"-- this claim is INVISIBLE. Real tracks: {sorted(tracks)}"
                        )

    # (5) the verification ledger -- the Maya/ZBrush check
    dnc = v.get("doNotClaim", {})
    tools = dnc.get("tools", [])
    unverified = []
    for t in tools:
        if isinstance(t, str):
            errors.append(
                f"doNotClaim.tools: {t!r} is a bare string. It MUST be an object with a "
                f"`status` -- a flat blocklist cannot tell 'nobody asked' from 'she doesn't "
                f"have it', which is exactly how Maya and ZBrush got wrongly forbidden."
            )
            continue
        name, status = t.get("name", "?"), t.get("status")
        if status not in STATUSES:
            errors.append(f"doNotClaim.tools.{name}: status {status!r} not in {sorted(STATUSES)}")
        elif status == "unverified":
            unverified.append(name)
        elif status == "confirmed-have":
            errors.append(f"doNotClaim.tools.{name}: status is `confirmed-have` -- move it to `skills`")

    if unverified:
        warnings.append(
            f"{len(unverified)} tool(s) are UNVERIFIED -- nobody has asked about them. "
            f"They are NOT gaps and must not be written off in an application: "
            f"{', '.join(unverified)}"
        )

    return errors, warnings


def main(argv):
    if "--all" in argv:
        paths = sorted(Path("storage").glob("*/resume-source.json"))
        if not paths:
            print("no vaults found under storage/*/resume-source.json")
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
            print(f"  ask    {w}")
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
