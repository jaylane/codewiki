---
description: Reconcile wiki pages whose source has drifted since their last ingest.
---

You are running `/wiki:sync`.

**Required:** Invoke the `codewiki` skill via the Skill tool first.

## Procedure

1. **Detect drift.** Run via the Bash tool:

   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.detect_stale docs/wiki .
   ```

   If the script returns no paths, report "Wiki up to date." and stop.

2. **Show the user the list of stale pages** and which `source_paths` changed for each. Use `git diff --stat <source_commit> HEAD -- <paths>` to summarize.

3. **Per stale page, re-ingest.** For each page, run an abbreviated version of `/wiki:ingest`:
   - Re-read all `source_paths` in the page's frontmatter
   - Diff the page's current claims against what the code now says
   - Update only the sections that changed; preserve unchanged prose
   - Bump `source_commit` to current `HEAD` and `last_ingest` to today
   - Update outgoing links if file paths moved/renamed

4. **Append one `log.md` entry** summarizing the whole sync pass: `## [YYYY-MM-DD] sync | <N> pages updated`.

5. **Do not auto-commit.**
