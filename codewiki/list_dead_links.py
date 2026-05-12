"""Pages that link to non-existent targets."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_WIKILINK = re.compile(r"\[\[([^\]]+?)\]\]")
_MDLINK = re.compile(r"\]\(([^)]+\.md)(?:#[^)]*)?\)")


def find_dead_links(wiki: Path) -> list[tuple[Path, str]]:
    dead: list[tuple[Path, str]] = []
    for page in sorted(wiki.rglob("*.md")):
        text = page.read_text()
        for m in _WIKILINK.finditer(text):
            target = m.group(1).split("|", 1)[0].strip()
            rel = target if target.endswith(".md") else target + ".md"
            if not (wiki / rel).exists():
                dead.append((page, rel))
        for m in _MDLINK.finditer(text):
            rel = m.group(1).strip()
            if not (page.parent / rel).resolve().exists():
                dead.append((page, rel))
    return dead


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 -m codewiki.list_dead_links <wiki_dir>", file=sys.stderr)
        return 2
    for page, target in find_dead_links(Path(argv[1])):
        print(f"{page}\t{target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
