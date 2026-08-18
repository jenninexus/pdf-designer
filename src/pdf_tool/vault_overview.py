"""Human-readable vault / skills / go-to résumé overview for Design Hub.

Read-only. Surfaces users/, vaults/, profiles/ (and the legacy storage/
aliases) plus boardSkills and goToPacks so agents and humans need not parse
raw JSON in the editor.
"""

from __future__ import annotations

import json
from pathlib import Path

from .paths import (
    has_private_workspace,
    iter_profile_paths,
    iter_user_paths,
    resolve_rel,
    vault_path,
)

PUBLIC_EXAMPLE_PROFILE = "examples"


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def _track_summaries(vault: dict) -> list[dict]:
    tracks = vault.get("roleTracks") or {}
    out = []
    for tid, t in tracks.items():
        if tid.startswith("_") or not isinstance(t, dict):
            continue
        out.append(
            {
                "id": tid,
                "covers": (t.get("covers") or "")[:220],
                "goToResume": t.get("goToResume"),
                "leadWith": (t.get("angle") or {}).get("leadWith", [])[:3],
            }
        )
    return out


def _board_skills(vault: dict) -> dict:
    bs = vault.get("boardSkills") or {}
    tags = bs.get("tags") or []
    return {
        "lastUpdated": bs.get("lastUpdated"),
        "tags": [{"label": t.get("label"), "group": t.get("group"), "mapsTo": t.get("mapsTo")} for t in tags if isinstance(t, dict)],
        "programs": bs.get("programs"),
    }


def _go_to_packs(vault: dict, root: Path) -> list[dict]:
    packs = vault.get("goToPacks") or {}
    out = []
    for key, p in packs.items():
        if key.startswith("_") or not isinstance(p, dict):
            continue
        html_rel = p.get("html") or ""
        html_path = resolve_rel(html_rel, root=root) if html_rel else None
        resolved_rel = _rel(root, html_path) if html_path else html_rel
        out.append(
            {
                "id": key,
                "label": p.get("label") or key,
                "targets": p.get("targets") or "",
                "focus": p.get("focus"),
                "rule": p.get("rule"),
                "html": resolved_rel if html_path and html_path.is_file() else html_rel,
                "htmlExists": bool(html_path and html_path.is_file()),
                "pages": p.get("pages"),
            }
        )
    return out


def _user_card(root: Path, user_path: Path) -> dict | None:
    data = _read_json(user_path)
    if not data:
        return None
    contact = data.get("contact") or {}
    identity = data.get("identity") or {}
    return {
        "id": data.get("id") or user_path.stem,
        "name": data.get("name"),
        "brand": data.get("brand"),
        "headline": identity.get("headline"),
        "email": contact.get("email"),
        "web": contact.get("web"),
        "location": contact.get("location"),
        "vault": data.get("vault"),
        "userFile": _rel(root, user_path),
    }


def _profile_card(root: Path, profile_path: Path) -> dict | None:
    data = _read_json(profile_path)
    if not data:
        return None
    user = data.get("user")
    user_id = Path(str(user)).stem.lower() if isinstance(user, str) and user else None
    return {
        "id": data.get("id") or profile_path.stem,
        "name": data.get("name"),
        "description": (data.get("description") or "")[:280],
        "user": user_id or user,
        "vault": data.get("vault"),
        "pages": (data.get("layout") or {}).get("pages"),
        "profileFile": _rel(root, profile_path),
    }


def _is_example_id(ident: str | None) -> bool:
    return (ident or "").lower() in {PUBLIC_EXAMPLE_PROFILE, "jane", "jane-example"}


def _enrich_user(root: Path, user_file: Path) -> dict | None:
    card = _user_card(root, user_file)
    if not card:
        return None
    uid = card.get("id") or user_file.stem
    vfile = vault_path(uid, root=root)
    if not vfile.exists():
        hint = card.get("vault")
        if hint:
            linked = (user_file.parent / hint)
            if linked.is_file():
                vfile = linked.resolve()
    vault = _read_json(vfile) if vfile.is_file() else None
    return {
        **card,
        "tracks": _track_summaries(vault) if vault else [],
        "boardSkills": _board_skills(vault) if vault else {"tags": []},
        "goToPacks": _go_to_packs(vault, root) if vault else [],
        "vaultFile": _rel(root, vfile) if vfile.is_file() else None,
        "example": _is_example_id(uid),
    }


def build_vault_overview(root: Path, profile: str | None = None) -> dict:
    """Return a JSON-serializable overview. Default view is Jane Example only."""
    users = []
    for user_file in iter_user_paths(root=root):
        card = _enrich_user(root, user_file)
        if card:
            users.append(card)

    profiles = []
    for profile_file in iter_profile_paths(root=root):
        card = _profile_card(root, profile_file)
        if card:
            profiles.append(card)

    example_users = [u for u in users if u.get("example")]
    personal_users = [u for u in users if not u.get("example")]
    profile_ids = []
    if example_users or any(
        (p.get("id") or "").lower() == PUBLIC_EXAMPLE_PROFILE
        or (p.get("user") or "").lower() in {PUBLIC_EXAMPLE_PROFILE, "examples"}
        for p in profiles
    ):
        profile_ids.append(PUBLIC_EXAMPLE_PROFILE)
    profile_ids.extend(sorted({u.get("id") for u in personal_users if u.get("id")}))

    requested = (profile or PUBLIC_EXAMPLE_PROFILE).strip().lower()
    if requested in ("", "all"):
        requested = PUBLIC_EXAMPLE_PROFILE

    if requested == PUBLIC_EXAMPLE_PROFILE:
        shown = example_users
        shown_profiles = [
            p for p in profiles
            if _is_example_id(p.get("user")) or _is_example_id(p.get("id"))
        ]
        hidden = len(personal_users)
    else:
        shown = [u for u in personal_users if (u.get("id") or "").lower() == requested]
        shown_profiles = [
            p for p in profiles
            if (p.get("user") or "").lower() == requested
            or (p.get("id") or "").lower().startswith(requested)
        ]
        hidden = 0

    if not users and not has_private_workspace(root=root) and not example_users:
        return {
            "ok": True,
            "users": [],
            "profiles": [],
            "profileIds": profile_ids,
            "selectedProfile": requested,
            "hiddenPersonal": 0,
            "note": "no private workspace yet (white-label clone) — add users/ or keep profiles/examples.json",
        }

    return {
        "ok": True,
        "users": shown,
        "profiles": shown_profiles,
        "profileIds": profile_ids,
        "selectedProfile": requested,
        "hiddenPersonal": hidden,
        "hubHint": "From /vault, use Open in library -> /?doc=<html-path> selects that resume in the Design Hub.",
    }
