---
name: weekly-org-summary
description: "Produce the weekly Open Austin org summary, broken out per team into separate Slack channels, from a fresh snapshot. Use when the user asks for a 'weekly summary', 'weekly update', 'org digest', or 'what's going on this week'."
---

# Weekly Org Summary
**Process, not automation.** As of 2026-09-07 this skill describes how the weekly summary is produced; it no longer wraps a sync tool. Drafting and Slack posting still have tooling here (`tools/notify/`); gathering issue state does not. A contributor can run this whole process by hand.

This is the Open Austin org repo's own weekly summary process. It supersedes the old `docs/runbook-weekly-summary.md` (removed) and is project authority here.

## What This Produces
As of 2026-07-07 this is a **multi-channel** report, not a single post. Each team's active issues go to that team's own Slack channel, and `#oa-org` is now a priority-only feed rather than a full org digest. See Routing below for the exact mapping.

Each channel's draft is written to its own file under `snapshot/` so review and Slack posting use the same text. `snapshot/` is gitignored, so these are temporary working output. Each draft is rendered to Block Kit JSON with the existing generic renderer before posting — no per-channel tooling changes are needed, `render_weekly_summary_blocks.py` and `post.sh` already take an input file / webhook var as arguments.

All drafts are shown in the conversation for review before anything is posted.

## Routing
Group issues by label into these destinations. An issue can appear in more than one channel if it carries more than one mapped label.

| Label | Webhook var | Channel |
|---|---|---|
| `board` | `SLACK_WEBHOOK_BOARD` | `#oa-board` |
| `infrastructure` | `SLACK_WEBHOOK_INFRASTRUCTURE` | `#t-infrastructure` |
| `finance` | `SLACK_WEBHOOK_FINANCE` | `#t-finance` |
| `fundraising` | `SLACK_WEBHOOK_FUNDRAISING` | `#t-fundraising` |
| `communications` | `SLACK_WEBHOOK_COMMUNICATIONS` | `#t-communications` |
| `education` | `SLACK_WEBHOOK_EDUCATION` | `#t-education` |
| `engagement` (excluding issues also labeled `product team` or `open role`) | `SLACK_WEBHOOK_ENGAGEMENT` | `#t-engagement` |
| `fellowship` | `SLACK_WEBHOOK_FELLOWSHIP` | `#pg-data-fellowship` |
| `priority` (any team) | `SLACK_WEBHOOK_ORG` | `#oa-org` |

`community` and `product team` are intentionally not routed anywhere — this was a deliberate call (2026-07-07), not an oversight. Their non-priority issues don't appear in any weekly post. `open role` issues are already covered by `role-pipeline-report.yaml` (monthly) and `stale-role-warning.yaml` (weekly) — never include them here.

`SLACK_WEBHOOK_BOARD`, `_INFRASTRUCTURE`, `_FINANCE`, `_FUNDRAISING`, `_COMMUNICATIONS`, `_EDUCATION`, and `_FELLOWSHIP` are new as of this routing change. Each needs its own Incoming Webhook created in Slack before it can be used — see `.env.example`. If a webhook var isn't set yet, skip posting to that channel but still show its draft in the conversation.

If a channel has zero matching issues that week, skip both drafting and posting for it — don't post an empty "nothing to report" message. Bounded notifications matter on a shared org.

## Steps
### 1. Gather current issue state
**This repo no longer ships a sync tool.** `tools/sync/` was removed on 2026-09-07 — it existed to feed one maintainer's private knowledge system, had no other users, and its absence is deliberate rather than an oversight. See `docs/archive/retire-sync-tooling.md`.

You need, for every open issue: number, title, labels, and assignees. Any of these works:

```bash
# Structured, and the easiest to route from:
gh issue list --limit 200 --state open --json number,title,labels,assignees,updatedAt

# Or read the board and issue list in the GitHub UI.
```

Whatever you use, get it **fresh**. Never summarize from a stale snapshot — a summary that reports closed issues as open is worse than no summary, and it will be noticed.

If you maintain your own tooling that produces a `snapshot/`-shaped set of files, it drops straight into the rest of this process; the steps below only assume you have current issue data in some form.

### 2. Read the supporting context
Load and read:
- `docs/templates/weekly-summary-template.md` — canonical per-channel and `#oa-org` message shapes
- recent folders in `docs/weekly-review-archive/` — trend context only, not source of truth

