# Application Helper (local prototype)

The Manifest V3 helper stores an explicitly approved profile in this browser and fills selected
ordinary application inputs only after **Review this page**. It never submits an application or
uploads a document. Review field labels and values yourself: even exact labels can be misleading.
No account, billing, Google login, cloud sync, store release or employer-site certification exists.

## Local contact editor

1. In Chrome (`chrome://extensions`) or Edge (`edge://extensions`), enable Developer mode and load
   the clean `browser-extension` directory containing `manifest.json`. Keep Python `__pycache__`
   directories out of an unpacked extension; Chromium rejects reserved underscore directory names.
2. Open the helper's toolbar action and choose **Edit approved contact profile**. It opens a
   separate local extension page, also available through the extension's options.
3. Enter only the first name, last name and contact values you want to disclose. Each field needs
   its own **Approve** check. Changing a value clears its check; unapproved drafts are not saved.
   Missing fields remain blank. A full name is never split into first/last names.
4. Inspect **Exact approved export**, then **Save approved values**. Reopening loads only saved
   approved fields. Uncheck a field and save to remove it. **Remove saved profile** clears all
   extension profile data and this editor's drafts.
5. **Export saved JSON** downloads exactly the saved preview. It is disabled while approvals differ
   from saved data. Keep personal JSON private. Import it through the helper's local JSON picker
   in either browser. Import replaces saved data; invalid imports leave it unchanged. Removal
   cannot erase exported files, browser backups or browser-managed filesystem remnants.

Previously imported values are checked because import already approves that profile. New values
are never checked automatically. Changes saved by another helper page require an editor reload
before saving/exporting and clear open fill reviews. Reload discards unsaved drafts. Storage is
local to the browser profile, without extension sync or encryption against local access.

## Profile schema and migration

The envelope has exactly `version` and `fields`; `fields` contains approved, nonempty values only.
`profile.example.json` is fictional. Never import a vault, rendering profile or application record.

| Fields | Editor and version 2 contract |
|---|---|
| `firstName`, `lastName` | Explicit strings only; never inferred or automatically sourced from a vault. |
| `email`, `phone`, `city`, `region`, `country`, `postalCode` | Optional single-line strings. Email needs a basic address shape without a display name; phone/address correctness remains yours to check. |
| `website`, `linkedin` | Complete HTTP(S) URLs without credentials or whitespace. Ownership, reachability and LinkedIn identity are not verified. |
| `fullName`, `currentTitle`, `currentCompany` | Previously approved imports are preserved as read-only values with removal checkboxes. This contact editor cannot add/edit them or infer career claims. |

Version 2 rejects unknown keys, non-string values, control characters and strings longer than
500 characters. Empty values are omitted. At least one approved value is required; use removal
to clear everything. All fields remain individually optional.

Version 1 remains readable under its original string validation. Opening/importing it never
automatically rewrites storage. **Save approved values** explicitly migrates the selected fields to
version 2, preserving legacy approved name/title/company values unless unchecked. Legacy email/URLs
that fail v2 validation must be corrected or unchecked first; the stored v1 original stays unchanged
until save/removal. Unsupported future versions are rejected without overwriting the saved original.

The optional `python browser-extension/export-profile.py <user>` still creates a v1 private starter
from the person record's name, default email and website only. It never infers separate names or
reads vaults/PDFs. It refuses overwrites and restricts checkout output to that person's private
`resumes/<user>/resources/`. Review the starter yourself before importing/editing it.

## Review and fill

Open the action on an application page, choose **Review this page**, check desired matches, then
**Fill selected fields**. Ctrl+Shift+Y (Command+Shift+Y on macOS) can invoke the action when assigned;
the browser's Extensions menu also exposes it. Repeat review on each page.

