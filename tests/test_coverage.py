"""Tests for check_vault coverage helpers."""

from pdf_tool.check_vault import extract_requirements, match_requirement

LISTING_FIXTURE = """\
# Example Co — Developer

## Requirements

- Experience shipping titles with proven delivery
- Strong systems design and core development skills
- Proficiency with FictionalToolXYZ (not in vault)

## The listing, verbatim

```
We need someone who can ship titles and write resume claims.
- Must demonstrate systems design experience
- Bonus: knowledge of ObscureFramework 9000
```
"""

CORPUS = [
    ("sk-example", "the claim phrased the way it would actually appear on a resume systems design"),
    ("emp-example", "company name what you did there shipped titles concrete specific evidence"),
]


def test_extract_requirements():
    reqs = extract_requirements(LISTING_FIXTURE)
    assert any("systems design" in r.lower() for r in reqs)
    assert any("shipping titles" in r.lower() or "ship titles" in r.lower() for r in reqs)
    assert any("fictionaltoolxyz" in r.lower().replace(" ", "") or "fictionaltoolxyz" in r.lower() for r in reqs)


def test_match_requirement_covered():
    assert match_requirement("systems design and core development", CORPUS) == "sk-example"
    assert match_requirement("Experience shipping titles with proven delivery", CORPUS) == "emp-example"


def test_match_requirement_unbacked():
    assert match_requirement("Proficiency with FictionalToolXYZ", CORPUS) is None
    assert match_requirement("ObscureFramework 9000 required", CORPUS) is None
