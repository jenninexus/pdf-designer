"""Tests for check_palette.classify() + is_magenta()."""

from pdf_tool.check_palette import classify, is_magenta


def test_banned_brown():
    verdict, label = classify("8B4513")
    assert verdict == "banned"
    assert "BROWN" in label or "MUSTARD" in label


def test_banned_mustard():
    verdict, label = classify("C4A000")
    assert verdict == "banned"


def test_banned_lime():
    verdict, label = classify("ADFF2F")
    assert verdict == "banned"
    assert "LIME" in label or "PUKE" in label


def test_ok_teal():
    verdict, _ = classify("4fd1c9")
    assert verdict == "ok"


def test_ok_purple():
    verdict, _ = classify("A563D1")
    assert verdict == "ok"


def test_ok_near_black():
    verdict, label = classify("080604")
    assert verdict == "ok"
    assert "near-black" in label


# --- magenta/pink ban (opt-in --no-magenta; shade + martian) ---------------

def test_magenta_flagged():
    # The old Synagen magenta secondary + a hot pink.
    assert is_magenta("E44FD0")   # old dark --secondary
    assert is_magenta("B0187E")   # old light --secondary
    assert is_magenta("FF2E88")   # hot pink
    assert is_magenta("C9186A")   # deep pink


def test_violet_is_not_magenta():
    # The new Synagen palette (violet + blue-violet + cyan) must all pass.
    for hx in ("9B5CF0", "6B6BF0", "4FD8E8", "6D28D9", "3D3FA8", "0E7C8C", "8F9BE8"):
        assert not is_magenta(hx), hx


def test_neutrals_not_magenta():
    for hx in ("ffffff", "0B0510", "2A2230", "808080"):
        assert not is_magenta(hx), hx
