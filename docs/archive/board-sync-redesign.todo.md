# Board ↔ Issue Sync Redesign — To Do
## Background
Execute the redesign described in `docs/active-spikes/board-sync-redesign.md`: native `Auto-close issue` for card→close (the one exception), all other board logic in code, one 5-minute reopen poller, all other native Projects workflows off. Continues the sync-layer work from `docs/active-spikes/github-automation.md`.

## Current State Overview
**Complete (2026-07-08).** Implemented, committed/pushed, and QA-confirmed live. Native config done by the user (only `Auto-close issue` on). The `board-reopen-reconcile` schedule is live and confirmed firing — the user observed a card→reopen actually happen, though GitHub delayed the first scheduled run ~25+ min (see the delay note now in the README and decision 0005). The one-time `baseline-terminal-cleanup` found the boards already clean and has since been deleted by the user; the fresh-close guard is the durable safeguard. Two low-risk QA paths were not explicitly exercised (see residuals below) — carried to `TODO.md` rather than blocking closure.

## Native Config Changes (user, in the Projects Workflows UI — not code)
User reported (2026-07-08): **only `Auto-close issue` is ON; every other native workflow is OFF** on both boards. This matches the plan. One detail to confirm when convenient:
- [x] Only `Auto-close issue` enabled; `Auto-add to project`, `Item added to project`, `Item closed`, `Item reopened` all OFF
- [x] `Auto-close issue` confirmed working for both boards — QA showed dragging to Done closes the Kanban issue and dragging to Filled closes the role, so it's configured for the right statuses

## Code Changes (in repo) — done
- [x] `open-role-add.yaml` rewritten: adds to Open Roles via GraphQL and **sets status to Open in code** (native "Item added" is off), then removes from Org Kanban (paginated) for the late-label case. `add-issue-to-kanban.yaml` already sets To Do.
- [x] Merged `kanban-status-reopen.yaml` + `open-roles-reopen.yaml` → single `board-reopen-reconcile.yaml` scanning both boards. Old two files deleted.
- [x] Reconciler uses `*/5` cron **(commented out)** + `workflow_dispatch` + `dry_run`. Only ever reopens (card→close is native's job).
- [x] Fresh-close guard added (`FRESH_CLOSE_SECONDS=600`): skips issues closed within the last 10 min.
- [x] `baseline-terminal-cleanup.yaml` created: `workflow_dispatch`, dry-run default true, moves closed issues in non-terminal columns → Done/Filled on both boards.

## Remaining To Do (ordered — mostly user-run, needs live org)
- [x] Commit/push the workflow changes so `baseline-terminal-cleanup` + `board-reopen-reconcile` appear in the Actions UI (schedule still commented, so nothing auto-runs yet).
- [x] Run `baseline-terminal-cleanup` with `dry_run=true` (run 28973381242) — **clean, nothing to move**. Verified via GraphQL: all 28 closed board issues already in Done/Filled.
- [x] Baseline `dry_run=false` — **skipped, unnecessary** (nothing to move).
- [x] Run `board-reopen-reconcile` with `dry_run=true` (run 28973517799) — **clean, nothing to reopen**.
- [x] Uncomment the `schedule:` block in `board-reopen-reconcile.yaml`.
- [x] Commit/push the schedule enable — reconciler is live and confirmed firing (with GitHub's usual scheduled-run delay).

## Docs — done
- [x] Decision record `docs/decisions/0005-board-sync-architecture.md`.
- [x] README Board Automation section + Mermaid updated (native `Auto-close` exception called out, `board-reopen-reconcile` ~5m, native workflows off).
- [x] Pointer added from `docs/active-spikes/github-automation.md` (Continues in).

## Human QA — results (2026-07-08)
- [x] New plain issue → Org Kanban To Do, once, no second actor
- [x] New open-role issue (via form) → Open Roles "Open" only, never appears on Org Kanban
- [x] Close an issue → card moves to Done/Filled immediately (both boards confirmed)
- [x] Drag a card to Done/Filled → issue closes immediately (native Auto-close, both boards)
- [x] Reopen an issue → card moves to To Do/Open immediately (both boards)
- [x] Drag a Done/Filled card back → issue reopens via the poller (confirmed; GitHub delayed the first scheduled run ~25+ min)
- [ ] **Residual (low-risk, not explicitly tested):** blank issue later labeled `open role` → moves Kanban→Open Roles. Logic is in `open-role-add.yaml`; not exercised because the form applies the label at creation, so late-labeling is rare. → carried to `TODO.md`.
- [ ] **Residual (low-risk):** fresh-close guard path (a just-closed issue is NOT spuriously reopened). Logic verified by reading; not exercised live. → carried to `TODO.md`.
- N/A: "legacy closed-in-To-Do moved to Done by baseline" — there were no legacy stragglers; the baseline dry-run found the boards already clean.

## Done
- [x] Established the platform constraint and the native/timer split with the user
- [x] Decided: native `Auto-close` exception + code-first + one 5-min reopen poller + native otherwise off
- [x] Wrote conceptual + this to-do doc
- [x] Implemented all code + docs (workflows, decision 0005, README) — 2026-07-08
- [x] QA-confirmed live; reconciler firing confirmed; `baseline-terminal-cleanup` deleted post-rollout; docs updated to note GitHub scheduled-run delay
