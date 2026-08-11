# The Vault — how this repo learns about us, and how to write from it

**Read this before authoring any resume or cover letter.** It is agent-agnostic: Claude,
Codex, Cursor, or a human should all be able to work from this page alone.

> **Tracked protocol** (this file). Private data lives under gitignored `storage/`.
> Layout + brand SSOT: [`STORAGE.md`](STORAGE.md). Job capture: [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md).
> Engineering next-steps (one active plan): [`../Plans/_Active/2026-07-21-next-agent-product-prompt.md`](../Plans/_Active/2026-07-21-next-agent-product-prompt.md).

---

## What "the vault" is

**The vault = `storage/<user>/resume-source.json`.** One per person:

| Person | Vault |
|---|---|
| Jenni | `storage/jenni/resume-source.json` |
| Shade | `storage/shade/resume-source.json` |

It is the **permanent career database** — the single source of truth for everything that
person may truthfully claim. It holds skills, employment, clients, credits, education,
metrics, *and their writing voice*.

> **A resume is a QUERY against the vault, not a copy of it.**
> You select the claims that fit the job, rewrite them in that job's vocabulary, and
> **leave the rest out.** A resume that dumps the whole vault is a bad resume.

### The four layers (don't confuse them)

| Layer | File | Answers |
|---|---|---|
| **Person** | `users/<user>.json` | *Who is applying* — contact, emails, brand palette, **`characterVoice`** (personality / contrast / register map), quick `hardFacts` |
| **Vault** ⭐ | `<user>/resume-source.json` | *What may be truthfully claimed* · *how application prose sounds* (`voice`) · *the angle for each role track* |
| **Profile** | `profiles/<user>-resume.json` | *How it renders* — layout, exports, cover-letter policy (voice = pointer only) |
| **Application** | `_job-listings/<Track>/` | *The job* — listing, apply link, pay, company palette |

**Voice is two layers (hybrid SSOT):**

| Edit… | File | For |
|---|---|---|
| Personality, partner contrast, emoji prefs, social/Discord pointers | `users/<user>.json#characterVoice` | Who they are; how they differ; where other registers live |
| Tone, signatureMoves, avoid, leadIdentityByTrack, resume vs coverLetter | `<user>/resume-source.json#voice` | How résumés and cover letters *sound* |

Socials `format-manifest.json` voice strings and bot STYLE-SPECs are **marketing registers** — emoji and post format only. Never the application prose SSOT.

> **Network map (not deep edit):** [`C:\Github\voice-seed`](../../voice-seed) holds the human
> voice **map**, public cards (`characters/humans/*.md`), and seed template
> (`templates/character-voice.seed.json`). Deep edit of applicant voice stays in
> **this** repo’s `storage/` (`characterVoice` + vault `voice`). Agency agents are
> fiction — **never** use them as applicant voice.

**One profile per person.** The per-role framing is **not** a separate file — it lives in the vault at
`roleTracks.<track>.angle`. (Per-track profiles were retired 2026-07-13: they duplicated the vault and drifted.)

---

## ⭐ Work-samples / portfolio — PER-USER SSOT (read before building one)

The visual **work-samples / "Additional Documents" portfolio** (`/make-work-examples`) is **not**
generic. Each person declares their OWN portfolio in **two per-user blocks** — never copy another
person's structure or assets:

| Block | File | Declares |
|---|---|---|
| **`workSamples`** | `profiles/<user>-resume.json#workSamples` | Page **structure** (which 3 beats, in what order), build pattern, flagship beats, `referenceBuild` |
| **`portfolio`** | `users/<user>.json#portfolio` | **Asset sources** (`workSampleAssets`: hero/banner, image grids), `flagshipTalkingPoints`, live portfolio links |

> **Hard rule — a work-samples page must be built from the applicant's OWN `workSamples` + `portfolio`.**
> If either block is **missing**, do **not** fall back to another user's page. Stop and author the block
> first (or ask which pieces to feature). Copying jenni's structure onto shade is exactly the bug that put
> **jenni's Agency agent grid** and the **Agency banner** onto a Shade portfolio (2026-07-20).

