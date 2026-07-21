"""Application tracker — list/status over existing application.json files.

Scans ``storage/_job-listings/**/application.json`` (gitignored workspace).
No separate SSOT: the per-job application records already hold company, role,
track, status, apply URL, and pay.

Usage:
    python -m pdf_tool.tracker list
    python -m pdf_tool.tracker status
    python -m pdf_tool.tracker status SUBMITTED
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_APPS = _REPO / "storage" / "_job-listings"


def _load_jobs() -> list[dict]:
    jobs = []
    if not _APPS.is_dir():
        return jobs
    for path in sorted(_APPS.glob("**/application.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            jobs.append({
                "id": path.parent.name,
                "company": "?",
                "role": "?",
                "track": "?",
                "status": f"UNREADABLE ({e})",
                "applyUrl": None,
                "pay": None,
                "updated": None,
                "path": str(path.relative_to(_REPO)).replace("\\", "/"),
            })
            continue

        links = data.get("links") if isinstance(data.get("links"), dict) else {}
        terms = data.get("terms") if isinstance(data.get("terms"), dict) else {}
        meta = data.get("_meta") if isinstance(data.get("_meta"), dict) else {}
        folder = path.parent.name
        jobs.append({
            "id": folder,
            "company": data.get("company") or folder,
            "role": data.get("roleTitle") or data.get("role") or "",
            "track": data.get("track") or folder,
            "status": data.get("status") or "UNKNOWN",
            "applyUrl": links.get("applyUrl"),
            "pay": terms.get("pay"),
            "updated": meta.get("lastUpdated") or meta.get("created"),
            "path": str(path.relative_to(_REPO)).replace("\\", "/"),
        })
    return jobs


def cmd_list(jobs: list[dict]) -> int:
    if not jobs:
        print(f"no application.json under {_APPS.relative_to(_REPO)}/")
        print("Copy examples/_job-listings/example-application/ into storage/_job-listings/<Track>/")
        return 0
    print(f"{'STATUS':<28} {'COMPANY':<22} {'ROLE':<36} TRACK")
    print("-" * 100)
    for j in jobs:
        role = (j["role"] or "")[:34]
        company = (j["company"] or "")[:20]
        status = (j["status"] or "")[:26]
        print(f"{status:<28} {company:<22} {role:<36} {j['track']}")
    print(f"\n{len(jobs)} application(s)")
    return 0


def cmd_status(jobs: list[dict], filter_status: str | None = None) -> int:
    if filter_status:
        needle = filter_status.lower()
        jobs = [j for j in jobs if needle in (j["status"] or "").lower()]
        if not jobs:
            print(f"no applications matching status ~ {filter_status!r}")
            return 0
        return cmd_list(jobs)

    if not jobs:
        print(f"no application.json under {_APPS.relative_to(_REPO)}/")
        return 0

    counts = Counter(j["status"] or "UNKNOWN" for j in jobs)
    print("STATUS BREAKDOWN")
    print("-" * 40)
    for status, n in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {n:3}  {status}")
    print(f"\n{len(jobs)} total")
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
