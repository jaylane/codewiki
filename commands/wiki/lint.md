---
description: Health-check the wiki. Flags orphans, dead links, gaps, and contradictions.
---

You are running `/wiki:lint`.

**Required:** Invoke the `codewiki` skill via the Skill tool first.

## Procedure

1. **Run the deterministic checks via Bash:**

   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.list_orphans docs/wiki
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.list_dead_links docs/wiki
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m codewiki.detect_stale docs/wiki .
   ```

2. **Read every module and concept page** (use ripgrep/glob). Look for:
   - **Contradictions:** two pages making mutually exclusive claims
   - **Concept gaps:** a phrase like "uses optimistic locking" mentioned in 3+ pages but no `concepts/optimistic-locking.md`
   - **Stale claims:** assertions referencing files that no longer exist
   - **Citation rot:** `file:42` references that no longer point at the claimed thing

3. **Produce a prioritized punch list.** Group by severity:
   - **Block:** dead links, drift in critical modules, contradictions
   - **Should fix:** orphans, missing concept pages
   - **Consider:** stylistic inconsistencies, thin pages

4. **Do not auto-fix.** Offer to address items one by one with the user.
