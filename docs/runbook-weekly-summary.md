# Runbook: Weekly Org Summary

This runbook describes how to produce the weekly Open Austin org summary. Run it whenever the user asks for a "weekly summary," "weekly update," "org digest," or similar.

---

## What This Produces

A short, human-readable summary of current org state:
- Active issues by team
- Board health (items in each column)
- Anything flagged as `priority`
- A brief summary on what's moving and what's stuck

The draft is written to `snapshot/weekly-summary.md` so review and Slack posting use the same text. `snapshot/` is gitignored, so this file is temporary working output.

Use `docs/templates/weekly-summary-template.md` for the message shape. Final approved summaries are archived in `docs/weekly-review-archive/` so future summaries can reference recent context.

Optionally posted to Slack. Always shown in the conversation first for review.

---

## Steps

### 1. Sync the snapshot

```bash
tools/sync/run.sh
```

This regenerates `snapshot/` from the live GitHub state. Always sync before summarizing — never summarize from a stale snapshot.

### 2. Read the snapshot and context

Load and read:
- `snapshot/issues.md` — open issues by team label
- `snapshot/board-org-kanban.md` — Org Kanban board state
- `snapshot/labels.md` — current label taxonomy (for reference)
- `docs/templates/weekly-summary-template.md` — canonical weekly summary format
- recent files in `docs/weekly-review-archive/`, if any — trend context only

Individual issue detail files (`snapshot/issues/*.md`) are available if a specific issue needs deeper context.

Always summarize from the fresh snapshot. The archive is useful context, not source of truth.

### 3. Produce the summary draft

Write the summary to `snapshot/weekly-summary.md`, following `docs/templates/weekly-summary-template.md`. Use Slack-friendly markdown: short headings, bullets, and plain text. Avoid tables and avoid composing the Slack message inline in a shell command. When naming issues, use human-readable issue titles with Slack links (`<https://github.com/open-austin/org/issues/123|Issue title>`) instead of bare issue numbers.

The summary should cover:

**Teams with active issues:**
List each team that has open issues. For each: number of issues, any with `priority` label, any assigned.

**Board state:**
Org Kanban column counts. Flag anything that's been In Progress for a long time without update.

**Blockers or flags:**
Anything that looks stuck, unduly stale, or needs a human decision. Keep this section brief and signal-dense.

**Summary (2–3 sentences):**
Plain language summary of where the org is at and what's most worth attention this week.

Keep the whole summary skimmable. Bullet points over paragraphs. Concrete numbers.

Do not include Open Roles or recruiting tickets unless the user explicitly asks for them. Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.

### 4. Review with user

Show the contents of `snapshot/weekly-summary.md` in the conversation. Ask:
- "Anything to add or correct before I post this?"
- Only post to Slack after explicit confirmation.

### 5. Post to Slack (if confirmed)

```bash
set -a
source .env
set +a
tools/notify/post.sh SLACK_WEBHOOK_ORG < snapshot/weekly-summary.md
```

For a general all-org channel, use the appropriate webhook variable from `.env`.

If no Slack webhook is configured yet, just deliver the summary in the conversation.

### 6. Archive the final summary

After the user approves the final summary, save the exact final text to `docs/weekly-review-archive/YYYY-MM-DD.md` using the date in the summary title:

```bash
cp snapshot/weekly-summary.md docs/weekly-review-archive/YYYY-MM-DD.md
```

If the summary was revised after posting, archive the revised text with a suffix such as `YYYY-MM-DD-revised.md`.

---

## Channels

| Webhook var | Channel | Used for |
|---|---|---|
| `SLACK_WEBHOOK_ORG` | `#oa-org` | Weekly org summary (agent-produced, manually posted) |

Add more channels to `.env.example` and `.env` as needed.

---

## Frequency

This is manually triggered — no cron. Run it when the user asks. Once a week is typical but there's no fixed schedule.

---

## Related

- `tools/sync/run.sh` — sync command
- `tools/notify/post.sh` — Slack post command
- `docs/templates/weekly-summary-template.md` — weekly summary template
- `docs/weekly-review-archive/` — final weekly summary archive
- `AGENTS.md` — agent rules and write safety
- `snapshot/` — gitignored, always regenerate before use
