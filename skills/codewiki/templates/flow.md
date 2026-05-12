---
kind: flow
title: {{TITLE}}
slug: {{SLUG}}
source_paths: []
source_commit: {{COMMIT_SHA}}
last_ingest: {{ISO_DATE}}
tags: []
entry_points: []
---

# {{TITLE}}

## Trigger
_What kicks this flow off (HTTP route, cron, webhook, etc.) with `file:line` citation._

## Steps
1. **{{step name}}** — `module/file.ext:line` — what happens
2. ...

## Data Shape at Each Hop
_Dataclass / serializer / payload definitions referenced by `file:line`._

## Failure Modes
_What can go wrong, where, and how the system recovers (or doesn't)._

## Related Modules
_Links to `[[modules/...]]` pages._