**Shared vs personal files (assets, not structure):** Martian Games **title stills** live once at
`storage/studio/resources/images/martiangames/` — both people point there via
`portfolio.workSampleAssets.mgGallerySsot`. Agency art stays under `jenni/…`; Synagen logo/engine
shots under `shade/…`. See [`STORAGE.md`](STORAGE.md) § Shared studio assets.

**Per-person content differs by identity — do not blur:**

| | Jenni | Shade |
|---|---|---|
| **Hero / banner** | Agency creative-technologist banner | **Synagen / Martian Games** content (NOT Agency) |
| **Page-2 showcase** | Agency agentic-AI **agent grid** (she designed it) | **Shipped Multiplayer Games** (Martian Games) — elaborated; **Synagen brand promo thumbnails**. **NO** full agency-agent grid |
| **Flagship** | Synagen (contributed) + Agency + Air Wars/Tank Off | Synagen (**lead dev**) + Shipped multiplayer + AAA tools credits |

Jenni's is the **reference build** and is considered correct/complete — do not change it. Shade's blocks
were added 2026-07-20 to stop the wrong-content recurrence. Reference build + build mechanics:
[`../.claude/commands/make-work-examples.md`](../.claude/commands/make-work-examples.md).

---

## 🧰 A TOOL YOU KNOW IS A TOOL YOU KNOW

**Software claims are selectable from EVERY track.** Not `3d-art` only, not `ui-ux` only — every
track. They carry `kind: "tool"` and `tracks: ["any"]`, and that is deliberate.

**Why:** track tags were being used to answer *"is this relevant to the job?"* when they should
only answer *"can this be selected at all?"* Those are different questions — and conflating them
made real skills **invisible**:

| Before | |
|---|---|
| Shade's `game-dev` track | saw **4 of her 12** software claims |
| Shade's `audio` track | saw **zero** |
| Jenni's `ai` track | saw **2 of 15** |
| 3ds Max, ZBrush | invisible to `game-dev`, `ai`, `synagen` — for **both** of them |

A game-dev listing absolutely may ask *"do you know 3ds Max?"* An AI lab building generative 3D
absolutely cares that you've shipped in Blender. Hiding a tool behind a track tag doesn't make the
résumé focused — it makes it **incomplete**.

**Relevance is the ranking's job, never the tag's.** Each track declares a **`toolbeltOrder`** —
which tools *lead* for that job family. A tool not in that list is still claimable; it just doesn't
open the section.

### What's shared, and what isn't

**Both founders know the same core software** — 3ds Max + V-Ray, Maya, Blender, ZBrush, Character
Creator 4, Unity, Unreal, Photoshop/Adobe CS, Figma, Affinity, NVIDIA, WebGPU. True for Jenni,
true for Shade, true for **Martian Games LLC** as a studio. **Both also worked on Synagen's
development.**

**What is NOT shared is depth and title:**

| | |
|---|---|
| **Shade** | Founder & **CEO**. **Creator and lead developer of Synagen.** May claim it fully. 25 years. |
| **Jenni** | **Co-founder.** *Contributed to* Synagen's development — TRUE. **Never** "created," "lead," "architect," or "principal engineer." 15 years. |
| **The studio** | May claim the engine wholly, and both founders' full toolbelt. |

Full rules: each vault's **`sharedCapabilities`** block. It is the SSOT for this.

> **The trap:** never flatten the two founders into one interchangeable person — and never withhold
> a tool from one of them that they actually know.

---

## 🔎 THE SILENT FAILURE — and the two commands that end it

**The vault's danger is not that it says something false. It is that a true claim goes
*invisible*.** A claim tagged with a track that doesn't exist, or with no track that matches the
job, is simply never selected. Nothing errors. The résumé renders, the page count is right, the
palette passes — and the best evidence its owner has just isn't on the page.

**This has now happened three times:**

