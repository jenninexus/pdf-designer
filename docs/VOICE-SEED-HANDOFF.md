# Optional Voice Seed handoff

Voice Seed is an optional **index of a person's public-facing voice card**. It is
not required to create, preview, export, or install a PDF Designer document.
PDF Designer remains the source of truth for application material.

## Ownership

| Information | Source of truth | May be handed off? |
|---|---|---|
| Personality and cross-register preferences | `users/<user>.json#characterVoice` | A deliberately selected, public-safe summary only |
| Résumé and cover-letter tone | `vaults/<user>.json#voice` | A deliberately selected, public-safe summary only |
| Contacts, claims, work history, listings, portfolio asset paths, brand maps | Local workspace files | **Never** |

The handoff is one-way. Editing a Voice Seed card does not edit the local person or
vault record; the owner changes those records first, then deliberately replaces the
public card.

## Product gate

Offer this only after the future guided wizard has a valid local `characterVoice` and
vault `voice` block. The wizard must make **Skip** the default-safe choice and must
work completely when Voice Seed is absent.

Before writing a card, show the exact proposed contents and require a human approval.
No network request, account, renderer dependency, or background sync is permitted.

## Minimal public card

```json
{
  "schemaVersion": 1,
  "kind": "pdf-designer-voice-card",
  "displayName": "Example Person",
  "summary": "Clear, practical, and warm.",
  "writing": {
    "signatureMoves": ["Lead with the useful point", "Use concrete language"],
    "avoid": ["empty hype", "unfounded claims"]
  },
  "provenance": {
    "source": "Owner-approved PDF Designer summary",
    "approvedAt": "YYYY-MM-DD"
  }
}
```

Allowed fields are the display name or pseudonym, a short non-biographical summary,
and owner-approved writing preferences. Do not include email addresses, employers,
dates, credentials, client names, samples, social handles, local paths, or IDs.

## Implementation contract for the future wizard

1. Read only the two local voice blocks.
2. Construct the minimal card in memory; redact anything outside the schema.
3. Let the owner edit the summary, inspect the final JSON, and approve or cancel.
4. Save or copy the card only to the owner-selected local Voice Seed location.
5. Record no secret, access token, or remote endpoint.

If Voice Seed is unavailable, the wizard displays a short explanation and leaves the
PDF Designer workflow unchanged.
