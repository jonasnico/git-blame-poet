"""Parse git blame output into structured data."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field


@dataclass
class BlameLine:
    commit: str
    author: str
    date: str
    line_number: int
    content: str


@dataclass
class BlameResult:
    file_path: str
    lines: list[BlameLine] = field(default_factory=list)

    @property
    def authors(self) -> list[str]:
        return sorted(set(line.author for line in self.lines))

    @property
    def commit_count(self) -> int:
        return len(set(line.commit for line in self.lines))

    def summary(self) -> str:
        """One-line drama teaser."""
        n = len(self.lines)
        a = len(self.authors)
        c = self.commit_count
        return (
            f"{n} lines, {a} author{'s' if a != 1 else ''}, "
            f"{c} commit{'s' if c != 1 else ''}"
        )


# Standard `git blame` line pattern:
#   ^hash (author date line) content
_BLAME_RE = re.compile(
    r"^(?P<commit>[0-9a-f^]+)\s+"
    r"\((?P<author>.+?)\s+"
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?:\d{2}:\d{2}:\d{2}\s+[+-]?\d{4}\s+)?"
    r"(?P<lineno>\d+)\)"
    r"(?P<content>.*)"
)


def parse_blame_text(text: str, file_path: str = "<stdin>") -> BlameResult:
    """Parse raw `git blame` output."""
    result = BlameResult(file_path=file_path)
    for raw_line in text.splitlines():
        m = _BLAME_RE.match(raw_line)
        if not m:
            continue
        result.lines.append(
            BlameLine(
                commit=m.group("commit"),
                author=m.group("author").strip(),
                date=m.group("date"),
                line_number=int(m.group("lineno")),
                content=m.group("content"),
            )
        )
    return result


def run_git_blame(file_path: str, revision: str | None = None) -> BlameResult:
    """Run `git blame` on a file and return structured data."""
    cmd = ["git", "blame", "--date=iso"]
    if revision:
        cmd.append(revision)
    cmd.append("--")
    cmd.append(file_path)

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("Error: 'git' is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"Error running git blame:\n{exc.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    return parse_blame_text(proc.stdout, file_path=file_path)
