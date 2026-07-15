"""Tests for check_palette.classify()."""

from pdf_tool.check_palette import classify


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
