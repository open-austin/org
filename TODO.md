# TODO
This is the coordination map for active work in this repo. See `skills/run-project-spike/SKILL.md` for the full process.

## Done
### Weekly Summary Per-Team Channels *(archived: `docs/archive/weekly-summary-channels.md`)*
Broke the weekly org summary into per-team Slack channels (`#oa-board`, `#t-infrastructure`, `#t-finance`, `#t-fundraising`, `#t-communications`, `#t-education`, `#pg-data-fellowship`, plus existing `#t-engagement`); `#oa-org` is now priority-only. First real run posted successfully 2026-07-07. See the archived to-do doc for two editorial points that weren't explicitly re-confirmed before closing (multi-label cross-posting, open-role issues in non-engagement channels).

### Wiki Migration *(archived: `docs/archive/wiki-migration.md`)*
Migrated GitHub wiki content to Google Drive: cloned the wiki, moved content over, left a forwarding note, formally retired the wiki. See the archived to-do doc for what wasn't explicitly confirmed (board onboarding doc gap, no settled norm on where future org docs should live).

### GitHub Tooling *(archived: `docs/archive/github-tooling.md`)*
Built Python sync tools (`tools/sync/`) that pull issues (with full comment threads), labels, and board state into local `snapshot/` markdown. Write operations use `gh` CLI directly. See `AGENTS.md` for tool usage.

### Repo Scaffolding
Getting the repo into a state where agents can work effectively and the methodology is established.

- [x] Adapt `docs/how-to-spike.md` to this repo's context *(superseded 2026-07-07: process now lives in `skills/run-project-spike/SKILL.md`)*
- [x] Create `AGENTS.md`
- [x] Create `CLAUDE.md` (symlink → `AGENTS.md`)
- [x] Add `.claude/` and `.env` to `.gitignore`
- [x] Create `TODO.md`
- [x] Create `.env.example`
- [x] Create `docs/decisions/0001-tooling-foundations.md`
- [x] Archive `prompt-doc.md`
- [x] Create `CONTRIBUTING.md`
- [x] Auth setup: `gh auth login` with PAT authorized for `open-austin` org
- [x] Confirm SAML SSO authorization if required
- [x] Verify `gh project list --owner open-austin` returns real board data
- [x] Initial backlog analysis: 27 open issues, staleness breakdown
- [x] Update `README.md` to document tooling and workflow

## Active Spikes
### Board ↔ Issue Sync Redesign
**Status:** Planned, not yet implemented
**Spike:** `docs/active-spikes/board-sync-redesign.md`
**Todo:** `docs/active-spikes/board-sync-redesign.todo.md`

Re-architecting board↔issue sync: native `Auto-close issue` for card→close (the one non-code exception), everything else in code, one 5-minute reopen poller, all other native Projects workflows off. Continues from the GitHub Automation spike. Plan is written; implementation pending (starts with native UI config + a one-time baseline cleanup).

### Backlog Triage *(archived: `docs/archive/backlog-triage.md`)*
Restructured label taxonomy to match Refactor 2026 Teams structure. Labeled all issues, closed dead issues, retired old labels. Done column cleanup and "To Do" column review deferred to automation spike and human triage.

### GitHub Automation
**Status:** Active
**Spike:** `docs/active-spikes/github-automation.md`
**Todo:** `docs/active-spikes/github-automation.todo.md`

GitHub Actions to keep boards and issue state in sync. Fixes the root cause of board noise. `ACTIONS_TOKEN` secret and project IDs are confirmed.

**Incident (2026-07-07):** `role-pipeline-report.yaml`'s cron mixed day-of-month and day-of-week fields, which cron evaluates as OR — it fired daily instead of monthly and spammed `#t-engagement`. Fix applied as a plain working-tree change (not yet committed) rather than a PR — see the to-do doc.

**Incident (2026-07-08):** the board→issue direction of both bidirectional syncs (Filled→close, Open/In Progress→reopen) was silently dead — `on: projects_v2_item` isn't a valid repo-level Actions trigger and never fired. See `docs/decisions/0004-projects-v2-automation-triggers.md`. `filled-to-close.yaml`/`done-to-close.yaml` deleted (superseded by Projects v2's native "Auto-close issue" workflow); `open-roles-reopen.yaml`/`kanban-status-reopen.yaml` rewritten as 15-minute scheduled reconciliation jobs. Also uncommitted working-tree changes.

- [x] Automation 1: Enhance open role routing (remove from Org Kanban when `open role` labeled)
- [x] Automation 2: New issue → Org Kanban "To Do"
- [x] Automation 3: Issue closed → move to Done on Org Kanban
- [x] Automation 4: Open Roles "Filled" → auto-close issue
- [x] Automation 5: Done > 6 months → auto-archive (scheduled)
- [x] Automation 6: Done → close issue (bidirectional Kanban)
- [x] Automation 7: To Do/In Progress → reopen issue (bidirectional Kanban)
- [x] Automation 8: Issue reopened → Kanban "To Do"
- [x] Automation 9: Issue closed (open role) → Open Roles "Filled"
- [x] Automation 10: Open Roles Open/In Progress → reopen issue
- [x] Automation 11: Issue reopened (open role) → Open Roles "Open"
- [x] Automation 12: Open Roles Filled > 1 year → auto-archive (scheduled)
- [ ] Human QA: test all workflows in live GitHub environment

- **Google Drive agent access** — once the GitHub layer is stable, giving agents GDrive read access would allow them to use org docs, meeting notes, and wiki exports as context without needing everything committed to the repo
- **Staleness surfacing** — periodic snapshot-based digest of stale issues for agent-assisted triage sessions
- **Board resolution tracking** — low priority for now; decision-making is highly human/interpersonal
- **Board onboarding doc** — carried over from the wiki migration (`docs/archive/wiki-migration.md`); unconfirmed whether existing material exists or still needs creating (closed #393 noted onboarding should be handled here)

*(Completed spikes and tasks are archived here or moved to `docs/archive/`.)*
