# TODO

This is the coordination map for active work in this repo. See `docs/how-to-spike.md` for the full process.

---

## Done

### GitHub Tooling *(archived: `docs/archive/github-tooling.md`)*

Built Python sync tools (`tools/sync/`) that pull issues (with full comment threads), labels, and board state into local `snapshot/` markdown. Write operations use `gh` CLI directly. See `AGENTS.md` for tool usage.

### Repo Scaffolding

Getting the repo into a state where agents can work effectively and the methodology is established.

- [x] Adapt `docs/how-to-spike.md` to this repo's context
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

---

## Active Spikes

### Backlog Triage *(archived: `docs/archive/backlog-triage.md`)*

Restructured label taxonomy to match Refactor 2026 Teams structure. Labeled all issues, closed dead issues, retired old labels. Done column cleanup and "To Do" column review deferred to automation spike and human triage.

### Wiki Migration

**Status:** Conceptual
**Spike:** `docs/scratch/wiki-migration.md`

Move GitHub wiki content to Google Drive where non-technical contributors can access it.

- [ ] Clone wiki repo locally, inventory all pages
- [ ] Assess staleness, flag redundant content
- [ ] Migrate content to Google Drive (destination TBD)
- [ ] Human review of Google Drive structure
- [ ] Leave forwarding note in wiki
- [ ] Formally retire wiki

### GitHub Automation

**Status:** Active
**Spike:** `docs/github-automation.md`
**Todo:** `docs/github-automation.todo.md`

GitHub Actions to keep boards and issue state in sync. Fixes the root cause of board noise. `ACTIONS_TOKEN` secret and project IDs are confirmed.

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

---

*(Completed spikes and tasks are archived here or moved to `docs/archive/`.)*
