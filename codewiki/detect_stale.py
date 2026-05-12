"""Find wiki pages whose `source_paths` have changed since their `source_commit`."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from codewiki.frontmatter import parse


def find_stale_pages(wiki: Path, repo: Path) -> list[Path]:
    stale: list[Path] = []
    for page in sorted(wiki.rglob("*.md")):
        text = page.read_text()
        fm, _ = parse(text)
        commit = fm.get("source_commit")
        paths = fm.get("source_paths") or []
        if not commit or not paths:
            continue
        if _any_path_changed_since(repo, commit, paths):
            stale.append(page)
    return stale


def _any_path_changed_since(repo: Path, since_sha: str, paths: list[str]) -> bool:
    cmd = ["git", "diff", "--name-only", since_sha, "HEAD", "--", *paths]
    try:
        out = subprocess.run(cmd, cwd=repo, check=True, capture_output=True, text=True).stdout
    except subprocess.CalledProcessError:
        return True  # unknown commit → treat as stale, force re-ingest
    return bool(out.strip())


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python3 -m codewiki.detect_stale <wiki_dir> <repo_dir>", file=sys.stderr)
        return 2
    wiki, repo = Path(argv[1]), Path(argv[2])
    for p in find_stale_pages(wiki, repo):
        print(p.relative_to(repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
