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
document ID, URL, actual input elements and their form owners, plus a single-use isolated-world
token. Profile changes clear the review; errors and fill attempts clear the action's selections.
Changing an input's value or matching clues skips that input, even with overwrite consent.

### Review invalidation boundary

A review lasts at most **five minutes** and can be used only once. Review again after any of:

| Observed trigger | Protection |
|---|---|
| Navigation API `navigate` or `currententrychange` | Invalidates even same-URL `pushState`, `replaceState`, entry-state updates and history traversal. No site history functions are patched. |
| Any light-DOM child-list, text or attribute mutation anywhere in the document | Invalidates replacements, moved controls, changed form ownership/action, changed job/step context and changes reverted before Fill. Unrelated page updates also invalidate conservatively. |
| `popstate`, `hashchange`, `pagehide`, `pageshow`, or document becoming hidden | Invalidates navigation/lifecycle changes and tab switches, including a hidden-then-visible document. |
| URL/document/tab mismatch, changed root, elapsed lifetime or replaced review token | Rejects stale targets and superseded reviews. Unsupported Navigation API or a hidden document cannot be reviewed. |

Pending mutation records are drained synchronously before filling and before every subsequent
write. If a site's input/change handlers mutate the DOM during a batch, later inputs are skipped;
values already written are not rolled back. Page scripts still receive native `input`/`change`
events and can reject or transform a value. Browsers may dismiss the action on navigation/tab
switches; dismissal writes nothing. A visible stale action may keep its displayed matches until
Fill, where validation rejects it and clears the review; this is not a live status indicator.

**Remaining unchanged-DOM limitation:** a site's private JavaScript/server state can change the
meaning of an unchanged form without a Navigation API event, observed light-DOM mutation,
visibility/lifecycle signal, URL change, or changed control value/clues. The helper cannot detect
that transition within the five-minute lifetime. CSSOM-only changes, shadow-root internals,
canvas content and changed event-handler closures are not watched. Property-only value changes
that return to the reviewed value before Fill are also not tracked as a history. The fictional invisible-state
fixture deliberately demonstrates this boundary; it is not a claim of universal SPA safety.
Always inspect the displayed application and review again after a job/step change.

Only selected values enter the isolated fill script; site scripts can observe their own field
values. No main-world bridge, persistent content script or extra permission is used.
Always review the application before manually sending it.

## Compatibility matrix

These are fictional, top-frame native-input patterns, **not proof of named ATS vendors or any
employer's live site**. No portal, account or real applicant data is used.

| Pattern / capability | What works | Manual / unverified |
|---|---|---|
| `fixtures/associated-labels.html` | Exact associated labels, required asterisks, first_name/last_name, email/tel/URL inputs. | Vendor changes, remote validation and actual employer forms. |
| `fixtures/wrapped-labels.html` | Nested native inputs with exact labels, given/family-name autocomplete clues, phone and portfolio aliases. | Dropdowns and work-authorization questions. |
| `fixtures/aria-labels.html` | Native inputs with exact aria-label clues and compatible autocomplete; conflicting name clues are skipped. | aria-labelledby-only matching, custom widgets, shadow DOM and frames. |
| Consent / stale controls | Empty-only defaults; explicit overwrite; single-use expiring review; defined navigation, DOM and lifecycle invalidation. | Invisible state changes described above; no universal SPA/site certification. |
| `fixtures/review-transitions.html` | Fictional same-URL history, step/job context, form/control mutations, navigation and stale-review negative cases. | Actual employer workflows, custom controls and server semantics. |
| Live site: Lightfox Games careers form (2026-10-31) | A real, top-frame form. Its **native text inputs** (Name, Email, Portfolio/Reel URL, LinkedIn URL) are ordinary fillable controls. | Its **custom brand-styled date picker**, **file upload**, **acknowledgment checkboxes**, **free-text note** and **Cloudflare Turnstile** are manual; a submission cannot be automated and the CAPTCHA must not be bypassed. This is one observed site, not vendor certification. |
| Unsupported / sensitive | Hidden, disabled, read-only, file, salary/authorization and ambiguous inputs excluded; top frame only. | Uploads, dropdowns, dates, radio/checkbox answers, demographic/legal/salary/free-text answers, iframes and custom controls. |
| Editor / JSON | Field approval, save/reopen/update/remove, v2 preview/export/import, v1 preservation and explicit migration. | Deliverability, URL ownership, encryption and erasure of external files/backups. |

On 2026-10-30, Windows Chrome 156.0.8078.74 and Edge 156.0.4314.50 passed the editor lifecycle,
v1 migration, downloaded JSON round trip and actual action on all three fixtures above. Each
fixture exercised five contact matches, empty-only defaults, explicit overwrite, native events,
replacement-control rejection and profile-change invalidation, with zero submissions/file changes.
Exact source hashes and acceptance receipts are recorded in the maintainer's active plan. This
supersedes the earlier synthetic baseline for these changed files, without expanding to live sites.

