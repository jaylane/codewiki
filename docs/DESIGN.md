# Design

This plugin is an implementation of the pattern described in Andrej Karpathy's [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted from ingesting articles/PDFs to ingesting source code.

## Why a persistent wiki instead of RAG?

Conventional code-RAG re-derives understanding on every question: chunk → embed → retrieve → answer. Nothing accumulates. Ask "how does auth work" twice in different sessions, the model rediscovers it from scratch each time.

This plugin instead has the LLM **compile** the codebase into an interlinked set of markdown pages — `modules/`, `concepts/`, `flows/`, `comparisons/`. The wiki is the synthesis, kept current by `/wiki:sync` when source drifts.

## Drift detection

The novel piece versus the original pattern (whose sources are immutable): code changes. Each entity page carries `source_paths` and `source_commit` in YAML frontmatter. `detect_stale` runs `git diff --name-only <source_commit> HEAD -- <source_paths>`; non-empty output means the page is stale. `/wiki:sync` reconciles.

## Why no embeddings, no MCP server?

Karpathy's observation: `index.md` plus grep is enough at small scale (~100 sources, hundreds of pages). The plugin defers vector retrieval until empirically necessary.

## Why a tiny stdlib YAML parser?

PyYAML is heavyweight and pulls in a C extension. Our frontmatter is a strict subset (key: scalar, key: [a, b], key: block-list). A 60-line parser covers it. Zero runtime deps == easier install.

## Plugin layout

- `skills/codewiki/SKILL.md` — conventions doc (the "schema")
- `commands/wiki/*.md` — five slash commands
- `codewiki/` — Python package, four helpers, stdlib only
- `templates/` — page templates the skill references

## Non-goals (v0.1)

- Cross-repo wikis
- Image handling
- Vector/BM25 retrieval
- Windows support
- Auto-commit
