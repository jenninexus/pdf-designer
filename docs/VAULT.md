# The Vault — how this repo learns about us, and how to write from it

**Read this before authoring any resume or cover letter.** It is agent-agnostic: Claude,
Codex, Cursor, or a human should all be able to work from this page alone.

> **Tracked protocol** (this file). Private data lives under gitignored root nouns (`users/`,
> `vaults/`, `profiles/`, `resumes/`, `_job-apps/`, `brands/`, and `_exports/`).
> Layout + brand SSOT: [`STORAGE.md`](STORAGE.md). Job capture: [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md).
> Engineering next-steps: [`ROADMAP.md`](ROADMAP.md); `Plans/` is local-only working context (gitignored).

---

## What "the vault" is

**The vault = `vaults/<user>.json`.** One per person:

It is the **permanent career database** — the single source of truth for everything that
person may truthfully claim. It holds skills, employment, clients, credits, education,
metrics, *and their writing voice*.

> **A resume is a QUERY against the vault, not a copy of it.**
> You select the claims that fit the job, rewrite them in that job's vocabulary, and
> **leave the rest out.** A resume that dumps the whole vault is a bad resume.

### Reusable specialist selections and submissions

Each applicant keeps one private vault and one rendering profile. A reusable specialist pack is
a **selection of existing claim IDs**, not another vault, person or employer-specific identity.
An optional `reusableSelections.<specialty>` block may point to a canonical source HTML, profile,
claim IDs, source-selection notes and claim boundaries. Put newly confirmed facts in the vault
before including them; keep source and confidence. A previously generated résumé helps discover
what to check but is not independent proof of its own claims.

Compare older specialist packs and per-person `resources/references/` against the vault. Carry
forward useful supported detail, current contact rules and the applicant's voice. Resolve source
ambiguity explicitly: work in development, research goals, deployed systems and completed training
are different claim levels. Do not infer numerical gains, publications or another person's credit.
Do not combine disputed totals or turn a contract credit into employment at the client.

Keep accepted light/dark exports, their source/dependency hashes and QA receipt with the person's
pack. Review fit per posting, then reuse an unchanged accepted document instead of rebuilding it.
Per-posting `_job-apps/<posting>/application.json` records who submitted, the exact file/hash, date,
method and response evidence; `_job-apps/applied-index.md` is the human roll-up. An export is not
proof of submission. Keep sent versions immutable and generate a new version when facts or fonts
change. Fictional public examples teach this structure without publishing personal records.

### The four layers (don't confuse them)

| Layer | File | Answers |
|---|---|---|
| **Person** | `users/<user>.json` | *Who is applying* — contact, emails, brand palette, **`characterVoice`** (personality / contrast / register map), quick `hardFacts` |
| **Vault** ⭐ | `vaults/<user>.json` | *What may be truthfully claimed* · *how application prose sounds* (`voice`) · *the angle for each role track* |
| **Profile** | `profiles/<user>-resume.json` | *How it renders* — layout, exports, cover-letter policy (voice = pointer only) |
| **Application** | `_job-apps/<Track>/` | *The job* — listing, apply link, pay, company palette |

**Voice is two layers (hybrid SSOT):**

| Edit… | File | For |
|---|---|---|
| Personality, partner contrast, emoji prefs, social/Discord pointers | `users/<user>.json#characterVoice` | Who they are; how they differ; where other registers live |
| Tone, signatureMoves, avoid, leadIdentityByTrack, resume vs coverLetter | `vaults/<user>.json#voice` | How résumés and cover letters *sound* |

Socials `format-manifest.json` voice strings and bot STYLE-SPECs are **marketing registers** — emoji and post format only. Never the application prose SSOT.

The personal `characterVoice` and vault `voice` remain the application voice sources.

**One profile per person.** The per-role framing is **not** a separate file — it lives in the vault at
`roleTracks.<track>.angle`. (Per-track profiles were retired 2026-07-13: they duplicated the vault and drifted.)

---

## Private AI-track records

