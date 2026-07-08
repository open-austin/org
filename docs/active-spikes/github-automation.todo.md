# GitHub Automation — To Do

## Background

Build GitHub Actions to keep boards and issue state in sync automatically, eliminating the manual triage overhead that accumulates when GitHub's default behavior (adding every new issue to every board as "No Status") is left unmanaged.

Related: `docs/active-spikes/github-automation.md` (conceptual doc)

---

## Project Organization

- Workflows live in `.github/workflows/`
- Existing: `open-role-add.yaml` (adds `open role` issues to Open Roles board — partial, needs enhancement)
- New workflows to build: see To Do below

---

## Key IDs

| Resource | ID |
|---|---|
| Org Kanban project | `PVT_kwDOAA7NZM4AqQF8` |
| Open Roles project | `PVT_kwDOAA7NZM4AmdbW` |
| Org Kanban Status field | `PVTSSF_lADOAA7NZM4AqQF8zghh1hc` |
| Open Roles Status field | `PVTSSF_lADOAA7NZM4AmdbWzgeWrcw` |
| Org Kanban → "To Do" | `f75ad846` |
| Org Kanban → "Done" | `98236657` |
| Open Roles → "Filled" | `47fc9ee4` |

Secret in use: `ACTIONS_TOKEN` (has `project` scope for org-level board mutations)

---

## General Principles

- GitHub's `GITHUB_TOKEN` does NOT have project scope for org-level projects — always use `ACTIONS_TOKEN`
- All workflows should be idempotent (safe to re-run)
- Board mutations require GraphQL (`gh api graphql`) — REST API cannot move Projects v2 items
- Prefer consolidating related triggers in one workflow file over many small files

---

## To Do

### Org Kanban ↔ Issue state (bidirectional)

- [x] `close-to-done.yaml` — issue closed → board Done (+ added guard: skip if already Done)
- [x] `done-to-close.yaml` — board moved to Done → close issue (guard: skip if already closed)
- [x] `kanban-status-reopen.yaml` — board moved to To Do/In Progress (issue closed) → reopen issue
- [x] `reopened-to-todo.yaml` — issue reopened (non-open-role) → board To Do

### Open Roles ↔ Issue state (bidirectional)

- [x] `filled-to-close.yaml` — board moved to Filled → close issue (+ added guard: skip if already closed)
- [x] `closed-to-filled.yaml` — issue closed (open role) → board Filled (guard: skip if already Filled)
- [x] `open-roles-reopen.yaml` — board moved to Open/In Progress (issue closed) → reopen issue
- [x] `open-role-reopened.yaml` — issue reopened (open role) → board Open

### Board routing

- [x] `open-role-add.yaml` — `open role` label added → add to Open Roles board, remove from Org Kanban
- [x] `add-issue-to-kanban.yaml` — new issue (non-open-role) → Org Kanban "To Do"

### Scheduled cleanup

- [x] `archive-old-done.yaml` — Org Kanban Done items > 6 months → archive (weekly + manual dry-run)
- [x] `archive-old-filled.yaml` — Open Roles Filled items > 1 year → archive (weekly + manual dry-run)

---

### Notifications + reporting

- [x] `stale-role-warning.yaml` — weekly, comments on open roles not updated in 90+ days (skips already-warned)
- [x] `role-pipeline-report.yaml` — monthly, posts role pipeline snapshot to `#t-engagement` via Slack webhook
- [x] `SLACK_WEBHOOK_ENGAGEMENT` secret added to GitHub Actions repo secrets
- [x] `tools/notify/post.sh` — manual Slack post helper for agent-produced summaries
- [x] `docs/runbook-weekly-summary.md` — runbook for agent-assisted weekly org summary
- [x] **Incident fix (2026-07-07):** `role-pipeline-report.yaml`'s cron `'0 10 1-7 * 1'` mixed day-of-month and day-of-week fields, which cron evaluates as OR — it fired daily (confirmed via run history: July 1-7 daily, plus June 15/22/29) instead of monthly, spamming `#t-engagement`. Fixed in [PR #485](https://github.com/open-austin/org/pull/485): plain weekly `0 10 * * 1` cron with a job-level guard that skips unless day-of-month ≤ 7.

### Issue template + form labeling

- [x] Updated `open-role.yaml` issue template — simplified to single team dropdown, commitment level, skills fields
- [x] `label-open-role-from-form.yaml` — reads team dropdown on new open role issues, applies correct label(s); Product Team → adds both `product team` + `engagement`

## Ready for Human QA

All workflows need testing in the live GitHub environment. Suggested test order:

1. **`add-issue-to-kanban.yaml`** — Open a new plain issue → should appear in Org Kanban "To Do"
2. **`open-role-add.yaml`** — Open a new issue, add `open role` label → should land on Open Roles, absent from Org Kanban
3. **`close-to-done.yaml`** — Close an issue on the Org Kanban → should move to Done
4. **`done-to-close.yaml`** — Move a Kanban item to Done manually → linked issue should close
5. **`kanban-status-reopen.yaml`** — Move a Done/closed item back to To Do → issue should reopen
6. **`reopened-to-todo.yaml`** — Reopen a closed non-open-role issue → Kanban status should go to To Do
7. **`filled-to-close.yaml`** — Move Open Roles item to Filled → issue should close
8. **`closed-to-filled.yaml`** — Close an open role issue directly → Open Roles board should show Filled
9. **`open-roles-reopen.yaml`** — Move a Filled role back to Open → issue should reopen
10. **`open-role-reopened.yaml`** — Reopen a closed open role issue → Open Roles board should show Open
11. **`archive-old-done.yaml`** — Trigger via Actions UI with `dry_run=true` → verify log output
12. **`archive-old-filled.yaml`** — Trigger via Actions UI with `dry_run=true` → verify log output
13. **`role-pipeline-report.yaml` fix** — merge [PR #485](https://github.com/open-austin/org/pull/485), confirm the workflow is enabled in Actions (it showed `active` as of 2026-07-07 despite the spam), and watch the next Monday: it should only post on the one that falls on day-of-month 1-7

---

## Done

- [x] Discovered existing `open-role-add.yaml` workflow (partial open role routing)
- [x] Confirmed `ACTIONS_TOKEN` secret is already configured
- [x] Confirmed "Filled" status option already exists on Open Roles board
- [x] Documented all project IDs, field IDs, and status option IDs
