# Document generation rules

Use the selected profile's [render preferences](../profiles/README.md) for heading
case, palette, and page caps. Keep official spelling in prose and credits. The
[example packet recipe](../layouts/application-packet.example.json) describes a
cover letter, résumé, and work examples in that order.

- **Print geometry.** Career documents use US Letter with equal margins on all
  four edges. Check each component in light and dark, then verify the merged
  package's page count and order. [Layout system](LAYOUT-SYSTEM.md)
- **Reading order.** Use selectable system-font text for names, headings, body
  copy, contacts, and signatures. Preserve ordinary reading order and explicit
  separators between contact items. [Document QA](QA.md)
- **Images.** Keep faces, logos, and evidence in frame. Use `object-fit: contain`
  on a dark mat when aspect ratios differ. Use a dark neutral scrim when text
  overlaps imagery. Put strong palette accents on adjacent type or rules.
- **Color.** Check both light and dark tokens and the rendered PDF. Follow
  [palette rules](PALETTE-RULES.md).

Run `python -m pdf_tool.check_generation <document.html>` on each source and
`python -m pdf_tool.check_ats <resume-light.pdf>` for an ATS-oriented résumé.
