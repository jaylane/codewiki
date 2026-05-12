---
description: Read a path in the user's codebase and integrate its knowledge into docs/wiki/.
argument-hint: <path-or-glob>
---

You are running `/wiki:ingest $ARGUMENTS`.

**Required:** Invoke the `codewiki` skill via the Skill tool before touching any wiki page.

## Procedure

1. **Read.** Read every file matched by `$ARGUMENTS`. For directories, list contents first and read the most-trafficked files (entry points, package-level inits, top-level modules). For single files, also read the file's nearest neighbours (same package).

2. **Locate or create the module page.** Determine the slug from the path (`src/auth/` → `modules/auth.md`). If `docs/wiki/modules/<slug>.md` exists, read it before changing it.

3. **Discuss takeaways briefly.** In 3–5 bullets, tell the user what you noticed: purpose, public surface, invariants, smells. Wait for any course-correction before editing pages.

4. **Update / create the module page** from the template at `${CLAUDE_PLUGIN_ROOT}/skills/codewiki/templates/module.md`. Preserve human-added prose where possible. Fill every section. Cite `file:line` for every non-trivial claim.

5. **Update `source_commit`** to the output of `git rev-parse HEAD` and `last_ingest` to today's ISO date.

6. **Propagate to concept and flow pages.** For each cross-cutting pattern noticed (auth, idempotency, retries, caching, etc.), either update an existing `docs/wiki/concepts/<slug>.md` or create one. Add bidirectional links.

7. **Update `docs/wiki/index.md`.** Add or refresh the entry under the right category with a one-line summary.

8. **Append `docs/wiki/log.md`** with: `## [YYYY-MM-DD] ingest | <slug> — <one-line summary>`

9. **Report changes.** Print a bulleted list of pages created vs. updated. **Do not auto-commit.**

## Anti-patterns
- Do not restate docstrings.
- Do not invent. File unknowns under "Open Questions".
- Do not bypass `index.md`.
