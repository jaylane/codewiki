# Usage

## Prerequisites

- Claude Code
- Python 3.10+ and `pip` available on PATH
- A git repo you want to document

### macOS Homebrew note

If you're on macOS using Homebrew's Python, `pip install --user .` may be refused with `error: externally-managed-environment` (PEP 668). Two workarounds:

```bash
# Option A: pipx (recommended for CLI usage)
pipx install /path/to/codewiki

# Option B: a project-local venv
cd /path/to/codewiki
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

If you're using the plugin marketplace install, you don't need to `pip install` at all — slash commands invoke the helpers via `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.<helper>`.

## Install

### Manual (recommended for v0.1.x)

```bash
git clone https://github.com/jaylane/codewiki ~/codewiki
cd ~/codewiki
./install.sh --global              # or --project /path/to/repo
pip install --user .               # see macOS note above if this fails
```

Restart Claude Code so it picks up the new skill and slash commands.

### Via plugin marketplace

Coming in v0.2. The marketplace manifest (`.claude-plugin/marketplace.json`) lands in the next release.

## First run

`cd` into the repo you want to document. In Claude Code:

```
/wiki:bootstrap
```

Approve the proposed module map. Claude will create `docs/wiki/` and populate it.

## Daily flow

- After a notable change: `/wiki:sync`
- New module added: `/wiki:ingest src/<new-module>/`
- Question about the system: `/wiki:query how does <X> work?`
- Periodically: `/wiki:lint`

## Tips

- The wiki is plain markdown. Commit it. Review changes in PR.
- Don't hand-edit `index.md` or `log.md` — let the slash commands maintain them.
- If a page disagrees with the code, the code wins. Run `/wiki:sync`.
- Obsidian's graph view is a great way to visualize the wiki's shape.
