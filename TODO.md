# TODO
This is the coordination map for active work in this repo. See `skills/run-project-spike/SKILL.md` for the full process.

## Done
### Board ↔ Issue Sync Redesign *(archived: `docs/archive/board-sync-redesign.md`)*
Re-architected board↔issue sync: native `Auto-close issue` is the single non-code exception (card→close), everything else is code, one `board-reopen-reconcile` poller (~5 min) handles card→reopen, all other native Projects workflows off. Confirmed working live 2026-07-08. Durable outcomes in `README.md` (Board Automation) and decisions `0004`/`0005`. Note: GitHub scheduled runs can be badly delayed (first reopen took ~25+ min).

### GitHub Automation *(archived: `docs/archive/github-automation.md`)*
Built the full board/issue automation set — routing, issue↔board status sync, scheduled archive, Slack reporting, form labeling. Two incidents fixed en route: `role-pipeline-report` cron firing daily instead of monthly, and the `projects_v2_item` trigger being invalid so board→issue sync never fired (decision `0004`, which spawned the Board Sync Redesign). Also hardened `label-open-role-from-form` (script-injection) and `stale-role-warning` (YAML block-scalar bug that had kept it from ever running).

### Backlog Triage *(archived: `docs/archive/backlog-triage.md`)*
Restructured label taxonomy to match Refactor 2026 Teams structure. Labeled all issues, closed dead issues, retired old labels. Done column cleanup and "To Do" column review deferred to automation spike and human triage.

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
### Weekly Meeting Processing
Develop the public Open Austin workflow and bounded tools for reconciling the weekly organizing meeting with its canonical shared Google Doc and GitHub issues. See [docs/active-spikes/weekly-meeting-processing.md](docs/active-spikes/weekly-meeting-processing.md) and [docs/active-spikes/weekly-meeting-processing.todo.md](docs/active-spikes/weekly-meeting-processing.todo.md).

## Automation — residual QA / watch
Low-priority follow-ups left after archiving the automation spikes (2026-07-08). None block anything; the automation is live and working.

- **`role-pipeline-report` next first-Monday** — the cron fix (skip unless day-of-month ≤ 7) hasn't been observed on a real first Monday yet. Confirm it posts once, not daily.
- **`archive-old-done` / `archive-old-filled`** — implemented with dry-run defaults but never exercised. Run each once via the Actions UI with `dry_run=true` to eyeball the output when convenient.
- **`stale-role-warning` dry-run** — YAML parse bug fixed and logic proven locally; a `dry_run` input was added (commit pending). After committing, dispatch once with `dry_run=true` to confirm end-to-end.
- **Two board-sync edge paths** — blank-issue-then-`open role` routing, and the fresh-close guard, are verified by reading but not exercised live.

## Later / Ideas
- **Google Drive agent access** — once the GitHub layer is stable, giving agents GDrive read access would allow them to use org docs, meeting notes, and wiki exports as context without needing everything committed to the repo
- **Staleness surfacing** — periodic snapshot-based digest of stale issues for agent-assisted triage sessions
- **Board resolution tracking** — low priority for now; decision-making is highly human/interpersonal
- **Board onboarding doc** — carried over from the wiki migration (`docs/archive/wiki-migration.md`); unconfirmed whether existing material exists or still needs creating (closed #393 noted onboarding should be handled here)
- **Contributor Profile board** — handled in the CoP repos, not here; the org-repo automation doesn't touch it (user to log a ticket)

Use `docs/scratch/future-ideas.md` for conceptual someday org/tooling/process material that is too early for active spike work.

*(Completed spikes and tasks are archived here or moved to `docs/archive/`.)*
