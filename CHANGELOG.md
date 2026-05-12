# Changelog

All notable changes to this project will be documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-05-12

### Added
- `.claude-plugin/marketplace.json` — plugin marketplace manifest. `/plugin marketplace add jaylane/codewiki` now works.

### Changed
- README and USAGE lead with marketplace install (now functional). Manual install remains documented as the alternative.
- Bumped plugin/Python package version to 0.2.0.

## [0.1.1] — 2026-05-11

### Changed
- README and USAGE now lead with manual install. The plugin marketplace path is deferred to v0.2 along with the marketplace.json manifest. Removed the stale "in development" banner.

## [0.1.0] — 2026-05-11

### Added
- Five slash commands: `/wiki:bootstrap`, `/wiki:ingest`, `/wiki:query`, `/wiki:sync`, `/wiki:lint`.
- `codewiki` skill encoding the schema and workflows.
- Python helpers: `frontmatter`, `detect_stale`, `list_orphans`, `list_dead_links` (stdlib only).
- Page templates for module, concept, flow, comparison.
- Plugin manifest, install.sh, GitHub Actions CI.
- USAGE.md and DESIGN.md.
