from __future__ import annotations

from pathlib import Path

from codewiki.list_orphans import find_orphans


def _write(p: Path, body: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)


def test_orphan_is_page_with_no_inbound_link(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "index.md", "# idx\n- [[modules/auth]]\n")
    _write(wiki / "modules/auth.md", "# auth\nsee [[concepts/security]]\n")
    _write(wiki / "concepts/security.md", "# sec\n")
    _write(wiki / "modules/orphan.md", "# nobody links here\n")
    assert find_orphans(wiki) == [wiki / "modules/orphan.md"]


def test_index_and_log_are_never_orphans(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "index.md", "# idx\n")
    _write(wiki / "log.md", "# log\n")
    assert find_orphans(wiki) == []


def test_markdown_links_count_as_inbound_too(tmp_path: Path) -> None:
    wiki = tmp_path
    _write(wiki / "index.md", "# idx\n- [auth](modules/auth.md)\n")
    _write(wiki / "modules/auth.md", "# auth\n")
    assert find_orphans(wiki) == []