| What went invisible | How |
|---|---|
| Five design claims (Photoshop, Figma, Affinity, Adobe CS, UX/UI) | Tagged `ui-ux` on a vault with **no `ui-ux` track**. A UI/UX résumé would have shipped without her entire design toolkit. |
| Five engine claims (WebGPU, multiplayer, WWISE, Unreal/Unity, platforms) | Tagged `game-dev` only — so an **engine-research** résumé built on the `ai` track couldn't see any of them. |
| Two industry-standard tools (Maya, ZBrush) | Sat in `doNotClaim` for months while both applicants had **years** of experience with each. |

**You cannot fix this with discipline.** "Remember to check the vault" is precisely the
instruction that already failed, three times. So it is now a **guard**:

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

> **Why `--suspect` exists.** Substance Painter sat `unverified` in **both** vaults for months
> while both founders had **five years** of production experience with it. Nothing was malformed,
> so `--all` stayed green; nothing matched a listing, so `--coverage` never raised it. It surfaced
> on 2026-07-25 only because a listing happened to name it *and* somebody thought to ask — the same
> way Maya and ZBrush surfaced in July, and four more tools on the Colour X build. **A fact with no
> routine that re-examines it will go stale silently.** Verified against a reconstructed pre-fix
> vault: `--suspect shade Sony.md` flags Substance Painter + Designer URGENT and correctly ignores
> Houdini/Rhino/SketchUp. Run it per application, and periodically without a listing.

---

## 🛑 THE RULE THAT MATTERS MOST — ASK BEFORE YOU CALL SOMETHING A GAP

**The vault is a record of what they have TOLD you. It is not the limit of what they can do.**

Before you write off a single listing requirement as a gap — **ask them.**

> *"The listing asks for X, Y, and Z. I don't have those in the vault. Do you have experience with any of them?"*

One question, up front, costs nothing. Getting it wrong costs the job.

**This has already bitten us twice:**

- **Color X (2026-07-13):** 3ds Max, V-Ray, Unreal, and CC4 apparel authoring were *all* missing from the
  vault — and *all four* turned out to be central to the role. They were nearly written off as gaps.
- **Maya + ZBrush (2026-07-13):** both sat in `doNotClaim` for months. Both founders have used them for
  years. They were forbidden on resumes purely because nobody had asked.

**So:** `doNotClaim` means *"not yet confirmed"*, **not** *"they can't do this."* If a listing needs
something on that list → **ASK FIRST.** If they have it → **write it into the vault** (`source: "owner
directive <date>"`) → **then use it.** Only after asking is something honestly a gap.

**Assume broad competence.** Both founders are advanced across 3D art, modeling, animation, rigging,
character design, game design and development, AI tooling, and their own specialties. When in doubt: ask,
don't assume absence.

---

## 🧍 Whose credit is it? — SUBMISSION-IDENTITY SCOPING

**Owner directive 2026-07-13.** Martian Games is a *studio with two founders*. A studio credit is not
automatically **your** credit. Before citing any client, contract, or shipped title, ask: **who is
submitting, and who actually did the work?**

| Submitting as… | May cite the studio's contract credits (Hasbro, Halfbrick, Oddworld, MetaArcade)? |
|---|---|
| **Jenni, as herself** (her own account, personal resume) | ❌ **NO.** Not in the body, not in "Studio Capabilities," not on a job-board profile — **not even as "our studio."** Those contracts were executed by **Shade**; Jenni had no hands-on role. |
| **Shade** | ✅ Yes — she did the work. |
| **The studio**, or **both founders together** | ✅ Yes — cite as studio contract work. |

**Why so strict:** an interviewer asking *"tell me about the Hasbro project"* must get a real answer.
A credit you can't speak to in the first person is a liability, not an asset — and on a personal
application, even the "our studio" framing invites exactly that question.

Each vault records this in `clients.studioContracts_scoped` (`usableWhen` / `forbiddenWhen`) and in
`doNotClaim.othersCredits`. **`/make-resume jenni` defaults to NOT USING them.**

