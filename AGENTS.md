# AGENTS.md — Open Austin Org Tooling

This file defines the rules and boundaries for AI agents working in this repo. Read it before taking any action.

---

## What This Repo Is

This repo is the operational layer for the Open Austin GitHub org. It contains tooling, documentation, and automation for managing issues, project boards, labels, milestones, and org health.

Agents are primary users of the tools here. This doc is your operating manual.

---

## Authority Ladder

When docs conflict, use this order:

1. `AGENTS.md` (this file) and `README.md` — durable project rules
2. `contributor-policy.md` — Open Austin governance doc; **do not edit it** through tooling or agent work
3. Active decision records in `docs/decisions/` — settled tradeoffs
4. Active spike docs — current thinking for a theme of work
5. `TODO.md` — active work coordination
6. `docs/scratch/` — exploratory, non-authoritative
7. `docs/archive/` — historical context only

---

## What Agents May Do

- Read and render snapshots from GitHub (issues, labels, milestones, project boards)
- Run any `gh` read command (`gh issue list`, `gh project item-list`, `gh api graphql` for reads, etc.)
- Analyze, cluster, triage, and summarize backlog state
- Draft proposed changes for user review
- Run write commands **only after the user explicitly approves a specific plan**

---

## What Agents Must NOT Do Without Explicit User Approval

- Create, edit, close, or delete GitHub issues
- Add, remove, or change labels or milestones on issues
- Move items on a Project v2 board (status field changes)
- Post comments on issues or PRs — comments notify real people
- Bulk-edit anything without a reviewed plan
- Push commits or open PRs
- Edit `contributor-policy.md`

If you are unsure whether an action requires approval, it does. Ask first.

---

## Write Safety Rules

These rules apply to all write operations, no exceptions:

1. **Dry-run by default.** All write tools must support a `--dry-run` flag that shows exactly what would change without changing it.
2. **Plan before bulk.** Any operation affecting more than one issue or item requires the user to review and approve a complete change plan first.
3. **Re-fetch before mutate.** Before executing a write, re-read current state from the API — never act on a stale snapshot.
4. **No destructive deletes.** Prefer close/archive/relabel over deletion. Never hard-delete issues, comments, or project items.
5. **Bounded notifications.** Be conservative about comments and @-mentions. Automated chatter on a shared org is costly.

---

## Auth Model

- Credentials are loaded from the environment at runtime — never hardcoded or committed.
- The required env var is `GH_TOKEN` (a GitHub PAT or token authorized via `gh auth login`).
- See `.env.example` for the full list of required variables and their required scopes.
- If the `open-austin` org enforces SAML SSO, the token must be SSO-authorized in GitHub's UI before use.
- Never commit `.env`, `gh` host config, or any file containing a real token.

---

## Tooling Overview

### Sync Tools

Run at the start of any work session to pull current org state into local markdown:

```bash
tools/sync/run.sh
```

Outputs to `snapshot/` (gitignored — always regenerate, never commit):
- `snapshot/issues.md` — index of all open issues grouped by team label
- `snapshot/issues/<number>.md` — full issue with complete comment thread
- `snapshot/labels.md` — current label taxonomy
- `snapshot/board-org-kanban.md` — Org Kanban project board by status column
- `snapshot/board-open-roles.md` — Open Roles project board

Tools are Python 3 scripts that call `gh` CLI and format output as readable markdown. No external dependencies beyond `gh`.

### Notify Tools

Post messages to Slack via Incoming Webhooks:

```bash
source .env
echo "Your message" | tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT
```

Webhook URLs are stored in `.env` (gitignored). See `.env.example` for the full list. The webhook var name maps to a specific channel — see `docs/runbook-weekly-summary.md` for the channel table.

### Write Operations

Use `gh` CLI directly for writes. All writes require explicit user approval first per the Write Safety Rules above.

Common commands:
```bash
gh issue edit <number> --repo open-austin/org --add-label <label>
gh issue edit <number> --repo open-austin/org --remove-label <label>
gh issue close <number> --repo open-austin/org --comment "<reason>"
gh label create <name> --repo open-austin/org --color <hex> --description "<desc>"
gh label delete <name> --repo open-austin/org --yes
```

For Projects v2 board moves, use `gh project item-edit` or the GraphQL API via `gh api graphql`.

---

## Process

This repo uses a spike-based workflow. See `docs/how-to-spike.md` for the full process.

Active work is tracked in `TODO.md`. Settled decisions live in `docs/decisions/`. Finished spikes are archived in `docs/archive/`.

---

## Runbooks

Runbooks describe repeatable agent-assisted workflows. When the user asks for one of these by name or intent, follow the runbook.

| Runbook | Trigger phrases |
|---|---|
| `docs/runbook-weekly-summary.md` | "weekly summary", "weekly update", "org digest", "what's going on this week" |
