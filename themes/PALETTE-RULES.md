# Palette Rules — the house SSOT (color)

The one **color** rule every theme, palette, and export in this repo must satisfy. Enforced by a guard, not by good intentions.

> **Broader generation rules** (name/company casing, no neon over images, 16:9 no-crop framing) live in
> the sibling hub [`GENERATION-RULES.md`](GENERATION-RULES.md). This file is color only.

| | |
|---|---|
| [The rule](#the-rule) | What is banned, verbatim |
| [Why it exists](#why-it-exists-the-amber-trap) | The amber-darkens-to-brown trap |
| [The bands](#the-bands-what-the-guard-enforces) | Exact hue/lightness the guard checks |
| [Run the guard](#run-the-guard) | `check_palette` usage |
| [The fix pattern](#the-fix-pattern) | Hand the amber role to another hue |
| [Limitations](#known-limitations) | What the guard cannot see |
| Related | [`../docs/VAULT.md`](../docs/VAULT.md) · [`../.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md) · [`check_palette.py`](../src/pdf_tool/check_palette.py) |

## The rule

> **No brown. No mustard. No puke/lime green.** Yellow and orange are allowed ONLY as bright, clean tones. Any other green is fine.
>
> **The trap:** darkening amber/gold for white paper TURNS IT BROWN. Amber has no readable dark form on white. On the LIGHT/print palette, give the amber role to ANOTHER HUE from the palette (a blue, teal, or violet). Dark mode keeps the bright amber — it's fine there.

Owner directive, 2026-07-13.

### Plus, for Shade + Martian Games: no magenta / no pink

> **⛔ NO MAGENTA, NO PINK** in any **Shade** or **Martian Games** document — any theme, any mode
> (owner directive 2026-07-20).

**Opt-in, brand-scoped** (Jenni's brand legitimately uses pink, so it's never a global default). Enforced by
the `--no-magenta` flag, which flags the magenta/pink hue band (~290–345°):

```bash
python -m pdf_tool.check_palette --no-magenta <doc>.html   # ALSO ban magenta/pink
```

Shade's Synagen palette (`storage/brand-design/brand-synagen.json`) was rebuilt magenta-free — orchid-**violet**
+ iridescent-**cyan**, heading gradient violet → blue-violet → cyan. The old magenta secondary
(`E44FD0`/`B0187E`) and the magenta-led gradient are gone. If pink ever reappears in a Shade/Martian doc,
replace it with **violet (< 290°)** or **cyan** — never pink. (In the "fix pattern" table below, use a
violet/teal/blue stand-in for Shade/Martian, never the magenta option.)

## Why it exists — the amber trap

A bright amber like `#ffaa00` is gorgeous on a dark background. On white paper it vanishes. The instinct is to darken it for contrast — and that is a **one-way trip into brown**, because amber's only route to darkness *is* brown. This is a color-space fact, not a mistake anyone makes on purpose, so it recurs forever unless something checks.

Real offenders caught in this codebase:

| Hex | Hue | L | What it actually is |
|---|---|---|---|
| `#9A6A05` | 41° | 0.32 | amber darkened → **mustard/brown** |
| `#8A6D0B` | 47° | 0.29 | gold darkened → **mustard** |
| `#b87800` | 39° | 0.36 | MG amber `#ffaa00` darkened → **BROWN** |
| `#d45700` | 25° | 0.42 | MG orange darkened → **burnt brown** |

Each one started life as a legitimate brand color and got "made print-legible." All four are banned.

## The bands — what the guard enforces

`classify()` converts hex → HLS and rejects:

| Band | Condition | Verdict |
|---|---|---|
| Orange–yellow, dark | hue **20–65°** and **L < 0.50** | BROWN/MUSTARD |
| Orange–yellow, dull | hue **20–65°**, **L < 0.58**, **S < 0.60** | MUSTARD |
| Yellow-green | hue **65–100°** — *unconditional* | LIME/PUKE GREEN |
| Olive | hue **100–150°**, **L < 0.35**, **S < 0.55** | OLIVE/PUKE |

**S < 0.18 is skipped as neutral** — greys, near-blacks, and paper white always pass. Everything else (reds, magentas, blues, teals, purples, clean greens) is allowed.

Practical consequence: an orange must stay **either bright (L ≥ 0.50) or below hue 20°**. That's why the Martian light primary is `#c2410c` — hue 17.5°, ducking *under* the band rather than trying to survive inside it.

## Run the guard

From the repo root (the package lives under `src/`, so it needs to be importable):

```bash
python -m pdf_tool.check_palette resume.html          # one or more files
python -m pdf_tool.check_palette --scan storage/      # walk a whole tree
```

Exit **0** = clean. Exit **1** = it prints every offending hex, what it is, the file, and the line. Run it before any export.

## The fix pattern

**On light, hand the amber role to another hue.** Do not darken the amber — reassign the *role*.

The palettes already ship this pattern:

| Theme | Dark warm highlight | → Light stand-in |
|---|---|---|
| `default-resume.json` | `e3b559` gold | `0E6E7A` teal |
| `brand-synagen.json` | `F0B25A` gold | `0E6E7A` teal |
| `brand-martian.json` | molten orange `FF6B00` / hot `FF4500` (live MG; **not** amber) | violet `6d3fd4` (brand purple) — print primary stays orange-RED `c2410c` |
| `brand-jenninexus.json` | `fff06b` yellow | `1D5FA8` blue |

Pick the stand-in from a hue the palette *already contains* (its cyan, its violet, its magenta) so the light document still reads as the same brand — and pick one the sibling tokens aren't already using, so the roles stay visually distinct. Dark mode is untouched for legal bright warms.

**Martian note (2026-07-16):** live `martiangames.com` roles are **primary `#FF6B00` · secondary `#8B5CF6` · accent `#FF4500`** on ember-nebula `#0c0a12` — not amber + teal, and **no brown chrome**. Resume dark tokens mirror `www-theme-kit/profiles/martiangames.json` (+ `#no_brown_rule`). Light secondary stays violet. Private map: `storage/brand-design/brand-martian.json` (gitignored); kit mirror: `www-theme-kit/palettes/resume-palettes.json#martian-resume`. Copilot/Portal/bot: same rule via `syna-theme-kit/profiles/martian-portal.json` + `martian-bot/docs/STYLE-SPEC.md`.

## Known limitations

- **Only 6-digit hex is visible.** `rgba()`, `hsl()`, `hsla()`, named colors, and 3-digit `#abc` are **invisible to the guard**. A brown smuggled in as `rgba(184,120,0,1)` passes silently. Write accents as 6-digit hex so they can be checked.
- **Warm near-black backgrounds false-positive.** `#080604`, `#0f0a06`, `#160e08`, `#1c1209`, `#1a0f08` land in the 20–65° band with low L and get flagged as BROWN. They are backgrounds and ink, not accents; at that lightness no brown is perceptible. Known and accepted — if these are the *only* hits, the file is clean.
- **The guard reads its own docs.** Any `#hex` in a comment or note gets scanned too. Palette-rule notes in JSON therefore write hexes **without** the leading `#`.
- It checks color only — not contrast. A passing hex can still be unreadable; aim for L ≈ 0.28–0.45 on white.
