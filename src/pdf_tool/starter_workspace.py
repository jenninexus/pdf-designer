"""Write a gitignored starter person + vault + profile from a reviewed draft."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import date
from html import escape
from pathlib import Path

from .check_palette import classify
from .paths import brand_dirs

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
STARTER_HEADING_CASES = ("as-written", "uppercase")
# Letter width minus the two 0.65in print margins, at 96 CSS pixels per inch.
STARTER_CONTENT_WIDTH_PX = round((8.5 - 2 * 0.65) * 96)
_BRAND_ROLES = ("--bg", "--text", "--primary", "--secondary", "--accent", "--support")
_HEX_COLOR = re.compile(r"#[0-9a-fA-F]{6}")


def _brand_tokens(data):
    modes = data.get("tokens") if isinstance(data, dict) else None
    if not isinstance(modes, dict):
        raise ValueError("Use a palette JSON with tokens.light and tokens.dark.")
    result = {}
    for mode in ("light", "dark"):
        colors = modes.get(mode)
        if not isinstance(colors, dict):
            raise ValueError(f"Add {mode} colors to the palette.")
        result[mode] = {}
        for role in _BRAND_ROLES:
            value = colors.get(role)
            if not isinstance(value, str) or not _HEX_COLOR.fullmatch(value):
                raise ValueError(f"{mode.title()} {role} needs a six-digit hex color.")
            verdict, label = classify(value[1:])
            if verdict == "banned":
                raise ValueError(f"{mode.title()} {role} uses an excluded color ({label}).")
            result[mode][role] = value.lower()
    return result


def save_brand_palette(root: Path, payload: dict) -> str:
    name = payload.get("filename")
    if not isinstance(name, str) or not name.lower().endswith(".json"):
        raise ValueError("Choose a brand palette JSON file.")
    stem = re.sub(r"[^a-z0-9-]+", "-", name[:-5].lower()).strip("-")
    ident = ("brand-" + stem.removeprefix("brand-"))[:32].rstrip("-")
    if ident == "brand":
        raise ValueError("Give the palette file a name before loading it.")
    data = payload.get("palette")
    tokens = _brand_tokens(data)
    metadata = data.get("_meta")
    title = metadata.get("name") if isinstance(metadata, dict) else None
    if not isinstance(title, str) or not title.strip():
        title = ident.removeprefix("brand-").replace("-", " ").title()
    brand_root = root / "brands"
    if not brand_root.resolve().is_relative_to(root.resolve()) or brand_root.is_symlink():
        raise ValueError("Use the local workspace's brands folder.")
    brand_root.mkdir(exist_ok=True)
    target = brand_root / f"{ident}.json"
    try:
        with target.open("x", encoding="utf-8") as handle:
            json.dump({"_meta": {"name": title.strip()[:80]}, "tokens": tokens}, handle, indent=2)
            handle.write("\n")
    except FileExistsError as exc:
        if target.is_symlink() or not target.resolve().is_relative_to(brand_root.resolve()):
            raise ValueError("Choose an unused palette filename.") from exc
        if _load_json(target).get("tokens") != tokens:
            raise ValueError("That palette filename already exists. Rename the import to keep both.") from exc
    return ident


def _private_brand_path(root: Path, palette_id: str) -> Path | None:
    if not palette_id.startswith("brand-"):
        return None
    for folder in brand_dirs(root=root):
        target = folder / f"{palette_id}.json"
        if target.is_file() and target.resolve().is_relative_to(root.resolve()):
            return target
    return None


def starter_brand_available(root: Path, palette_id: str) -> bool:
    path = _private_brand_path(root, palette_id)
    if path is None:
        return False
    try:
        _brand_tokens(_load_json(path))
    except (OSError, ValueError):
        return False
    return True


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


def _resume_html(
    user: dict, vault: dict, layout: str, palette: dict, base_css: str, *,
    heading_case: str, page_cap: int, gradient: bool = False,
) -> str:
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
    summary_section = section("Summary", f"<p>{summary}</p>" if summary else "")
    first_page_body = summary_section + first
    second_page_body = second + education
    # Keep the document's standard paper, text contrast and geometry. Palette
    # tokens are limited to validated accent colors.
    def colors(mode):
        return " ".join(
            f"{token}: {value};"
            for token, value in palette[mode].items()
            if token in {"--primary", "--secondary", "--accent", "--support"}
            and isinstance(value, str) and re.fullmatch(r"#[a-fA-F0-9]{6}", value)
        )

    finish = """
html:not([data-theme="light"]) .page {
  background-image: linear-gradient(140deg, transparent 35%, color-mix(in srgb, var(--surface) 92%, var(--accent)));
}
@media print {
  html:not([data-pdf-theme="dark"]) .page { background-image: none; }
  html[data-pdf-theme="dark"] .page {
    background-image: linear-gradient(140deg, transparent 35%, color-mix(in srgb, var(--surface) 92%, var(--accent)));
  }
}
""" if gradient else ""

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

    if page_cap == 1:
        pages = page(first_page_body + second_page_body, first_page=True)
    else:
        pages = page(first_page_body, first_page=True) + page(second_page_body)
    heading_style = "h1, h2, h3 { text-transform: uppercase; }" if heading_case == "uppercase" else ""

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
{heading_style}
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
{finish}
</style></head><body>
{pages}
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
        if (
            not isinstance(layout, str) or layout not in STARTER_LAYOUTS
            or not isinstance(palette_id, str) or not _SLUG_RE.fullmatch(palette_id)
        ):
            raise ValueError("Choose an available résumé layout and palette.")
        layout_prefs = profile.setdefault("layoutPrefs", {})
        max_pages = layout_prefs.setdefault(
            "maxPages", {"coverLetter": 1, "resume": 2, "workSamples": 2, "packet": 5}
        )
        heading_case = resume_options.get("headingCase", layout_prefs.get("headingCase", "as-written"))
        page_cap = resume_options.get("resumeMaxPages", max_pages.get("resume", 2))
        if heading_case not in STARTER_HEADING_CASES or type(page_cap) is not int or page_cap not in (1, 2):
            raise ValueError("Choose a heading style and a one- or two-page résumé.")
        palette_path = templates / "themes" / "presets" / f"{palette_id}.json"
        private_brand = _private_brand_path(root, palette_id)
        if private_brand is not None:
            palette_path = private_brand
        if palette_id == "default-resume":
            palette = {"light": {}, "dark": {}}
        elif not palette_path.is_file():
            raise ValueError("Choose an available résumé palette.")
        else:
            data = _load_json(palette_path)
            palette = _brand_tokens(data) if private_brand else data["tokens"]
        profile["theme"]["preset"] = palette_id
        gradient = resume_options.get("subtleGradient") is True
        if gradient:
            profile["theme"]["subtleGradient"] = True
        profile["layout"]["variant"] = layout
        profile["layout"]["pages"] = page_cap
        layout_prefs["headingCase"] = heading_case
        max_pages["resume"] = page_cap
        profile["source"] = f"../{paths['resume'].relative_to(root).as_posix()}"
        base_css = (templates / "themes/default-resume.css").read_text(encoding="utf-8")
        resume = _resume_html(
            user, vault, layout, palette, base_css, heading_case=heading_case, page_cap=page_cap,
            gradient=gradient,
        )

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
