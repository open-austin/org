# TODO
This is the coordination map for active work in this repo. See `project-workflows/run-project-spike/SKILL.md` for the full process.

## Active
- **Project Workflows adoption** — [reconciliation](docs/active-spikes/project-workflows-adoption.md) · [local validation and publication hold](docs/active-spikes/project-workflows-adoption.todo.md).

## Done
### Retire Sync Tooling *(archived: `docs/archive/retire-sync-tooling.md`)*
Removed `tools/sync/` and `tools/issues/create.sh` — single-maintainer tooling that had no second user and split the maintainer's own workflow across two repos. The weekly org summary ran a final time to all seven team channels on 2026-09-07 and is now retired, its skill kept as the reimplementation record. What stayed at retirement: `tools/notify/`, `tools/google-docs/`, `tools/airtable/`, all thirteen Actions workflows, and both the PAT setup and Write Safety sections of CONTRIBUTING, which turned out not to be sync-specific. **2026-10-27 correction:** the scheduled role report uses inline curl, not `tools/notify/`; Google Docs is now delegated to Agent Hands. See the Agent Hands cutover below.

### Board ↔ Issue Sync Redesign *(archived: `docs/archive/board-sync-redesign.md`)*
Re-architected board↔issue sync: native `Auto-close issue` is the single non-code exception (card→close), everything else is code, one `board-reopen-reconcile` poller (~5 min) handles card→reopen, all other native Projects workflows off. Confirmed working live 2026-07-08. Durable outcomes in `README.md` (Board Automation) and policies `0004`/`0005`. Note: GitHub scheduled runs can be badly delayed (first reopen took ~25+ min).

### GitHub Automation *(archived: `docs/archive/github-automation.md`)*
Built the full board/issue automation set — routing, issue↔board status sync, scheduled archive, Slack reporting, form labeling. Two incidents fixed en route: `role-pipeline-report` cron firing daily instead of monthly, and the `projects_v2_item` trigger being invalid so board→issue sync never fired (policy `0004`, which spawned the Board Sync Redesign). Also hardened `label-open-role-from-form` (script-injection) and `stale-role-warning` (YAML block-scalar bug that had kept it from ever running).

### Backlog Triage *(archived: `docs/archive/backlog-triage.md`)*
Restructured label taxonomy to match Refactor 2026 Teams structure. Labeled all issues, closed dead issues, retired old labels. Done column cleanup and "To Do" column review deferred to automation spike and human triage.

### Weekly Summary Per-Team Channels *(archived: `docs/archive/weekly-summary-channels.md`; the workflow itself was **retired 2026-09-07** — see `skills/weekly-org-summary/SKILL.md`)*
Broke the weekly org summary into per-team Slack channels (`#oa-board`, `#t-infrastructure`, `#t-finance`, `#t-fundraising`, `#t-communications`, `#t-education`, `#pg-data-fellowship`, plus existing `#t-engagement`); `#oa-org` is now priority-only. First real run posted successfully 2026-07-07. See the archived to-do doc for two editorial points that weren't explicitly re-confirmed before closing (multi-label cross-posting, open-role issues in non-engagement channels).

### Wiki Migration *(archived: `docs/archive/wiki-migration.md`)*
Migrated GitHub wiki content to Google Drive: cloned the wiki, moved content over, left a forwarding note, formally retired the wiki. See the archived to-do doc for what wasn't explicitly confirmed (board onboarding doc gap, no settled norm on where future org docs should live).

### GitHub Tooling *(archived: `docs/archive/github-tooling.md`)*
Built Python sync tools (`tools/sync/`) that pull issues (with full comment threads), labels, and board state into local `snapshot/` markdown. Write operations use `gh` CLI directly. See `AGENTS.md` for tool usage. *(Superseded 2026-09-07: `tools/sync/` was removed — see `docs/archive/retire-sync-tooling.md`.)*

### Repo Scaffolding
Getting the repo into a state where agents can work effectively and the methodology is established.

- [x] Adapt `docs/how-to-spike.md` to this repo's context *(superseded 2026-07-07: process now lives in `project-workflows/run-project-spike/SKILL.md`)*
- [x] Create `AGENTS.md`
- [x] Create `CLAUDE.md` (symlink → `AGENTS.md`)
- [x] Add `.claude/` and `.env` to `.gitignore`
- [x] Create `TODO.md`
- [x] Create `.env.example`
- [x] Create `docs/policies/0001-tooling-foundations.md`
- [x] Archive `prompt-doc.md`
- [x] Create `CONTRIBUTING.md`
- [x] Auth setup: `gh auth login` with PAT authorized for `open-austin` org
- [x] Confirm SAML SSO authorization if required
- [x] Verify `gh project list --owner open-austin` returns real board data
- [x] Initial backlog analysis: 27 open issues, staleness breakdown
- [x] Update `README.md` to document tooling and workflow

## Active Spikes
- Agent Hands cutover (slug `agent-hands-cutover`, opened 2026-10-27): [scope and ownership](docs/active-spikes/agent-hands-cutover.md), [checks and remaining limits](docs/active-spikes/agent-hands-cutover.todo.md). Generic Docs moved to Agent Hands and webhook preview hardening is implemented; final publication checks remain in progress.
- Policies Migration (slug `policies-migration`, opened 2026-10-14): migrated current guidance and local routing to `docs/policies/`; verification and checkpoint state in [reasoning](docs/active-spikes/policies-migration.md) and [tasks](docs/active-spikes/policies-migration.todo.md). Closure pending.
### Airtable Tooling → `docs/active-spikes/airtable-tooling.md` (+ `.todo.md`)
Org-specific Airtable operations remain in `tools/airtable/`; Agent Hands currently has no Airtable capability. The owning spike records completed read tooling and guarded schema/import work. Follow its current task list and evidence rather than the superseded initial credential-setup blocker; this review does not verify current account access or authorize further data changes.

## Automation — residual QA / watch
Low-priority follow-ups left after archiving the automation spikes (2026-07-08). None block anything; the automation is live and working.

- **`role-pipeline-report` next first-Monday** — the cron fix (skip unless day-of-month ≤ 7) hasn't been observed on a real first Monday yet. Confirm it posts once, not daily.
- **`archive-old-done` / `archive-old-filled`** — implemented with dry-run defaults but never exercised. Run each once via the Actions UI with `dry_run=true` to eyeball the output when convenient.
- **`stale-role-warning` dry-run** — YAML parse bug fixed and logic proven locally; the `dry_run` input is committed. An authorized dispatch with `dry_run=true` still needs end-to-end confirmation.
- **Two board-sync edge paths** — blank-issue-then-`open role` routing, and the fresh-close guard, are verified by reading but not exercised live.

*(Completed spikes and tasks are archived here or moved to `docs/archive/`.)*
