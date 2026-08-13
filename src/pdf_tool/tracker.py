"""Application tracker — who sent which résumé to which job.

Scans ``_job-apps/**/application.json`` (aliases: ``applications/``,
``storage/_job-listings/``). This is **not** a daily count of submissions.
The human log is ``_job-apps/applied-index.md`` (who × job × outcome). Do not
treat ``N SUBMITTED`` as a standing check.

Usage:
    python -m pdf_tool.tracker list
    python -m pdf_tool.tracker status
    python -m pdf_tool.tracker status jenni
"""

from __future__ import annotations

import json
import sys

from .paths import iter_application_json, repo_root

_REPO = repo_root()
_APPLICANTS = ("jenni", "shade")


def _applicant_cell(data: dict, user: str) -> str:
    """Return a short who-sent cell: ``sent YYYY-MM-DD``, ``sent``, ``not sent``, or ``—``."""
    sub = data.get("submission")
    if isinstance(sub, dict):
        rec = sub.get(user)
        if isinstance(rec, dict):
            if rec.get("submitted") is True:
                date = (rec.get("date") or "").strip()
                return f"sent {date}" if date else "sent"
            if rec.get("submitted") is False:
                return "not sent"

    apps = data.get("applicants")
    if isinstance(apps, list):
        for rec in apps:
            if not isinstance(rec, dict) or rec.get("user") != user:
                continue
            nested = rec.get("submitted")
            if nested is True or str(rec.get("status") or "").upper() == "SUBMITTED":
                date = (rec.get("submittedOn") or rec.get("date") or "").strip()
                return f"sent {date}" if date else "sent"
            if isinstance(nested, dict) and nested.get("submitted") is True:
                date = (nested.get("date") or rec.get("submittedOn") or "").strip()
                return f"sent {date}" if date else "sent"

    if data.get("bothApplicantsSubmitted") is True:
        date = (data.get("submittedOn") or "").strip()
        return f"sent {date}" if date else "sent"

    if data.get("submittedBy") == user or data.get("applicant") == user:
        status_u = str(data.get("status") or "").upper()
        if "SUBMIT" in status_u or data.get("submittedOn"):
            date = (data.get("submittedOn") or "").strip()
            return f"sent {date}" if date else "sent"

    if str(data.get("status") or "").upper() == "SUBMITTED" and isinstance(apps, list):
        named = [r.get("user") for r in apps if isinstance(r, dict) and r.get("user")]
        if named == [user]:
            date = (data.get("submittedOn") or "").strip()
            return f"sent {date}" if date else "sent"

    status = (data.get("status") or "").upper()
    uname = user.upper()
    if uname in status and "SUBMIT" in status:
        return "sent"
    return "—"


def _load_jobs() -> list[dict]:
    jobs = []
    for path in iter_application_json(root=_REPO):
        try:
            rel_parent = path.parent.relative_to(_REPO).as_posix()
        except ValueError:
            rel_parent = path.parent.name
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            jobs.append({
                "id": path.parent.name,
                "company": "?",
                "role": "?",
                "jenni": "UNREADABLE",
                "shade": "UNREADABLE",
                "outcome": str(e),
                "path": rel_parent,
            })
            continue

        outcome = data.get("outcome") or data.get("statusNote") or ""
        if isinstance(outcome, str):
            outcome = outcome.replace("\n", " ").strip()
        else:
            outcome = ""

        jobs.append({
            "id": path.parent.name,
            "company": data.get("company") or path.parent.name,
            "role": data.get("roleTitle") or data.get("role") or "",
            "jenni": _applicant_cell(data, "jenni"),
            "shade": _applicant_cell(data, "shade"),
            "outcome": outcome[:60],
            "path": rel_parent,
        })
    return jobs


def cmd_list(jobs: list[dict]) -> int:
    if not jobs:
        print("no application.json under _job-apps/ (aliases: applications/, storage/_job-listings/)")
        print(
            "Copy examples/_job-listings/example-application/ into "
            "_job-apps/<Track>/  ·  human log: _job-apps/applied-index.md"
        )
        return 0
    print(f"{'JOB':<28} {'JENNI':<18} {'SHADE':<18} ROLE")
    print("-" * 100)
    for j in jobs:
        role = (j["role"] or j["company"] or "")[:34]
        print(f"{j['id']:<28} {j['jenni']:<18} {j['shade']:<18} {role}")
    print("\nHuman log (who × job × outcome): _job-apps/applied-index.md")
    print("Do not count submissions as a daily check — update a row when someone sends, or when they hear back.")
    return 0


def cmd_status(jobs: list[dict], filter_who: str | None = None) -> int:
    if not jobs:
        print("no application.json under _job-apps/ (aliases: applications/, storage/_job-listings/)")
        return 0

    who = (filter_who or "").strip().lower()
    if who and who not in _APPLICANTS:
        # Treat unknown filter as a job-folder / company substring (not a count).
        needle = who
        jobs = [
            j for j in jobs
            if needle in (j["id"] or "").lower()
            or needle in (j["company"] or "").lower()
            or needle in (j["role"] or "").lower()
        ]
        if not jobs:
            print(f"no jobs matching {filter_who!r}")
            return 0
        return cmd_list(jobs)

    people = (who,) if who in _APPLICANTS else _APPLICANTS
    for user in people:
        print(user.upper())
        sent = [j for j in jobs if str(j.get(user, "")).startswith("sent")]
        pending = [j for j in jobs if j.get(user) == "not sent"]
        other = [
            j for j in jobs
            if not str(j.get(user, "")).startswith("sent") and j.get(user) != "not sent"
        ]
        print("  sent:")
        if sent:
            for j in sent:
                print(f"    {j['id']:<28} {j[user]}")
        else:
            print("    (none recorded)")
        print("  not sent:")
        if pending:
            for j in pending:
                print(f"    {j['id']}")
        else:
            print("    (none recorded)")
        if other:
            print("  other / unknown:")
            for j in other:
                print(f"    {j['id']:<28} {j[user]}")
        print()
    print("Human log: _job-apps/applied-index.md  ·  tell the agent when there is a response.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2 if not args else 0

    cmd = args[0].lower()
    jobs = _load_jobs()
    if cmd == "list":
        return cmd_list(jobs)
    if cmd == "status":
        filt = args[1] if len(args) > 1 else None
        return cmd_status(jobs, filt)
    print(f"unknown command: {cmd}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
