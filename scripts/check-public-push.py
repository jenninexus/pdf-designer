#!/usr/bin/env python3
"""Public-push privacy gate - refuse to publish personal files or identifiers.

This repository is public. Personal data lives in the same checkout, kept out by
``.gitignore`` (see docs/PUBLIC-LOCAL-SPLIT.md). An ignore rule only stops ``git add``;
it does not stop ``git add -f``, a loosened ``.gitignore``, or a personal email pasted
into a public doc. This gate runs as the ``pre-push`` hook and checks every commit a push
would publish, before the remote accepts it:

1. **Paths** - no pushed path may be one ``.gitignore`` ignores, and none may sit under a
   private root (``users/``, ``vaults/``, ``resumes/``, ...) or be a document/image export,
   unless it is a named public seed. The floor holds even if the same push edits ``.gitignore``.
2. **Identifiers** - no added line or commit message may contain a private marker. Markers
   are derived from this machine's real ``users/*.json`` and ``vaults/*.json`` (emails, phone
   numbers, full names, profile links), plus this machine's name and home path, plus any line
   in the local, gitignored ``.config/private-markers.txt``.

Install once per clone::

    git config core.hooksPath .githooks

Manual use::

    python scripts/check-public-push.py --range origin/main..HEAD
    python scripts/check-public-push.py --tree        # audit every tracked path at HEAD

Exit 0 = clean; 1 = blocked (the report names each offending path or commit).
Standard library only, so the hook works before the dev extras are installed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]
ZERO_SHA = "0" * 40

# Roots that hold a person's data. Only named public seeds may be tracked inside them.
PRIVATE_ROOTS = (
    "users",
    "vaults",
    "profiles",
    "resumes",
    "applications",
    "collages",
    "brands",
    "private",
    "notes",
    "output",
    ".codex",
    ".agents",
    ".git-private",
    "docs/private",
)
PUBLIC_SEED_PATHS = frozenset(
    {
        "users/examples.json",
        "vaults/examples.json",
        "profiles/examples.json",
    }
)
# Public product media is limited to deliberately reviewed files.
EXPORT_SUFFIXES = (".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".docx", ".doc")
PUBLIC_MEDIA_PATHS = frozenset(
    {
        "assets/public/overview/pdf-designer-overview.pdf",
        "assets/public/hub/hub-library.png",
        "assets/public/hub/hub-recipes.png",
        "assets/public/hub/hub-splash.png",
        "assets/public/hub/hub-start.png",
        "assets/public/hub/hub-vault.png",
        "assets/public/hub/wizard-palettes-dark.png",
        "assets/public/hub/wizard-palettes-light.png",
    }
)
PRIVATE_ONLY_ROOTS = (
    "storage", "plans", "_exports", "_job-apps", "_collabs", ".local-artifacts", ".memory",
    ".form-helper", ".codex", ".agents", ".cursor",
)
# Hub/UI assets under src/pdf_tool/static are part of the public engine, not personal exports.
PUBLIC_ENGINE_ASSET_ROOT = "src/pdf_tool/static/"
PRIVATE_DOC_NAMES = frozenset({
    "docs/marketing.md", "docs/workspace.md", "docs/history-scrub.md", "docs/roadmap.md",
    "docs/development-flow.md", "docs/voice-seed-handoff.md",
})
WINDOWS_RELEASE_SUFFIXES = (
    ".exe", ".msi", ".msix", ".msixbundle", ".msixupload", ".appx", ".appxbundle", ".appxupload",
)

LOCAL_MARKERS_FILE = REPO / ".config" / "private-markers.txt"
# Contact fields whose values identify a real person. First names are deliberately absent:
# public docs may say "Shade" or "Jane", but never a full name, email, phone or profile link.
IDENTIFIER_KEYS = re.compile(
    r"^(e-?mail\w*|phone\w*|full_?name|last_?name|legal_?name|linkedin|github|discord|"
    r"website|web|portfolio_?url|address|street)$",
    re.IGNORECASE,
)
NAME_KEYS = re.compile(r"^(full_?name|last_?name|legal_?name)$", re.IGNORECASE)
MIN_MARKER_LEN = 6
MIN_PHONE_DIGITS = 7


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        raise SystemExit(f"check-public-push: git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout


# --- path rules -----------------------------------------------------------------------------


def path_floor_violation(path: str) -> str | None:
    """Return why ``path`` may never be public, or None. Independent of ``.gitignore``."""
    posix = PurePosixPath(path)
    name = posix.name
    lower_name = name.lower()
    lower_path = path.lower()
    if lower_name == ".env" or (lower_name.startswith(".env.") and lower_name != ".env.example"):
        return "local environment file"
    if lower_name == ".pypirc" or lower_name.endswith((".pfx", ".p12")):
        return "local publishing credential"
    if lower_name.endswith(WINDOWS_RELEASE_SUFFIXES):
        return "Windows release binary"
    if lower_path == "desktop/azure-trusted-signing.json":
        return "local signing config"
    if lower_path == "layouts/application-packet.json":
        return "local application packet recipe"
    if lower_path.startswith("themes/fonts/") and path != "themes/fonts/README.md":
        return "local font asset"
    if path == "browser-extension" or path.startswith("browser-extension/") or path == "docs/BROWSER-HELPER.md":
        return "local-only extension"
    for root in PRIVATE_ONLY_ROOTS:
        if lower_path == root or lower_path.startswith(root + "/"):
            return f"private root {root}/"
    if path in PUBLIC_SEED_PATHS:
        return None
    for root in PRIVATE_ROOTS:
        if path == root or path.startswith(root + "/"):
            is_root_readme = name == "README.md" and str(posix.parent) == root
            if is_root_readme or ".example." in name:
                return None
            return f"private root {root}/"
    if lower_path in PRIVATE_DOC_NAMES or lower_name.endswith((".local.md", ".private.md")):
        return "private note"
    if lower_path == ".mcp.json":
        return "machine-local MCP config"
    if lower_path.startswith(".vscode/") and path not in {".vscode/tasks.json.example", ".vscode/mcp.json.example"}:
        return "machine-local editor config"
    if lower_path.startswith(".claude/"):
        if posix.parent != PurePosixPath(".claude/commands") or not name.endswith(".example.md"):
            return "local Claude data (only command examples are public)"
    if lower_path.startswith(".config/"):
        is_public_example = posix.parent == PurePosixPath(".config") and name.endswith(".example.json")
        if not is_public_example and path != ".config/capture/hub.breakpoints.example.json":
            return "machine-local config"
    if (
        lower_name.endswith(EXPORT_SUFFIXES)
        and path not in PUBLIC_MEDIA_PATHS
        and not path.startswith(PUBLIC_ENGINE_ASSET_ROOT)
    ):
        return "document/image export outside approved public assets"
    return None


def ignored_paths(paths: list[str]) -> set[str]:
    """Paths the working tree's ``.gitignore`` would ignore (i.e. force-added)."""
    if not paths:
        return set()
    # NUL-separated bytes: text mode on Windows would turn "\n" into "\r\n", and git would
    # then test "path\r", which no negation rule matches.
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--stdin", "-z"],
        cwd=REPO,
        input=b"\0".join(p.encode("utf-8") for p in paths) + b"\0",
        capture_output=True,
    )
    return {p for p in result.stdout.decode("utf-8", "replace").split("\0") if p}


