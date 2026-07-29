# Open Austin Org Tooling
This repo contains tools, documentation, and automation for managing the [Open Austin](https://www.open-austin.org/) GitHub organization.

**Purpose:** Keep our issue tracker, project boards, labels, and documentation in sync with the org's current structure and priorities.

## Quick Start
### For Contributors
See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions (GitHub CLI, auth, spike workflow).

### For Agents
See [AGENTS.md](AGENTS.md) or [CLAUDE.md](CLAUDE.md) for rules, boundaries, and write safety requirements.

## Sync Tools
The sync tools pull current org state into local markdown snapshots. This gives you (or an agent) full context without repeated API calls.

**Run the sync:**

```bash
tools/sync/run.sh
```

**Output:**
- `snapshot/issues.md` — all open issues grouped by team label
- `snapshot/labels.md` — current label taxonomy
- `snapshot/board-org-kanban.md` — Org Kanban project board
- `snapshot/board-open-roles.md` — Open Roles project board

**Snapshots are gitignored** — always regenerate them at the start of a work session.

## Write Operations
Guarded writes happen through the **board-automation workflows** described below, the repo's narrow dry-run-first tools, and the **`gh` CLI** for ad-hoc changes that do not yet justify a wrapper. Use `tools/issues/create.sh` for issue creation and `tools/google-docs/run.sh` for bounded shared-Doc reads and exact-match replacements. See [AGENTS.md](AGENTS.md) for the approval and write-safety rules.

All write operations follow the write-safety rules: dry-run first where supported, and explicit approval before anything that mutates shared org state.

### Issue Creation
```bash
tools/issues/create.sh --title "Task title" --body-file /tmp/issue.md --label infrastructure --assign-me
tools/issues/create.sh --title "Task title" --body-file /tmp/issue.md --label infrastructure --assign-me --execute
```

The first command prints the exact plan and changes nothing. `--execute` creates the approved issue and refreshes `snapshot/` unless `--no-sync` is supplied.

### Shared Google Docs
Copy `.env.example` to the ignored `.env`, set the Google credential/token paths, and enable the Google Docs API for the OAuth project. New contributors can authorize with:

```bash
tools/google-docs/run.sh auth
```

When the standard LifeOS credential and Open Austin token files exist under `~/configs/lifeos-tools/secrets/`, the wrapper reuses them automatically; the repo does not create a second credential or token copy. Other contributors configure their own paths in `.env`.

An existing read-only LifeOS token can run `read` and dry-run planning, but the first executed Doc replacement requires the Google Docs write scope. Run `tools/google-docs/run.sh auth` once to grant that scope into the same configured token file before the first approved write.

Read the canonical weekly notes or preview one exact replacement:

```bash
tools/google-docs/run.sh read
tools/google-docs/run.sh replace-once --old-file /tmp/current.txt --new-file /tmp/replacement.txt
```

The replacement tool requires the old text to occur exactly once, re-fetches before mutation, and writes only with `--execute`. Use it for bounded corrections, action-state changes, and issue cross-links—not for inserting parallel agent minutes.

## Weekly Organizing Meeting
Follow [skills/process-weekly-meeting/SKILL.md](skills/process-weekly-meeting/SKILL.md) when reconciling the recurring weekly organizing meeting. `General Organizing - meeting notes` remains canonical. The workflow audits chatbot-produced beat-by-beat notes and analysis against the matching dated section and fresh GitHub state, then produces an exact approval slate before any shared Doc or public issue changes.

## Board Automation
GitHub Actions in [`.github/workflows/`](.github/workflows/) keep issue state and the two project boards (Org Kanban, Open Roles) in sync, so closing/reopening an issue and moving a board card stay consistent without manual bookkeeping. **Almost everything is custom Actions in this repo** — with exactly **one deliberate exception**: the native Projects "Auto-close issue" workflow (see below). All other native Projects workflows are intentionally turned **off**, so code is the single source of truth.

A tracked issue has one continuous lifecycle: it's **opened**, routed once (by whether it carries the `open role` label) to one board, and then cycles between an open state and a closed state on that board. Each cycle transition can be driven from **either side** — act on the issue, or move the card — and they stay in sync.

```mermaid
flowchart TD
    OPENED([Issue opened]) --> Q{Open role?}

    subgraph KANBAN["Org Kanban board"]
        K_TODO["To Do<br/>(issue open)"]
        K_DONE["Done<br/>(issue closed)"]
        K_TODO -->|"close issue → close-to-done<br/>· or drag card to Done → native Auto-close"| K_DONE
        K_DONE -->|"reopen issue → reopened-to-todo<br/>· or drag card off Done → reconcile poll ~5m"| K_TODO
    end

    subgraph ROLES["Open Roles board"]
        R_OPEN["Open<br/>(issue open)"]
        R_FILLED["Filled<br/>(issue closed)"]
        R_OPEN -->|"close issue → closed-to-filled<br/>· or drag card to Filled → native Auto-close"| R_FILLED
        R_FILLED -->|"reopen issue → open-role-reopened<br/>· or drag card off Filled → reconcile poll ~5m"| R_OPEN
    end

    Q -->|no · add-issue-to-kanban| K_TODO
    Q -->|yes · open-role-add| R_OPEN
```

Everything on the issue side (open / close / reopen) and the native card→close is **immediate**. The one lagging path is **card → reopen** (dragging a card out of Done/Filled): it's the single scheduled job (`board-reopen-reconcile`), and **GitHub's scheduled runs are best-effort, often delayed 10–30+ minutes** (the first run after enabling is slowest) — so reopening the *issue* directly is the instant option. That reconciler is the one exception to "immediate"; the one exception to "in the repo" is the native `Auto-close issue` workflow (card→close), which is configured in the Projects UI and has no workflow file. A fresh-close guard keeps the reconciler from resurrecting issues closed before this automation existed (it skips anything closed in the last 10 minutes; a one-time cleanup tool used during rollout confirmed the boards were already consistent and has since been removed).

**Routing is right-the-first-time — no board is wastefully double-touched.** An open-role issue created via the form goes straight to Open Roles and never lands on the Kanban. The *only* time anything is removed from a board is **reclassification**: a plain issue that landed on the Kanban is *later* labeled `open role`, so `open-role-add` moves it to Open Roles and clears the now-stale Kanban card. Separately, `label-open-role-from-form` reads the open-role form's team dropdown and applies the team label(s).

**Scheduled maintenance & reporting** (separate from the sync loop above):

| Workflow | Cadence | Purpose |
|---|---|---|
| `archive-old-done` | weekly | Archive Org Kanban `Done` items older than 180 days |
| `archive-old-filled` | weekly | Archive Open Roles `Filled` items older than 1 year |
| `stale-role-warning` | weekly | Comment on open roles with no update in 90+ days |
| `role-pipeline-report` | monthly (1st Monday) | Post the Open Roles pipeline snapshot to `#t-engagement` |

Per-team weekly issue summaries to Slack are handled separately by the [`weekly-org-summary`](skills/weekly-org-summary/SKILL.md) skill, not by these Actions.

## Documentation
- **Active spikes:** `docs/active-spikes/` — current work with accompanying `.todo.md` files
- **Decisions:** `docs/decisions/` — settled architectural choices
- **Pinned issues:** `docs/pinned-issues.md` — unresolved org/tooling/process questions intentionally preserved for later
- **Future ideas:** `docs/scratch/future-ideas.md` — conceptual someday material that is not active work
- **Misc intake:** `docs/scratch/misc.md` — raw observed friction and issue intake
- **Scratch:** `docs/scratch/` — exploratory drafts
- **Archive:** `docs/archive/` — historical context

See [skills/run-project-spike/SKILL.md](skills/run-project-spike/SKILL.md) for the full workflow, and [skills/](skills/) for the repo's other agent-assisted workflows.
