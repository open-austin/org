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

## Write Tools
Write tools for guarded mutations (label changes, issue closes, board moves) are in active development. See `docs/github-tooling.todo.md` for status.

All write operations require `--dry-run` by default and explicit approval before execution.

## Documentation
- **Active spikes:** `docs/active-spikes/` — current work with accompanying `.todo.md` files
- **Decisions:** `docs/decisions/` — settled architectural choices
- **Scratch:** `docs/scratch/` — exploratory drafts
- **Archive:** `docs/archive/` — historical context

See [skills/run-project-spike/SKILL.md](skills/run-project-spike/SKILL.md) for the full workflow, and [skills/](skills/) for the repo's other agent-assisted workflows.
