# 0005 — Board ↔ Issue Sync Architecture
## Current Approach
1. **Card → close** uses the native **`Auto-close issue`** workflow (Org Kanban → close on `Done`; Open Roles → close on `Filled`). This is the single, deliberate exception to "everything in code," accepted because closing-by-drag is common and instant beats a poll lag. It is documented here and in the README so its lack of a workflow file is not a surprise.
2. **Card → reopen** is the only behavior forced onto a timer (no native, no instant-code path). It is a single scheduled reconciliation Action, `board-reopen-reconcile.yaml`, covering both boards, `*/5` cron, with `workflow_dispatch` + `dry_run`.
3. **Everything else is immediate code Actions**, and **all other native Projects workflows are turned off** (`Auto-add to project`, `Item added to project`, `Item closed`, `Item reopened`), so code is the only actor except the one `Auto-close` exception. Because native "Item added to project" is off, `open-role-add.yaml` and `add-issue-to-kanban.yaml` set initial board status in code.
4. The reopen reconciler's durable safeguard is a **fresh-close guard** that skips issues closed within the last 10 minutes, so a just-closed issue mid-sync isn't spuriously reopened.

## Rationale
Issue events can trigger repository Actions immediately; board field changes cannot. The architecture prioritizes auditable code, immediate behavior where available, and one actor per direction. Native `Auto-close issue` is the deliberate exception to code ownership because closing by dragging a card is common; scheduled reopening handles the direction without a native equivalent. No hosted infrastructure is required.

## Operating Notes
- Exactly one piece of board logic lives outside the repo (the native `Auto-close issue` config in each Project's Workflows UI). It is not version-controlled and leaves no history if changed — an accepted, documented trade for instant close.
- Reopening via a board move lags at least ~5 minutes. **GitHub scheduled workflows are best-effort and frequently delayed** — 10–30+ minutes is normal, and the first run after a schedule is added is the slowest to start (confirmed during rollout: the first scheduled reopen took ~25+ minutes to fire). Reopening the issue directly is immediate and is the reliable path when timing matters.
- The reconciler uses a five-minute cron (`*/5`), with `workflow_dispatch` and `dry_run` for manual checks.
- Any future board-reactive automation must be native or a poll — never `on: projects_v2_item` (per 0004). Before adding a custom Action, check whether a native built-in already covers it.

## Links
- `docs/policies/0004-projects-v2-automation-triggers.md` — the platform constraint this builds on
- `docs/archive/board-sync-redesign.md` / `.todo.md` — the design and execution (since archived)
- `.github/workflows/board-reopen-reconcile.yaml`, `open-role-add.yaml` (the one-time `baseline-terminal-cleanup.yaml` was removed after rollout)
