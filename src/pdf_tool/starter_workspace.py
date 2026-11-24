"""Write a gitignored starter person + vault + profile from a reviewed draft."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import date
from html import escape
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
STARTER_LAYOUTS = {"experience-first": "Experience first", "skills-first": "Skills first"}
# Letter width minus the two 0.65in print margins, at 96 CSS pixels per inch.
STARTER_CONTENT_WIDTH_PX = round((8.5 - 2 * 0.65) * 96)


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
                "bullets": [b for b in (row.get("bullets") or []) if str(b).strip()],
                "tracks": [track],
                "strength": "solid" if index == 1 else "supporting",
                "source": source,
                "confidence": "inferred",
            }
        )
    return jobs


ASSET_README = """# Your reusable document resources

Put this person's images (headshots, project shots, game art) in `images/`, brand marks in `logos/`,
reusable clips in `videos/`, and source CVs or owner-supplied notes in `references/`.
Résumé, work-samples, and letter templates reference media by relative path, for example
`<img src="../../resumes/<id>/resources/images/project-hero.webp">`, and
`python -m pdf_tool.inline_images --board <template>.html <out>.html` embeds them.
Prefer WebP or JPEG; keep 16:9 shots uncropped. Art shared by several people lives in
`resumes/studio/resources/images/<collection>/`. This folder is gitignored.
"""


def asset_dirs(slug: str) -> dict[str, str]:
    """Repo-relative resource folders for one person's career documents."""
    base = f"resumes/{slug}/resources"
    return {
        "root": f"{base}/",
        "images": f"{base}/images/",
        "logos": f"{base}/logos/",
        "videos": f"{base}/videos/",
        "references": f"{base}/references/",
    }