> **The generalizable rule:** every credit needs an owner. Before it goes on a document, know which
> human performed it and whether that human is the one applying.

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
> **Maya and ZBrush were on this list until 2026-07-13** and both founders had years of experience with
> both. Let that be the cautionary tale.

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
| `studioCapabilities` | What we can *mobilize* (Synagen, the team, distribution) | new studio offering |
| `petCare` *(Jenni)* | Alice / senior-cat / crowdfunding / caregiver tracker — animal-welfare & donor-UX listings | new pet-care product or care detail |
| `doNotClaim` | Tools/claims that are off-limits + honest equivalents | **a tool we're asked for but don't have** |

### Sourcing a new fact

Anything you tell an agent in conversation is a **valid source**. Record it as:

```json
{ "source": "owner directive 2026-07-13", "confidence": "verified" }
```

That's it. Say *"add X to my vault"* and the agent writes it into the right section with
that source. Also acceptable: a live URL (`martiangames.com/about`), a PDF, a repo.

---

## 🧰 The capability matrix — check here BEFORE you assume a gap

**Both founders are advanced 3D generalists.** Shared ground: 3D art, modeling, animation, rigging,
character design, 3D game design and development, and AI tooling. Where they differ is **depth**, not
presence. Full sourced detail is in each vault's `skills` block — this is the at-a-glance check.

| | Jenni | Shade |
|---|---|---|
| **3D / DCC** | 3ds Max + V-Ray · Maya · Blender · ZBrush · Unity · Unreal · Omniverse | same |
| **Characters** | ⭐ **CC4 specialist** — custom apparel, footwear, hair, beauty on hyper-real humans; body + facial rigging; iClone | ⭐ **CC4 specialist** — same |
| **2D / design** | Photoshop · Adobe CS · Figma · Affinity Designer + Publisher · PowerPoint | same |
| **UX / UI** | ⭐ UI implementation in shipped products; design systems | UX partnership (UX Magicians) |
| **Platforms** | mobile · web · **multiplayer web** · PC · **VR** | same — 15 titles, 12 multiplayer |
| **AI** | ⭐ Stable Diffusion, prompt engineering, production AI asset pipeline | ⭐⭐ **Principal ML + Research Scientist / Engineer** — 6 yrs memory HRM / novel RAG / associative & dynamic memory / physical-world modeling for robotic intuition; Synagen productization 3 yrs full-time (multi-agent, MCP, agent-first APIs) |
| **Audio** | ⭐ **VO / narration / game SFX / session engineering** (Audacity · FL Studio · Cool Edit Pro · DJ Pro · DaVinci audio) — voice track go-to | ⭐⭐ **AAA specialty** — composition (SF Conservatory), **3D/spatial**, **reactive**, **WWISE** (*Oddworld: Soulstorm*) |
| **Video** | DaVinci Resolve · OBS · custom in-house tooling | DaVinci Resolve · custom tooling |
| **Art direction** | scene layout, lighting, particles, polish | ⭐ art direction; photoreal ↔ stylized |
| **Engineering** | HTML/SASS/JS · C# · Git · VS Code · Cursor | + PHP, MySQL, Photon, WebGPU, multiplayer architecture |
| **Training** | CalArts-adjacent? **no** — studio-built path, 15 yrs | ⭐ **CalArts** (art, animation, music) · **SF Conservatory** (composition, piano) |
| **Tenure** | **15 years** (joined Dec 2011) | **25 years** (founded the studio, 2000) |

**⚠ The tenure trap.** The studio is **25 years old** (founded 2000). **Jenni's tenure is 15 years.** Both are
true; they are different numbers. Never write anything implying Jenni has 25 years.

**⚠ The audio split (updated 2026-07-24).** AAA spatial / WWISE / reactive middleware depth is **Shade's**.
**Jenni owns** voice acting, narration, game SFX, and session audio engineering — use her **`roleTracks.voice`**
go-to pack (`storage/jenni/defaults/jenni-default-voice-resume.html`) for VO / AI speech-training jobs.
Do **not** put Shade's WWISE/spatial claims on Jenni's résumé.

---

## Role tracks — the job families

