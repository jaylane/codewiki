"""Pages with no inbound link from any other page."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_WIKILINK = re.compile(r"\[\[([^\]]+?)\]\]")
_MDLINK = re.compile(r"\]\(([^)]+\.md)(?:#[^)]*)?\)")

_NEVER_ORPHAN = {"index.md", "log.md", "overview.md", "README.md"}


def find_orphans(wiki: Path) -> list[Path]:
    pages = list(wiki.rglob("*.md"))
    referenced: set[Path] = set()
    for p in pages:
        text = p.read_text()
        for m in _WIKILINK.finditer(text):
            target = m.group(1).split("|", 1)[0].strip()
            if not target.endswith(".md"):
                target = target + ".md"
            referenced.add((wiki / target).resolve())
        for m in _MDLINK.finditer(text):
            target = m.group(1).strip()
            referenced.add((p.parent / target).resolve())
    return [
        p
        for p in sorted(pages)
        if p.name not in _NEVER_ORPHAN and p.resolve() not in referenced
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 -m codewiki.list_orphans <wiki_dir>", file=sys.stderr)
        return 2
    for p in find_orphans(Path(argv[1])):
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
