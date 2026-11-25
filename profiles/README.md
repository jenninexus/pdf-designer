# Render profiles

[`examples.json`](examples.json) is the live Hub profile for the fictional demo. It points to the
runnable templates in [`examples/profiles/`](../examples/profiles/).
Copy [`you-resume.example.json`](you-resume.example.json) to `profiles/<id>-resume.json` to
start a private profile manually. The wizard uses the same seed.

## Set your preferences

The wizard saves the palette, résumé section order, heading case and résumé page limit to the
local profile. It writes the editable starter HTML and later PDFs under `resumes/<id>/` in your
workspace. For an existing profile, edit the JSON directly or tell an agent to save a lasting
preference there. Previously authored HTML keeps its layout and colors until you edit or
regenerate it.

| Profile key | What it controls |
|---|---|
| `layoutPrefs.headingCase` | `as-written` or `uppercase` for titles and headings |
| `layoutPrefs.maxPages` | Limits for `coverLetter`, `resume`, `workSamples` and `packet` |
| `layoutPrefs.applicationPacketRecipe` | Profile-relative path to the public starter or a workspace recipe |
| `layout.variant` | Section order selected in the wizard |
| `theme.preset` | Default preset selected in the wizard |
| `exports.exportPrefs` | Which PDFs and theme variants to deliver |

A one-off request takes precedence for that document. Otherwise, use the profile, then
the recipe defaults. The [example packet](../layouts/application-packet.example.json) sets
the part order and starting geometry. Copy it to `layouts/application-packet.json` for
an ignored shared recipe and update the profiles that use it. The old `profiles/layouts/`
redirect has been retired.

Use the requested palette when specified. Otherwise follow the profile's palette policy
and preset, the person's optional `users/<id>.json#brandTheme.ssot`, then the public default.
Store custom color tokens in the brand map and link to it from the person record.

The [person file](../users/README.md) owns identity, contact details and `characterVoice`.
The [vault](../vaults/README.md) owns evidence and application prose preferences in `voice`.
Keep real records and exports in the local workspace.
