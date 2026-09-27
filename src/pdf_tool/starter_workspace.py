"""Write a gitignored starter person + vault + profile from a reviewed draft."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import date
from pathlib import Path

RESERVED_SLUGS = frozenset(
    {
        "examples",
        "example",
        "jane",
        "jane-example",
        "you",
        "readme",
        "default",
        "default-resume",
    }
)
_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}$")


def normalize_slug(value: str) -> str:
    slug = (value or "").strip().lower()
    if not _SLUG_RE.fullmatch(slug) or slug in RESERVED_SLUGS:
        raise ValueError(
            f"Choose a workspace id like alex or alex-rivera — not {value!r} "
            "(reserved names: examples, you)."
        )
    return slug


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _skill_entries(draft: dict, track: str, source: str) -> list[dict]:
    entries = []
    for index, row in enumerate(draft.get("skills") or [], start=1):
        claim = (row.get("claim") if isinstance(row, dict) else str(row) or "").strip()
        if not claim:
            continue
        sid = f"sk-imported-{index:02d}"
        entries.append(
            {
                "id": sid,
                "claim": claim,
                "strength": "supporting",
                "tracks": [track],
                "source": source,
                "confidence": "inferred",
            }
        )
    return entries


def _jobs(draft: dict, track: str, source: str) -> list[dict]:
    jobs = []
    for index, row in enumerate(draft.get("jobs") or [], start=1):
        if not isinstance(row, dict):
            continue
        org = (row.get("org") or "").strip()
        role = (row.get("role") or "").strip()
        if not org and not role:
            continue
        jobs.append(
            {
                "id": f"emp-imported-{index:02d}",
                "org": org or "Unknown organization",
                "role": role or "Role (review)",
                "dates": (row.get("dates") or "").strip() or "dates unknown — review",
                "summary": (row.get("summary") or "").strip(),
                "bullets": [b for b in (row.get("bullets") or []) if str(b).strip()][:8],
                "tracks": [track],
                "strength": "solid" if index == 1 else "supporting",
                "source": source,
                "confidence": "inferred",
            }
        )
    return jobs


ASSET_README = """# Your images and logos