The 2026-10-31 live capture above is a single real site inspected read-only and then filled by the
site's owner under their own direction. It confirms the boundary in the table: only the plain text
inputs are helper-fillable; uploads, custom widgets, legal acknowledgments, free text and the
Turnstile CAPTCHA stay with the human. It is not a general claim that any named ATS vendor works,
and it does not certify any employer's site.

Version 0.3.0 review guards were verified on Windows Chrome 156.0.8078.74 (headed) and Edge
156.0.4314.50 (headless), using each installed browser's real native default action. Each complete
suite passed 26 transition/lifecycle scenarios, all three matching fixtures, editor/JSON lifecycle,
explicit overwrite and profile-change invalidation, with zero submissions/uploads. The invisible-state
case deliberately still fills, proving the documented boundary. Headed Edge also passed the 26 guard
scenarios, but its full suite was intermittently dismissed; no uninterrupted headed Edge receipt is
claimed. Exact production-byte hashes bind the completed receipts to this version.

## Permissions and checks

Permissions remain exactly `activeTab`, `scripting`, `storage`: no persistent host permissions,
content scripts, message endpoint, submit/upload path, downloads permission or production network
client. Storage is restricted to `TRUSTED_CONTEXTS` before use; unsupported browsers fail closed.
See [activeTab](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab),
[storage access](https://developer.chrome.com/docs/extensions/reference/api/storage/StorageArea) and
[Edge compatibility](https://learn.microsoft.com/en-us/microsoft-edge/extensions-chromium/developer-guide/port-chrome-extension).

## CSP and localhost development

The helper's popup and editor are extension pages, even when the reviewed form is on localhost.
Without a CSP override, Manifest V3 applies `script-src 'self'; object-src 'self'`. Keep executable
code in packaged script files; do not add inline handlers, remote scripts or `unsafe-eval` to fix a
test. This is separate from the form page's HTTP/meta CSP and from CORS response headers.
See [Chrome's extension CSP contract](https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy).

| Context | Owning policy | Reusable development approach |
|---|---|---|
| Extension popup/editor | Manifest V3 extension-page CSP; independent of a PHP router | Packaged scripts and function callbacks in automation; preserve the installed-browser receipt. |
| An HTTP form or website on localhost | That app's actual response headers, HTML CSP and local-server configuration | Use its existing router/settings and inspect the actual response; do not invent a second permissive policy for QA. |
| Cross-origin HTTP API read | The endpoint's CORS headers plus the caller's applicable CSP | Reuse the owning API's origin/method rules only if the feature actually needs such a request. |

Website `cors.php` helpers and `server.php`/`router.php` routing can inform an HTTP fixture or site
investigation; they do not override extension CSP. This helper has no production HTTP API client
and does not need a PHP server, localhost host permission or website CORS change. Its fictional
native-form fixtures remain served by the isolated Python test harness. For future selected-site QA,
honor the site's existing local policy and record the effective headers/meta policy separately.

If Playwright reports a CSP error while waiting on the editor, use an actual function callback such
as `page.wait_for_function("() => document.querySelector('#save').disabled")`. Avoid string-evaluating
wait expressions. Diagnose that harness error separately from an application failure. A .NET or
PowerShell out-of-memory dialog is a host/runtime failure and needs its process/stack evidence;
changing web CSP or CORS is not a remedy for it.

## Reproducible checks

Navigation/mutation references: [Navigation events](https://developer.mozilla.org/en-US/docs/Web/API/Navigation/navigate_event) and
[pending mutation records](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/takeRecords).

Run `node browser-extension/test-profile.cjs`, `node browser-extension/test-helper.cjs`, and
`python -B -m unittest discover -s browser-extension -p test_export_profile.py`.
For real installed-browser checks, use Playwright in an isolated QA environment:
`python browser-extension/test-browser.py --channel chrome --work-dir <scratch>`, then `--channel msedge`.
Use an interactive Windows desktop for headed mode, or add `--headless` to avoid desktop-focus
dismissals. Both modes use the installed browser and its real default action. The harness stages
exact production bytes, loads them through
Chromium's [unpacked-extension debug API](https://chromedevtools.github.io/devtools-protocol/tot/Extensions/#method-loadUnpacked),
invokes the real default action with native `Extensions.triggerAction` on its exact fixture tab,
and records browser/source
receipts. It never uses the user's browser profile or submits/uploads a fixture. Preserve textual
evidence and clean owned QA contexts/scratch after the run.