def build_user(draft: dict, slug: str) -> dict:
    name = (draft.get("displayName") or slug.replace("-", " ").title()).strip()
    dirs = asset_dirs(slug)
    return {
        "id": slug,
        "aliases": [slug],
        "name": name,
        "brand": f"{slug}-local",
        "pronouns": "",
        "created": date.today().isoformat(),
        "contact": {
            "email": (draft.get("email") or "").strip(),
            "phone": (draft.get("phone") or "").strip(),
            "web": (draft.get("web") or "").strip(),
            "github": "",
            "location": "",
            "signatureName": name,
            "signatureTitle": (draft.get("headline") or "").strip(),
        },
        "vault": f"../vaults/{slug}.json",
        "portfolio": {
            "_note": "ONE resource home for this person's career documents. Templates reference media "
            "by relative paths; inline_images embeds images for self-contained PDFs.",
            "imagesDir": dirs["images"],
            "logosDir": dirs["logos"],
            "videosDir": dirs["videos"],
            "referencesDir": dirs["references"],
            "sharedStudioImages": "resumes/studio/resources/images/<collection>/ (art shared by several people)",
        },
        "identity": {
            "headline": (draft.get("headline") or "").strip(),
            "summary": (draft.get("summary") or "").strip(),
            "company": "",
            "role": "",
            "voice": "Imported draft — replace with the person's real application voice.",
            "background": (draft.get("coverLetterNotes") or "")[:280],
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


def _resume_html(user: dict, vault: dict, layout: str, palette: dict, base_css: str) -> str:
    def content(value):
        return escape(str(value or ""))

    def section(title, body):
        return f"<section><h2>{title}</h2>{body}</section>" if body else ""

    def list_items(rows):
        return "<ul>" + "".join(f"<li>{content(row)}</li>" for row in rows) + "</ul>" if rows else ""

    name = content(user["name"])
    contact = user["contact"]
    contact_line = " · ".join(content(contact[key]) for key in ("email", "phone", "web") if contact[key])
    headline = content(user["identity"]["headline"])
    summary = content(user["identity"]["summary"])
    experience = section("Work experience", "".join(
        f"<article><h3>{content(job['role'])} · {content(job['org'])}</h3>"
        f"<p>{content(job['dates'])}</p><p>{content(job['summary'])}</p>"
        f"{list_items(job['bullets'])}</article>"
        for job in vault["employment"]
    ))
    skills = section("Skills", list_items([entry["claim"] for entry in vault["skills"]["imported"]]))
    education = section("Education", list_items([entry["claim"] for entry in vault["education"]]))
    first, second = (skills, experience) if layout == "skills-first" else (experience, skills)
    # Keep the document's standard paper, text contrast and geometry. Palette
    # tokens are limited to color values from the installed public presets.
    def colors(mode):
        return " ".join(
            f"{token}: {value};"
            for token, value in palette[mode].items()
            if token in {"--primary", "--secondary", "--accent", "--support"}
            and isinstance(value, str) and re.fullmatch(r"#[a-fA-F0-9]{6}", value)
        )

    def page(body, first_page=False):
        heading = "h1" if first_page else "h2"
        header = f"<{heading} class=\"resume-name\">{name}</{heading}>"
        if first_page:
            if headline:
                header += f"<p>Job title: {headline}</p>"
            if contact_line:
                header += f"<p>{contact_line}</p>"
        return (f'<div class="page"><div class="page-main"><header class="page-head">{header}</header>'
                f'{body}</div><footer class="page-sig">{name}</footer></div>')

    return f'''<!doctype html>
<html lang="en" data-starter-resume><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · Résumé</title>
<style>
{base_css}
html:not([data-theme="light"]) {{ {colors("dark")} }}
html[data-theme="light"] {{ {colors("light")} }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 14px/1.45 var(--ats-safe); overflow-wrap: anywhere; }}
.page {{ margin: 24px auto; background: var(--surface); }}
.page-head {{ margin-bottom: 24px; }}
.resume-name {{ font-size: 38px; color: var(--primary); line-height: 1.1; margin: 0 0 12px; }}
section {{ margin-bottom: 20px; }}
section h2 {{ font-size: 15px; margin: 0 0 10px; border-bottom: 1px solid var(--border2); }}
article {{ margin-bottom: 14px; }}
h3, p {{ margin: 0 0 4px; }}
ul {{ padding-inline-start: 20px; margin: 4px 0; }}
li {{ margin-block: 4px; }}
.page-sig {{ margin-top: auto; text-align: right; font-size: 12px; }}
@media print {{
  @page starter-dark {{ size: Letter; margin: 0.65in; background: #0b0d12; }}
  html:not([data-pdf-theme="dark"]) {{ {colors("light")} }}
  html[data-pdf-theme="dark"] {{ {colors("dark")} }}
  html[data-pdf-theme="dark"] body {{ page: starter-dark; }}
  .page {{ margin: 0; }}
  .page + .page {{ break-before: page; }}
}}
</style></head><body>
{page(section("Summary", f"<p>{summary}</p>" if summary else "") + first, first_page=True)}
{page(second + education)}
</body></html>
'''


def save_starter(
    workspace_root: Path,
    draft: dict,
    *,
    slug: str | None = None,
    overwrite: bool = False,
    template_root: Path | None = None,
    resume_options: dict | None = None,
) -> dict:
    root = Path(workspace_root).resolve()
    templates = Path(template_root) if template_root else root
    ident = normalize_slug(slug or draft.get("slug") or "")
    user_path = root / "users" / f"{ident}.json"
    vault_path = root / "vaults" / f"{ident}.json"
    profile_path = root / "profiles" / f"{ident}-resume.json"
    paths = {"user": user_path, "vault": vault_path, "profile": profile_path}
    if resume_options is not None:
        paths["resume"] = root / "resumes" / ident / f"{ident}-resume.html"
    if any(not path.resolve().is_relative_to(root) for path in paths.values()):
        raise ValueError("Choose a workspace folder inside PDF Designer.")
    existing = [p for p in paths.values() if p.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "Starter files already exist for "
            f"{ident}: {', '.join(p.as_posix() for p in existing)}. Pass overwrite to replace."
        )
    profile_template = _load_json(templates / "profiles" / "you-resume.example.json")
    user = build_user(draft, ident)
    vault = build_vault(draft, ident)
    profile = build_profile(ident, profile_template, user["name"])
    if resume_options is not None:
        if not (draft.get("displayName") or "").strip() or not (vault["employment"] or vault["skills"]["imported"] or vault["education"]):
            raise ValueError("Add your name and at least one job, skill or education entry.")
        layout = resume_options.get("layout")
        palette_id = resume_options.get("palette")
        if layout not in STARTER_LAYOUTS or not isinstance(palette_id, str) or not _SLUG_RE.fullmatch(palette_id):
            raise ValueError("Choose an available résumé layout and palette.")
        palette_path = templates / "themes" / "presets" / f"{palette_id}.json"
        if not palette_path.is_file():
            raise ValueError("Choose an available résumé palette.")
        palette = _load_json(palette_path)["tokens"]
        profile["theme"]["preset"] = palette_id
        profile["layout"]["variant"] = layout
        profile["source"] = f"../{paths['resume'].relative_to(root).as_posix()}"
        resume = _resume_html(user, vault, layout, palette, (templates / "themes/default-resume.css").read_text(encoding="utf-8"))

    dirs = asset_dirs(ident)
    if any(not (root / directory).resolve().is_relative_to(root) for directory in dirs.values()):
        raise ValueError("Choose resource folders inside PDF Designer.")
    for key in ("images", "logos", "videos", "references"):
        (root / dirs[key]).mkdir(parents=True, exist_ok=True)
    readme = root / dirs["root"] / "README.md"
    if not readme.exists():
        readme.write_text(ASSET_README.replace("<id>", ident), encoding="utf-8")
    payloads = {key: json.dumps(value, indent=2, ensure_ascii=False) + "\n"
                for key, value in (("user", user), ("vault", vault), ("profile", profile))}
    if resume_options is not None:
        payloads["resume"] = resume
    written = []
    try:
        for key, path in paths.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w" if overwrite else "x", encoding="utf-8") as file:
                written.append(path)
                file.write(payloads[key])
    except OSError:
        if not overwrite:
            for path in written:
                path.unlink(missing_ok=True)
        raise
    return {
        "ok": True,
        "slug": ident,
        "files": {key: path.as_posix() for key, path in paths.items()},
        "assets": dirs,
        "warnings": list(draft.get("warnings") or []),
        "vaultHref": f"/vault?profile={ident}",
        **({"resumePath": paths["resume"].relative_to(root).as_posix()} if resume_options is not None else {}),
    }