Existing values are unchecked. Checking one explicitly consents to overwrite that reviewed value.
Less-specific full-name/title/company matches are also unchecked. Review binds to the tab,
document ID, URL and actual input elements. Changed values/signatures, replaced or unavailable
controls are skipped; changed URLs/documents require review again. Profile changes clear the review.
Browsers may dismiss the action themselves when the tab URL changes.

Same-URL SPA transitions preserving an unchanged control and its signature/value are **not**
reliably distinguished. That remains a separate review-invalidation slice. Native `input` and
`change` events are dispatched, but site frameworks or validation can still reject a value.
Only selected values enter the isolated script; site scripts can observe their own field values.
Always review the application before manually sending it.

## Compatibility matrix

These are fictional, top-frame native-input patterns, **not proof of named ATS vendors or any
employer's live site**. No portal, account or real applicant data is used.

| Pattern / capability | What works | Manual / unverified |
|---|---|---|
| `fixtures/associated-labels.html` | Exact associated labels, required asterisks, first_name/last_name, email/tel/URL inputs. | Vendor changes, remote validation and actual employer forms. |
| `fixtures/wrapped-labels.html` | Nested native inputs with exact labels, given/family-name autocomplete clues, phone and portfolio aliases. | Dropdowns and work-authorization questions. |
| `fixtures/aria-labels.html` | Native inputs with exact aria-label clues and compatible autocomplete; conflicting name clues are skipped. | aria-labelledby-only matching, custom widgets, shadow DOM and frames. |
| Consent / stale controls | Empty-only defaults; explicit overwrite; changed values/replaced nodes skipped; changed URL/document rejected or action dismissed. | Same-URL unchanged-control transitions and form semantics. |
| Unsupported / sensitive | Hidden, disabled, read-only, file, salary/authorization and ambiguous inputs excluded; top frame only. | Uploads, dropdowns, dates, radio/checkbox answers, demographic/legal/salary/free-text answers, iframes and custom controls. |
| Editor / JSON | Field approval, save/reopen/update/remove, v2 preview/export/import, v1 preservation and explicit migration. | Deliverability, URL ownership, encryption and erasure of external files/backups. |

On 2026-10-30, Windows Chrome 156.0.8078.74 and Edge 156.0.4314.50 passed the editor lifecycle,
v1 migration, downloaded JSON round trip and actual action on all three fixtures above. Each
fixture exercised five contact matches, empty-only defaults, explicit overwrite, native events,
replacement-control rejection and profile-change invalidation, with zero submissions/file changes.
Exact source hashes and acceptance receipts are recorded in the maintainer's active plan. This
supersedes the earlier synthetic baseline for these changed files, without expanding to live sites.

## Permissions and checks

Permissions remain exactly `activeTab`, `scripting`, `storage`: no persistent host permissions,
content scripts, message endpoint, submit/upload path, downloads permission or production network
client. Storage is restricted to `TRUSTED_CONTEXTS` before use; unsupported browsers fail closed.
See [activeTab](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab),
[storage access](https://developer.chrome.com/docs/extensions/reference/api/storage/StorageArea) and
[Edge compatibility](https://learn.microsoft.com/en-us/microsoft-edge/extensions-chromium/developer-guide/port-chrome-extension).

Run `node browser-extension/test-profile.cjs`, `node browser-extension/test-helper.cjs`, and
`python -B -m unittest discover -s browser-extension -p test_export_profile.py`.
For real installed-browser checks, use Playwright and websocket-client in an isolated QA environment:
`python browser-extension/test-browser.py --channel chrome --work-dir <scratch>`, then `--channel msedge`.
Use an interactive Windows desktop. The harness stages exact production bytes, loads them through
Chromium's [unpacked-extension debug API](https://chromedevtools.github.io/devtools-protocol/tot/Extensions/#method-loadUnpacked),
invokes the real action with an OS gesture on its own fixture window, and records browser/source
receipts. It never uses the user's browser profile or submits/uploads a fixture. Preserve textual
evidence and clean owned QA contexts/scratch after the run.
