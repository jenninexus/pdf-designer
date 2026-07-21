# QA — one gate for every generation

**Run this before shipping any resume, cover letter, or work-samples.** One command checks every house
rule at once, so a generation can't go out with a brown wash, a magenta Shade doc, an all-lowercase name,
a drifting margin, an unpinned signature, or a neon color painted over a photo.

```bash
python -m pdf_tool.check_generation <doc>.html            # auto-detects the user; runs all checks
python -m pdf_tool.check_generation <doc>.html --user shade   # force per-user rules (no-magenta)
python -m pdf_tool.check_generation --scan storage/shade/defaults   # sweep a folder of .html
python -m pdf_tool.check_generation <doc>.html --no-render     # skip the overflow render (fast)
python -m pdf_tool.check_generation <doc>.html --json          # machine-readable
```

**Exit 0 = all pass · exit 1 = one or more FAIL · exit 2 = usage error.** CI-usable.

| | |
|---|---|
| [What it checks](#the-checks) | The 7 rules, and which SSOT owns each |
| [Per-user / per-doc rules](#per-user--per-doc-awareness) | Why Shade fails on magenta but Jenni doesn't |
| [Reading a report](#reading-a-report) | PASS/FAIL/skip and how to fix |
| [When to run](#when-to-run) | Wired into make-resume / make-work-examples |
| Related | [`../themes/GENERATION-RULES.md`](../themes/GENERATION-RULES.md) · [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) · [`LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) |

## The checks

`check_generation` is the **one QA pass**. It composes the existing single-purpose guards and adds the
rules they didn't cover:

| # | Check | Rule | SSOT |
|---|---|---|---|
| 1 | **palette** | no brown / mustard / lime; **+ no magenta/pink for Shade & Martian** | [PALETTE-RULES.md](../themes/PALETTE-RULES.md) |
| 2 | **rgba-magenta** | magenta/pink smuggled in as `rgba()`/`hsl()` — invisible to the hex-only palette guard | GENERATION-RULES |
| 3 | **casing** | names & company names **never all-lowercase** in display text (`jenni`, `shade`, `martian games`, `synagen`, …). Stylized wordmarks like the `jenninexus` logo are allowed | GENERATION-RULES §1 |
| 4 | **overlay** | no bright/neon/primary **fill washed over a banner/hero/photo** — only a black→transparent scrim | GENERATION-RULES §2 |
| 5 | **signature** | resume + work-samples: signature **bottom-pinned, bottom-right** (`margin-top:auto` + `align-self:flex-end`). Cover letter: a sign-off just needs to exist (natural flow) | LAYOUT-SYSTEM.md |
| 6 | **margins** | `@page` margins **equal on all four edges** (one value, or a symmetric v/h pair) — no drift | LAYOUT-SYSTEM.md §Equal margins |
| 7 | **overflow** | no page overflows its print box (the pinned footer won't collide). **Render-based** — needs playwright/pypdfium2; `--no-render` skips it | LAYOUT-SYSTEM.md §content-fit |

Checks 1 and 7 shell out to the standalone `check_palette` / `check_overflow` so there is one
implementation of each rule, not two.

## Per-user / per-doc awareness

The tool detects **who** the doc is for (from the path or the signature/contact) and **what** it is
(resume / cover-letter / work-samples), then applies the right rule set:

- **Shade & Martian** → `no_magenta` is **on** (checks 1 + 2 ban pink). **Jenni** → off (her brand uses pink).
- **Cover letters** → the sign-off flows after the body (not bottom-pinned); check 5 only requires it exists.
- **Resumes / work-samples** → check 5 requires the bottom-right pin.

Override detection with `--user <name>` when the filename doesn't say.

## Reading a report

```
============================================================================
FAIL  storage/shade/…/foo.html   (user=shade, no-magenta=True)
  OK palette       …
  XX margins       equal/consistent @page margins
        - @page margin '0.42in 0.48in 0.48in' is asymmetric (drift) — use equal margins…
  ~ overflow      skipped
```

`OK` passed · `XX` failed (indented lines say exactly what + where) · `~` skipped (`--no-render`).
Fix the source and re-run. **Never override a FAIL** — fix it (a brown hex, a lowercase name, a margin,
an unpinned signature are all cheap to fix and each has bitten a real doc).

## When to run

- **make-resume** step 8 and **make-work-examples** step 4/5 call this as the final gate before an export
  is considered done — it replaces running `check_palette` + `check_overflow` separately.
- **Before any submission**, run it on the final `.html`.
- **After a bulk change** (palette swap, dir move), `--scan storage/<user>/defaults` sweeps the go-to set.

> This tool found and fixed real margin drift in **both** favorite resumes (Shade `0.42/0.48/0.48`,
> Jenni `0.45/0.5/0.55`) the day it was written — exactly the "consistent margin/padding" class of bug
> it exists to catch.
