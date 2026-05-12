"""Tiny YAML-subset parser for wiki page frontmatter.

Handles only what our templates use: scalar key:value, null, inline-list `[a, b]`,
and block-list (`-` items). No nesting, no anchors, no exotic quoting.
"""
from __future__ import annotations

import re
from typing import Any

_FENCE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse(text: str) -> tuple[dict[str, Any], str]:
    m = _FENCE.match(text)
    if not m:
        return {}, text
    return _parse_block(m.group(1)), m.group(2)


def _parse_block(block: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key, rest = key.strip(), rest.strip()
        if rest == "":
            items: list[str] = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith("  -") or lines[j].startswith("\t-")):
                items.append(lines[j].split("-", 1)[1].strip())
                j += 1
            out[key] = items
            i = j
            continue
        out[key] = _scalar(rest)
        i += 1
    return out


def _scalar(s: str) -> Any:
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_scalar(p.strip()) for p in inner.split(",")]
    low = s.lower()
    if low in ("null", "~"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s
