# codewiki

> [!WARNING]
> **v0.1 in development.** The slash commands and install scripts described below ship with the v0.1.0 release. Until then this repo is a scaffold — see the [issues](https://github.com/jaylane/codewiki/issues) for progress.

A Claude Code plugin that incrementally builds and maintains a [Karpathy-style](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) persistent markdown wiki for the codebase your agent is working on.

Instead of re-deriving understanding on every question (the RAG pattern), the LLM **compiles** the codebase into an interlinked set of markdown pages, then keeps them in sync as the code changes.

## What it does

- `/wiki:bootstrap` — first-time scan; produces `docs/wiki/modules/*.md` per significant package
- `/wiki:ingest <path>` — read a path, integrate its knowledge across modules/concepts/flows
- `/wiki:query <question>` — answer using the wiki; optionally file the answer back as a page
- `/wiki:sync` — detect pages whose `source_commit` has drifted from `git HEAD` and reconcile
- `/wiki:lint` — orphans, dead links, gaps, contradictions

The wiki is plain markdown under `docs/wiki/` in your repo. It's a git artifact, code-reviewable like any other.

## Install (plugin marketplace)

```bash
/plugin marketplace add jaylane/codewiki
/plugin install codewiki@jaylane
```

## Install (manual)

```bash
git clone https://github.com/jaylane/codewiki ~/codewiki
cd ~/codewiki
./install.sh --global              # install to ~/.claude/
# or
./install.sh --project /your/repo  # install to /your/repo/.claude/
pip install --user .
```

## Requirements

- Claude Code
- Python 3.10+
- git
- macOS or Linux (Windows untested)

## Quickstart

Inside any git repo, in Claude Code:

```
/wiki:bootstrap
```

Approve the proposed module map. Walk away. Come back to a populated `docs/wiki/`.

## License

MIT. See [LICENSE](LICENSE).

## Credits

Pattern from Andrej Karpathy's [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
