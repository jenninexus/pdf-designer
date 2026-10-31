# Lesson: person-record defaults are annotated instructions, not values

**Trap.** A generator that copies `users/<user>.json#contact.emailRules.default` verbatim into another
data file looks correct in a diff and is wrong at the point of use. That field is an *instruction to
an agent*, e.g.:

```
"owner@example.org — THE DEFAULT, always, until the owner lifts the domain freeze (emailDomainFreeze)."
```

`browser-extension/export-profile.py` copied it into the Form Helper starter, and version 1 profile
validation (which is deliberately lenient, for legacy reads) accepted it. Importing that starter would
have typed the whole sentence into a real employer's Email input — a silent, plausible-looking bad fill
that no test would flag, because the file "validated".

**Root cause.** Two independent, individually reasonable decisions met: person records are written for
human/agent reading (annotations welcome), and legacy version 1 profiles accept strings without shape
checks. Nothing in between enforced that a generated profile had to satisfy the *current* schema.

**Guard now in place.**

- `export-profile.py` emits **version 2** and only values version 2 accepts: it extracts a single bare
  address from an annotated default, refuses to choose when a note contains two addresses, upgrades a
  bare `linkedin.com/in/name` to an explicit HTTPS URL, and drops anything else.
- `test_export_profile.py` covers the annotated, ambiguous, non-URL and credentials-in-URL cases, so a
  regression fails before any browser is opened.
- `docs/BROWSER-HELPER.md` states the rule: the generated starter always imports, and missing values
  stay blank until the owner approves them in the editor.

**Rule for the next generator.** When a derived artifact is consumed by a strict schema, generate to
the strict schema and prove it with a validation call on the finished bytes — never by reasoning that
the source field "obviously" contains the value. Annotate the source freely; sanitize at the boundary.
