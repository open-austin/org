# 0004 — Projects v2 Board Changes Can't Trigger Repo-Level Actions
## Current Approach
Do not use `on: projects_v2_item` in repository GitHub Actions workflows to react to Projects v2 field changes. Use a native Projects workflow when it fits; otherwise use scheduled reconciliation under this repository's no-hosting boundary.

Issue-state events can drive board updates through repository Actions. Board-to-issue close uses native `Auto-close issue`. Board-to-issue reopen uses the single `board-reopen-reconcile.yaml` workflow, covering both boards with a five-minute cron and a manual `dry_run` input. [0005](0005-board-sync-architecture.md) owns the current routing, native-workflow exception, and fresh-close guard. The former separate fifteen-minute reopen workflows are retired.

## Rationale
Projects v2 field-change webhooks are organization-scoped; repository Actions cannot subscribe directly to them. The earlier workflows parsed as valid YAML but never ran. A hosted webhook bridge would add infrastructure this repository avoids. Native close and scheduled reopen respect that platform boundary.

## Operating Notes
Before building board-reactive automation, check the project's native workflows. Scheduled reconciliation is best-effort and may be delayed; the five-minute cron is not a delivery guarantee. Reopening the issue directly uses the immediate issue-event path.

## Links
- `docs/archive/github-automation.md`, `docs/archive/github-automation.todo.md` (since archived)
- [.github/workflows/board-reopen-reconcile.yaml](../../.github/workflows/board-reopen-reconcile.yaml)
- [Current board sync policy](0005-board-sync-architecture.md)
- `AGENTS.md` — write-safety rules, no-hosting preference
