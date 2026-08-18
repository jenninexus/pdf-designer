"""Vault overview defaults to Jane Example and hides personal cards."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_tool.vault_overview import build_vault_overview


def _write_user_vault(root: Path, ident: str, name: str) -> None:
    (root / "users").mkdir(exist_ok=True)
    (root / "vaults").mkdir(exist_ok=True)
    (root / "users" / f"{ident}.json").write_text(
        json.dumps(
            {
                "id": ident,
                "name": name,
                "identity": {"headline": f"{name} headline"},
                "contact": {"email": f"{ident}@example.test"},
            }
        ),
        encoding="utf-8",
    )
    (root / "vaults" / f"{ident}.json").write_text(
        json.dumps(
            {
                "roleTracks": {
                    "product-design": {
                        "covers": "Tools",
                        "angle": {"leadWith": ["Shipped work"]},
                    }
                },
                "boardSkills": {"tags": [{"label": "HTML", "group": "web"}]},
                "goToPacks": {},
            }
        ),
        encoding="utf-8",
    )


def test_vault_overview_defaults_to_examples_and_hides_personal(tmp_path: Path):
    _write_user_vault(tmp_path, "examples", "Jane Example")
    _write_user_vault(tmp_path, "alex", "Alex Private")

    default = build_vault_overview(tmp_path)
    assert [u["id"] for u in default["users"]] == ["examples"]
    assert default["hiddenPersonal"] == 1
    assert "examples" in default["profileIds"]
    assert "alex" in default["profileIds"]

    personal = build_vault_overview(tmp_path, profile="alex")
    assert [u["id"] for u in personal["users"]] == ["alex"]
    assert personal["hiddenPersonal"] == 0


def test_live_repo_vault_default_is_jane_example():
    root = Path(__file__).resolve().parents[1]
    data = build_vault_overview(root)
    ids = [u["id"] for u in data["users"]]
    assert ids == ["examples"]
    names = " ".join((u.get("name") or "") for u in data["users"]).lower()
    assert "jane example" in names
    assert "jennifer" not in names
    assert "shade" not in names
