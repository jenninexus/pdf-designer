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
    return {
        "id": data.get("id") or profile_path.stem,
        "name": data.get("name"),
        "description": (data.get("description") or "")[:280],
        "user": data.get("user"),
        "vault": data.get("vault"),
        "pages": (data.get("layout") or {}).get("pages"),
        "profileFile": _rel(root, profile_path),
    }


def build_vault_overview(root: Path) -> dict:
    """Return a JSON-serializable overview of private workspace vaults."""
    if not has_private_workspace(root=root):
        return {
            "ok": True,
            "users": [],
            "note": "no private workspace yet (white-label clone) — add users/ or storage/users/",
        }

    users = []
    for user_file in iter_user_paths(root=root):
        card = _user_card(root, user_file)
        if not card:
            continue
        uid = card.get("id") or user_file.stem
        vfile = vault_path(uid, root=root)
        if not vfile.exists():
            hint = card.get("vault")
            if hint:
                linked = (user_file.parent / hint)
                if linked.is_file():
                    vfile = linked.resolve()
        vault = _read_json(vfile) if vfile.is_file() else None
        users.append(
            {
                **card,
                "tracks": _track_summaries(vault) if vault else [],
                "boardSkills": _board_skills(vault) if vault else {"tags": []},
                "goToPacks": _go_to_packs(vault, root) if vault else [],
                "vaultFile": _rel(root, vfile) if vfile.is_file() else None,
            }
        )

    profiles = []
    for profile_file in iter_profile_paths(root=root):
        card = _profile_card(root, profile_file)
        if card:
            profiles.append(card)

    return {
        "ok": True,
        "users": users,
        "profiles": profiles,
        "hubHint": "From /vault, use Open in library -> /?doc=<html-path> selects that resume in the Design Hub.",
    }
