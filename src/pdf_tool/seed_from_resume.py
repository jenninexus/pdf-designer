"""Heuristic local extract: old résumé / cover-letter bytes → a starter vault draft.

No network. No model. Every claim is inferred until a human edits it.
"""

from __future__ import annotations

import base64
import re
from datetime import date
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

MAX_IMPORT_BYTES = 2_000_000
ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm"}

_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
_URL = re.compile(r"https?://[^\s)>\]]+", re.I)
_PHONE = re.compile(
    r"(?<!\w)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]*)\d{3}[\s.-]?\d{4}(?!\w)"
)
_YEAR_SPAN = re.compile(
    r"(?:19|20)\d{2}\s*[-–—]\s*(?:(?:19|20)\d{2}|present|current|now)",
    re.I,
)
_SECTION = re.compile(
    r"^(?:"
    r"experience|work experience|employment|professional experience|"
    r"education|academic|"
    r"skills|technical skills|core skills|competencies|"
    r"summary|profile|objective|about|"
    r"cover letter"
    r")\s*:?\s*$",
    re.I,
)
_COVER_HINT = re.compile(r"cover\s*letter|^dear\b", re.I)
_BULLET = re.compile(r"^\s*(?:[-*•●▪]|\d+[.)])\s+(.*\S)\s*$")
_JOB_LINE = re.compile(
    r"^(?P<left>.+?)\s+(?:[\u2014\u2013\-|]| at )\s+(?P<right>.+)$",
    re.I,
)


def slugify(value: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:32]


def extract_text(filename: str, payload: bytes) -> str:
    suffix = Path(filename or "upload.txt").suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(BytesIO(payload))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    return payload.decode("utf-8", errors="replace")


def _clean_lines(text: str) -> list[str]:
    lines = []
    for raw in (text or "").replace("\r", "").split("\n"):
        line = re.sub(r"\s+", " ", raw).strip()
        if line:
            lines.append(line)
    return lines


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "header": [],
        "summary": [],
        "experience": [],
        "education": [],
        "skills": [],
        "other": [],
    }
    current = "header"
    for line in lines:
        if _SECTION.match(line):
            key = line.lower()
            if "educat" in key:
                current = "education"
            elif "skill" in key or "competenc" in key:
                current = "skills"
            elif "experience" in key or "employment" in key:
                current = "experience"
            elif "cover" in key:
                current = "other"
            else:
                current = "summary"
            continue
        buckets[current].append(line)
    return buckets


def _guess_name(header: list[str]) -> str:
    for line in header[:6]:
        if _EMAIL.search(line) or _URL.search(line) or _PHONE.search(line):
            continue
        if _SECTION.match(line):
            continue
        words = line.split()
        if 2 <= len(words) <= 5 and line[0].isalpha() and len(line) < 60:
            return line
    return ""


def _parse_skills(lines: list[str]) -> list[str]:
    found: list[str] = []
    for line in lines:
        for chunk in re.split(r"[,;|/•]+", line):
            skill = chunk.strip(" -")
            if 1 < len(skill) < 48 and not _EMAIL.search(skill):
                found.append(skill)
    seen: set[str] = set()
    out: list[str] = []
    for skill in found:
        key = skill.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(skill)
    return out[:24]


def _parse_jobs(lines: list[str]) -> list[dict]:
    jobs: list[dict] = []
    current: dict | None = None
    for line in lines:
        dates = _YEAR_SPAN.search(line)
        job_match = _JOB_LINE.match(line)
        bullet = _BULLET.match(line)
        if job_match and not bullet:
            if current:
                jobs.append(current)
            left, right = job_match.group("left").strip(), job_match.group("right").strip()
            current = {
                "org": right,
                "role": left,
                "dates": dates.group(0) if dates else "",
                "summary": "",
                "bullets": [],
            }
            continue
        if current is None:
            continue
        if dates and not current["dates"]:
            current["dates"] = dates.group(0)
            rest = _YEAR_SPAN.sub("", line).strip(" -,")
            if rest and not current["summary"]:
                current["summary"] = rest
            continue
        if bullet:
            current["bullets"].append(bullet.group(1))
        elif not current["summary"] and len(line) > 24:
            current["summary"] = line
    if current:
        jobs.append(current)
    return jobs[:8]


