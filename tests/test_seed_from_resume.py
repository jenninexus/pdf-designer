"""Local résumé/cover-letter extract builds a reviewable starter draft."""

from pdf_tool.seed_from_resume import draft_from_text, draft_from_uploads

RESUME = """
Alex Rivera
Product Designer
alex@example.studio
https://example.studio

SUMMARY
Local-first document systems for honest applications.

EXPERIENCE
Product Designer — Example Studio
2022 – Present
- Shipped a résumé studio with light and dark PDFs
- Kept personal vaults off GitHub

SKILLS
HTML, CSS, Python, Playwright

EDUCATION
B.A. Design, Example University
"""

COVER = """
Dear Hiring Manager,

I would like to join your document-systems team.

Sincerely,
Alex Rivera
"""


def test_draft_extracts_contact_jobs_and_skills():
    draft = draft_from_text(resume_text=RESUME, filenames=["alex-resume.txt"])
    assert draft["displayName"] == "Alex Rivera"
    assert draft["slug"] == "alex-rivera"
    assert draft["email"] == "alex@example.studio"
    assert draft["web"].startswith("https://example.studio")
    assert draft["jobs"]
    assert draft["jobs"][0]["org"] == "Example Studio"
    assert draft["jobs"][0]["role"] == "Product Designer"
    assert any("HTML" == row["claim"] for row in draft["skills"])
    assert "inferred" in draft["source"]


def test_cover_letter_is_notes_not_employment():
    draft = draft_from_uploads(
        [
            {"name": "cover-letter.txt", "kind": "cover-letter", "text": COVER},
        ]
    )
    assert "Hiring Manager" in draft["coverLetterNotes"]
    assert draft["warnings"]
    assert not draft["jobs"]


def test_combined_resume_and_cover_keeps_jobs():
    draft = draft_from_uploads(
        [
            {"name": "alex-resume.txt", "text": RESUME},
            {"name": "alex-cover-letter.txt", "text": COVER},
        ]
    )
    assert draft["jobs"][0]["org"] == "Example Studio"
    assert "Sincerely" in draft["coverLetterNotes"]
