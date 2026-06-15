# Weekly Org Summary Template

Use this template when drafting `snapshot/weekly-summary.md` for the weekly org summary. The body inside the fenced block is the Slack-ready shape.

```text
*Weekly Org Summary - {Month D, YYYY}*

*Active Issues by Team*
- *Finance* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
- *Fundraising* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- *Communications* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- *Engagement* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
- *Education* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- *Infrastructure* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
- *Community* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- *Board* ({count}):
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})

*Board Health*
- Org Kanban:
  - {done_count} Done
  - {in_progress_count} In Progress
  - {todo_count} To Do
- In Progress:
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names}; stale {days}d)
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names}; stale {days}d)
- Notable To Do:
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names or none})
  - {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names or none})

*Needs Attention*
- {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}>: {why it matters or what decision is needed}.
- {Brief blocker/staleness note, only if it needs human attention.}

*Summary*
{Two concise sentences: one on what seems to be moving, one on what most needs attention this week.}
```

## Style Rules

- Use Slack `mrkdwn` links, not standard Markdown links: `Issue title | <https://github.com/open-austin/org/issues/123|#123>`.
- Put the issue title first as plain text, then link only the issue number.
- Omit teams with no active in-scope issues.
- This markdown is both the human-review draft and the input format for `tools/notify/render_weekly_summary_blocks.py`. Use `-` markers and two-space indentation consistently so the renderer can create Block Kit `rich_text_list` blocks.
- In the plain-text fallback path, `-` markers plus line breaks mimic lists. Do not use `*` as bullets because `*text*` is Slack bold formatting.
- For true Slack bullet rendering, post the rendered Block Kit payload with `tools/notify/post.sh SLACK_WEBHOOK_ORG --payload snapshot/weekly-summary.blocks.json`.
- Use nested bullets so each issue gets its own line. Do not pack multiple issue links into one semicolon-separated sentence.
- Keep assignment status on each issue because unowned work is useful signal: `(assigned: none)`, `(assigned: name)`, or `(assigned: name; stale 123d)`.
- Omit empty/default priority metadata such as `Priority: none`.
- Do not include Open Roles or recruiting tickets unless the user explicitly asks for them.
- Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.
- Keep Slack formatting simple: bold section headers, bullets, no tables.
- Avoid emojis by default. If the user wants them, use at most one section-level emoji per heading.
- Prefer `Summary` over `Narrative`.
- Prefer `Needs Attention` over `Priority / Flags`. Only mention priority-labeled items when they require a human decision or action; otherwise focus on blockers, stale lanes, and concrete follow-up.
