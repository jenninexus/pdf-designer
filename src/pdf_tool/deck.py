"""Build editable, browser-native 16:9 presentation starter decks.

The output is semantic HTML/CSS that can be edited directly and exported with
``python -m pdf_tool.html_to_pdf``. It does not create PPTX files or charts.

Usage::

    python -m pdf_tool.deck --list-starters
    python -m pdf_tool.deck --starter pitch --output pitch.html
    python -m pdf_tool.deck --starter status --output status.html --input content.json
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


MAX_SLIDES = 20
MAX_TEXT_CHARS = 1200
SLIDE_KINDS = {
    "title", "statement", "two-column", "process", "timeline", "metrics",
    "team", "quote", "closing",
}
SLIDE_FIELDS = {
    "title": {"title", "subtitle", "eyebrow"},
    "statement": {"title", "body", "tag"},
    "two-column": {"title", "leftTitle", "left", "rightTitle", "right"},
    "process": {"title", "steps"},
    "timeline": {"title", "events"},
    "metrics": {"title", "items", "footer"},
    "team": {"title", "members"},
    "quote": {"title", "quote", "by", "source"},
    "closing": {"title", "body", "meta"},
}
OBJECT_FIELDS = {
    "steps": {"title", "body"},
    "events": {"date", "title", "body"},
    "items": {"value", "label", "note"},
    "members": {"name", "role", "bio"},
}

STARTERS: dict[str, dict[str, Any]] = {
    "pitch": {
        "title": "Pitch deck",
        "subtitle": "A clear story for a product, venture, or initiative",
        "slides": [
            {"kind": "title", "title": "[Your company or product]", "subtitle": "[One-line value proposition]", "eyebrow": "PITCH · [DATE]"},
            {"kind": "statement", "title": "The problem is worth solving", "body": "[Describe who experiences the problem and when. Use evidence you can support.]", "tag": "THE OPPORTUNITY"},
            {"kind": "two-column", "title": "A better way to get the job done", "leftTitle": "Today", "left": ["[Current workaround]", "[Cost or friction, with source]"], "rightTitle": "With [your product]", "right": ["[What changes for the user]", "[Why this approach is different]"]},
            {"kind": "process", "title": "How it works", "steps": [{"title": "Discover", "body": "[First user action]"}, {"title": "Deliver", "body": "[Core product experience]"}, {"title": "Improve", "body": "[How feedback makes it better]"}]},
            {"kind": "metrics", "title": "Evidence to date", "items": [{"value": "[Verified value]", "label": "[Metric and period]", "note": "[Source / definition]"}, {"value": "[Verified value]", "label": "[Metric and period]", "note": "[Source / definition]"}, {"value": "[Verified value]", "label": "[Metric and period]", "note": "[Source / definition]"}], "footer": "Replace every prompt with sourced, current evidence."},
            {"kind": "two-column", "title": "A focused path to the market", "leftTitle": "Who starts", "left": ["[First customer segment]", "[How you will reach them]"], "rightTitle": "What unlocks growth", "right": ["[Repeatable acquisition insight]", "[Next proof point to earn]"]},
            {"kind": "team", "title": "People close to the problem", "members": [{"name": "[Name]", "role": "[Role]", "bio": "[Relevant experience or evidence]"}, {"name": "[Name]", "role": "[Role]", "bio": "[Relevant experience or evidence]"}, {"name": "[Name]", "role": "[Role]", "bio": "[Relevant experience or evidence]"}]},
            {"kind": "closing", "title": "Build the next step with us", "body": "[Specific request or decision sought]", "meta": "[Contact · website · date]"},
        ],
    },
    "proposal": {
        "title": "Proposal",
        "subtitle": "A decision-ready plan with scope, value, and next steps",
        "slides": [
            {"kind": "title", "title": "[Proposal name]", "subtitle": "Prepared for [audience] · [date]", "eyebrow": "PROPOSAL"},
            {"kind": "statement", "title": "The decision in front of us", "body": "[State the requested decision and why it matters now. Add a source or constraint.]", "tag": "THE ASK"},
            {"kind": "two-column", "title": "The need and the opportunity", "leftTitle": "Current state", "left": ["[Observed challenge]", "[Who is affected]"], "rightTitle": "Desired outcome", "right": ["[Measurable outcome to agree]", "[Why this approach fits]"]},
            {"kind": "process", "title": "Work plan", "steps": [{"title": "Align", "body": "[Confirm goals, owners, and constraints]"}, {"title": "Deliver", "body": "[Describe the work and review points]"}, {"title": "Learn", "body": "[Evaluate results and recommend next step]"}]},
            {"kind": "timeline", "title": "A practical sequence", "events": [{"date": "[Phase 1]", "title": "Define", "body": "[Scope and decision gate]"}, {"date": "[Phase 2]", "title": "Execute", "body": "[Milestone and owner]"}, {"date": "[Phase 3]", "title": "Review", "body": "[Acceptance and next decision]"}, {"date": "[Phase 4]", "title": "Extend", "body": "[Optional follow-on]"}]},
            {"kind": "two-column", "title": "Scope and investment", "leftTitle": "Included", "left": ["[Deliverable and owner]", "[Review / revision boundary]"], "rightTitle": "Assumptions", "right": ["[Dependency or access needed]", "[Cost, terms, or estimate with basis]"]},
            {"kind": "statement", "title": "A clear first step", "body": "[Name the first action, owner, and date needed to begin.]", "tag": "RECOMMENDATION"},
            {"kind": "closing", "title": "Ready to align on the plan", "body": "[Decision requested]", "meta": "[Contact · proposal valid through date, if applicable]"},
        ],
    },
    "kickoff": {
        "title": "Project kickoff",
        "subtitle": "Align people, outcomes, ways of working, and the first milestone",
        "slides": [
            {"kind": "title", "title": "[Project name]", "subtitle": "Kickoff · [date] · [team or sponsor]", "eyebrow": "LET'S BEGIN"},
            {"kind": "statement", "title": "Why this project, why now", "body": "[Shared context and the change that makes this work timely.]", "tag": "CONTEXT"},
            {"kind": "two-column", "title": "What success means", "leftTitle": "Outcome", "left": ["[User or business outcome]", "[Evidence that will show progress]"], "rightTitle": "Boundaries", "right": ["[In-scope work]", "[Out of scope / constraints]"]},
            {"kind": "team", "title": "Who is in the room", "members": [{"name": "[Name]", "role": "[Decision owner]", "bio": "[Responsibility]"}, {"name": "[Name]", "role": "[Delivery lead]", "bio": "[Responsibility]"}, {"name": "[Name]", "role": "[Partner / reviewer]", "bio": "[Responsibility]"}]},
            {"kind": "process", "title": "How we will work", "steps": [{"title": "Plan", "body": "[Cadence and planning tool]"}, {"title": "Share", "body": "[Review rhythm and decision path]"}, {"title": "Adapt", "body": "[How risks and changes are handled]"}]},
            {"kind": "timeline", "title": "First milestones", "events": [{"date": "[Date]", "title": "Align", "body": "[Milestone / owner]"}, {"date": "[Date]", "title": "Checkpoint", "body": "[Milestone / owner]"}, {"date": "[Date]", "title": "Review", "body": "[Milestone / owner]"}, {"date": "[Date]", "title": "Decide", "body": "[Milestone / owner]"}]},
            {"kind": "two-column", "title": "Risks and open questions", "leftTitle": "Watch", "left": ["[Risk, signal, mitigation owner]", "[Dependency or assumption]"], "rightTitle": "Resolve", "right": ["[Open question and decision owner]", "[When we will revisit]"]},
            {"kind": "closing", "title": "Leave with one next action", "body": "[Name the action, owner, and due date before the team leaves.]", "meta": "[Shared workspace or contact]"},
        ],
    },
    "status": {
        "title": "Project status",
        "subtitle": "A concise view of progress, evidence, risks, and decisions",
        "slides": [
            {"kind": "title", "title": "[Project / program]", "subtitle": "Status update · [reporting period]", "eyebrow": "STATUS"},
            {"kind": "metrics", "title": "At a glance", "items": [{"value": "[RAG / state]", "label": "Overall", "note": "[Definition / as of date]"}, {"value": "[Verified value]", "label": "[Milestone or measure]", "note": "[Source / period]"}, {"value": "[Verified value]", "label": "[Milestone or measure]", "note": "[Source / period]"}], "footer": "Use verified values and define each measure."},
            {"kind": "two-column", "title": "What changed this period", "leftTitle": "Completed", "left": ["[Outcome delivered + evidence]", "[Outcome delivered + evidence]"], "rightTitle": "Next", "right": ["[Next milestone + owner]", "[Target date or dependency]"]},
            {"kind": "timeline", "title": "Milestone view", "events": [{"date": "[Date]", "title": "[Milestone]", "body": "[State · owner]"}, {"date": "[Date]", "title": "[Milestone]", "body": "[State · owner]"}, {"date": "[Date]", "title": "[Milestone]", "body": "[State · owner]"}, {"date": "[Date]", "title": "[Milestone]", "body": "[State · owner]"}]},
            {"kind": "two-column", "title": "Risks needing attention", "leftTitle": "Risk / impact", "left": ["[Risk and likely effect]", "[Evidence or trigger]"], "rightTitle": "Response", "right": ["[Mitigation and accountable owner]", "[Decision needed by when]"]},
            {"kind": "statement", "title": "Decision requested", "body": "[One concrete decision, with options and deadline. If none, say no decision is needed.]", "tag": "FOR [AUDIENCE]"},
            {"kind": "closing", "title": "Next update: [date]", "body": "[The single most important next outcome]", "meta": "[Owner · contact · source link]"},
        ],
    },
    "case-study": {
        "title": "Case study",
        "subtitle": "A source-backed story from challenge to outcome and learning",
        "slides": [
            {"kind": "title", "title": "[Case study headline]", "subtitle": "[Organization or anonymized context] · [date]", "eyebrow": "CASE STUDY"},
            {"kind": "statement", "title": "The starting point", "body": "[Describe the context and challenge. Identify the source and permission for any client details.]", "tag": "CHALLENGE"},
            {"kind": "two-column", "title": "What we learned before acting", "leftTitle": "Signals", "left": ["[Interview / data finding and source]", "[Constraint or user need]"], "rightTitle": "Decision", "right": ["[Chosen approach]", "[Tradeoff and reason]"]},
            {"kind": "process", "title": "The approach", "steps": [{"title": "Focus", "body": "[First intervention]"}, {"title": "Build", "body": "[What was delivered]"}, {"title": "Measure", "body": "[How outcomes were evaluated]"}]},
            {"kind": "metrics", "title": "Observed outcomes", "items": [{"value": "[Verified result]", "label": "[Measure / period]", "note": "[Source / method]"}, {"value": "[Verified result]", "label": "[Measure / period]", "note": "[Source / method]"}, {"value": "[Verified result]", "label": "[Measure / period]", "note": "[Source / method]"}], "footer": "Do not imply causation beyond the available evidence."},
            {"kind": "quote", "title": "In their words", "quote": "[Use an approved, exact quote or replace this slide with a verified observation.]", "by": "[Name / title, with permission]", "source": "[Interview or publication · date]"},
            {"kind": "two-column", "title": "What we would carry forward", "leftTitle": "Repeat", "left": ["[Practice that worked]", "[Condition that enabled it]"], "rightTitle": "Improve", "right": ["[What we would change]", "[Question still open]"]},
            {"kind": "closing", "title": "Apply the learning", "body": "[Specific invitation, next step, or contact]", "meta": "[Source notes · permissions · contact]"},
        ],
    },
    "training": {
        "title": "Training session",
        "subtitle": "Teach a usable skill with examples, practice, and a clear takeaway",
        "slides": [
            {"kind": "title", "title": "[Session title]", "subtitle": "[Audience] · [duration] · [facilitator]", "eyebrow": "LEARN BY DOING"},
            {"kind": "statement", "title": "By the end, you can…", "body": "[Write an observable learning outcome: what participants will do.]", "tag": "LEARNING GOAL"},
            {"kind": "two-column", "title": "The idea and the example", "leftTitle": "Principle", "left": ["[One useful rule]", "[Why it helps]"], "rightTitle": "Example", "right": ["[Concrete scenario]", "[What to notice]"]},
            {"kind": "process", "title": "A repeatable method", "steps": [{"title": "Notice", "body": "[What to observe]"}, {"title": "Choose", "body": "[How to make a decision]"}, {"title": "Try", "body": "[Action and feedback]"}]},
            {"kind": "statement", "title": "Practice: your turn", "body": "[Prompt, timebox, materials, and what participants should produce.]", "tag": "5–10 MINUTES · [PAIR / SOLO]"},
            {"kind": "two-column", "title": "Debrief the practice", "leftTitle": "What worked", "left": ["[Reflection question]", "[Evidence to look for]"], "rightTitle": "Try next", "right": ["[Common pitfall to avoid]", "[Small next experiment]"]},
            {"kind": "quote", "title": "Keep this in mind", "quote": "[A short principle, sourced quotation, or memorable summary written by you.]", "by": "[Attribution or facilitator]", "source": "[Source, if quoted]"},
            {"kind": "closing", "title": "One thing to use this week", "body": "[Concrete transfer action]", "meta": "[Resources · follow-up · contact]"},
        ],
    },
}


def _validate_deck(data: Any) -> dict[str, Any]:
    """Validate a user-supplied deck, rejecting unknown layout/data fields."""
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object")
    if set(data) - {"title", "subtitle", "slides"}:
        raise ValueError("deck fields are limited to title, subtitle, and slides")
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("deck title is required")
    if len(data["title"]) > MAX_TEXT_CHARS:
        raise ValueError(f"deck title exceeds {MAX_TEXT_CHARS} characters")
    if not isinstance(data.get("subtitle", ""), str):
        raise ValueError("deck subtitle must be text")
    if len(data.get("subtitle", "")) > MAX_TEXT_CHARS:
        raise ValueError(f"deck subtitle exceeds {MAX_TEXT_CHARS} characters")
    slides = data.get("slides")
    if not isinstance(slides, list) or not 1 <= len(slides) <= MAX_SLIDES:
        raise ValueError(f"slides must contain between 1 and {MAX_SLIDES} items")
    for index, slide in enumerate(slides, start=1):
        kind = slide.get("kind") if isinstance(slide, dict) else None
        if not isinstance(kind, str) or kind not in SLIDE_KINDS:
            raise ValueError(f"slide {index} kind must be one of: {', '.join(sorted(SLIDE_KINDS))}")
        unknown = set(slide) - ({"kind"} | SLIDE_FIELDS[kind])
        if unknown:
            raise ValueError(f"slide {index} has unsupported fields: {', '.join(sorted(unknown))}")
        if not isinstance(slide.get("title"), str) or not slide["title"].strip():
            raise ValueError(f"slide {index} needs a non-empty title")
        list_fields = {"left", "right"} if kind == "two-column" else set(OBJECT_FIELDS) & set(slide)
        for key, value in slide.items():
            if key == "kind":
                continue
            if key in list_fields:
                if not isinstance(value, list):
                    raise ValueError(f"slide {index} field {key!r} must be a list")
                if len(value) > 8:
                    raise ValueError(f"slide {index} field {key!r} may contain at most 8 items")
                if key in {"left", "right"}:
                    if not all(isinstance(item, str) for item in value):
                        raise ValueError(f"slide {index} field {key!r} must contain only text")
                    text_values = value
                else:
                    object_fields = OBJECT_FIELDS[key]
                    if not all(
                        isinstance(item, dict)
                        and set(item) == object_fields
                        and all(isinstance(item[field], str) for field in object_fields)
                        for item in value
                    ):
                        raise ValueError(
                            f"slide {index} field {key!r} must contain objects with text fields: "
                            f"{', '.join(sorted(object_fields))}"
                        )
                    text_values = [text for item in value for text in item.values()]
                if any(len(text) > MAX_TEXT_CHARS for text in text_values):
                    raise ValueError(f"slide {index} field {key!r} text exceeds {MAX_TEXT_CHARS} characters")
            elif isinstance(value, str):
                if len(value) > MAX_TEXT_CHARS:
                    raise ValueError(f"slide {index} field {key!r} exceeds {MAX_TEXT_CHARS} characters")
            else:
                raise ValueError(f"slide {index} field {key!r} must be text")
    return data


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _list(items: list[str], class_name: str = "") -> str:
    cls = f' class="{_e(class_name)}"' if class_name else ""
    return "<ul" + cls + ">" + "".join(f"<li>{_e(item)}</li>" for item in items) + "</ul>"


def _render_slide(slide: dict[str, Any], number: int) -> str:
    kind = slide["kind"]
    title = _e(slide["title"])
    parts: list[str] = []
    if kind == "title":
        parts.append(f'<div class="title-mark">{_e(slide.get("eyebrow", "PRESENTATION"))}</div>')
        parts.append(f'<h1>{title}</h1><p class="lead">{_e(slide.get("subtitle", ""))}</p>')
    elif kind == "closing":
        parts.append('<div class="closing-mark">NEXT</div>')
        parts.append(f'<h1>{title}</h1><p class="lead">{_e(slide.get("body", ""))}</p>')
        if slide.get("meta"):
            parts.append(f'<p class="meta">{_e(slide["meta"])}</p>')
    elif kind == "statement":
        parts.append(f'<div class="tag">{_e(slide.get("tag", "KEY POINT"))}</div><h2>{title}</h2><p class="statement">{_e(slide.get("body", ""))}</p>')
    elif kind == "two-column":
        parts.append(f'<h2>{title}</h2><div class="columns"><section><h3>{_e(slide.get("leftTitle", ""))}</h3>{_list(slide.get("left", []))}</section><section class="column-accent"><h3>{_e(slide.get("rightTitle", ""))}</h3>{_list(slide.get("right", []))}</section></div>')
    elif kind == "process":
        steps = slide.get("steps", [])
        cells = "".join(f'<article class="step"><div class="step-num">{i:02}</div><h3>{_e(s.get("title", ""))}</h3><p>{_e(s.get("body", ""))}</p></article>' for i, s in enumerate(steps, 1))
        parts.append(f'<h2>{title}</h2><div class="steps">{cells}</div>')
    elif kind == "timeline":
        events = slide.get("events", [])
        cells = "".join(f'<article class="event"><div class="event-date">{_e(x.get("date", ""))}</div><h3>{_e(x.get("title", ""))}</h3><p>{_e(x.get("body", ""))}</p></article>' for x in events)
        parts.append(f'<h2>{title}</h2><div class="timeline">{cells}</div>')
    elif kind == "metrics":
        cards = "".join(f'<article class="metric"><div class="metric-value">{_e(x.get("value", ""))}</div><h3>{_e(x.get("label", ""))}</h3><p>{_e(x.get("note", ""))}</p></article>' for x in slide.get("items", []))
        parts.append(f'<h2>{title}</h2><div class="metrics">{cards}</div>')
        if slide.get("footer"):
            parts.append(f'<p class="footnote">{_e(slide["footer"])}</p>')
    elif kind == "team":
        cards = "".join(f'<article class="person"><div class="avatar">{_e((x.get("name") or "?")[:1].upper())}</div><h3>{_e(x.get("name", ""))}</h3><div class="role">{_e(x.get("role", ""))}</div><p>{_e(x.get("bio", ""))}</p></article>' for x in slide.get("members", []))
        parts.append(f'<h2>{title}</h2><div class="team">{cards}</div>')
    elif kind == "quote":
        parts.append(f'<h2>{title}</h2><blockquote>“{_e(slide.get("quote", ""))}”</blockquote><div class="quote-by">{_e(slide.get("by", ""))}</div><div class="quote-source">{_e(slide.get("source", ""))}</div>')
    content = "".join(parts)
    return f'<section class="slide slide-{_e(kind)}" aria-label="Slide {number}: {title}"><div class="slide-inner">{content}</div><div class="slide-number">{number:02}</div></section>'


def render_html(deck: dict[str, Any]) -> str:
    """Return a standalone, editable HTML presentation source."""
    deck = _validate_deck(deck)
    slides = "\n".join(_render_slide(s, i) for i, s in enumerate(deck["slides"], 1))
    title = _e(deck["title"])
    return f'''<!doctype html>
<html lang="en" data-document-kind="presentation"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
@page {{ size: 13.333333in 7.5in; margin: 0.5in; }}
:root {{ color-scheme: light dark; --paper:#f7f8fb; --ink:#172033; --muted:#596579; --line:#d9deea; --accent:#176b87; --accent-soft:#dff2f5; --panel:#fff; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; font-family:Arial,Helvetica,sans-serif; color:var(--ink); background:#e9edf4; }}
.slide {{ width:1280px; height:720px; margin:28px auto; padding:48px; background:var(--paper); position:relative; overflow:hidden; page-break-after:always; break-after:page; }}
.slide:last-child {{ page-break-after:auto; break-after:auto; }}
.slide-inner {{ height:100%; display:flex; flex-direction:column; justify-content:center; position:relative; z-index:1; }}
h1,h2,h3,p {{ margin-top:0; }} h1 {{ font-size:64px; line-height:1.12; max-width:980px; letter-spacing:-.035em; margin:0 0 22px; }}
h2 {{ font-size:43px; line-height:1.08; letter-spacing:-.025em; max-width:1050px; margin:0 0 36px; }}
h3 {{ font-size:23px; margin:0 0 14px; }} p {{ color:var(--muted); font-size:21px; line-height:1.4; }}
.lead {{ font-size:28px; max-width:900px; }} .title-mark,.tag,.closing-mark {{ color:var(--accent); font-size:15px; font-weight:700; letter-spacing:.14em; margin-bottom:28px; }}
.slide-title {{ background:linear-gradient(125deg,#f7f8fb 0%,#e7f3f6 100%); }}
.slide-title .slide-inner,.slide-closing .slide-inner {{ justify-content:flex-end; padding-bottom:64px; }}
.slide-title h1,.slide-closing h1 {{ max-width:950px; }} .slide-title:before {{ content:""; position:absolute; width:370px; height:370px; border:1px solid #a8c9d2; border-radius:50%; right:70px; top:80px; box-shadow:0 0 0 36px #e9f4f6,0 0 0 37px #c9e0e5,0 0 0 82px #eff7f8,0 0 0 83px #dae9ec; }}
.statement {{ border-left:8px solid var(--accent); padding:8px 0 8px 30px; max-width:1020px; font-size:34px; color:var(--ink); line-height:1.35; }}
.columns {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }} .columns section {{ border-top:3px solid var(--line); background:var(--panel); padding:27px 30px; min-height:250px; }} .columns .column-accent {{ border-color:var(--accent); background:var(--accent-soft); }}
ul {{ padding-left:23px; margin:0; }} li {{ font-size:22px; line-height:1.35; margin:0 0 16px; color:var(--muted); }} li::marker {{ color:var(--accent); }}
.steps {{ display:grid; grid-template-columns:repeat(3,1fr); gap:22px; }} .step {{ border-top:3px solid var(--accent); padding:23px 24px; background:var(--panel); min-height:230px; }} .step-num {{ font-size:18px; font-weight:700; color:var(--accent); margin-bottom:28px; }} .step p,.event p,.person p,.metric p {{ font-size:18px; margin:0; }}
.timeline {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; border-top:2px solid var(--line); padding-top:22px; }} .event {{ position:relative; padding:25px 18px 15px 0; }} .event:before {{ content:""; position:absolute; top:-31px; left:0; width:15px; height:15px; border-radius:50%; background:var(--accent); border:5px solid var(--paper); }} .event-date {{ color:var(--accent); font-size:16px; font-weight:700; margin-bottom:22px; }}
.metrics {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }} .metric {{ padding:29px 24px; border:1px solid var(--line); background:var(--panel); min-height:210px; }} .metric-value {{ font-size:37px; line-height:1.1; font-weight:700; color:var(--accent); margin-bottom:22px; overflow-wrap:anywhere; }} .metric h3 {{ font-size:19px; }} .footnote {{ margin:24px 0 0; font-size:15px; }}
.team {{ display:grid; grid-template-columns:repeat(3,1fr); gap:22px; }} .person {{ text-align:center; padding:26px; background:var(--panel); border-bottom:4px solid var(--accent); }} .avatar {{ display:grid; place-items:center; width:70px; height:70px; border-radius:50%; margin:0 auto 19px; background:var(--accent-soft); color:var(--accent); font-size:28px; font-weight:bold; }} .person h3 {{ margin-bottom:5px; }} .role {{ color:var(--accent); font-size:16px; font-weight:700; margin-bottom:15px; }}
blockquote {{ max-width:1000px; font-size:38px; line-height:1.3; color:var(--ink); margin:0 0 30px; border-left:5px solid var(--accent); padding-left:30px; }} .quote-by {{ font-size:20px; font-weight:bold; }} .quote-source,.meta {{ color:var(--muted); font-size:16px; margin-top:8px; }}
.slide-closing {{ color:#f7f8fb; background:#172033; }} .slide-closing h1,.slide-closing .lead,.slide-closing .meta {{ color:#f7f8fb; }} .slide-closing .closing-mark {{ color:#83c8d5; }} .slide-closing:after {{ content:""; position:absolute; width:520px; height:520px; right:-150px; bottom:-240px; border:1px solid #49717b; border-radius:50%; box-shadow:0 0 0 48px #213c49,0 0 0 49px #34515d; }}
.slide-number {{ position:absolute; right:48px; bottom:27px; font-size:14px; color:var(--muted); font-variant-numeric:tabular-nums; }} .slide-closing .slide-number {{ color:#c0c8d5; }}
@media (prefers-color-scheme:dark) {{ :root {{ --paper:#111827; --ink:#edf2fa; --muted:#b2bfd0; --line:#354258; --accent:#77c9d6; --accent-soft:#1d3742; --panel:#192334; }} body {{ background:#080d15; }} .slide-title {{ background:linear-gradient(125deg,#111827 0%,#172c3a 100%); }} .slide-title:before {{ border-color:#446d79; box-shadow:0 0 0 36px #152d39,0 0 0 37px #294652,0 0 0 82px #132531,0 0 0 83px #243c48; }} .slide-closing {{ --paper:#111827; --ink:#edf2fa; --muted:#b2bfd0; --accent:#83c8d5; }} .slide-closing:after {{ border-color:#49717b; box-shadow:0 0 0 48px #213c49,0 0 0 49px #34515d; }} }}
html[data-pdf-theme="dark"] {{ color-scheme:dark; --paper:#111827; --ink:#edf2fa; --muted:#b2bfd0; --line:#354258; --accent:#77c9d6; --accent-soft:#1d3742; --panel:#192334; }}
html[data-pdf-theme="dark"] body {{ background:#080d15; }}
html[data-pdf-theme="dark"] .slide-title {{ background:linear-gradient(125deg,#111827 0%,#172c3a 100%); }}
html[data-pdf-theme="dark"] .slide-title:before {{ border-color:#446d79; box-shadow:0 0 0 36px #152d39,0 0 0 37px #294652,0 0 0 82px #132531,0 0 0 83px #243c48; }}
html[data-pdf-theme="dark"] .slide-closing {{ --paper:#111827; --ink:#edf2fa; --muted:#b2bfd0; --accent:#83c8d5; }}
html[data-pdf-theme="dark"] .slide-closing:after {{ border-color:#49717b; box-shadow:0 0 0 48px #213c49,0 0 0 49px #34515d; }}
html[data-pdf-theme="light"] {{ color-scheme:light; --paper:#f7f8fb; --ink:#172033; --muted:#596579; --line:#d9deea; --accent:#176b87; --accent-soft:#dff2f5; --panel:#fff; }}
html[data-pdf-theme="light"] body {{ background:#e9edf4; }}
html[data-pdf-theme="light"] .slide-title {{ background:linear-gradient(125deg,#f7f8fb 0%,#e7f3f6 100%); }}
html[data-pdf-theme="light"] .slide-title:before {{ border-color:#a8c9d2; box-shadow:0 0 0 36px #e9f4f6,0 0 0 37px #c9e0e5,0 0 0 82px #eff7f8,0 0 0 83px #dae9ec; }}
@media print {{ html,body {{ background:var(--paper); }} .slide {{ width:auto; height:6.5in; margin:0; padding:0; overflow:hidden; page-break-after:always; break-after:page; }} .slide:last-child {{ page-break-after:auto; break-after:auto; }} .slide-inner {{ padding:0; }} }}
</style></head><body>
<!-- Edit the visible text directly, or create a JSON deck with the documented slide kinds. -->
{slides}
</body></html>'''


def build_deck(starter: str, output: str | Path, input_path: str | Path | None = None) -> Path:
    if starter not in STARTERS:
        raise ValueError(f"unknown starter {starter!r}; choose from {', '.join(STARTERS)}")
    deck = STARTERS[starter]
    if input_path:
        try:
            deck = json.loads(Path(input_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read input JSON: {exc}") from exc
    content = render_html(deck)
    destination = Path(output).resolve()
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against a file appearing after the check.
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starter", choices=sorted(STARTERS), help="story starter to use")
    parser.add_argument("--output", help="new editable HTML file to create; existing files are never replaced")
    parser.add_argument("--input", help="optional JSON deck content (replaces the built-in prompt content)")
    parser.add_argument("--list-starters", action="store_true", help="list the available deck starters")
    args = parser.parse_args(argv)
    if args.list_starters:
        for key, deck in STARTERS.items():
            print(f"{key:12} {deck['title']} — {deck['subtitle']}")
        return 0
    if not args.starter or not args.output:
        parser.error("--starter and --output are required unless --list-starters is used")
    try:
        path = build_deck(args.starter, args.output, args.input)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Saved editable HTML: {path}")
    print("To export PDF: python -m pdf_tool.html_to_pdf <that-file.html>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