def _parse_education(lines: list[str]) -> list[str]:
    return [line for line in lines[:6] if len(line) > 8]


def draft_from_text(
    *,
    resume_text: str = "",
    cover_text: str = "",
    filenames: list[str] | None = None,
) -> dict:
    names = filenames or []
    lines = _clean_lines(resume_text)
    if not lines and cover_text:
        lines = _clean_lines(cover_text)
    sections = _split_sections(lines)
    name = _guess_name(sections["header"] or lines[:8])
    blob = f"{resume_text}\n{cover_text}"
    emails = _EMAIL.findall(blob)
    phones = _PHONE.findall(blob)
    urls = []
    for match in _URL.finditer(blob):
        urls.append(match.group(0).rstrip(".,)"))
    headline = ""
    header_lines = sections["header"][1:5] if sections["header"] else lines[1:5]
    for line in header_lines:
        if name and line == name:
            continue
        if _EMAIL.search(line) or _PHONE.search(line) or _URL.search(line):
            continue
        if 8 < len(line) < 90:
            headline = line
            break
    jobs = _parse_jobs(sections["experience"])
    skills = _parse_skills(sections["skills"])
    education = _parse_education(sections["education"])
    warnings = []
    if not name:
        warnings.append("Could not guess a name — type it in the editor.")
    if not jobs:
        warnings.append("No jobs parsed. Add employment by hand; do not invent titles.")
    if not skills:
        warnings.append("No skills list parsed. Add only skills you can source.")
    if not resume_text.strip() and cover_text.strip():
        warnings.append("Cover letter only — employment/skills will be thin until a résumé is added.")
    source = (
        f"imported local file {', '.join(names) or 'paste'} {date.today().isoformat()} "
        "— inferred, not verified"
    )
    return {
        "slug": slugify(name) or "applicant",
        "displayName": name,
        "headline": headline,
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "web": urls[0] if urls else "",
        "skills": [{"claim": skill} for skill in skills],
        "jobs": jobs,
        "education": [{"claim": row} for row in education],
        "coverLetterNotes": cover_text.strip()[:4000],
        "source": source,
        "warnings": warnings,
        "filenames": names,
    }


def _kind_for_name(name: str, explicit: str | None = None) -> str:
    if explicit in {"resume", "cover-letter"}:
        return explicit
    lower = (name or "").lower()
    if "cover" in lower or "letter" in lower:
        return "cover-letter"
    return "resume"


def draft_from_uploads(files: list[dict]) -> dict:
    """Each file: ``name``, optional ``kind``, and ``text`` or ``contentBase64``."""
    resume_parts: list[str] = []
    cover_parts: list[str] = []
    names: list[str] = []
    for item in files or []:
        name = str(item.get("name") or "upload.txt")
        suffix = Path(name).suffix.lower()
        if suffix and suffix not in ALLOWED_SUFFIXES:
            raise ValueError(f"Unsupported file type: {suffix}. Use PDF, TXT, MD, or HTML.")
        if item.get("text"):
            text = str(item["text"])
        else:
            raw_b64 = item.get("contentBase64") or ""
            payload = base64.b64decode(raw_b64) if raw_b64 else b""
            if len(payload) > MAX_IMPORT_BYTES:
                raise ValueError(f"{name} is over {MAX_IMPORT_BYTES} bytes.")
            if not payload:
                continue
            text = extract_text(name, payload)
        names.append(name)
        kind = _kind_for_name(name, item.get("kind"))
        if kind == "cover-letter" or (
            not resume_parts and _COVER_HINT.search((text or "")[:400])
        ):
            cover_parts.append(text)
        else:
            resume_parts.append(text)
    if not names:
        raise ValueError("No résumé or cover letter text was provided.")
    return draft_from_text(
        resume_text="\n\n".join(resume_parts),
        cover_text="\n\n".join(cover_parts),
        filenames=names,
    )
