---
description: Answer a question about the codebase using the wiki at docs/wiki/.
argument-hint: <question>
---

You are running `/wiki:query $ARGUMENTS`.

**Required:** Invoke the `codewiki` skill via the Skill tool first.

## Procedure

1. **Read `docs/wiki/index.md`.** Identify candidate pages. If the question is broad, also read `docs/wiki/overview.md`.

2. **Drill into matching pages.** Read each candidate. If a page's `source_commit` is many commits behind HEAD, warn inline (`⚠ <page> last synced at <sha>, current HEAD is <sha>`) and ask whether to `/wiki:sync` it before continuing.

3. **Answer.** Cite both wiki pages (`[[modules/auth]]`) and source (`src/auth/middleware.py:42`). Distinguish what you found in the wiki versus what you had to look up live in the source.

4. **Offer to file the answer.** Ask: "File this answer back into the wiki as `comparisons/<slug>.md`?" If yes:
   - Render from `${CLAUDE_PLUGIN_ROOT}/skills/codewiki/templates/comparison.md`
   - Add an entry to `index.md` under Comparisons
   - Append `log.md`: `## [YYYY-MM-DD] query | <slug> — <one-line>`

5. **Do not auto-commit.**
