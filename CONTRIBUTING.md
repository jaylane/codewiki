# Contributing to codewiki

Thanks for considering a contribution. This document covers the basics.

## Reporting bugs

Use the [Bug report](https://github.com/jaylane/codewiki/issues/new?template=bug_report.md) template. Include:

- What you ran (slash command, helper CLI, install command)
- What you expected
- What actually happened, including the exact error text
- Your Python version (`python3 --version`) and OS

## Requesting features

Use the [Feature request](https://github.com/jaylane/codewiki/issues/new?template=feature_request.md) template. Describe the workflow you want and the problem it solves — concrete use cases beat abstract wishes.

## Code changes

Workflow:

1. Fork and clone.
2. Create a branch off `main` named after the change (e.g. `fix-crlf-frontmatter`, `feat-batch-detect-stale`).
3. Set up a local environment:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -e ".[dev]"
   ```

4. Make the change with tests. We use TDD — write the failing test first, then the implementation. See `tests/` for examples.
5. Run the full suite: `.venv/bin/python -m pytest -v`. Everything must pass.
6. Commit with a [Conventional Commits](https://www.conventionalcommits.org/) subject (e.g. `feat(parser): ...`, `fix(sync): ...`, `docs: ...`).
7. Push your branch and open a PR.

## Design constraints

- **No new runtime dependencies.** The Python helpers are stdlib-only. If a feature seems to need an external dep, propose the design in an issue first.
- **One responsibility per file.** Helpers live in their own modules (`frontmatter.py`, `detect_stale.py`, etc.). Tests mirror that layout.
- **Tests cite real behaviour.** Use real subprocess, real git, real filesystem (via `tmp_path`). Avoid mocks.
- **Markdown slash commands are prompts, not code.** They live under `commands/wiki/`. Keep their procedures numbered and action-oriented.
- **Read [DESIGN.md](docs/DESIGN.md) before proposing architectural changes.** Drift detection, parser scope, and the no-embeddings stance are deliberate.

## Code review

A maintainer will review and may ask for changes. Reviews look at: correctness, test coverage, docs accuracy, and whether the change matches the design constraints above. Smaller PRs land faster.

## License

By contributing you agree your contributions are licensed under the [MIT License](LICENSE) of this project.