Both vaults define these in `roleTracks`, each with a `covers` line and an **`angle`** (what to lead with,
what to demote for that role family). Every claim's `tracks` array says which tracks it serves.

| Track | Covers | Whose |
|---|---|---|
| **`game-dev`** | Game Developer / Designer — Unity, C#, gameplay, multiplayer, level design, shipping. Mobile · web · PC · VR. | both |
| **`3d-art`** | 3D Artist / Animator / Character Artist — modeling, rigging, animation, characters, environments | both |
| **`3d-viz`** | 3D Visualization — archviz, retail, product viz; lighting, materials, composition, photoreal + stylized | both |
| **`ui-ux`** | UI / UX / product design — interface, interaction, design systems | Jenni |
| **`ai`** | Principal ML / Research Scientist *(Shade)* — memory HRM, RAG, agentic systems · applied AI creative pipelines *(Jenni)* | both, different depth |
| **`audio`** | Audio engineer / composer / sound designer — spatial, reactive, WWISE | **Shade only** |
| **`synagen`** | Custom software on the Synagen Engine — bespoke tools, pipelines, WebGPU, AI tooling, team training | both |

### What overlaps (why a new resume is a tweak, not a rebuild)

- **Shared by ALL tracks:** AI-assisted creative pipeline · studio production discipline ·
  Git / clean workflows · collaboration and communication · shipped-product credibility.
- **`game-dev` ∩ `3d-art`:** Unity, Blender, rigging, optimization, shipped titles, iterative cadence.
- **`3d-art` ∩ `3d-viz`:** lighting, materials, composition, **Character Creator 4 characters + apparel**, Blender, 3ds Max + V-Ray.
- **`ai` ∩ `synagen`:** multi-agent orchestration, MCP servers, RAG, agent-first APIs, generative tooling.

**The AI-pipeline cluster is the sleeper.** Listings now ask for it explicitly (Color X asked
twice), and most applicants have nothing real to say. We have years. **Whenever a listing
mentions AI, lead with it.**

**The CC4 apparel cluster is the other one.** Custom clothing, footwear, hair, and beauty on
hyper-real humans — that is *rare*. Any apparel, footwear, fashion, beauty, retail, or
character-driven employer should hear about it early.

---

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
   resume/coverLetter notes). Match both — tone matters as much as the facts. For Shade, also
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
- **Output location:** finished PDFs/PNGs go to **`storage/<user>/_exports/<Application-Dir>/`** —
  never into the application folder (that keeps the listing, `application.json`, `theme.json`, and the
  HTML sources only).
- **Palette:** **no brown, no mustard, no puke/lime green.** Amber cannot be darkened for white paper
  without turning brown — on light, hand the amber role to another hue. Full rule + the guard:
  [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md). Run `python -m pdf_tool.check_palette` before every export.
- **Emails — the default is the default; don't deliberate.** Jenni → **`jenni@jenninexus.com`**.
  Shade → **`shade@martiangames.com`** (that one *is* the studio domain, so it covers her
  studio-voice applications too). Use them on every résumé and letter, automatically, without
  asking. The gmails (`jenninexus@gmail.com`, `martiangames@gmail.com`) are **valid addresses but
  not the preferred ones** — recorded so an agent can *recognize* them (an old résumé, a job-board
  account), **never** to auto-select. Being on file is not permission. Only the person naming one
  in the conversation overrides the default.
- **Clients:** *"contract/outsourced development for Hasbro, Halfbrick, and Oddworld Inhabitants."*
  Never imply employment there. (Kixeye IS genuine prior employment — for **Shade** only.)
- **Tenure:** studio = 25 yrs (founded 2000). Jenni = 15 yrs (joined 2011). Different numbers. Don't blur them.
- **Deliverable:** unless asked otherwise, an application ships **light + dark PDFs for BOTH the resume and
  the cover letter**, plus the **merged FINAL bundle**. PNGs only when asked.

Build an application with **`/make-resume <user> <application-dir>`** — it runs this whole
routine, plus company research, remote/pay verification, theming, export, and the bundle.
The command lives in the repo at [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md).