Keep provider-specific records and task materials private. Publish a provider or partner name only with explicit authorization.

## ⭐ Work-samples / portfolio — PER-USER SSOT (read before building one)

The visual **work-samples / "Additional Documents" portfolio** (`/make-work-examples`) is **not**
generic. Each person declares their OWN portfolio in **two per-user blocks** — never copy another
person's structure or assets:

| Block | File | Declares |
|---|---|---|
| **`workSamples`** | `profiles/<user>-resume.json#workSamples` | Page **structure** (which 3 beats, in what order), build pattern, flagship beats, `referenceBuild` |
| **`portfolio`** | `users/<user>.json#portfolio` | **Asset sources** (`workSampleAssets`: hero/banner, image grids), `flagshipTalkingPoints`, live portfolio links |

**Hard rule:** build each applicant’s work samples from their own profile and assets. Never substitute another applicant’s portfolio; shared resources require separately verified permission and attribution.

---

## 🧰 A TOOL YOU KNOW IS A TOOL YOU KNOW

**Software claims are selectable from EVERY track.** Not `3d-art` only, not `ui-ux` only — every
track. They carry `kind: "tool"` and `tracks: ["any"]`, and that is deliberate.

**Why:** track tags were being used to answer *"is this relevant to the job?"* when they should
only answer *"can this be selected at all?"* Those are different questions — and conflating them
made real skills **invisible**:

For example, a software claim restricted to one track may disappear from another relevant résumé.

A game-dev listing absolutely may ask *"do you know 3ds Max?"* An AI lab building generative 3D
absolutely cares that you've shipped in Blender. Hiding a tool behind a track tag doesn't make the
résumé focused — it makes it **incomplete**.

**Relevance is the ranking's job, never the tag's.** Three different jobs — do not collapse them:

| Field | Job | Example |
|---|---|---|
| `skills` | What may be claimed at all | 3D modeling (craft) *and* Maya (program) |
| `kind: "tool"` | This claim is a **program** | Maya, 3ds Max, Blender |
| `software` | Convenience roster of program **names** so you can collect and find apps | `{name: "Maya", skillId: "sk-maya"}` |
| `toolbeltOrder` | On *this* track, which programs **open** the Tools line | Ranked names, not a second inventory |
| `roleTracks` | Which résumé family you are building | `3d-art`, `game-dev` |

**Do not put “3D Art” or “3D modeling” in `toolbeltOrder`.** That is the track / a craft. Software is additional to skills, never a substitute. Add a new app in `software` + a `skills` claim with `kind: "tool"`; only add it to `toolbeltOrder` if it should *lead* that track.

Each track declares a **`toolbeltOrder`** — which tools *lead* for that job family. A tool not in that list is still claimable; it just doesn't open the section.

### What is shared

Verify each person’s skills and credit independently. A shared studio capability does not transfer a person’s title, tenure, or individual work to another person.

---

## 🔎 THE SILENT FAILURE — and the two commands that end it

**The vault's danger is not that it says something false. It is that a true claim goes
*invisible*.** A claim tagged with a track that doesn't exist, or with no track that matches the
job, is simply never selected. Nothing errors. The résumé renders, the page count is right, the
palette passes — and the best evidence its owner has just isn't on the page.

A claim can disappear when it is tagged only for a different role or refers to an undefined track. Use the guards below to expose thin or unmatched evidence before writing.

```bash
# BEFORE you write a word — what can this résumé even say? (blocks on schema + thin track)
python -m pdf_tool.check_vault --explain <user> <track>

# AFTER listing captured — mechanical requirement → claim map (unbacked = ask first)
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>

# AFTER listing captured — is what the vault SAYS still TRUE? (urgent rows = exit 1, ask first)
python -m pdf_tool.check_vault --suspect <user> <listing.md>
python -m pdf_tool.check_vault --suspect <user>            # periodic health check, no listing

# AFTER light PDF export — what does an ATS parser read?
python -m pdf_tool.check_ats <resume-light.pdf>
```

