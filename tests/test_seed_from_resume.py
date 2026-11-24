"""Local résumé/cover-letter extract builds a reviewable starter draft."""

import base64
from io import BytesIO
from xml.sax.saxutils import escape
from zipfile import ZipFile

import pytest

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


def test_word_resume_is_read_from_document_body():
    payload = BytesIO()
    paragraphs = "".join(f"<w:p><w:r><w:t>{escape(line)}</w:t></w:r></w:p>" for line in RESUME.splitlines())
    with ZipFile(payload, "w") as docx:
        docx.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                      f"<w:body>{paragraphs}</w:body></w:document>")
    draft = draft_from_uploads([{"name": "candidate.docx", "contentBase64": base64.b64encode(payload.getvalue())}])
    assert draft["displayName"] == "Alex Rivera"
    assert draft["jobs"][0]["dates"] == "2022 – Present"
    assert len(draft["jobs"][0]["bullets"]) == 2


def test_html_resume_extracts_body_text_and_ignores_scripts():
    draft = draft_from_uploads([{"name": "resume.html", "text": """
      <head><title>Discard this title</title></head>
      <h1>Alex Rivera</h1><p>Product Designer</p>
      <script>incorrect@example.studio</script><p>alex@example.studio</p>
      <h2>Experience</h2><p>Product Designer at Example Studio | 2022 – Present</p>
      <ul><li>Built a reusable résumé.</li></ul><h2>Skills</h2><p>HTML</p>
    """}])
    assert draft["displayName"] == "Alex Rivera"
    assert draft["email"] == "alex@example.studio"
    assert draft["jobs"][0]["org"] == "Example Studio"
    assert draft["jobs"][0]["bullets"] == ["Built a reusable résumé."]


def test_empty_html_directs_user_to_text_fallback():
    with pytest.raises(ValueError, match="No selectable text"):
        draft_from_uploads([{"name": "resume.html", "text": '<img src="scan.png">'}])
