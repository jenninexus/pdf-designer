"""local-state finds which copy of a command is newest and folds a wrapper edit back into the source."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "scripts" / "local-state.py"
HEADER = "---\nname: {n}\n---\n\n<!--\nGenerated.\nSource: $SYDIO_PATH/pdf-designer/.claude/commands/{n}.md\n-->\n\n"


@pytest.fixture()
def tool(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("local_state", TOOL)
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "local_state", mod)  # dataclasses resolve their module here
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "REPO", tmp_path)
    monkeypatch.setattr(mod, "COMMANDS", tmp_path / ".claude" / "commands")
    monkeypatch.setattr(mod, "WRAPPER_ROOTS", {"codex": tmp_path / ".codex" / "skills",
                                               "agents": tmp_path / ".agents" / "skills"})
    monkeypatch.setattr(mod, "CONFIG", tmp_path / ".config")
    (tmp_path / ".claude" / "commands").mkdir(parents=True)
    return mod


def _source(tool, name: str, body: str) -> Path:
    path = tool.COMMANDS / f"{name}.md"
    path.write_text(f'---\ndescription: "{name}"\n---\n\n{body}\n', encoding="utf-8")
    return path


def _wrapper(tool, runtime: str, name: str, body: str, *, newer_than: Path | None = None) -> Path:
    folder = tool.WRAPPER_ROOTS[runtime] / (name if runtime == "codex" else f"source-command-{name}")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "SKILL.md"
    path.write_bytes((HEADER.format(n=name) + body + "\n").encode("utf-8"))  # exact bytes, no newline translation
    if newer_than is not None:
        stamp = newer_than.stat().st_mtime
        os.utime(path, (stamp + 60, stamp + 60))
    return path


def test_matching_wrappers_are_in_sync(tool):
    _source(tool, "pdf-start", "# start\nstep one")
    _wrapper(tool, "codex", "pdf-start", "# start\nstep one")
    _wrapper(tool, "agents", "pdf-start", "# start\r\nstep one   ")  # line endings and trailing space ignored
    lines, action = tool.command_report()
    assert not action and "1 commands, 2 wrappers in sync" in lines[0]


def test_an_edited_wrapper_is_reported_and_adopted(tool):
    src = _source(tool, "make-resume", "# resume\nold rule")
    os.utime(src, (1_000_000, 1_000_000))
    _wrapper(tool, "codex", "make-resume", "# resume\nnew rule from codex", newer_than=src)
    lines, action = tool.command_report()
    assert action and any("EDITED" in line and "adopt make-resume --from codex" in line for line in lines)

    assert tool.cmd_adopt("make-resume", "codex") == 0
    text = src.read_text(encoding="utf-8")
    assert text.startswith('---\ndescription: "make-resume"\n---') and "new rule from codex" in text
    assert "old rule" not in text


def test_an_older_wrapper_needs_regeneration(tool):
    _wrapper(tool, "codex", "pdf-wrap", "# wrap\nold")
    src = _source(tool, "pdf-wrap", "# wrap\nnew")
    stamp = src.stat().st_mtime
    os.utime(tool.WRAPPER_ROOTS["codex"] / "pdf-wrap" / "SKILL.md", (stamp - 60, stamp - 60))
    lines, action = tool.command_report()
    assert action and any("regenerate  pdf-wrap [codex]: the source is newer" in line for line in lines)


def test_public_seed_wrappers_are_stale_and_missing_wrappers_flagged(tool):
    _source(tool, "make-resume.example", "# public seed")
    _source(tool, "README", "# index")
    _source(tool, "start", "# alias")
    _wrapper(tool, "codex", "make-resume.example", "# old seed")
    lines, action = tool.command_report()
    assert action
    assert any(line.strip().startswith("STALE") and "make-resume.example" in line for line in lines)
    assert any("regenerate  start: no wrapper yet" in line for line in lines)
    assert not any("README" in line for line in lines)


def test_config_reports_keys_the_seed_gained(tool):
    tool.CONFIG.mkdir()
    (tool.CONFIG / "app.example.json").write_text(json.dumps({"a": 1, "b": {"c": 2}, "_note": "x"}), encoding="utf-8")
    (tool.CONFIG / "app.json").write_text(json.dumps({"a": 9}), encoding="utf-8")
    lines, action = tool.config_report()
    assert action and "b, b.c" in lines[0]
    (tool.CONFIG / "app.json").write_text(json.dumps({"a": 9, "b": {"c": 3}}), encoding="utf-8")
    lines, action = tool.config_report()
    assert not action and lines[0].strip().startswith("ok")