- **`--explain`** prints every claim the track can reach, in rank order. **Exits 1** on vault
  schema errors or when the **target track is THIN** (< 5 narrative claims + employment + credits).
  **Exits 2** if the vault or track is missing. If something you'd expect is missing from that
  list, it is tagged wrong and will never appear on any résumé. Fix the tags, not the résumé.
- **`--coverage`** extracts requirement bullets from the listing doc (Requirements/Qualifications
  headers + verbatim listing section) and matches them against vault claims reachable on that
  track. **COVERED** = vault-backed. **UNBACKED** = ask before calling it a gap — exit 0 with
  unbacked rows is normal. Exit 1 = thin target track or schema errors. Exit 2 = missing files
  or no requirements found.
- **`--suspect`** ⭐ asks the question the other three do not: **is what the vault says still
  TRUE?** `--all` checks the vault is *well-formed*; `--coverage` checks it *covers this listing*.
  Neither notices a fact that is simply **stale or never confirmed**. This lists every entry that
  should be **re-confirmed**, ranked, and ends with a ready-to-paste question. With a listing it
  reads **only the employer's words** (the verbatim block — not our own "never claimed" notes,
  which would otherwise match every tool we deliberately excluded) and promotes any `unverified`
  tool the listing names to **URGENT → exit 1**, blocking the build until someone asks. It matches
  head words too, because listings rarely write a product name in full. Also reports, non-blocking:
  **undated sources** (provenance you can no longer age) and **thin tracks**.
- **`check_ats`** shows the PDF text layer, word count, a **required-cue checklist**
  (`job title` · `work experience` · `education` must be contiguous), and **mid-word split**
  detection (Montserrat body shreds). Exit 1 if < 40 words, a required cue is missing/split, or
  mid-word splits exceed the threshold. Upload **`*-resume-light.pdf`** to boards. Jobright’s
  content rank is a separate score — see [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) § Tier 4.5.
And `check_vault --all` now validates **every** section — skills, employment, credits, education,
clients. A track typo anywhere is an error, not a silent omission.

> **Why `--suspect` exists:** a valid vault can still contain stale or unconfirmed claims. Recheck relevant entries against the listing and ask the applicant before resolving uncertainty.

---

## 🛑 THE RULE THAT MATTERS MOST — ASK BEFORE YOU CALL SOMETHING A GAP

**The vault is a record of what they have TOLD you. It is not the limit of what they can do.**

Before you write off a single listing requirement as a gap — **ask them.**

> *"The listing asks for X, Y, and Z. I don't have those in the vault. Do you have experience with any of them?"*

One question, up front, costs nothing. Getting it wrong costs the job.

An unconfirmed entry may reflect missing evidence rather than lack of experience.

**So:** `doNotClaim` means *"not yet confirmed"*, **not** *"they can't do this."* If a listing needs
something on that list → **ASK FIRST.** If they have it → **write it into the vault** (`source: "owner
directive <date>"`) → **then use it.** Only after asking is something honestly a gap.

Do not infer lack of experience from missing records.

---

## Whose credit is it? — submission identity

A studio credit is not automatically an individual credit. Check the applicant’s own role and supporting evidence before attributing a client, project or title. Keep identity-specific restrictions in the private vault.

---

## The one hard rule

**SOURCE-BACKED ONLY.** Never write a resume claim that isn't in the vault.

But this is **not** a gag order. The job is to **elaborate persuasively on what genuinely
matches** — take a real skill and show precisely why it's valuable *for this employer*.
That's not spin, it's translation.

| ✅ Do this | ❌ Never this |
|---|---|
| Reframe a real claim in the listing's own words | Add a tool we don't have |
| Draw an honest line from our experience to their need | Invent a number, credit, or client |
| Elaborate on *why* a matching skill matters to them | Imply employment at an outsourcer client |
| Lead with our strongest genuine overlap | Quietly omit a gap they'll discover in week two |
| Name a gap plainly, then pivot to the real equivalent | Claim seniority, awards, or degrees we don't hold |

