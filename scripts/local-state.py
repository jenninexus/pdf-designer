#!/usr/bin/env python3
"""local-state — check the parts of this checkout that never go to GitHub.

    python scripts/local-state.py              # report; exit 1 when something needs action
    python scripts/local-state.py adopt <cmd> --from codex|agents
                                               # fold a wrapper edit back into .claude/commands/<cmd>.md

Three surfaces, all gitignored:

1. Private files. ``private-sync status``: unshared local edits, and commits to push or pull.
2. Command wrappers. ``.claude/commands/<cmd>.md`` is the source. ``.codex/skills/`` and
   ``.agents/skills/`` hold generated copies for other agent runtimes. Someone working in Codex
   or another runtime can edit a copy instead of the source; the generator would then overwrite
   that edit. Each command is reported as in sync, needing regeneration (source is newer), or
   edited in a wrapper (that wrapper is newer and differs). An edited wrapper is adopted with
   ``adopt``, then the wrappers are regenerated.
3. ``.config/``. Each local ``<name>.json`` is compared with its tracked ``<name>.example.json``,
   so a new key in the public seed is noticed on every machine.

Read-only except ``adopt``. Paths are relative to this checkout; nothing here names a machine.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMMANDS = REPO / ".claude" / "commands"
WRAPPER_ROOTS = {"codex": REPO / ".codex" / "skills", "agents": REPO / ".agents" / "skills"}
CONFIG = REPO / ".config"
_SOURCE_RE = re.compile(r"^Source:\s*(?P<src>\S+)\s*$", re.MULTILINE)
_HEADER_END = "-->"
UNWRAPPED = frozenset({"README"})  # command-folder index, not a command


@dataclass(frozen=True)
class Wrapper:
    runtime: str
    path: Path
    command: str  # source basename without .md
    body: str


def _norm(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


def source_body(text: str) -> str:
    """A command source without its YAML frontmatter."""
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4 :]
    return _norm(text)


def wrapper_body(text: str) -> str:
    """A generated wrapper without its frontmatter and generated-header comment."""
    text = text.replace("\r\n", "\n")
    end = text.find(_HEADER_END)
    return _norm(text[end + len(_HEADER_END) :] if end != -1 else source_body(text))


def iter_wrappers() -> list[Wrapper]:
    found: list[Wrapper] = []
    for runtime, root in WRAPPER_ROOTS.items():
        if not root.is_dir():
            continue
        for skill in sorted(root.glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8", errors="replace")
            match = _SOURCE_RE.search(text)
            if not match or "/.claude/commands/" not in match.group("src").replace("\\", "/"):
                continue
            command = Path(match.group("src").replace("\\", "/")).stem
            found.append(Wrapper(runtime, skill, command, wrapper_body(text)))
    return found


def command_report() -> tuple[list[str], bool]:
    lines: list[str] = []
    action = False
    sources = {p.stem: p for p in sorted(COMMANDS.glob("*.md"))} if COMMANDS.is_dir() else {}
    wrappers = iter_wrappers()
    by_command: dict[str, list[Wrapper]] = {}
    for wrapper in wrappers:
        by_command.setdefault(wrapper.command, []).append(wrapper)
    for name, src in sources.items():
        mine = by_command.get(name, [])
        if name in UNWRAPPED or name.endswith(".example"):
            # The generator makes no wrapper for the folder README or the tracked public seeds;
            # a wrapper left from an older generator is stale and steers agents to old rules.
            for wrapper in mine:
                rel = wrapper.path.parent.relative_to(REPO).as_posix()
                lines.append(f"  STALE       {name} [{wrapper.runtime}]: leftover wrapper for a public seed; delete {rel}/")
                action = True
            continue
        body = source_body(src.read_text(encoding="utf-8", errors="replace"))
        if not mine:
            lines.append(f"  regenerate  {name}: no wrapper yet")
            action = True
            continue
        src_time = src.stat().st_mtime
        for wrapper in mine:
            label = f"{name} [{wrapper.runtime}]"
            if wrapper.body == body:
                continue
            if wrapper.path.stat().st_mtime > src_time:
                lines.append(
                    f"  EDITED      {label}: the wrapper is newer and differs. Keep its edit with: "
                    f"python scripts/local-state.py adopt {name} --from {wrapper.runtime}"
                )
            else:
                lines.append(f"  regenerate  {label}: the source is newer")
            action = True
    for name, mine in sorted(by_command.items()):
        if name not in sources:
            runtimes = ", ".join(sorted({w.runtime for w in mine}))
            lines.append(f"  orphan      {name} [{runtimes}]: no source here (made on another machine?); review, keep or delete")
    if not lines:
        real = [n for n in sources if n not in UNWRAPPED and not n.endswith(".example")]
        lines.append(f"  ok          {len(real)} commands, {len(wrappers)} wrappers in sync")
    return lines, action


def _keys(data: object, prefix: str = "") -> set[str]:
    if not isinstance(data, dict):
        return set()
    keys: set[str] = set()
    for key, value in data.items():
        if key.startswith("_"):
            continue
        path = f"{prefix}{key}"
        keys.add(path)
        keys |= _keys(value, f"{path}.")
    return keys


def config_report() -> tuple[list[str], bool]:
    lines: list[str] = []
    action = False
    if not CONFIG.is_dir():
        return ["  ok          no .config/ folder"], False
    for seed in sorted(CONFIG.glob("**/*.example.json")):
        local = seed.with_name(seed.name.replace(".example.json", ".json"))
        rel = local.relative_to(REPO).as_posix()
        if not local.is_file():
            lines.append(f"  optional    {rel}: not created (copy {seed.name} when this machine needs it)")
            continue
        try:
            missing = _keys(json.loads(seed.read_text(encoding="utf-8-sig"))) - _keys(
                json.loads(local.read_text(encoding="utf-8-sig"))
            )
        except ValueError as exc:
            lines.append(f"  INVALID     {rel}: {exc}")
            action = True
            continue
        if missing:
            lines.append(f"  update      {rel}: missing keys the seed now has: {', '.join(sorted(missing))}")
            action = True
        else:
            lines.append(f"  ok          {rel}")
    return lines, action


def private_sync_report() -> tuple[list[str], bool]:
    if not (REPO / ".git-private" / "HEAD").is_file():
        return ["  not set up  run: python scripts/private-sync.py setup <your private remote>"], True
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "private-sync.py"), "status"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = (result.stdout + result.stderr).strip().splitlines()
    head = [line for line in out if line.startswith("private-sync:")]
    counts = re.search(r"(\d+) local commit\(s\) to push, (\d+) to pull", "\n".join(head))
    unshared = re.search(r"(\d+) local change\(s\) not yet shared", "\n".join(head))
    to_push, to_pull = (int(counts.group(1)), int(counts.group(2))) if counts else (0, 0)
    pending = int(unshared.group(1)) if unshared else 0
    lines = [f"  {line.removeprefix('private-sync: ')}" for line in head] or ["  (no status output)"]
    if to_pull:
        lines.append("  -> pull first: python scripts/private-sync.py pull")
    if pending or to_push:
        lines.append('  -> share: python scripts/private-sync.py push -m "<what changed>"')
    return lines, bool(result.returncode or to_pull or to_push or pending)


def cmd_check() -> int:
    needs = False
    for title, report in (
        ("Private files (private-sync)", private_sync_report),
        ("Command wrappers (.claude source -> .codex / .agents)", command_report),
        ("Local config (.config)", config_report),
    ):
        lines, action = report()
        needs |= action
        print(title)
        print("\n".join(lines))
    print("\nlocal-state: action needed" if needs else "\nlocal-state: all local-only surfaces in sync")
    return 1 if needs else 0


def cmd_adopt(command: str, runtime: str) -> int:
    source = COMMANDS / f"{command}.md"
    if not source.is_file():
        raise SystemExit(f"local-state: no source {source.relative_to(REPO).as_posix()}")
    matches = [w for w in iter_wrappers() if w.command == command and w.runtime == runtime]
    if not matches:
        raise SystemExit(f"local-state: no {runtime} wrapper for {command}")
    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    front = ""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            front = text[: end + 4] + "\n\n"
    source.write_text(front + matches[0].body + "\n", encoding="utf-8", newline="\n")
    print(f"local-state: adopted the {runtime} edit into {source.relative_to(REPO).as_posix()}.")
    print("Next: regenerate the wrappers (/pdf-start step 0), then private-sync push.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("check", help="report local-only state (default)")
    adopt = sub.add_parser("adopt", help="fold a wrapper edit back into its .claude source")
    adopt.add_argument("command")
    adopt.add_argument("--from", dest="runtime", choices=sorted(WRAPPER_ROOTS), required=True)
    args = parser.parse_args(argv)
    if args.cmd == "adopt":
        return cmd_adopt(args.command, args.runtime)
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main())
