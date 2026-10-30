#!/usr/bin/env python3
"""Create a minimal, reviewable browser-helper profile from a local person file."""
import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*\Z")


def extract(person):
    """Only copy directly confirmed fields; never infer names or addresses."""
    if not isinstance(person, dict):
        raise ValueError("Person record must be an object")
    contact = person.get("contact", {})
    if not isinstance(contact, dict):
        raise ValueError("Contact must be an object")
    rules = contact.get("emailRules", {})
    if not isinstance(rules, dict):
        raise ValueError("Email rules must be an object")
    candidates = {"fullName": person.get("name"), "email": rules.get("default"), "website": contact.get("web")}
    fields = {}
    for key, value in candidates.items():
        if isinstance(value, str) and value.strip() and len(value.strip()) <= 500 and not any(ord(c) < 32 for c in value):
            fields[key] = value.strip()
    if not fields:
        raise ValueError("No approved contact fields found")
    return {"version": 1, "fields": fields}


def validate_output(output, user, root=ROOT):
    """Within the checkout, only the user's private resources folder is allowed."""
    root = root.resolve()
    lexical = Path(os.path.abspath(output))
    destination = output.resolve()
    try:
        lexical.relative_to(root)
        was_inside = True
    except ValueError:
        was_inside = False
    try:
        destination.relative_to(root)
        is_inside = True
    except ValueError:
        is_inside = False
    if not was_inside and not is_inside:
        return destination
    private_root = root / "resumes" / user / "resources"
    # Reject symlinks that redirect the allowed tree outside its expected path.
    if private_root.resolve() != private_root:
        raise ValueError("Private resources path must not redirect through a symlink")
    try:
        lexical.relative_to(private_root)
        destination.relative_to(private_root)
    except ValueError:
        raise ValueError("Output inside the checkout must stay in the user's private resources folder")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user", help="Lowercase local user slug")
    parser.add_argument("--output", type=Path, help="Private output path; must not already exist")
    args = parser.parse_args()
    if not SLUG.fullmatch(args.user):
        parser.error("user must be a lowercase slug containing letters, digits, hyphens or underscores")
    source_dir = (ROOT / "users").resolve()
    source = (source_dir / (args.user + ".json")).resolve()
    if source.parent != source_dir:
        parser.error("person file must be inside users/")
    output = args.output or (ROOT / "resumes" / args.user / "resources" / "browser-helper-profile.json")
    try:
        output = validate_output(output, args.user)
        with source.open(encoding="utf-8-sig") as handle:
            profile = extract(json.load(handle))
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(profile, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Export failed: {type(exc).__name__}. Check the input and output paths; existing files are never overwritten.\n")
    print(f"Created {output} ({len(profile['fields'])} fields). Review the file before importing.")


if __name__ == "__main__":
    main()
