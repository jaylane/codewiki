"""Entry point for `python3 -m codewiki`."""
from __future__ import annotations

import sys

_HELP = """\
codewiki — helpers for the Claude Code wiki plugin

Usage:
  python3 -m codewiki.detect_stale <wiki_dir> <repo_dir>
  python3 -m codewiki.list_orphans <wiki_dir>
  python3 -m codewiki.list_dead_links <wiki_dir>

See https://github.com/jaylane/codewiki for the slash commands that drive these.
"""


def main(argv: list[str]) -> int:
    sys.stdout.write(_HELP)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
