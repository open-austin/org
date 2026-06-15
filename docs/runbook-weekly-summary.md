# Runbook: Weekly Org Summary

This runbook describes how to produce the weekly Open Austin org summary. Run it whenever the user asks for a "weekly summary," "weekly update," "org digest," or similar.

---

## What This Produces

A short, human-readable summary of current org state:
- Active issues by team
- Board health (items in each column)
- Actionable flags, including priority-labeled items only when they need attention
- A brief summary on what's moving and what's stuck

The draft is written to `snapshot/weekly-summary.md` so review and Slack posting use the same text. `snapshot/` is gitignored, so this file is temporary working output.

For Slack posting, render that draft to `snapshot/weekly-summary.blocks.json` with Block Kit `rich_text_list` blocks so Slack shows real bullets instead of plain hyphen text.

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

Write the summary to `snapshot/weekly-summary.md`, following `docs/templates/weekly-summary-template.md`. This markdown file is the human-review draft, the input to the Block Kit renderer, and the plain-text fallback. Use Slack-friendly `mrkdwn`: short headings, `-` markers with line breaks for list structure, and plain text. Avoid tables and avoid composing the Slack message inline in a shell command. Do not use `*` as a bullet marker in this text fallback; in Slack `mrkdwn`, `*text*` means bold.

For true Slack bullet rendering, render and post a Block Kit payload with `rich_text` / `rich_text_list` blocks. Incoming webhooks support `blocks`, and `tools/notify/post.sh` can send a rendered payload with `--payload`.

When naming issues, put the issue title first, then link only the issue number:

```text
Issue title | <https://github.com/open-austin/org/issues/123|#123>
```

Do not use full-title links or standard Markdown links such as `[Issue title](https://...)`; Slack renders incoming webhook text more predictably with angle-bracket links.

The summary should cover:

**Teams with active issues:**
List each team that has open issues. Use one parent bullet per team and one indented child bullet per issue. Include assignment status on every issue because unowned work is useful signal: `(assigned: none)` or `(assigned: lianilychee)`.

**Board state:**
Org Kanban column counts. Put counts and issue lists on separate nested bullets so the Slack post does not become a dense paragraph. Flag anything that's been In Progress for a long time without update.

**Blockers or flags:**
Anything that looks stuck, unduly stale, or needs a human decision. Use a `Needs Attention` section. Do not include routine `Priority: none` lines; only mention priority-labeled issues if they are actionable.

**Summary (2–3 sentences):**
Plain language summary of where the org is at and what's most worth attention this week.

Keep the whole summary skimmable. Use bullet points over paragraphs, one issue per line, and concrete numbers. Avoid semicolon-separated chains of issues.

Do not include Open Roles or recruiting tickets unless the user explicitly asks for them. Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.

### 4. Review with user

Show the contents of `snapshot/weekly-summary.md` in the conversation. Ask:
- "Anything to add or correct before I post this?"
- Only post to Slack after explicit confirmation.

### 5. Post to Slack (if confirmed)

Render the reviewed markdown draft into a Slack Block Kit payload:

```bash
tools/notify/render_weekly_summary_blocks.py snapshot/weekly-summary.md --output snapshot/weekly-summary.blocks.json
```

Preview the payload without posting:

```bash
tools/notify/post.sh SLACK_WEBHOOK_ORG --payload snapshot/weekly-summary.blocks.json --dry-run
```

Then post the payload after approval:

```bash
set -a
source .env
set +a
tools/notify/post.sh SLACK_WEBHOOK_ORG --payload snapshot/weekly-summary.blocks.json
```

For a general all-org channel, use the appropriate webhook variable from `.env`.

If Block Kit rendering fails, fall back to the plain-text message:

```bash
tools/notify/post.sh SLACK_WEBHOOK_ORG < snapshot/weekly-summary.md
```

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
- `tools/notify/render_weekly_summary_blocks.py` — renders weekly summary markdown to Slack Block Kit JSON
- `docs/templates/weekly-summary-template.md` — weekly summary template
- `docs/weekly-review-archive/` — final weekly summary archive
- `AGENTS.md` — agent rules and write safety
- `snapshot/` — gitignored, always regenerate before use
