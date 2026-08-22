"""Build the deliberately small, read-only Voice Seed preview card.

This module is intentionally a one-way projection.  It reads only
``characterVoice`` and the vault's application ``voice`` block, and returns
only the public-card shape; it never returns either source object.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .paths import user_path, vault_path

PUBLIC_EXAMPLE_PROFILE = "examples"
_PROFILE_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
_UNSAFE_TEXT = re.compile(
    r"(?:https?://|www\.|\S+@\S+|[a-z]:[\\/]|[\\/]|\b20\d{2}\b|\b(?:linkedin|github)\b)",
    re.IGNORECASE,
)


def _read_json(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _safe_text(value: object, *, limit: int = 240) -> str | None:
    """Accept a compact writing preference, never a locator or identifier."""
    if not isinstance(value, str):
        return None
    text = " ".join(value.split())
    if not text or len(text) > limit or _UNSAFE_TEXT.search(text):
        return None
    return text


def _safe_list(value: object, *, limit: int = 8) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _safe_text(item)
        if text and text not in result:
            result.append(text)
        if len(result) == limit:
            break
    return result


def build_voice_card(root: Path, profile: str | None = None) -> dict:
    """Return a redacted Voice Seed card payload, or a safe unavailable state.

    No profile means the tracked Jane Example.  A non-example profile has to be
    named explicitly by the caller; profile IDs never enter the card itself.
    """
    requested = (profile or PUBLIC_EXAMPLE_PROFILE).strip().lower()
    if requested in {"jane", "jane-example"}:
        requested = PUBLIC_EXAMPLE_PROFILE
    if not _PROFILE_RE.fullmatch(requested):
        return {"ok": False, "reason": "Voice Seed preview is unavailable for this local profile."}

    user = _read_json(user_path(requested, root=root))
    vault = _read_json(vault_path(requested, root=root))
    character_voice = user.get("characterVoice") if user else None
    voice = vault.get("voice") if vault else None
    # Jane is the public, backwards-compatible demo.  Older public fixtures
    # have no characterVoice block, but its vault voice remains a safe demo.
    if not isinstance(voice, dict) or (
        requested != PUBLIC_EXAMPLE_PROFILE and not isinstance(character_voice, dict)
    ):
        return {"ok": False, "reason": "Voice Seed preview needs valid local voice settings."}

    # Only writing-preference scalars are projected.  In particular, this does
    # not inspect identity/contact/role/claim data or any other vault section.
    # A private vault's free-form tone may contain biographical context that a
    # lexical filter cannot reliably distinguish from a safe preference.  Its
    # preview therefore uses a deliberately generic summary; only the public,
    # fictional Jane fixture demonstrates a descriptive summary.
    summary = (
        _safe_text(voice.get("tone"))
        if requested == PUBLIC_EXAMPLE_PROFILE
        else "Local application-writing preferences."
    ) or "Local application-writing preferences."
    # A private writing-preference string can still contain a client name,
    # credential, phone number, or résumé claim that a lexical filter cannot
    # prove safe.  The read-only private preview therefore proves the schema
    # with empty preference lists.  Only the tracked fictional fixture may
    # demonstrate real preference text; a future owner-edit/approval flow can
    # deliberately add public-safe wording before any card is written.
    writing = (
        {
            "signatureMoves": _safe_list(voice.get("signatureMoves")),
            "avoid": _safe_list(voice.get("avoid")),
        }
        if requested == PUBLIC_EXAMPLE_PROFILE
        else {"signatureMoves": [], "avoid": []}
    )
    card = {
        "schemaVersion": 1,
        "kind": "pdf-designer-voice-card",
        "displayName": "Jane Example" if requested == PUBLIC_EXAMPLE_PROFILE else "Local writing preferences",
        "summary": summary,
        "writing": writing,
        "provenance": {"source": "Local PDF Designer voice preview"},
    }
    return {"ok": True, "card": card}
