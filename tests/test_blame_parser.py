"""Tests for the blame parser."""

from git_blame_poet.blame_parser import parse_blame_text

SAMPLE_BLAME = """\
a1b2c3d4 (Alice Smith  2025-11-03 14:22:01 +0100  1) def hello():
f5e6d7c8 (Bob Johnson 2026-01-15 09:11:44 +0100  2)     # TODO: fix this hack
a1b2c3d4 (Alice Smith  2025-11-03 14:22:01 +0100  3)     print("hello world")
99887766 (Charlie Dev  2026-03-28 17:45:00 +0100  4)     return 42  # magic number
"""


def test_parse_line_count():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert len(result.lines) == 4


def test_parse_authors():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert result.authors == ["Alice Smith", "Bob Johnson", "Charlie Dev"]


def test_parse_commit_count():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert result.commit_count == 3


def test_parse_content():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert result.lines[0].content.strip() == "def hello():"
    assert result.lines[3].content.strip() == "return 42  # magic number"


def test_parse_dates():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert result.lines[0].date == "2025-11-03"
    assert result.lines[1].date == "2026-01-15"


def test_summary():
    result = parse_blame_text(SAMPLE_BLAME, "hello.py")
    assert result.summary() == "4 lines, 3 authors, 3 commits"


def test_empty_input():
    result = parse_blame_text("", "empty.py")
    assert len(result.lines) == 0
    assert result.authors == []
