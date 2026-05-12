from __future__ import annotations

from pathlib import Path

from codewiki.list_dead_links import find_dead_links


def _write(p: Path, body: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_reports_wikilink_to_missing_page(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "modules/auth.md", "see [[concepts/idempotency]]\n")
    _write(wiki / "index.md", "# idx\n")
    dead = find_dead_links(wiki)
    assert (wiki / "modules/auth.md", "concepts/idempotency.md") in dead


def test_reports_markdown_link_to_missing_page(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "modules/auth.md", "see [x](../concepts/missing.md)\n")
    dead = find_dead_links(wiki)
    assert (wiki / "modules/auth.md", "../concepts/missing.md") in dead


def test_valid_links_not_reported(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "modules/auth.md", "see [[concepts/security]]\n")
    _write(wiki / "concepts/security.md", "# sec\n")
    assert find_dead_links(wiki) == []
