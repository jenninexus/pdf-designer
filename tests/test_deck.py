import json

import pytest

from pdf_tool.deck import STARTERS, build_deck, render_html


def test_builtin_starters_have_distinct_multi_slide_structures():
    assert set(STARTERS) == {"pitch", "proposal", "kickoff", "status", "case-study", "training"}
    signatures = set()
    for deck in STARTERS.values():
        assert len(deck["slides"]) >= 6
        signatures.add(tuple(slide["kind"] for slide in deck["slides"]))
        markup = render_html(deck)
        assert "@page { size: 13.333333in 7.5in; margin: 0.5in; }" in markup
        assert 'html[data-pdf-theme="dark"]' in markup
        assert 'html[data-pdf-theme="light"]' in markup
        assert markup.count('class="slide ') == len(deck["slides"])
    assert len(signatures) == len(STARTERS)


def test_user_content_is_escaped_and_layout_is_not_user_controlled():
    deck = {
        "title": 'A <script>alert("x")</script>',
        "subtitle": "Editable deck",
        "slides": [{"kind": "statement", "title": "Safe", "body": '<img src=x onerror="alert(1)">'}],
    }
    markup = render_html(deck)
    assert "&lt;script&gt;" in markup
    assert "&lt;img" in markup
    assert "onerror=\"alert(1)\"" not in markup
    with pytest.raises(ValueError, match="deck fields"):
        render_html({**deck, "css": "body { display:none }"})
    with pytest.raises(ValueError, match="kind"):
        render_html({"title": "Bad", "slides": [{"kind": "custom", "title": "Unsafe"}]})


def test_input_limits_slide_count_and_text_length():
    with pytest.raises(ValueError, match="between 1 and"):
        render_html({"title": "Too many", "slides": [{"kind": "title", "title": "x"}] * 21})
    with pytest.raises(ValueError, match="exceeds"):
        render_html({"title": "Too long", "slides": [{"kind": "statement", "title": "x", "body": "x" * 1201}]})


def test_malformed_layout_lists_and_empty_slide_titles_are_rejected():
    malformed = [
        {"kind": "two-column", "title": "Bad columns", "left": None, "right": []},
        {"kind": "two-column", "title": "Bad items", "left": [{"text": "unexpected object"}], "right": []},
        {"kind": "process", "title": "Bad steps", "steps": None},
        {"kind": "timeline", "title": "Bad events", "events": ["not an event object"]},
        {"kind": "metrics", "title": "Bad metrics", "items": [{"value": "missing other fields"}]},
        {"kind": "team", "title": "Bad team", "members": [None]},
        {"kind": "statement", "title": "   ", "body": "body"},
    ]
    for slide in malformed:
        with pytest.raises(ValueError):
            render_html({"title": "Validation", "slides": [slide]})


def test_input_json_replaces_prompt_content_and_never_overwrites(tmp_path):
    output = tmp_path / "custom.html"
    source = tmp_path / "deck.json"
    source.write_text(json.dumps({
        "title": "Customer story",
        "subtitle": "A sourced example",
        "slides": [{"kind": "title", "title": "Customer story", "subtitle": "Prepared for review"}],
    }), encoding="utf-8")

    assert build_deck("case-study", output, source) == output.resolve()
    contents = output.read_text(encoding="utf-8")
    assert "Customer story" in contents
    assert "[Case study headline]" not in contents
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        build_deck("pitch", output)
    assert output.read_text(encoding="utf-8") == contents
