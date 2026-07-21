#!/usr/bin/env python3
"""Inline {{img:name}} placeholders in a work-samples template -> self-contained HTML.
Usage: python inline_imgs.py <template.html> <out.html> name=path [name=path ...]"""
import sys, base64, mimetypes, re, os

tpl, out = sys.argv[1], sys.argv[2]
mapping = {}
for arg in sys.argv[3:]:
    k, v = arg.split("=", 1)
    mapping[k] = v

html = open(tpl, encoding="utf-8").read()

def datauri(path):
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "image/webp" if path.lower().endswith(".webp") else "image/png"
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b}"

missing = []
placeholders = set(re.findall(r"\{\{img:([^}]+)\}\}", html))
for ph in placeholders:
    if ph not in mapping:
        missing.append(ph); continue
    p = mapping[ph]
    if not os.path.exists(p):
        missing.append(f"{ph} -> {p} (FILE NOT FOUND)"); continue
    html = html.replace("{{img:%s}}" % ph, datauri(p))

if missing:
    print("MISSING:", missing); sys.exit(1)

# any leftover placeholders?
left = re.findall(r"\{\{img:[^}]+\}\}", html)
if left:
    print("LEFTOVER placeholders:", left); sys.exit(1)

open(out, "w", encoding="utf-8").write(html)
print(f"OK wrote {out} ({len(html)} bytes, {len(placeholders)} images inlined)")
