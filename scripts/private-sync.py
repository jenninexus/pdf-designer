#!/usr/bin/env python3
"""Private sync - share your personal workspace between your own machines, never via GitHub.

The public repository tracks the engine; your vaults, résumés, applications, collages and
plans stay gitignored (docs/PUBLIC-LOCAL-SPLIT.md). This tool versions those private roots
in a SECOND Git repository that lives beside the public one in the same folder:

    .git           public engine  -> GitHub
    .git-private   personal data  -> a remote you own (a LAN share, a USB disk, a private server)

Both use the same working tree, so the Design Hub sees one workspace. The private repository
only ever contains the private roots, never a file the public repository tracks.

Commands::

    python scripts/private-sync.py setup <remote>   # first time on each machine (safe to re-run)
    python scripts/private-sync.py status           # what changed locally vs. the shared copy
    python scripts/private-sync.py pull             # bring in the other machines' changes
    python scripts/private-sync.py push [-m MSG]    # commit your changes and share them
    python scripts/private-sync.py git <args...>    # any git command against the private repo

``<remote>`` is any Git URL or path, e.g. a bare repo on a LAN share. Hosted services
(GitHub, GitLab, Bitbucket) are refused: this data must not leave your machines.

Nothing here deletes or overwrites a local file. ``setup`` on a machine that already holds
personal files adopts the shared history without touching them: files missing locally are
restored, files that differ are reported and stay yours until you ``push`` them. ``pull``
stops rather than overwrite an uncommitted local change; resolve it and run ``pull`` again.
"""

from __future__ import annotations

import argparse
import re
import socket
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GIT_DIR_NAME = ".git-private"
BRANCH = "main"

# Private roots shared between your machines. storage/ (retired alias), output/ and _exports/
# (disposable scratch) are deliberately absent.
SHARED_ROOTS = (
    "users",
    "vaults",
    "profiles",
    "resumes",
    "_job-apps",
    "applications",
    "collages",
    "brands",
    "Plans",
)
SHARED_FILES = (
    "docs/*.local.md",
    "docs/MARKETING.md",
    "docs/WORKSPACE.md",
    "docs/HISTORY-SCRUB.md",
    "docs/private/",
    ".config/private-markers.txt",
)
NOISE = ("desktop.ini", "Thumbs.db", ".DS_Store", "__pycache__/", "*.pyc", "~$*")
HOSTED = re.compile(r"(github\.com|gitlab\.com|bitbucket\.org|dev\.azure\.com)", re.IGNORECASE)


def exclude_rules(public_paths: set[str]) -> str:
    """info/exclude for the private repo: ignore everything, re-include the private roots,
    then drop every file the public repo tracks (README stubs, *.example seeds)."""
    lines = ["# Written by scripts/private-sync.py on every run - do not edit.", "/*"]
    lines += [f"!/{root}/" for root in SHARED_ROOTS]
    lines += ["!/docs/", "/docs/*", "!/.config/", "/.config/*"]
    lines += [f"!/{pattern}" for pattern in SHARED_FILES]
    lines += list(NOISE)
    roots = tuple(f"{root}/" for root in SHARED_ROOTS) + ("docs/", ".config/")
    lines += [f"/{path}" for path in sorted(public_paths) if path.startswith(roots)]
    return "\n".join(lines) + "\n"


def pgit(
    *args: str, check: bool = True, capture: bool = True, stdin: str | None = None
) -> subprocess.CompletedProcess[str]:
    """Run git against the private repository with the shared working tree."""
    result = subprocess.run(
        ["git", f"--git-dir={REPO / GIT_DIR_NAME}", f"--work-tree={REPO}", *args],
        cwd=REPO,
        input=stdin,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip() if capture else ""
        raise SystemExit(f"private-sync: git {' '.join(args)} failed\n{detail}")
    return result


def public_tracked() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True
    ).stdout
    return {p for p in out.split("\0") if p}


def private_tracked() -> set[str]:
    return {p for p in pgit("ls-files", "-z").stdout.split("\0") if p}


def remote_has_branch() -> bool:
    return bool(pgit("ls-remote", "--heads", "origin", BRANCH, check=False).stdout.strip())


def ensure_repo(remote: str | None) -> None:
    git_dir = REPO / GIT_DIR_NAME
    if not git_dir.is_dir():
        pgit("init", "--quiet", f"--initial-branch={BRANCH}")
    # Byte-identical files on every machine; the public repo's line-ending rules do not apply.
    pgit("config", "core.autocrlf", "false")
    pgit("config", "core.safecrlf", "false")
    pgit("config", "pull.ff", "false")
    (git_dir / "info").mkdir(exist_ok=True)
    (git_dir / "info" / "exclude").write_text(exclude_rules(public_tracked()), encoding="utf-8")
    if remote:
        if HOSTED.search(remote):
            raise SystemExit(
                "private-sync: refusing a hosted remote. Personal data must stay on machines you "
                "own; use a LAN share, a local disk or your own server."
            )
        existing = pgit("remote", "get-url", "origin", check=False).stdout.strip()
        if not existing:
            pgit("remote", "add", "origin", remote)
        elif existing != remote:
            pgit("remote", "set-url", "origin", remote)
    elif not pgit("remote", "get-url", "origin", check=False).stdout.strip():
        raise SystemExit("private-sync: no remote yet - run: python scripts/private-sync.py setup <remote>")


def exclude_file() -> Path:
    return REPO / GIT_DIR_NAME / "info" / "exclude"


