# Board ↔ Issue Sync Redesign — To Do
## Background
Execute the redesign described in `docs/active-spikes/board-sync-redesign.md`: native `Auto-close issue` for card→close (the one exception), all other board logic in code, one 5-minute reopen poller, all other native Projects workflows off. Continues the sync-layer work from `docs/active-spikes/github-automation.md`.

## Current State Overview
Code + docs implemented and the workflow changes committed/pushed (2026-07-08). Native config done by the user (only `Auto-close issue` on). Dry-runs of both `baseline-terminal-cleanup` and `board-reopen-reconcile` came back clean — all 28 closed issues across both boards were already in their terminal columns (Kanban Done / Open Roles Filled), so the baseline had nothing to move and the reconciler nothing to reopen. The reconciler `schedule:` has been uncommented (edit uncommitted). Remaining: commit/push the schedule enable, then human QA of the live behavior.

## Native Config Changes (user, in the Projects Workflows UI — not code)
User reported (2026-07-08): **only `Auto-close issue` is ON; every other native workflow is OFF** on both boards. This matches the plan. One detail to confirm when convenient:
- [x] Only `Auto-close issue` enabled; `Auto-add to project`, `Item added to project`, `Item closed`, `Item reopened` all OFF
- [ ] Confirm `Auto-close issue` is configured for **Done** on Org Kanban and **Filled** on Open Roles (the status that should close the issue), not left on a default

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
- [x] Uncomment the `schedule:` block in `board-reopen-reconcile.yaml` (edit made, commit/push pending).
- [ ] Commit/push the schedule enable to activate the 5-min cadence.

## Docs — done
- [x] Decision record `docs/decisions/0005-board-sync-architecture.md`.
- [x] README Board Automation section + Mermaid updated (native `Auto-close` exception called out, `board-reopen-reconcile` ~5m, native workflows off).
- [x] Pointer added from `docs/active-spikes/github-automation.md` (Continues in).

## Ready for Human QA
Test each path in the live org after the changes land (and after baseline + schedule enable):
- [ ] New plain issue → lands on Org Kanban in To Do, once, no second actor
- [ ] New open-role issue (via form) → lands on Open Roles in Open only, never appears on Org Kanban (no add-then-remove)
- [ ] Blank issue later labeled `open role` → moves from Kanban to Open Roles, removed from Kanban
- [ ] Close an issue (from the issue) → card moves to Done/Filled immediately (code)
- [ ] Drag a card to Done/Filled → issue closes immediately (native Auto-close)
- [ ] Reopen an issue (from the issue) → card moves to To Do/Open immediately (code)
- [ ] Drag a Done/Filled card back to To Do/Open → issue reopens within ~5 min (poller)
- [ ] Confirm a freshly-closed issue is NOT spuriously reopened by the poller (fresh-close guard works)
- [ ] Confirm a legacy closed-in-To-Do issue was moved to Done by the baseline cleanup, not reopened

## Done
- [x] Established the platform constraint and the native/timer split with the user
- [x] Decided: native `Auto-close` exception + code-first + one 5-min reopen poller + native otherwise off
- [x] Wrote conceptual + this to-do doc
- [x] Implemented all code + docs (workflows, decision 0005, README) — 2026-07-08, uncommitted
