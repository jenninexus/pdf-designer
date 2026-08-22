"""Voice Seed preview stays a tiny, local-only redacted projection."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_tool.voice_card import build_voice_card


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_voice_card_uses_only_safe_voice_preferences(tmp_path: Path):
    _write(tmp_path / "users" / "avery.json", {
        "name": "Do Not Expose", "contact": {"email": "secret@example.test"},
        "characterVoice": {"personality": {"traits": ["Warm"]}},
    })
    _write(tmp_path / "vaults" / "avery.json", {
        "voice": {
            "tone": "Clear, practical, and warm.",
            "signatureMoves": ["Lead with the useful point", "Call 555-0100", "Acme Studios launch"],
            "avoid": ["empty hype", "secret@example.test"],
        },
        "roleTracks": {"private": {"claims": ["never expose"]}},
    })

    result = build_voice_card(tmp_path, "avery")

    assert result["ok"] is True
    card = result["card"]
    assert set(card) == {"schemaVersion", "kind", "displayName", "summary", "writing", "provenance"}
    assert card["displayName"] == "Local writing preferences"
    assert card["writing"] == {"signatureMoves": [], "avoid": []}
    payload = json.dumps(card)
    for secret in ("Do Not Expose", "secret@example.test", "private.test", "555-0100", "Acme Studios", "never expose", "avery", "Clear, practical, and warm."):
        assert secret not in payload


def test_voice_card_defaults_to_public_jane_and_handles_bad_or_missing_profiles(tmp_path: Path):
    _write(tmp_path / "users" / "examples.json", {})
    _write(tmp_path / "vaults" / "examples.json", {"voice": {"tone": "Concrete and warm."}})

    result = build_voice_card(tmp_path)

    assert result["ok"] is True
    assert result["card"]["displayName"] == "Jane Example"
    assert build_voice_card(tmp_path, "../not-a-profile")["ok"] is False
    assert build_voice_card(tmp_path, "missing")["ok"] is False