def untracked_private_files() -> list[str]:
    """New files under the private roots, chosen by the private rules ONLY.

    The working tree's ``.gitignore`` belongs to the public repo and ignores exactly these
    roots, so normal ``git add``/``git status`` would never see them. ``--exclude-from``
    without ``--exclude-standard`` applies our rules and skips every ``.gitignore``.
    """
    out = pgit("ls-files", "-z", "--others", f"--exclude-from={exclude_file()}").stdout
    return sorted(p for p in out.split("\0") if p)


def stage_private_changes() -> None:
    pgit("add", "--update")  # edits and deletions of files already shared
    new_files = untracked_private_files()
    if new_files:
        # -f because the public .gitignore matches them; the list itself is the filter.
        pgit("add", "-f", "--pathspec-from-file=-", "--pathspec-file-nul", stdin="\0".join(new_files))
    # The public repository owns its tracked files (README stubs, *.example seeds).
    overlap = sorted(private_tracked() & public_tracked())
    if overlap:
        pgit("rm", "--cached", "--quiet", "--pathspec-from-file=-", "--pathspec-file-nul", stdin="\0".join(overlap))


def has_head() -> bool:
    return pgit("rev-parse", "--verify", "--quiet", "HEAD", check=False).returncode == 0


def commit(message: str) -> bool:
    stage_private_changes()
    if has_head() and pgit("diff", "--cached", "--quiet", check=False).returncode == 0:
        return False
    if not has_head() and not pgit("ls-files").stdout.strip():
        return False
    pgit("commit", "--quiet", "-m", message)
    return True


def default_message() -> str:
    return f"private: sync from {socket.gethostname()}"


def cmd_setup(remote: str) -> int:
    ensure_repo(remote)
    pgit("fetch", "--quiet", "origin")
    if not remote_has_branch():
        if commit(f"private: first snapshot from {socket.gethostname()}"):
            pgit("push", "--quiet", "-u", "origin", BRANCH)
            print(f"private-sync: created the shared copy with {len(private_tracked())} files.")
        else:
            print("private-sync: nothing private to share yet.")
        return 0
    if has_head():
        print("private-sync: already set up; remote refreshed.")
        return cmd_status()
    # Adopt the shared history without touching the working tree.
    pgit("update-ref", f"refs/heads/{BRANCH}", f"origin/{BRANCH}")
    pgit("symbolic-ref", "HEAD", f"refs/heads/{BRANCH}")
    pgit("reset", "--quiet", "--mixed")
    pgit("branch", "--quiet", f"--set-upstream-to=origin/{BRANCH}", BRANCH)
    missing = [p for p in pgit("ls-files", "--deleted", "-z").stdout.split("\0") if p]
    if missing:
        pgit("checkout", "--", *missing)
    print(f"private-sync: joined the shared copy; restored {len(missing)} file(s) this machine lacked.")
    return cmd_status()


def cmd_status() -> int:
    ensure_repo(None)
    pgit("fetch", "--quiet", "origin", check=False)
    changes = pgit("status", "--short", "--untracked-files=no").stdout.splitlines()
    changes += [f"?? {path}" for path in untracked_private_files()]
    ahead_behind = pgit("rev-list", "--left-right", "--count", f"HEAD...origin/{BRANCH}", check=False).stdout.split()
    if len(ahead_behind) == 2:
        print(f"private-sync: {ahead_behind[0]} local commit(s) to push, {ahead_behind[1]} to pull.")
    print(f"private-sync: {len(changes)} local change(s) not yet shared" + (":" if changes else "."))
    for line in changes[:200]:
        print(f"  {line}")
    if len(changes) > 200:
        print(f"  ... and {len(changes) - 200} more")
    return 0


def cmd_pull() -> int:
    ensure_repo(None)
    pgit("fetch", "--quiet", "origin")
    result = pgit("merge", "--no-edit", "--no-overwrite-ignore", f"origin/{BRANCH}", check=False)
    if result.returncode != 0:
        print(result.stdout + result.stderr, file=sys.stderr)
        print(
            "private-sync: pull stopped without overwriting anything. Share or move your local "
            "change (push), then pull again. For a conflict: private-sync.py git status.",
            file=sys.stderr,
        )
        return 1
    print("private-sync: up to date with the shared copy.")
    return 0


def cmd_push(message: str | None) -> int:
    ensure_repo(None)
    made = commit(message or default_message())
    pgit("fetch", "--quiet", "origin")
    if remote_has_branch():
        result = pgit("merge", "--no-edit", "--no-overwrite-ignore", f"origin/{BRANCH}", check=False)
        if result.returncode != 0:
            print(result.stdout + result.stderr, file=sys.stderr)
            print("private-sync: merge conflict - resolve with private-sync.py git ..., then push.", file=sys.stderr)
            return 1
    pgit("push", "--quiet", "-u", "origin", BRANCH)
    print(f"private-sync: shared ({'new commit' if made else 'no new local changes'}).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("setup", help="create or join the private repo")
    setup.add_argument("remote", help="Git URL or path of the private remote")
    sub.add_parser("status", help="show unshared local changes")
    sub.add_parser("pull", help="bring in changes from your other machines")
    push = sub.add_parser("push", help="commit and share local changes")
    push.add_argument("-m", "--message")
    passthrough = sub.add_parser("git", help="run git against the private repo")
    passthrough.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.command == "setup":
        return cmd_setup(args.remote)
    if args.command == "status":
        return cmd_status()
    if args.command == "pull":
        return cmd_pull()
    if args.command == "push":
        return cmd_push(args.message)
    return pgit(*args.args, check=False, capture=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
