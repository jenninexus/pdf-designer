---
description: Build a tailored, source-backed résumé for one job application. Verifies the apply URL, remote/pay facts, applicant fit, vault coverage, voice, theme, export preferences, QA, and ATS safety. Public seed — copy to make-resume.md for local specifics.
argument-hint: "<user> <application-dir|job-url> [light|dark|full]"
---

# /make-resume — tailored résumé builder (public seed)

This is the clone-safe protocol seed. Copy it to `make-resume.md` (gitignored) if you add personal
applicant routing, machine paths, real employers, or private brand maps. Do not put those details back
into this tracked file.

This command builds the résumé only. Cover letters and work samples are separate opt-in commands:
[`make-cover-letter.example.md`](make-cover-letter.example.md) and
[`make-work-examples.example.md`](make-work-examples.example.md).

## Inputs

```text
/make-resume <user> <application-dir|job-url> [light|dark|full]
```

- `<user>` resolves the private person, vault, and render profile under root nouns (`users/` · `vaults/` · `profiles/`).
- `<application-dir>` is a private folder under `_job-apps/` (aliases `applications/`, `storage/_job-listings/`).
- A pasted job URL creates a new private application folder before any résumé prose is written.
- Export mode never overrides `profiles/<user>-resume.json#exports.exportPrefs` silently.

If an input can be resolved from the current application folder or profile, proceed. Ask only when a
missing choice would materially change the applicant, truth claims, or output set.

## Blocking preflight

Do these in order. Do not begin the résumé until every blocking item is satisfied.

### 1. Capture and verify the listing

Record the direct apply URL, company, role, location/remote policy, compensation, date checked, and
posting status in the private application folder. A company careers index or search result is not an
apply URL.

- No verified apply URL → `BLOCKED — no apply link`.
- Direct posting confirmed gone → `BLOCKED — posting dead`.
- Remote/hybrid/on-site must be stated from evidence, not inferred from a board filter.
- Compare pay with the applicant's private floor and the market before recommending effort.

Follow [`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md). Materials may be prepared, but this
tool never submits an application.

### 2. Confirm the applicant fits the role's spine

Identify the capability the listing repeats. Test the selected applicant against that requirement
before doing layout or theme work. If another applicant/profile is materially stronger, present the
evidence and ask before switching.

Never transfer a studio, partner, or team credit onto an individual unless that person's vault backs
their first-person involvement.

### 3. Load the four private layers

| Layer | Path | Owns |
|---|---|---|
| Person | `users/<user>.json` | Contact, default email, character voice, brand pointer |
| Vault | `vaults/<user>.json` | Every claim that may be made, application voice, role tracks |
| Profile | `profiles/<user>-resume.json` | Layout, theme pointer, `exportPrefs`, work-sample policy |
| Application | `_job-apps/<App>/` | Listing evidence, assessment, application state, generated HTML |

The vault is the truth boundary. Read [`docs/VAULT.md`](../../docs/VAULT.md) before authoring claims.
Use the person's configured default email automatically; another address on record is not permission.

### 4. Validate the vault and voice

```bash
python -m pdf_tool.check_vault --all
python -m pdf_tool.check_vault --explain <user> <track>
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>
```

Non-zero schema or thin-vault results block the build. Load both voice layers:

- `users/<user>.json#characterVoice` — the person.
- `vaults/<user>.json#voice` — the application register.

If the role track changes the lead identity, use the track-specific value. The résumé should sound
like the applicant, not like the employer or a generic assistant.

### 5. Ask before calling anything a gap

The vault records what has been confirmed; it is not the limit of the person's ability. Collect every
unbacked requirement into one concise question.

- If the applicant has it, write a sourced claim into the vault first, then use it.
- If it is confirmed absent, use the closest honest equivalent and keep the limitation explicit.
- `unverified` and `doNotClaim` mean “not yet confirmed,” not “cannot do.”
- Never invent metrics, tenure, titles, tools, clients, or outcomes.

## Build

### 6. Map the evidence

Rank vault-backed evidence against the listing:

1. Role spine and required outcomes.
2. Shipped or measurable proof.
3. Required tools and methods.
4. Supporting breadth.

Employer-specific promises and gap framing belong in a cover letter, not the résumé body. Keep the
résumé reusable, factual, and first-person defensible.

### 7. Derive the company theme

Capture the company's public visual language, then map it into the repository token contract:

`--bg, --surface, --elevated, --text, --dim, --dim2, --border, --border2, --primary, --secondary,
--accent, --support`.

Palette changes may not alter paper size, margins, content, or pagination. Preserve both modes:

- Light = print/ATS file.
- Dark = branded human-facing file.

Run the palette guard during authoring. No brown, mustard, lime, or puke green; see
[`themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md).

### 8. Author the résumé

Follow [`docs/LAYOUT-SYSTEM.md`](../../docs/LAYOUT-SYSTEM.md) and the selected tracked recipe under
`layouts/resume/`.

- US Letter with equal margins on all four edges; default `0.65in`.
- Expected résumé page count comes from the profile/recipe; the default is two pages.
- Every `.page` is a flex column; the signature pins bottom-right.
- Content must fit its page box. Fix overflow by moving or cutting content, never by shrinking margins.
- Prose bullets stay one column and in DOM reading order.
- ATS-critical print body and headings use a system font.
- Use exact machine-readable cues such as `Job Title`, `Work Experience`, and `Education`.

## Export and verify

### 9. Run the ship gate before export is called done

```bash
python -m pdf_tool.check_generation _job-apps/<App>/<resume>.html
```

All checks must pass for every mode being shipped. A source grep or browser preview is not verification.

### 10. Export exactly what `exportPrefs` requests

```bash
# Light / ATS
python -m pdf_tool.html_to_pdf <resume>.html --output-dir storage/<user>/_exports/<App>/

# Dark / branded
python -m pdf_tool.html_to_pdf <resume>.html --pdf-theme dark --output-dir storage/<user>/_exports/<App>/
```

The normal profile contract is light + dark. Do not infer optional cover-letter or work-sample output
from another profile. Go-to reusable packs export into `storage/<user>/defaults/`, beside their HTML,
not `_exports/defaults/`.

### 11. Gate the board file

```bash
python -m pdf_tool.check_ats storage/<user>/_exports/<App>/<resume>-light.pdf
```

Read the extracted text. It must contain contiguous job-title, work-experience, and education cues,
with no shredded mid-word splits. A board's content grade is not the same as parse failure.

Board upload = the light résumé only. Dark PDFs, cover letters, work samples, and merged bundles are
not substitutes for the ATS upload.

### 12. Verify the artifact and log the result

- Confirm the PDF page count from the PDF itself.
- Rasterize and inspect the actual export when layout changed.
- Record generated paths, QA results, posting verification, and the next human action in
  `application.json` and the private application index.
- Use `READY TO SUBMIT` only when the direct apply URL is verified and required files pass their gates.
- The human submits; never auto-submit.

## Public/private contract

Tracked and clone-safe:

- This `*.example.md` seed.
- Engine, layouts, themes, generic docs, and `examples/` fixtures.

Local and gitignored:

- Bare `make-resume.md`, start/wrap ritual, and generated `.codex/` adapters.
- `storage/` vaults, profiles, real listings, brand maps, exports, and private docs.

Architecture: [`docs/PUBLIC-LOCAL-SPLIT.md`](../../docs/PUBLIC-LOCAL-SPLIT.md). Agent contracts:
[`AGENTS.md`](../../AGENTS.md).
