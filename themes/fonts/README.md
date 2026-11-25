# Local fonts

Add fonts you have permission to use here. Reference them with relative URLs
from your own HTML and keep any license and attribution files alongside the
fonts. For a screen-only accent, put the `@font-face` and its use in
`@media screen`. Use system fonts such as Arial or Helvetica for all text in
light and dark career PDFs, including names, headings, contacts, and signatures.

Job websites can use an applicant tracking system (ATS) to extract text from a
PDF and map it to fields. Extraction needs selectable text with characters that
map correctly to Unicode. Field matching also depends on reading order and
recognizable section headings. A custom font can extract correctly when the
generated PDF maps its characters, but missing mappings or unexpected spacing can
yield garbled words even if the page looks fine. Text flattened into images
requires OCR. [Adobe PDF accessibility guide](https://helpx.adobe.com/acrobat/using/accessibility-features-pdfs.html)
· [Greenhouse resume parsing guide](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse)

Keep experience prose in one column. Before uploading, copy text from the light
PDF into a text editor and check the reading order. Run
`python -m pdf_tool.check_ats <resume-light.pdf>` and review the fields that
the destination site fills. [PDF Designer export verification](../../docs/EXPORTS.md)