def check_paths(paths: list[str]) -> list[str]:
    problems = [f"{path}: {why}" for path in paths if (why := path_floor_violation(path))]
    floor = {p.split(":", 1)[0] for p in problems}
    problems += [
        f"{path}: ignored by .gitignore (force-added?)"
        for path in sorted(ignored_paths(paths))
        if path not in floor
    ]
    return problems


# --- identifier markers ---------------------------------------------------------------------


def _collect_identifiers(node: object, out: set[str], key: str = "") -> None:
    if isinstance(node, dict):
        for child_key, value in node.items():
            _collect_identifiers(value, out, str(child_key))
    elif isinstance(node, list):
        for value in node:
            _collect_identifiers(value, out, key)
    elif isinstance(node, str) and IDENTIFIER_KEYS.match(key):
        value = node.strip()
        if NAME_KEYS.match(key):
            if 0 < len(value.split()) <= 4:  # a name, not a sentence about naming
                out.add(value)
        elif _is_phone(value) or (" " not in value and ("@" in value or "." in value)):
            out.add(value)  # email, phone, domain or profile link; skips policy notes


def _is_example(path: Path) -> bool:
    return ".example." in path.name or path.name == "examples.json"


def _marker_lines(repo: Path = REPO) -> list[str]:
    file = repo / LOCAL_MARKERS_FILE.relative_to(REPO)
    return file.read_text(encoding="utf-8-sig").splitlines() if file.is_file() else []


def derive_markers(repo: Path = REPO) -> set[str]:
    """Identifiers that must never appear in a public commit, from this machine's real data."""
    raw: set[str] = set()
    for folder in ("users", "vaults"):
        for path in sorted((repo / folder).glob("*.json")):
            if _is_example(path):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue
            _collect_identifiers(data, raw)
    public: set[str] = set()
    for line in _marker_lines(repo):
        line = line.strip()
        if line.startswith("!"):
            if "\t" not in line:
                public.add(_normalize(line[1:]))  # deliberately public, e.g. a studio domain
        elif line and not line.startswith("#"):
            raw.add(line)
    host = os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or ""
    if len(host) >= MIN_MARKER_LEN:
        raw.add(host)
    home = str(Path.home())
    raw.update({home, home.replace("\\", "/"), home.replace("\\", "\\\\")})

    markers = {_normalize(value) for value in raw}
    return {m for m in markers if len(m) >= MIN_MARKER_LEN and m not in public}


