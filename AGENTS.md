# AGENTS.md — Open Austin Org Tooling
This file defines the rules and boundaries for AI agents working in this repo. Read it before taking any action.

## What This Repo Is
This repo is the public operational layer for Open Austin. It contains tooling, documentation, and automation for managing GitHub issues, project boards, labels, milestones, org health, and bounded updates to shared organizational records used by its workflows.

Agents are primary users of the tools here. This doc is your operating manual.

## Authority Ladder
When docs conflict, use this order:

1. `AGENTS.md` (this file) and `README.md` — durable project rules
2. `contributor-policy.md` — Open Austin governance doc; **do not edit it** through tooling or agent work
3. Active decision records in `docs/decisions/` — settled tradeoffs
4. Active spike docs in `docs/active-spikes/` — current thinking for a theme of work
5. `TODO.md` — active work coordination
6. `docs/pinned-issues.md` — unresolved issues intentionally preserved for later
7. `docs/scratch/future-ideas.md` — conceptual someday material
8. `docs/scratch/misc.md` and other `docs/scratch/` files — exploratory intake, non-authoritative
9. `docs/archive/` — historical context only

This repo carries its own agent workflows in `skills/`. Repo-local skills are project authority — prefer `skills/<skill-name>/SKILL.md` over similarly named global skills, which are fallback seed material only.

## What Agents May Do
- Read and render snapshots from GitHub (issues, labels, milestones, project boards)
- Read shared Open Austin Google Docs when the current workflow needs them
- Run any `gh` read command (`gh issue list`, `gh project item-list`, `gh api graphql` for reads, etc.)
- Analyze, cluster, triage, and summarize backlog state
- Draft proposed GitHub or shared-Doc changes for user review
- Run write commands **only after the user explicitly approves a specific plan**

## What Agents Must NOT Do Without Explicit User Approval
- Create, edit, close, or delete GitHub issues
- Add, remove, or change labels or milestones on issues
- Move items on a Project v2 board (status field changes)
- Post comments on issues or PRs — comments notify real people
- Edit a shared Google Doc
- Bulk-edit anything without a reviewed plan
- Push commits or open PRs
- Edit `contributor-policy.md`

If you are unsure whether an action requires approval, it does. Ask first.

## Write Safety Rules
These rules apply to all write operations, no exceptions:

1. **Dry-run by default.** All write tools must support a `--dry-run` flag that shows exactly what would change without changing it.
2. **Plan before bulk.** Any operation affecting more than one issue or item requires the user to review and approve a complete change plan first.
3. **Re-fetch before mutate.** Before executing a write, re-read current state from the API — never act on a stale snapshot.
4. **No destructive deletes.** Prefer close/archive/relabel over deletion. Never hard-delete issues, comments, or project items.
5. **Bounded notifications.** Be conservative about comments and @-mentions. Automated chatter on a shared org is costly.

## Auth Model
- Credentials are loaded from the environment at runtime — never hardcoded or committed.
- GitHub operations use `GH_TOKEN` (a GitHub PAT or token authorized via `gh auth login`).
- Google Docs operations use the local credential and token paths documented in `.env.example`; real OAuth files remain outside this repo. The wrapper can reuse standard LifeOS credential and Open Austin token files when they already exist.
- See `.env.example` for the full list of required variables and their required scopes.
- If the `open-austin` org enforces SAML SSO, the token must be SSO-authorized in GitHub's UI before use.
- Never commit `.env`, `gh` host config, or any file containing a real token.

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

Webhook URLs are stored in `.env` (gitignored). See `.env.example` for the full list. The webhook var name maps to a specific channel — see `skills/weekly-org-summary/SKILL.md` for the channel table.

### Google Docs Tools
Use `tools/google-docs/run.sh read` for document text and `replace-once` for one exact, uniquely occurring replacement. `replace-once` is dry-run by default, re-fetches before execution, and uses the live revision ID. Follow `skills/process-weekly-meeting/SKILL.md` for the weekly organizing meeting's canonical-record and approval rules.

### Write Operations
Use the guarded repo tools when a matching operation exists, and use `gh` CLI directly for other writes. All writes require explicit user approval first per the Write Safety Rules above.

Create a new issue with `tools/issues/create.sh`, which prints an exact dry-run plan unless `--execute` is supplied. Use `tools/google-docs/run.sh` for bounded shared-Doc reads and exact-match replacements. Google Docs replacements are also dry-run by default and must match exactly once before execution.

Common commands:
```bash
gh issue edit <number> --repo open-austin/org --add-label <label>
gh issue edit <number> --repo open-austin/org --remove-label <label>
gh issue close <number> --repo open-austin/org --comment "<reason>"
gh label create <name> --repo open-austin/org --color <hex> --description "<desc>"
gh label delete <name> --repo open-austin/org --yes
```

For Projects v2 board moves, use `gh project item-edit` or the GraphQL API via `gh api graphql`.

## Process
This repo uses a spike-based workflow. See `skills/run-project-spike/SKILL.md` for the full process.

Active work is tracked in `TODO.md`. Settled decisions live in `docs/decisions/`. Unresolved issues intentionally preserved for later live in `docs/pinned-issues.md`. Conceptual someday material lives in `docs/scratch/future-ideas.md`. Raw observed friction and issue intake live in `docs/scratch/misc.md`. Finished spikes are archived in `docs/archive/`.

Use these holding areas carefully: `docs/pinned-issues.md` is not a GitHub issue backlog, `docs/scratch/future-ideas.md` is not active roadmap, and `docs/scratch/misc.md` is not durable authority. Public-org writes still require explicit approval.

## Skills
Repeatable agent-assisted workflows live in `skills/`. When the user asks for one of these by name or intent, follow the local skill.

| Skill | Trigger phrases / use |
|---|---|
| `skills/commit-work/SKILL.md` | Committing completed work atomically by explicit pathspec without pushing or rewriting history |
| `skills/run-project-spike/SKILL.md` | Starting, continuing, promoting, or archiving spike work |
| `skills/triage-project-misc/SKILL.md` | Reviewing or routing `docs/scratch/misc.md` |
| `skills/pin-issue/SKILL.md` | Preserving unresolved org/tooling/process issues for later |
| `skills/log-future-idea/SKILL.md` | Capturing conceptual someday org/tooling/process ideas |
| `skills/update-local-skills/SKILL.md` | Refreshing repo-local skill copies from global seed skills while preserving local divergence |
| `skills/weekly-org-summary/SKILL.md` | "weekly summary", "weekly update", "org digest", "what's going on this week" |
| `skills/process-weekly-meeting/SKILL.md` | Processing or reconciling the Open Austin weekly organizing meeting, canonical shared notes, and resulting GitHub work |

Each `SKILL.md`'s frontmatter `description` is the source of truth for exact trigger phrasing — this table is a quick index.

## Markdown And Prose Style
Do not hard-wrap prose in Markdown, comments, docs, or examples. Let editors handle soft wrapping. Preserve paragraphs as single lines unless line breaks carry meaning, such as lists, tables, code blocks, quoted text, frontmatter, or an existing semantic-line-break style.

Avoid reflow-only diffs. When editing prose, change the smallest relevant span instead of rewrapping neighboring paragraphs.

When touching existing Markdown or prose, apply this preferred style to the paragraph, section, or example being edited so files converge over time. Do not mass-reformat untouched sections just to normalize style unless the user asks for a cleanup pass.

Prefer compact Markdown heading spacing in hand-authored docs: do not add blank lines only to separate adjacent headings from each other. Follow existing file style, and let explicit project tooling win when a formatter or linter requires a different layout.