The current label taxonomy is visible in the GitHub UI under Labels, or via `gh label list`.

### 3. Produce the per-channel drafts
For each row in Routing with at least one matching issue, write `snapshot/weekly-summary-<slug>.md` (e.g. `weekly-summary-infrastructure.md`, `weekly-summary-org.md` for the priority feed), following `docs/templates/weekly-summary-template.md`. Use Slack-friendly `mrkdwn`: short headings, `-` markers with line breaks for list structure, plain text. Avoid tables. Do not use `*` as a bullet marker; in Slack `mrkdwn`, `*text*` means bold.

When naming issues, put the issue title first, then link only the issue number:

```text
Issue title | <https://github.com/open-austin/org/issues/123|#123>
```

Do not use full-title links or standard Markdown links such as `[Issue title](https://...)`; Slack renders incoming webhook text more predictably with angle-bracket links.

For a team channel draft: a flat bulleted list of that team's matching issues, one per line, with assignment status (`(assigned: none)` or `(assigned: name)`). No per-team header nesting needed — the channel itself is the team.

For the `#oa-org` priority draft: a flat bulleted list of all priority-labeled issues across every team, each line prefixed with its originating team label so cross-team context isn't lost: `[infrastructure] Issue title | <URL|#123> (assigned: none)`.

Keep it skimmable. One issue per line, concrete numbers, no semicolon-separated chains. Do not include Open Roles or recruiting tickets. Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.

### 4. Review with user
Show every non-empty draft in the conversation together. Ask:
- "Anything to add or correct before I post these?"
- Only post to Slack after explicit confirmation.

### 5. Post to Slack (if confirmed)
For each approved draft, render it into a Slack Block Kit payload using the same generic renderer for every channel:

```bash
tools/notify/render_weekly_summary_blocks.py snapshot/weekly-summary-<slug>.md --output snapshot/weekly-summary-<slug>.blocks.json
```

Preview each payload without posting:

```bash
tools/notify/post.sh SLACK_WEBHOOK_<VAR> --payload snapshot/weekly-summary-<slug>.blocks.json --dry-run
```

Then post each after approval:

```bash
set -a
source .env
set +a
tools/notify/post.sh SLACK_WEBHOOK_<VAR> --payload snapshot/weekly-summary-<slug>.blocks.json
```

Skip posting to any channel whose webhook var isn't set in `.env` yet — report that in the conversation rather than failing silently.

If Block Kit rendering fails for a given draft, fall back to the plain-text message for that channel only:

```bash
tools/notify/post.sh SLACK_WEBHOOK_<VAR> < snapshot/weekly-summary-<slug>.md
```

If no Slack webhooks are configured yet at all, just deliver every draft in the conversation.

### 6. Archive the final drafts
After the user approves, save each posted channel's exact final text to `docs/weekly-review-archive/YYYY-MM-DD/<slug>.md`:

```bash
mkdir -p docs/weekly-review-archive/YYYY-MM-DD
cp snapshot/weekly-summary-<slug>.md docs/weekly-review-archive/YYYY-MM-DD/<slug>.md
```

This is a change from the old flat `docs/weekly-review-archive/YYYY-MM-DD.md` naming (single file per week) to one dated folder per week containing one file per channel that was posted. Older flat files are historical and don't need renaming.

If a draft was revised after posting, archive the revised text with a suffix such as `<slug>-revised.md`.

## Frequency
This is manually triggered — no cron. Run it when the user asks. Once a week is typical but there's no fixed schedule.

## Related
- `tools/notify/post.sh` — Slack post command, generic across channels/webhook vars
- `tools/notify/render_weekly_summary_blocks.py` — renders any weekly-summary-shaped markdown file to Slack Block Kit JSON, generic across files
- `docs/templates/weekly-summary-template.md` — per-channel and `#oa-org` message templates
- `docs/weekly-review-archive/` — final weekly summary archive
- `.env.example` — webhook var placeholders, including the new per-team ones
- `AGENTS.md` — agent rules and write safety
- `snapshot/` — gitignored working directory for drafts and rendered payloads. Nothing in this repo regenerates it from GitHub any more; it is scratch space that `tools/notify/` reads from.
