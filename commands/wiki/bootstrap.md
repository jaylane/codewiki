---
description: First-time wiki scan. Proposes a module map, then ingests each approved module into docs/wiki/.
---

You are running `/wiki:bootstrap`. This is a one-time operation per repo.

**Required:** Invoke the `codewiki` skill via the Skill tool before touching any wiki page.

## Procedure

1. **Confirm intent.** Check whether `docs/wiki/modules/` already contains content. If yes, ask the user whether to abort, augment, or wipe-and-restart. Default to abort.

2. **Create scaffolding.** Run:

   ```bash
   mkdir -p docs/wiki/{modules,concepts,flows,comparisons}
   ```

   Then create `docs/wiki/index.md`, `docs/wiki/log.md`, `docs/wiki/overview.md`, and `docs/wiki/README.md` if they don't exist — minimal seed content per the schema.

3. **Map top-level structure.** List the repo's top-level directories. For each, decide whether it should become a module page (significant code/services) or be ignored (`node_modules`, `dist`, `.venv`, `migrations`, `vendor`, `target`, `build`, etc.). Use `.gitignore` as a starting hint.

4. **Present the proposed module map** as a checklist. Wait for user approval before ingesting anything.

5. **For each approved module, run the ingest procedure** (see `/wiki:ingest`). Prefer the Task tool to dispatch ingests in parallel where modules are independent. Only one agent writes to `index.md` and `log.md` at a time.

6. **Write `overview.md`** after all module pages exist. Synthesize the system from the module pages, not by re-reading the code. Cite `[[modules/...]]` pages, not source files, in the overview.

7. **Append a single `log.md` entry:** `## [YYYY-MM-DD] bootstrap | <N> modules ingested`.

8. **Print a summary** of created pages. Recommend next steps (`/wiki:lint`).

9. **Do not auto-commit.**
