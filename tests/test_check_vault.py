"""Tests for check_vault.collect() ranking."""

from pdf_tool.check_vault import collect


def _mini_vault():
    return {
        "roleTracks": {"ai": {"covers": "AI roles", "angle": {"leadWith": []}}},
        "skills": {
            "domain": [
                {
                    "id": "sk-track-lead",
                    "claim": "Track-specific lead claim",
                    "strength": "lead",
                    "tracks": ["ai"],
                    "source": "test",
                    "confidence": "verified",
                },
                {
                    "id": "sk-any-lead",
                    "claim": "Universal lead claim",
                    "strength": "lead",
                    "tracks": ["any"],
                    "source": "test",
                    "confidence": "verified",
                },
                {
                    "id": "sk-track-support",
                    "claim": "Track-specific supporting",
                    "strength": "supporting",
                    "tracks": ["ai"],
                    "source": "test",
                    "confidence": "verified",
                },
                {
                    "id": "sk-any-solid",
                    "claim": "Universal solid claim",
                    "strength": "solid",
                    "tracks": ["any"],
                    "source": "test",
                    "confidence": "verified",
                },
            ]
        },
    }


def test_track_specific_before_any():
    got = collect(_mini_vault(), "ai")
    ids = [h[3]["id"] for h in got["skills"]]
    assert ids.index("sk-track-lead") < ids.index("sk-any-lead")
    assert ids.index("sk-track-support") < ids.index("sk-any-lead")


def test_strength_order_within_tier():
    got = collect(_mini_vault(), "ai")
    ids = [h[3]["id"] for h in got["skills"]]
    # track-specific: lead before supporting
    assert ids.index("sk-track-lead") < ids.index("sk-track-support")
    # any tier: lead before solid
    assert ids.index("sk-any-lead") < ids.index("sk-any-solid")
