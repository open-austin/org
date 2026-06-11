# Runbook: Weekly Org Summary

This runbook describes how to produce the weekly Open Austin org summary. Run it whenever the user asks for a "weekly summary," "weekly update," "org digest," or similar.

---

## What This Produces

A short, human-readable summary of current org state:
- Active issues by team
- Open roles snapshot (how many, any stale)
- Board health (items in each column)
- Anything flagged as `priority`
- A brief narrative on what's moving and what's stuck

Optionally posted to Slack. Always shown in the conversation first for review.

---

## Steps

### 1. Sync the snapshot

```bash
tools/sync/run.sh
```

This regenerates `snapshot/` from the live GitHub state. Always sync before summarizing — never summarize from a stale snapshot.

### 2. Read the snapshot

Load and read:
- `snapshot/issues.md` — open issues by team label
- `snapshot/board-org-kanban.md` — Org Kanban board state
- `snapshot/board-open-roles.md` — Open Roles board state
- `snapshot/labels.md` — current label taxonomy (for reference)

Individual issue detail files (`snapshot/issues/*.md`) are available if a specific issue needs deeper context.

### 3. Produce the summary

Write a summary covering:

**Teams with active issues:**
List each team that has open issues. For each: number of issues, any with `priority` label, any assigned.

**Open Roles:**
Total open roles. Any stale (> 90 days without update). Any in progress. Any recently filled.

**Board state:**
Org Kanban column counts. Flag anything that's been In Progress for a long time without update.

**Blockers or flags:**
Anything that looks stuck, unduly stale, or needs a human decision. Keep this section brief and signal-dense.

**Narrative (2–3 sentences):**
Plain language summary of where the org is at and what's most worth attention this week.

Keep the whole summary skimmable. Bullet points over paragraphs. Concrete numbers.

### 4. Review with user

Show the summary in the conversation. Ask:
- "Anything to add or correct before I post this?"
- Only post to Slack after explicit confirmation.

### 5. Post to Slack (if confirmed)

```bash
source .env
echo "<summary text>" | tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT
```

For a general all-org channel, use the appropriate webhook variable from `.env`.

If no Slack webhook is configured yet, just deliver the summary in the conversation.

---

## Channels

| Webhook var | Channel | Used for |
|---|---|---|
| `SLACK_WEBHOOK_ENGAGEMENT` | `#t-engagement` | Open Roles pipeline report (automated, monthly) |
| `SLACK_WEBHOOK_ORG` | `#oa-org` | Weekly org summary (agent-produced, manually posted) |

Add more channels to `.env.example` and `.env` as needed.

---

## Frequency

This is manually triggered — no cron. Run it when the user asks. Once a week is typical but there's no fixed schedule.

---

## Related

- `tools/sync/run.sh` — sync command
- `tools/notify/post.sh` — Slack post command
- `AGENTS.md` — agent rules and write safety
- `snapshot/` — gitignored, always regenerate before use