Each vault ends with a **`doNotClaim`** block — tools **not yet confirmed** (Houdini, Substance,
After Effects, Rhino, SketchUp, Corona, Enscape, IWD) plus their **`honestEquivalents`**.

> **⚠ `doNotClaim` is a "not yet confirmed" list, not a "can't do this" list.** If a listing demands one of
> them, **ask first** (see the rule at the top). Only if they confirm they *don't* have it: put the honest
> equivalent on the resume and name the gap once, plainly, in the cover letter. That honesty has *won* us
> credibility — keep it.
>
> Unconfirmed skills require a fresh question, not an assumption.

---

## Vault structure — where to add things

Every section entry carries `source` (where it's provable) and `confidence`. Most also carry:

- **`tracks`** — which job families this claim serves (see below). `any` = usable everywhere.
- **`strength`** — `lead` (open with it) · `solid` (include when relevant) · `supporting` (only if room).

| Section | What goes here | Add a… |
|---|---|---|
| `identity` | Name, contact, links, title | new email / site |
| `voice` | **How application prose sounds** — tone, signatureMoves, avoid, vsPartner, leadIdentityByTrack / studioPolicy. Personality/contrast live on `users/<user>.json#characterVoice` | new stylistic note |
| `roleTracks` | The job families + each one's **`angle`** (leadWith / demote) and theme mode | a new job family, or a better proven angle |
| `skills.*` | Grouped by domain: `3d-dcc`, `adobe-2d-design`, `ui-ux-design`, `characters-apparel`, `realtime-game`, `art-direction`, `ai-pipeline` / `ai-tooling`, `audio`, `engineering`, `platforms`, `production-craft`, `web-media` | **new tool, software, or technique** |
| `employment` | Real jobs/roles with dates, summary, bullets | **new job or long-term role** |
| `clients` | Studio-level partners, split into `development-partners` and `distribution-platforms`, each with its exact `relationship` | **new client or partner** |
| `credits` | Shipped titles, outsourcer credits, own IP | **new shipped title** |
| `metrics` | Verifiable published numbers (plays, followers, years) | **new public figure** |
| `education` | Schools, programs, training | **new course or credential** |
| `studioCapabilities` | Capabilities supported by evidence | new studio offering |

| `doNotClaim` | Tools/claims that are off-limits + honest equivalents | **a tool we're asked for but don't have** |

### Sourcing a new fact

Anything you tell an agent in conversation is a **valid source**. Record it as:

```json
{ "source": "owner directive 2026-07-13", "confidence": "verified" }
```

That's it. Say *"add X to my vault"* and the agent writes it into the right section with


---

## Capability matrix

Consult each applicant’s private capability matrix and evidence before assuming a gap. Ask the applicant when a needed capability is unconfirmed.

---

## Role tracks — the job families

A vault may define tracks in `roleTracks`, each with a `covers` line and an **`angle`** (what to lead with,
what to demote for that role family). Every claim's `tracks` array says which tracks it serves.

| Track | Covers | Whose |
|---|---|---|
| **`game-dev`** | Game Developer / Designer — Unity, C#, gameplay, multiplayer, level design, shipping. Mobile · web · PC · VR. | per applicant |
| **`3d-art`** | 3D Artist / Animator / Character Artist — modeling, rigging, animation, characters, environments | per applicant |
| **`3d-viz`** | 3D Visualization — archviz, retail, product viz; lighting, materials, composition, photoreal + stylized | per applicant |
| **`ui-ux`** | Select evidence appropriate to this track | Per applicant |
| **`graphic-art`** | Select evidence appropriate to this track | Per applicant |
| **`ai`** | Select evidence appropriate to this track | Per applicant |
| **`audio`** | Select evidence appropriate to this track | Per applicant |
| **`synagen`** | Select evidence appropriate to this track | Per applicant |

### Track overlap

Select shared claims only when supported by the applicant’s vault and relevant to the listing. Avoid assuming a particular skill or project applies to every person.

## How to author a resume from the vault

1. **Read the listing.** Extract its literal vocabulary — those words are the ATS surface.
2. **Pick the track.** Which family is this? Read the vault's **`roleTracks.<track>.angle`** — it tells you
   what to lead with and what to demote. Load `profiles/<user>-resume.json` for layout/export rules.
3. **🛑 Gap-check FIRST.** Any requirement with no vault backing → **ask the user before building**
   (see the rule at the top). If they have it, write it into the vault, *then* use it.
4. **Query the vault — in this order.** Select claims whose `tracks` include that track **or `any`**, then
   rank them:

   > **① track-specific claims before `any` claims · ② then by `strength` (lead → solid → supporting)**

   **Do not sort by `strength` alone.** An `any`+`lead` claim (like the AI-pipeline one) will otherwise
   outrank every claim that is actually *about the job*. Sorted naively, an **audio** résumé opens with
   AI tooling — which is precisely what `voice.leadIdentityByTrack` tells you not to do.

   Then **cut**. Two pages. Choose the best options; do not include everything.
5. **Match their language.** Same skill, their words — a game listing's "asset optimization"
   and an archviz listing's "render efficiency" can be the same vault claim, worded for the reader.
6. **Read voice (both layers).** First `users/<user>.json#characterVoice` (personality,
   contrastWithPartner, sampleLines), then vault `voice` (tone, signatureMoves, avoid,

   read `voice.leadIdentityByTrack` — **her lead identity changes by track.** If either layer
   is missing/thin, ask before inventing tone.
7. **Handle any confirmed gap honestly.** Name it once in the cover letter, pivot to the honest
   equivalent, move on. Never hide it; never fake it.
8. **Resume = company-agnostic** within the track (reusable). **Cover letter = all the
   company-specific content** (their mission, their clients, the gap, the hook).

For prose quality, Claude's creative-writing skills are welcome — **within** these rules.
Persuasion is the goal; fabrication is never the method.

---

## Keeping the vault current

- **When the user states a new capability, credit, client, or number → write it into the
  vault FIRST**, in the right section, sourced as `owner directive <date>`. Then use it.
- **Note vault additions in the wrap-up/task summary** so the next agent sees what was captured.
- **Correct, don't duplicate.** If a fact changes (years of experience, a new title), edit
  the existing entry rather than appending a second version.
- The vault is **gitignored** (`storage/`) — it holds real personal data and never leaves the machine.

## House rules that bite

- **🛑 Ask before you call something a gap.** The one at the top. It's the one we keep learning.
- **Output location:** private finished PDFs/PNGs go to **`resumes/<user>/<Application-Dir>/`** —
  never into the application folder (that keeps the listing, `application.json`, `theme.json`, and the
  HTML sources only — those stay in `_job-apps/<Application-Dir>/`). Go-to packs: `resumes/<user>/`
  flat (HTML stays in `resumes/<user>/defaults/`). `_exports/` is the fallback only.
- **Palette:** **no brown, no mustard, no puke/lime green.** Amber cannot be darkened for white paper
  without turning brown — on light, hand the amber role to another hue. Full rule + the guard:
  [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md). Run `python -m pdf_tool.check_palette` before every export.
- **Emails — the default is the default; don't deliberate.** Read
  `users/<user>.json#contact.emailRules.default` and use that address on every résumé and letter
  automatically. Other addresses on file are recognition/recovery data, **never** permission to
  auto-select them. Only the person naming one
  in the conversation overrides the default.
- **Clients:** represent the exact verified relationship; do not imply direct employment.


- **Deliverable:** unless asked otherwise, an application ships **light + dark PDFs for BOTH the resume and
  the cover letter**, plus the **merged FINAL bundle**. PNGs only when asked.

Build an application with **`/make-resume <user> <application-dir>`** — it runs this whole
routine, plus company research, remote/pay verification, theming, export, and the bundle.
The command lives in the repo at [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md).
