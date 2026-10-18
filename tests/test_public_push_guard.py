"""The pre-push privacy gate must block personal files and identifiers, and pass clean work.

Each test builds a throwaway repository with a copy of the real gate and the real
``.gitignore``, so the rules under test are exactly the ones a push runs.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / "scripts" / "check-public-push.py"


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    shutil.copy2(GATE, tmp_path / "scripts" / GATE.name)
    shutil.copy2(REPO / ".gitignore", tmp_path / ".gitignore")
    (tmp_path / "users").mkdir()
    (tmp_path / "users" / "pat.json").write_text(
        json.dumps({"contact": {"email": "pat.private@mailhost.test", "phone": "(555) 010-4477",
                                "fullName": "Pat Q Applicant", "emailPolicy": "never share this"}}),
        encoding="utf-8",
    )
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "add", ".gitignore", "scripts")
    _git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def _gate(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / GATE.name), "--range", "HEAD~1..HEAD"],
        cwd=repo, capture_output=True, text=True,
    )


def _commit(repo: Path, path: str, text: str, *, force: bool = False) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    _git(repo, "add", *(["-f"] if force else []), path)
    _git(repo, "commit", "-q", "-m", f"add {path}")


def test_clean_public_change_passes(repo: Path) -> None:
    _commit(repo, "docs/NOTES.md", "A public note about the engine.\n")
    result = _gate(repo)
    assert result.returncode == 0, result.stderr


def test_force_added_private_file_is_blocked(repo: Path) -> None:
    _commit(repo, "users/pat.json", "{}", force=True)
    result = _gate(repo)
    assert result.returncode == 1
    assert "users/pat.json" in result.stderr


def test_floor_holds_when_gitignore_is_loosened(repo: Path) -> None:
    (repo / ".gitignore").write_text("", encoding="utf-8")
    _commit(repo, "resumes/pat/cv.html", "<p>cv</p>")
    result = _gate(repo)
    assert result.returncode == 1
    assert "private root resumes/" in result.stderr


@pytest.mark.parametrize("path", ["users/README.md", "vaults/you.example.json", "users/examples.json"])
def test_named_public_seeds_pass_the_floor(repo: Path, path: str) -> None:
    _commit(repo, path, "{}\n")
    assert _gate(repo).returncode == 0


@pytest.mark.parametrize(
    "line",
    ["Contact pat.private@mailhost.test for details", "Call 555.010.4477", "Signed, Pat Q Applicant"],
)
def test_private_identifier_in_added_line_is_blocked(repo: Path, line: str) -> None:
    _commit(repo, "docs/NOTES.md", f"{line}\n")
    result = _gate(repo)
    assert result.returncode == 1
    assert "private identifier" in result.stderr
    assert "pat.private@mailhost.test" not in result.stderr  # the report redacts what it found


def test_policy_sentences_are_not_markers(repo: Path) -> None:
    _commit(repo, "docs/NOTES.md", "never share this\n")
    assert _gate(repo).returncode == 0


def test_local_marker_file_and_public_exemption(repo: Path) -> None:
    config = repo / ".config"
    config.mkdir()
    (config / "private-markers.txt").write_text("secret-project-name\n!mailhost.test\n", encoding="utf-8")
    _commit(repo, "docs/NOTES.md", "codename secret-project-name\n")
    assert _gate(repo).returncode == 1


def test_export_outside_docs_is_blocked(repo: Path) -> None:
    _commit(repo, "art/cover.pdf", "%PDF-1.4", force=True)
    result = _gate(repo)
    assert result.returncode == 1
    assert "export outside docs/" in result.stderr
