# Generation Rules — the house SSOT for every generated output

**One page. Read it before generating any resume, cover letter, or work-samples for Jenni or Shade.**
These rules apply to **all** generated documents (resume · cover letter · work-samples), for **both**
applicants, in **every** track and company theme. They are the "must always be true" list — the taste
and identity rules that sit above any single job.

| | |
|---|---|
| [Naming & casing](#1-naming--casing--never-all-lowercase) | Our names + company names are never all-lowercase |
| [Images & overlays](#2-images--overlays--no-neon-over-photos) | No neon/primary wash over banners or photos — dark→transparent scrims only |
| [Image framing](#3-image-framing--169-no-crop) | 16:9, show the whole image, don't crop faces/logos |
| [Color](#4-color--house-palette--no-magenta-for-shade) | → `PALETTE-RULES.md` (no brown/mustard/lime; no magenta for Shade/Martian) |
| [Per-user prefs](#5-per-user-quick-reference) | The one-look table: what each person's outputs must obey |
| Related | [`PALETTE-RULES.md`](PALETTE-RULES.md) · [`../docs/VAULT.md`](../docs/VAULT.md) · [`../.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md) |

---

## 1. Naming & casing — NEVER all-lowercase

> **⛔ Our names and business/company names are NEVER rendered all-lowercase in a generated document.**
> (Owner directive 2026-07-20.)

- **People:** `Jenni`, `Shade` — never `jenni`, `shade` in headings, signatures, or body prose.
  (The lowercase `jenni` / `shade` is only ever a **file/user key**, never display text.)
- **Companies / products:** `Martian Games`, `Synagen`, `Synabrain`, `IQO`, `Agency` — never
  `martian games`, `synagen`, etc.
- A **stylized display** (e.g. a wordmark logo image, or an all-**UPPERCASE** `SHADE` header) is fine —
  the ban is specifically on **all-lowercase**.
- **Why this is a hard rule:** some earlier Martian Games resumes rendered the name/company all-lowercase
  and the user **cannot submit those** — it reads as a typo / unprofessional. Any doc with an all-lowercase
  name or company name is a **defect to fix at the source**, not a style choice.

**Check before export:** grep the rendered HTML for a lowercase name/company as a standalone word —
`grep -nE '>\s*(jenni|shade|martian games|synagen)\b' <doc>.html` (in display text; ignore `mailto:`,
URLs, and file paths, which are legitimately lowercase).

---

## 2. Images & overlays — NO neon over photos

> **⛔ Never lay a bright/neon/primary color wash over a banner, hero, or any photographic image.**
> If text must sit on top of an image, use a **black → transparent gradient scrim** (or a dark solid at
> reduced opacity) — never a saturated brand color. (Owner directive 2026-07-20.)

**What went wrong:** a work-samples banner had a bright-pink/neon-primary tint painted over the hero image
(seen in the 2026-07-18 Jenni Netflix work-samples PDFs). It fights the image and looks amateur.

**Do instead — the only approved on-image overlays:**

```css
/* text legibility scrim over a hero/banner image — dark, not colored */
.hero-overlay {
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 100%);
  /* or top-anchored: linear-gradient(0deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.6) 100%) */
}
```

- **Allowed:** `black → transparent` gradients, a **dark** solid at low opacity, a thin brand-colored
  **border/rule** *beside* the image (not washed over it), a small logo/badge chip in a corner.
- **Banned:** any neon/primary/saturated **fill** over an image (pink, cyan, red, violet washes), a
  `mix-blend`/tint that recolors the photo, a colored `::before` covering the image.
- The brand color belongs on **text, rules, borders, and solid panels next to the image** — not painted
  across the image itself.

---

## 3. Image framing — 16:9, no-crop

> **Show the whole image. Frame to 16:9 without cropping off faces, logos, or the subject.**

- Game shots, hero art, and promo thumbnails render in a **16:9** frame. Use
  `object-fit: contain` (letterbox on a dark panel) **or** a genuinely 16:9 source — do **not**
  `object-fit: cover` a non-16:9 image and chop the sides/top off.
- When the art isn't 16:9, **letterbox it on a neutral dark panel** (`#0f0f10`) rather than cropping.
  A slim rounded frame + the dark mat reads intentional; a cropped-off head reads broken.
- **Logos** (e.g. `martiangames-logo-16x9.webp`, `synagen-logo-16-9.png`): size them to **look good, not
  huge** — a tasteful mark, not a page-dominating block. Center on a dark panel with padding; keep the
  logo's own aspect ratio (never stretch).
- Applies to **both** applicants' work-samples Martian-Games galleries and any logo-only panel.

---

## 4. Color — house palette + no magenta for Shade

The color rules live in their own guard-enforced SSOT — **do not duplicate hexes here:**

- **Everyone:** no brown, no mustard, no puke/lime green → [`PALETTE-RULES.md`](PALETTE-RULES.md).
- **Shade + Martian Games only:** **⛔ NO magenta / NO pink** (any theme, any mode). Verify with
  `python -m pdf_tool.check_palette --no-magenta <doc>.html`. Jenni's brand legitimately uses pink, so
  this is brand-scoped, never global.

---

## 5. Per-user quick reference

| Rule | Jenni | Shade |
|---|---|---|
| **Name casing** | `Jenni` — never `jenni` | `Shade` — never `shade` |
| **Company casing** | `Martian Games`, `Synagen`, `Agency` — never lowercase | same — never lowercase |
| **Magenta / pink** | ✅ allowed (her brand) | ⛔ **BANNED** (`--no-magenta`) |
| **Brown / mustard / lime** | ⛔ banned | ⛔ banned |
| **Neon over images** | ⛔ banned — dark scrim only | ⛔ banned — dark scrim only |
| **Work-samples hero** | Agency creative-technologist banner | **Synagen / Martian** (NOT Agency) — see [`../docs/VAULT.md`](../docs/VAULT.md) § Work-samples |
| **Work-samples page-2** | Agency agent grid (hers) | **Shipped Multiplayer Games** + Synagen promo thumbs — **no** agency grid |
| **Default brand theme** | `storage/brand-design/brand-jenninexus.json` | `storage/brand-design/brand-synagen.json` (violet + cyan) |

## Enforcement — one QA command

Every rule on this page is checked by **`python -m pdf_tool.check_generation <doc>.html`** — the single QA
gate (palette · rgba-magenta · casing · overlay · signature-pin · equal-margins · overflow), per-user and
per-doc aware. Run it before shipping any generation; exit 1 = a rule failed. Full map: [`../docs/QA.md`](../docs/QA.md).

When you touch generation code or a template and discover a new taste rule, fold it into **this file**
(the human SSOT) **and** add a check to `check_generation` (the machine SSOT) so it can't regress.
