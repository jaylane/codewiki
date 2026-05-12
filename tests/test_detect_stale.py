from __future__ import annotations

import subprocess
from pathlib import Path

from codewiki.detect_stale import find_stale_pages


def _commit_file(repo: Path, rel: str, content: str, msg: str) -> str:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    subprocess.run(["git", "add", rel], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=repo, check=True, capture_output=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _write_page(wiki: Path, rel: str, source_paths: list[str], commit: str) -> Path:
    p = wiki / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    paths_block = "\n".join(f"  - {sp}" for sp in source_paths)
    p.write_text(
        f"---\nkind: module\ntitle: x\nsource_paths:\n{paths_block}\nsource_commit: {commit}\n---\n# x\n"
    )
    return p


def test_no_stale_pages_when_source_unchanged(git_repo: Path) -> None:
    sha = _commit_file(git_repo, "src/auth.py", "x = 1\n", "add auth")
    wiki = git_repo / "wiki"
    _write_page(wiki, "modules/auth.md", ["src/auth.py"], sha)
    assert find_stale_pages(wiki, git_repo) == []


def test_detects_stale_when_source_changed_after_commit(git_repo: Path) -> None:
    sha_a = _commit_file(git_repo, "src/auth.py", "x = 1\n", "add auth")
    wiki = git_repo / "wiki"
    page = _write_page(wiki, "modules/auth.md", ["src/auth.py"], sha_a)
    _commit_file(git_repo, "src/auth.py", "x = 2\n", "change auth")
    assert find_stale_pages(wiki, git_repo) == [page]


def test_detects_stale_when_directory_source_path_changed(git_repo: Path) -> None:
    sha_a = _commit_file(git_repo, "src/pkg/a.py", "a = 1\n", "add a")
    wiki = git_repo / "wiki"
    page = _write_page(wiki, "modules/pkg.md", ["src/pkg/"], sha_a)
    _commit_file(git_repo, "src/pkg/b.py", "b = 2\n", "add b under pkg")
    assert page in find_stale_pages(wiki, git_repo)


def test_pages_without_source_commit_are_skipped(git_repo: Path) -> None:
    wiki = git_repo / "wiki"
    p = wiki / "concepts/idempotency.md"
    p.parent.mkdir(parents=True)
    p.write_text("---\nkind: concept\ntitle: idem\n---\n# x\n")
    assert find_stale_pages(wiki, git_repo) == []