def _normalize(value: str) -> str:
    value = value.strip().lower()
    for prefix in ("https://", "http://", "www."):
        value = value.removeprefix(prefix)
    return value.rstrip("/")


def find_markers(text: str, markers: set[str]) -> list[str]:
    lowered = text.lower()
    hits = [marker for marker in markers if not _is_phone(marker) and marker in lowered]
    digits = re.sub(r"\D", "", text)
    for marker in markers:
        if _is_phone(marker):
            marker_digits = re.sub(r"\D", "", marker)
            # Match on the national number so "+1 (555) 010-0199" equals "555-010-0199".
            if marker_digits[-10:] and marker_digits[-10:] in digits:
                hits.append(marker)
    return sorted(set(hits))


def _is_phone(value: str) -> bool:
    return bool(re.fullmatch(r"[\d\s().+-]+", value)) and len(re.sub(r"\D", "", value)) >= MIN_PHONE_DIGITS


def _redact(marker: str) -> str:
    return marker[:2] + "*" * max(len(marker) - 4, 2) + marker[-2:]


def check_content(rev_range: list[str], markers: set[str]) -> list[str]:
    if not markers:
        return []
    log = git("log", "-p", "--no-color", "--no-ext-diff", "--format=%x00%H%n%B", *rev_range)
    public_links: dict[str, list[str]] = {}
    for line in _marker_lines():
        path, _, url = line.strip().partition("\t")
        if path.startswith("!") and path.endswith((".md", ".py", ".cjs")) and re.fullmatch(r"https://[^\s()'\"<>]+", url):
            public_links.setdefault(path[1:], []).append(url)
    problems: list[str] = []
    for chunk in log.split("\x00")[1:]:
        sha, _, body = chunk.partition("\n")
        message, _, patch = body.partition("\ndiff --git ")
        current = "(commit message)"
        added: list[tuple[str, str]] = [("(commit message)", message)]
        for line in ("diff --git " + patch).splitlines() if patch else []:
            if line.startswith("+++ "):
                current = line[6:] if line.startswith("+++ b/") else line[4:]
            elif line.startswith("+") and not line.startswith("+++"):
                added.append((current, line[1:]))
        for where, text in added:
            for url in public_links.get(where, ()):
                if where.endswith(".md"):
                    text = text.replace(f"]({url})", "](approved-public-link)")
                else:
                    for quote in ('"', "'"):
                        text = text.replace(f"{quote}{url}{quote}", f"{quote}approved-public-link{quote}")
            for marker in find_markers(text, markers):
                problems.append(f"{sha[:10]} {where}: private identifier {_redact(marker)}")
    return sorted(set(problems))


# --- ranges ---------------------------------------------------------------------------------


def ranges_from_pre_push(stdin: str, remote: str) -> list[list[str]]:
    ranges: list[list[str]] = []
    for line in stdin.splitlines():
        parts = line.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if local_sha == ZERO_SHA:
            continue  # deleting a remote ref publishes nothing
        if remote_sha == ZERO_SHA or not git("cat-file", "-t", remote_sha, check=False).strip():
            ranges.append([local_sha, "--not", f"--remotes={remote}"])
        else:
            ranges.append([f"{remote_sha}..{local_sha}"])
    return ranges


def pushed_paths(rev_range: list[str]) -> list[str]:
    out = git("log", "--format=", "--name-only", "--diff-filter=ACMRT", "--no-renames", *rev_range)
    return sorted({line.strip() for line in out.splitlines() if line.strip()})


def run(rev_ranges: list[list[str]]) -> int:
    markers = derive_markers()
    problems: list[str] = []
    for rev_range in rev_ranges:
        problems += check_paths(pushed_paths(rev_range))
        problems += check_content(rev_range, markers)
    problems = sorted(set(problems))
    if problems:
        print("check-public-push: BLOCKED - this push would publish private material:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            "Fix the commits (amend or drop the change) and push again. Personal files belong in\n"
            "the private sync repo (docs/PRIVATE-SYNC.md), never on GitHub.",
            file=sys.stderr,
        )
        return 1
    print(f"check-public-push: ok ({len(markers)} private markers checked)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--pre-push", nargs="*", metavar="ARG", help="git pre-push hook mode (remote, url)")
    mode.add_argument("--range", help="revision range to check, e.g. origin/main..HEAD")
    mode.add_argument("--tree", action="store_true", help="audit every tracked path at HEAD")
    args = parser.parse_args(argv)

    if args.tree:
        problems = check_paths(git("ls-files").splitlines())
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(f"check-public-push --tree: {'BLOCKED' if problems else 'ok'}")
        return 1 if problems else 0
    if args.range:
        return run([[args.range]])
    remote = args.pre_push[0] if args.pre_push else "origin"
    return run(ranges_from_pre_push(sys.stdin.read(), remote))


if __name__ == "__main__":
    raise SystemExit(main())
