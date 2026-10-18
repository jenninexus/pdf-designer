# Private sync — your workspace on every machine, never on GitHub

This repository is public. Your vaults, résumés, applications, collages, brand maps and plans stay
gitignored ([`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md)). Two tools keep it that way when you
work on more than one machine:

| Tool | Job |
|---|---|
| [`scripts/check-public-push.py`](../scripts/check-public-push.py) via [`.githooks/pre-push`](../.githooks/pre-push) | Refuses a GitHub push that would publish a private file or identifier |
| [`scripts/private-sync.py`](../scripts/private-sync.py) | Shares the private roots between *your* machines through a remote you own |

## One-time setup per clone

```bash
git config core.hooksPath .githooks
python scripts/private-sync.py setup <your-private-remote>
```

`<your-private-remote>` is any Git URL or path that is **not** a hosted service: a bare repository
on a LAN share, a USB disk, or your own server. Create it once with
`git init --bare -b main <path>`. Hosted remotes (GitHub, GitLab, Bitbucket) are refused.

`setup` is safe on a machine that already holds personal files. It adopts the shared history
without touching the working tree: files this machine lacks are restored, and files that differ are
listed and stay as they are until you `push` them.

## Daily use

```bash
python scripts/private-sync.py pull                  # before you start
python scripts/private-sync.py push -m "new cover letter"   # after you finish
python scripts/private-sync.py status                # what is not shared yet
```

`pull` never overwrites a local file. An unshared edit, or a new local file with the same name as an
incoming one, stops the pull with a message; `push` yours first (or rename it), then `pull` again.
Two people editing the same file produce an ordinary Git merge conflict; resolve it with
`python scripts/private-sync.py git <command>`. History is kept, so nothing shared is ever lost.

## Check every local-only surface

`python scripts/local-state.py` reports what GitHub never sees in one place. It covers private-sync state,
the command wrappers (`.claude/commands/` is the source, and `.codex/` and `.agents/` are generated copies),
and each `.config/<name>.json` compared with its tracked `.example` seed. It exits 1 when something needs
action. A wrapper edited in another agent runtime is reported as `EDITED`. Fold it back into the source with
`python scripts/local-state.py adopt <cmd> --from codex|agents`, then regenerate the wrappers, so the newest
edit wins whichever tool made it.

## What is shared

The private repository lives in `.git-private/` beside `.git/` and uses the same folder, so the
Design Hub sees one workspace. It holds only:

- `users/` `vaults/` `profiles/` `resumes/` `_job-apps/` `applications/` `collages/` `brands/` `Plans/`
- `docs/*.local.md`, `docs/private/`, and the private notes listed in `PUBLIC-LOCAL-SPLIT.md`
- `.config/private-markers.txt` (so every machine guards every person's identifiers)
- the bare personal commands `.claude/commands/*.md` (`/make-resume`, `/pdf-start`, …), so any machine can
  build any person's documents. The tracked `*.example.md` seeds stay public, and the `.codex/` and `.agents/`
  wrappers are regenerated on each machine from these sources rather than shared.

To keep something on one machine only, list it in `.git-private/skip` (gitignore syntax, one pattern
per line, e.g. `/vaults/me.json` or `/collages/drafts/`). A path that is already shared must also be
removed from the shared copy once: `python scripts/private-sync.py git rm --cached <path>`, then `push`.

Never shared: anything the public repository tracks (README stubs, `*.example.*` seeds), the retired
`storage/` alias, and the disposable `output/` and `_exports/` scratch trees.

## What the push gate checks

On every `git push`, before GitHub accepts it, for each commit being published:

1. **Paths.** No pushed path may be one `.gitignore` ignores (a force-add), and none may sit under a
   private root or be a PDF/image outside `docs/`, unless it is a named public seed. This floor is
   built into the script, so it holds even if the same push loosens `.gitignore`.
2. **Identifiers.** No added line or commit message may contain a private marker. Markers come from
   this machine's real `users/*.json` and `vaults/*.json` (emails, phone numbers, full names,
   profile links), this machine's name and home path, and `.config/private-markers.txt`.

`.config/private-markers.txt` takes one marker per line. `#` starts a comment. A line starting with
`!` marks a value as deliberately public (for example a studio domain that already appears in the
docs), so editing a line that contains it is not blocked.

There is no bypass flag. If the gate blocks a push, amend or drop the offending commit. Do not use
`git push --no-verify`.

Run it by hand: `python scripts/check-public-push.py --range origin/main..HEAD`, or `--tree` to audit
every tracked path.