Put this person's images (headshots, project shots, game art) in `images/` and logos in `logos/`.
Work-samples and letter templates reference them by relative path, for example
`<img src="../../resumes/<id>/resources/images/project-hero.webp">`, and
`python -m pdf_tool.inline_images --board <template>.html <out>.html` embeds them.
Prefer WebP or JPEG; keep 16:9 shots uncropped. Art shared by several people lives in
`resumes/studio/resources/images/<collection>/`. This folder is gitignored.
"""


def asset_dirs(slug: str) -> dict[str, str]:
    """Repo-relative asset folders for one person — the single image/logo SSOT."""
    base = f"resumes/{slug}/resources"
    return {"root": f"{base}/", "images": f"{base}/images/", "logos": f"{base}/logos/"}


def build_user(draft: dict, slug: str) -> dict:
    name = (
        draft.get("displayName")
        or draft.get("displayName")
        or slug.replace("-", " ").title()
    ).strip()
    return {
        "id": slug,
        "aliases": [slug],
        "name": name,
        "brand": f"{slug}-local",
        "pronouns": "",
        "created": date.today().isoformat(),
        "contact": {
            "email": (draft.get("email") or "").strip(),
            "web": (draft.get("web") or draft.get("web") or "").strip(),
            "github": "",
            "location": "",
            "signatureName": name,
            "signatureTitle": (draft.get("headline") or "").strip(),
        },
        "vault": f"../vaults/{slug}.json",
        "portfolio": {
            "_note": "ONE place for this person's images and logos. Templates reference these files "
            "by relative <img src> path; inline_images embeds them for self-contained PDFs.",
            "imagesDir": asset_dirs(slug)["images"],
            "logosDir": asset_dirs(slug)["logos"],
            "sharedStudioImages": "resumes/studio/resources/images/<collection>/ (art shared by several people)",
        },
        "identity": {
            "headline": (draft.get("headline") or "").strip(),
            "company": "",
            "role": "",
            "voice": "Imported draft — replace with the person's real application voice.",
            "background": (draft.get("coverLetterNotes") or draft.get("coverLetterNotes") or "")[:280],
        },
        "_imported": {
            "warning": "Starter files from a local résumé parse. Every claim is inferred until reviewed.",
            "source": draft.get("source"),
            "files": draft.get("filenames") or [],
        },
    }


def build_vault(draft: dict, slug: str) -> dict:
    source = draft.get("source") or f"imported local résumé {date.today().isoformat()}"
    track = "imported"
    skills = _skill_entries(draft, track, source)
    jobs = _jobs(draft, track, source)
    education = []
    for index, row in enumerate(draft.get("education") or [], start=1):
        claim = (row.get("claim") if isinstance(row, dict) else str(row) or "").strip()
        if not claim:
            continue
        education.append(
            {
                "id": f"edu-imported-{index:02d}",
                "claim": claim,
                "tracks": ["any"],
                "strength": "supporting",
                "source": source,
                "confidence": "inferred",
            }
        )
    track_body = {
        "covers": "Imported from a local résumé. Replace this track id when you know the real job family.",
        "angle": {
            "leadWith": [
                job.get("summary") or job.get("role")
                for job in jobs[:2]
                if job.get("summary") or job.get("role")
            ]
            or ["Review inferred claims before any application export."],
            "demote": ["Anything the parser guessed that you cannot source."],
        },
        "toolbeltOrder": [],
        "goToResume": None,
    }
    tags = []
    for skill in skills[:16]:
        tags.append(
            {
                "label": skill["claim"][:40],
                "group": "imported",
                "mapsTo": skill["id"],
            }
        )
    cover_note = (draft.get("coverLetterNotes") or draft.get("coverLetterNotes") or "").strip()
    tracks = {track: deepcopy(track_body)}
    skill_groups = {"imported": deepcopy(skills)}
    jobs_body = deepcopy(jobs)
    vault = {
        "_meta": {
            "schema": "vault/v2",
            "whatThisIs": (
                f"STARTER vault for {slug} parsed from a local file. "
                "Inferred claims are not yet verified. Edit before any job-board export."
            ),
            "imported": True,
            "source": source,
        },
        "roleTracks": tracks,
        "voice": {
            "person": "First person until you edit this.",
            "tone": "Replace with the real application voice.",
            "personality": "Imported draft.",
            "resume": "Claim-dense after you verify the inferred rows.",
            "coverLetter": cover_note[:400] or "Imported cover-letter notes live in identity.background until you rewrite voice.",
            "avoid": ["Exporting inferred claims without review"],
        },
        "boardSkills": {"lastUpdated": date.today().isoformat(), "tags": tags},
        "software": {"_note": "PROGRAM roster — add real tools after review.", "programs": []},
        "goToPacks": {},
        "skills": skill_groups,
        "employment": jobs_body,
        "education": education,
        "doNotClaim": {"tools": []},
        "importedCoverLetter": cover_note,
        "warnings": list(draft.get("warnings") or []),
    }
    # Hub overview reads the Jane-shaped keys; check_vault reads the protocol keys.
    vault["roleTracks"] = tracks
    vault["skills"] = skill_groups
    vault["employment"] = jobs_body
    return vault


def build_profile(slug: str, template: dict, name: str) -> dict:
    profile = deepcopy(template)
    profile["id"] = f"{slug}-resume"
    profile["name"] = f"{name} — local starter profile"
    profile["status"] = "local-draft"
    profile["lastUpdated"] = date.today().isoformat()
    profile["user"] = f"../users/{slug}.json"
    profile["vault"] = f"../vaults/{slug}.json"
    profile["privacy"] = {
        "tracked": False,
        "reason": "Starter profile from a local résumé import. Gitignored.",
    }
    exports = profile.get("exports") if isinstance(profile.get("exports"), dict) else {}
    exports["dir"] = f"../resumes/{slug}/"
    profile["exports"] = exports
    return profile


def save_starter(
    workspace_root: Path,
    draft: dict,
    *,
    slug: str | None = None,
    overwrite: bool = False,
    template_root: Path | None = None,
) -> dict:
    root = Path(workspace_root)
    templates = Path(template_root) if template_root else root
    ident = normalize_slug(slug or draft.get("slug") or "")
    user_path = root / "users" / f"{ident}.json"
    vault_path = root / "vaults" / f"{ident}.json"
    profile_path = root / "profiles" / f"{ident}-resume.json"
    existing = [p for p in (user_path, vault_path, profile_path) if p.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "Starter files already exist for "
            f"{ident}: {', '.join(p.as_posix() for p in existing)}. Pass overwrite to replace."
        )
    profile_template = _load_json(templates / "profiles" / "you-resume.example.json")
    user = build_user(draft, ident)
    vault = build_vault(draft, ident)
    profile = build_profile(ident, profile_template, user["name"])
    _dump(user_path, user)
    _dump(vault_path, vault)
    _dump(profile_path, profile)
    dirs = asset_dirs(ident)
    for key in ("images", "logos"):
        (root / dirs[key]).mkdir(parents=True, exist_ok=True)
    readme = root / dirs["root"] / "README.md"
    if not readme.exists():
        readme.write_text(ASSET_README.replace("<id>", ident), encoding="utf-8")
    return {
        "ok": True,
        "slug": ident,
        "files": {
            "user": user_path.as_posix(),
            "vault": vault_path.as_posix(),
            "profile": profile_path.as_posix(),
        },
        "assets": dirs,
        "warnings": list(draft.get("warnings") or []),
        "vaultHref": f"/vault?profile={ident}",
    }
