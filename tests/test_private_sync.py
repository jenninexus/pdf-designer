"""Private sync shares personal roots between machines without overwriting anyone's files.

Two throwaway "machines" share one bare remote, exactly as two PCs share a LAN repo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "scripts" / "private-sync.py"


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def _machine(root: Path) -> Path:
    """A public checkout with one tracked README stub inside a private root."""
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(TOOL, root / "scripts" / TOOL.name)
    # The real public ignore rules: they hide every private root from normal git commands.
    shutil.copy2(REPO / ".gitignore", root / ".gitignore")
    (root / "users").mkdir()
    (root / "users" / "README.md").write_text("public stub\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "engine.py").write_text("print('engine')\n", encoding="utf-8")
    _git(root, "init", "-q", "-b", "main")
    _git(root, "add", ".gitignore", "scripts", "users/README.md", "src")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "public")
    return root


IDENTITY = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}


def _sync(machine: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(machine / "scripts" / TOOL.name), *args],
        cwd=machine, capture_output=True, text=True, env={**os.environ, **IDENTITY},
    )


@pytest.fixture()
def lan(tmp_path: Path) -> tuple[Path, Path, Path]:
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", str(remote))
    return remote, _machine(tmp_path / "a"), _machine(tmp_path / "b")


def _private_files(machine: Path) -> set[str]:
    out = _git(machine, f"--git-dir={machine / '.git-private'}", "ls-files")
    return set(out.split())


def test_first_machine_shares_only_private_roots(lan: tuple[Path, Path, Path]) -> None:
    remote, a, _ = lan
    (a / "users" / "pat.json").write_text('{"name": "Pat"}', encoding="utf-8")
    (a / "resumes" / "pat").mkdir(parents=True)
    (a / "resumes" / "pat" / "cv.html").write_text("<p>cv</p>", encoding="utf-8")
    result = _sync(a, "setup", str(remote))
    assert result.returncode == 0, result.stderr
    files = _private_files(a)
    assert files == {"users/pat.json", "resumes/pat/cv.html"}
    assert "users/README.md" not in files and "src/engine.py" not in files


def test_personal_commands_are_shared_but_public_seeds_and_settings_are_not(lan: tuple[Path, Path, Path]) -> None:
    remote, a, _ = lan
    commands = a / ".claude" / "commands"
    commands.mkdir(parents=True)
    (commands / "make-resume.example.md").write_text("public seed\n", encoding="utf-8")
    _git(a, "add", "-f", ".claude/commands/make-resume.example.md")
    _git(a, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "seed")
    (commands / "make-resume.md").write_text("my resume command\n", encoding="utf-8")
    (a / ".claude" / "settings.local.json").write_text("{}", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0
    files = _private_files(a)
    assert ".claude/commands/make-resume.md" in files
    assert ".claude/commands/make-resume.example.md" not in files
    assert ".claude/settings.local.json" not in files


def test_joining_machine_keeps_its_own_files(lan: tuple[Path, Path, Path]) -> None:
    remote, a, b = lan
    (a / "users" / "pat.json").write_text("A version", encoding="utf-8")
    (a / "users" / "sam.json").write_text("only on A", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0

    (b / "users" / "pat.json").write_text("B version", encoding="utf-8")
    (b / "users" / "lee.json").write_text("only on B", encoding="utf-8")
    result = _sync(b, "setup", str(remote))
    assert result.returncode == 0, result.stderr

    assert (b / "users" / "pat.json").read_text(encoding="utf-8") == "B version"  # never overwritten
    assert (b / "users" / "sam.json").read_text(encoding="utf-8") == "only on A"  # restored
    assert (b / "users" / "lee.json").read_text(encoding="utf-8") == "only on B"
    assert "users/pat.json" in result.stdout and "users/lee.json" in result.stdout


def test_round_trip_push_and_pull(lan: tuple[Path, Path, Path]) -> None:
    remote, a, b = lan
    (a / "users" / "pat.json").write_text("v1", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0
    assert _sync(b, "setup", str(remote)).returncode == 0

    (b / "users" / "pat.json").write_text("v2 from B", encoding="utf-8")
    (b / "Plans").mkdir()
    (b / "Plans" / "next.md").write_text("plan", encoding="utf-8")
    assert _sync(b, "push").returncode == 0
    assert _sync(a, "pull").returncode == 0
    assert (a / "users" / "pat.json").read_text(encoding="utf-8") == "v2 from B"
    assert (a / "Plans" / "next.md").read_text(encoding="utf-8") == "plan"


def test_pull_never_overwrites_an_uncommitted_local_edit(lan: tuple[Path, Path, Path]) -> None:
    remote, a, b = lan
    (a / "users" / "pat.json").write_text("v1", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0
    assert _sync(b, "setup", str(remote)).returncode == 0
    (b / "users" / "pat.json").write_text("v2 from B", encoding="utf-8")
    assert _sync(b, "push").returncode == 0

    (a / "users" / "pat.json").write_text("unsaved edit on A", encoding="utf-8")
    assert _sync(a, "pull").returncode == 1
    assert (a / "users" / "pat.json").read_text(encoding="utf-8") == "unsaved edit on A"


def test_pull_never_overwrites_an_unshared_local_file(lan: tuple[Path, Path, Path]) -> None:
    """Git treats ignored files as expendable on merge; private files are all 'ignored'."""
    remote, a, b = lan
    (a / "users" / "pat.json").write_text("v1", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0
    assert _sync(b, "setup", str(remote)).returncode == 0
    (b / "users" / "new.json").write_text("from B", encoding="utf-8")
    assert _sync(b, "push").returncode == 0

    (a / "users" / "new.json").write_text("A's own unshared file", encoding="utf-8")
    assert _sync(a, "pull").returncode == 1
    assert (a / "users" / "new.json").read_text(encoding="utf-8") == "A's own unshared file"


def test_skip_list_keeps_a_file_on_this_machine(lan: tuple[Path, Path, Path]) -> None:
    remote, a, _ = lan
    (a / "users" / "pat.json").write_text("share me", encoding="utf-8")
    (a / "users" / "mine.json").write_text("keep me here", encoding="utf-8")
    (a / ".git-private").mkdir()
    (a / ".git-private" / "skip").write_text("/users/mine.json\n", encoding="utf-8")
    assert _sync(a, "setup", str(remote)).returncode == 0
    assert _private_files(a) == {"users/pat.json"}


def test_hosted_remote_is_refused(lan: tuple[Path, Path, Path]) -> None:
    _, a, _ = lan
    result = _sync(a, "setup", "https://github.com/someone/private.git")
    assert result.returncode != 0
    assert "refusing a hosted remote" in (result.stdout + result.stderr)
