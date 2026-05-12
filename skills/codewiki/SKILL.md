---
name: codewiki
description: Use when working on, exploring, or maintaining a Karpathy-style engineering wiki at `docs/wiki/` in the user's repo. Activate for any `/wiki:*` slash command, when the user asks about wiki conventions, or when code changes might invalidate existing wiki pages. This is the schema — read it before writing or updating any wiki page.
---

# codewiki — Engineering Wiki Schema

You maintain a persistent, LLM-authored engineering wiki at `docs/wiki/` inside the user's project. The user's codebase is the source of truth; the wiki is a structured, interlinked synthesis of it.

## Layout (inside the user's project)

- `docs/wiki/index.md` — content catalog. Every page listed under a category heading with a link and a one-line summary. Always read first when answering a question.
- `docs/wiki/log.md` — append-only. Each entry begins with `## [YYYY-MM-DD] <verb> | <subject>`. Verbs: `ingest`, `sync`, `query`, `lint`, `bootstrap`.
- `docs/wiki/overview.md` — top-level synthesis.
- `docs/wiki/modules/<slug>.md` — one entity page per significant module/service/package.
- `docs/wiki/concepts/<slug>.md` — cross-cutting patterns, conventions, invariants.
- `docs/wiki/flows/<slug>.md` — multi-module flows.
- `docs/wiki/comparisons/<slug>.md` — answers from `/wiki:query` worth keeping.

## Frontmatter contract

Every page starts with YAML frontmatter. See `${CLAUDE_PLUGIN_ROOT}/skills/codewiki/templates/` for the canonical shape of each kind.

Required fields:
- All pages: `kind`, `title`, `slug`, `last_ingest`
- Module + flow: also `source_paths` (list of file/dir paths relative to repo root) and `source_commit` (git SHA at last ingest)

`source_commit` is the contract that makes drift mechanically detectable. **Always update it when you re-read the source.** Use `git rev-parse HEAD` at ingest time.

## Linking

Use Obsidian-style wikilinks for inter-wiki references: `[[modules/auth]]`, `[[concepts/idempotency]]`. Use standard markdown links for source citations: `[auth/middleware.py:42](../../src/auth/middleware.py#L42)`. Every module page should link to at least one concept page and vice versa — orphans are flagged by `/wiki:lint`.

## Workflows

### Ingest (`/wiki:ingest <path>`)
1. Read the source at `<path>` and obvious neighbours (same package, callers, callees).
2. Briefly summarise key takeaways to the user.
3. Decide which page(s) to write/update:
   - New module → new `modules/<slug>.md` from `templates/module.md`
   - Existing module → update in place; preserve human edits where you can detect them
   - New cross-cutting pattern → new `concepts/<slug>.md`
4. Set `source_commit` to current `git rev-parse HEAD`. Set `last_ingest` to today's ISO date.
5. Update `index.md` (add or refresh the entry under the right category).
6. Append a `log.md` entry: `## [YYYY-MM-DD] ingest | <slug> — <one-line>`.
7. Update inbound/outbound cross-references on touched pages.
8. Show the user a summary of pages changed. Do not auto-commit.

A single ingest may touch 5–15 pages. That's expected.

### Query (`/wiki:query <question>`)
1. Read `index.md` first to find relevant pages.
2. Drill into matching pages. If a page's `source_commit` looks stale, warn the user and offer to `/wiki:sync` first.
3. Answer with citations to wiki pages AND source `file:line` refs.
4. Ask the user whether to file the answer back as `comparisons/<slug>.md` (use `templates/comparison.md`). If yes, add it to `index.md` and `log.md`.

### Sync (`/wiki:sync`)
1. Run via Bash: `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.detect_stale docs/wiki .`
2. For each stale page, re-read its `source_paths`, diff against the page's claims, and update the page (and any pages it links into).
3. Bump `source_commit` and `last_ingest` on each updated page.
4. Append a single `log.md` entry summarizing the sync.

### Lint (`/wiki:lint`)
1. Run via Bash: `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.list_orphans docs/wiki` and `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.list_dead_links docs/wiki`.
2. Additionally inspect for: contradictions between pages, concepts mentioned in module pages but lacking their own page, modules with no inbound references, stale `source_commit` entries.
3. Produce a prioritized to-do list. Do not auto-fix.

### Bootstrap (`/wiki:bootstrap`)
First-time scan. Enumerate top-level directories under the repo root, propose a module map, then run an ingest pass per module. Sub-agents (via Task tool) can run module ingests in parallel as long as each writes to a distinct `modules/<slug>.md` — they must serialize their index/log updates.

## Anti-patterns

- **Don't restate the obvious.** A module page is not a docstring dump.
- **Don't invent.** If a fact isn't in the code, file it under "Open Questions".
- **Don't lose source links.** Every non-trivial claim cites a `file:line`.
- **Don't bypass the index.** New pages must appear in `index.md` in the same edit pass.
- **Don't pretend to test the code.** This skill maintains documentation, not behaviour.
- **Don't write outside `docs/wiki/`** unless the user explicitly asks.
