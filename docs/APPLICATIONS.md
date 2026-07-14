# The application workflow

One folder per job — how to go after a job without ever inventing a claim.

The workflow for going after a job without ever inventing a claim.

> Your real applications live in `storage/applications/` (gitignored). The copyable templates live
> in [`../examples/applications/example-application/`](../examples/applications/example-application/).

---

## Two rules, both blocking

### 🔗 1. Capture the apply link BEFORE you build

**A perfectly tailored application you can't submit is worthless.**

If a listing arrives with no URL — **ask for it.** One question costs nothing; a dead
application costs the whole build. Status stays **`BLOCKED`** until an apply URL or an apply
email exists. This has already burned us twice.

> **Trap:** a company page showing *"no open jobs"* does **not** mean the posting is dead.
> Board postings frequently never appear on the employer's own page. **Only the direct job
> link is authoritative** — fetch it before concluding anything.

### 🛑 2. Ask about gaps BEFORE you build

For every listing requirement with **no vault backing** — **ask the applicant first.**

The vault records what they have *told* you. It is **not the limit of what they can do.** On a
real application, four requirements looked like gaps and *all four* turned out to be
long-standing strengths nobody had thought to ask about. Two industry-standard tools sat on a
"never claim" list for months while the applicants had years of experience with each.

**Only a *confirmed* absence is a gap.** Then — and only then — name the honest equivalent and
address it once, plainly, in the cover letter. That candor wins credibility.

---

## Folder anatomy

Folders are keyed by **role track**, *not* by date — so each new job in a track is a
copy-and-tweak of the last one rather than a rebuild.

```text
storage/applications/
  3D-Visualizer/            ← the TRACK, not a date
    Company.md              research · verified links · pay verdict · evidence map · the listing verbatim
    application.json        the machine record: apply URL · pay · status · who applied
    theme.json              the palette derived from THIS COMPANY's real brand CSS
    *.html                  the résumé + cover-letter SOURCES
    evidence/               screenshots of the live posting
  Backend/
  …
```

**⭐ No PDFs in here.** Finished PDFs and PNGs go to **`storage/<user>/_exports/<Track>/`** —
per *person*, so everything one applicant needs to send sits in one place:

```text
storage/jenni/_exports/3D-Visualizer/     one applicant's PDFs for that job
storage/shade/_exports/3D-Visualizer/     the other's, for the same job
```

Facts about the *job* (the apply link, the pay, the company palette) belong to the *job* — so
two people applying to the same posting share **one** record and it can never drift apart
between them.

## Templates in this folder

| Copy this | To | For |
|---|---|---|
| [`Company.example.md`](../examples/applications/example-application/Company.example.md) | `<Track>/<Company>.md` | Research — links, checks, the requirement→evidence map, the verbatim listing |
| [`application.example.json`](../examples/applications/example-application/application.example.json) | `<Track>/application.json` | The machine record — apply URL, pay verdict, status, applicants |
| [`theme.example.json`](../examples/applications/example-application/theme.example.json) | `<Track>/theme.json` | The company-derived palette — with split accent runs when two people apply |

---

## Build it

```bash
/make-resume <user> storage/applications/<Track>
```

One command runs the routine end to end: capture the apply link → verify remote + pay →
**gap-check and ask** → research the company → derive a theme from their real brand CSS →
write → export light + dark for both documents → merge the bundle → log it.

📖 [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.md) — and it is
**agent-agnostic**: plain markdown, no vendor APIs. Any assistant, or a human with a terminal,
can follow it.

## Then log it — three places

1. `<Track>/application.json` — the machine record
2. `storage/applications/README.md` — the human index, with the status and any ⚠ caveat
3. `<Track>/<Company>.md` — the status line + the materials index

*A finished application nobody can find in a month wasn't finished.*

## Principles

- **Source-backed only** — a tailored résumé never claims anything not in the vault.
- **Employer-specific framing lives in the cover letter**, never in the résumé body.
- **No auto-submission, ever.** The tool prepares; the human submits.
