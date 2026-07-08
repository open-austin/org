# 0005 — Board ↔ Issue Sync Architecture
**Date:** 2026-07-08
**Status:** Accepted

## Context
The board↔issue automation needed a coherent architecture after two failures: the original `projects_v2_item`-triggered workflows never ran (see `docs/decisions/0004-projects-v2-automation-triggers.md`), and the custom Actions ran alongside GitHub's native Projects workflows, producing duplicate/cross-board behavior (an issue added by native auto-add, then re-touched by a custom Action; open-role issues added to both boards then cleaned up).

The platform imposes a hard asymmetry:
- **Issue → board** events (open/close/reopen/label) are repository events → immediate code Actions.
- **Board → issue** (a card move) is not deliverable to a repo workflow at all without hosted infrastructure. Its only implementations are a native Projects workflow (instant, UI-configured, not in the repo) or a scheduled poll (in code, but timer-based). Native ships `Auto-close issue` but has **no** auto-reopen, so card→reopen has no instant path in either native or code.

The user's priorities, in order: auditable/version-controlled in the repo; immediate where the platform allows; minimal surface area (one system, not custom + native fighting). No hosted infrastructure.

## Decision
1. **Card → close** uses the native **`Auto-close issue`** workflow (Org Kanban → close on `Done`; Open Roles → close on `Filled`). This is the single, deliberate exception to "everything in code," accepted because closing-by-drag is common and instant beats a poll lag. It is documented here and in the README so its lack of a workflow file is not a surprise.
2. **Card → reopen** is the only behavior forced onto a timer (no native, no instant-code path). It is a single scheduled reconciliation Action, `board-reopen-reconcile.yaml`, covering both boards, `*/5` cron, with `workflow_dispatch` + `dry_run`.
3. **Everything else is immediate code Actions**, and **all other native Projects workflows are turned off** (`Auto-add to project`, `Item added to project`, `Item closed`, `Item reopened`), so code is the only actor except the one `Auto-close` exception. Because native "Item added to project" is off, `open-role-add.yaml` and `add-issue-to-kanban.yaml` set initial board status in code.
4. Two safeguards make the reopen reconciler safe: a **one-time baseline cleanup** (`baseline-terminal-cleanup.yaml`) that moves already-closed issues into their terminal column before the reconciler's schedule is enabled, and a **fresh-close guard** that skips issues closed within the last 10 minutes so a just-closed issue mid-sync isn't spuriously reopened.

## Consequences
- Exactly one piece of board logic lives outside the repo (the native `Auto-close issue` config in each Project's Workflows UI). It is not version-controlled and leaves no history if changed — an accepted, documented trade for instant close.
- Reopening via a board move lags up to ~5 minutes (plus GitHub's own scheduled-run delays). Reopening the issue directly is immediate.
- `board-reopen-reconcile.yaml` ships with its `schedule:` commented out. It must stay that way until `baseline-terminal-cleanup` has been run and a dry-run of the reconciler confirms it won't touch legacy issues. Only then is the cron uncommented.
- Any future board-reactive automation must be native or a poll — never `on: projects_v2_item` (per 0004). Before adding a custom Action, check whether a native built-in already covers it.

## Related
- `docs/decisions/0004-projects-v2-automation-triggers.md` — the platform constraint this builds on
- `docs/active-spikes/board-sync-redesign.md` / `.todo.md` — the design and execution
- `.github/workflows/board-reopen-reconcile.yaml`, `baseline-terminal-cleanup.yaml`, `open-role-add.yaml`
