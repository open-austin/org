# Weekly Org Summary Template

Use this template when drafting `snapshot/weekly-summary.md` for the weekly org summary. The body inside the fenced block is the Slack-ready shape.

```text
*Weekly Org Summary - {Month D, YYYY}*

*Active Issues by Team*
- *Finance* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names})
- *Fundraising* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names})
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
- *Communications* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
- *Engagement* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names})
- *Education* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
- *Infrastructure* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names})
- *Community* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
- *Board* ({count}):
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names})

*Board Health*
- Org Kanban:
  - {done_count} Done
  - {in_progress_count} In Progress
  - {todo_count} To Do
- In Progress:
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names}; stale {days}d)
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title} (assigned: {names}; stale {days}d)
- Notable To Do:
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}
  - <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}

*Needs Attention*
- <https://github.com/open-austin/org/issues/{number}|#{number}> {Issue title}: {why it matters or what decision is needed}.
- {Brief blocker/staleness note, only if it needs human attention.}

*Summary*
{Two concise sentences: one on what seems to be moving, one on what most needs attention this week.}
```

## Style Rules

- Use Slack `mrkdwn` links, not standard Markdown links: `<https://github.com/open-austin/org/issues/123|#123> Issue title`.
- Link only the issue number. Keep the issue title as plain text after the link.
- Omit teams with no active in-scope issues.
- Use nested bullets so each issue gets its own line. Do not pack multiple issue links into one semicolon-separated sentence.
- Keep issue metadata short and inline: `(assigned: name)` or `(assigned: name; stale 123d)`.
- Omit empty/default metadata such as `Priority: none` and `Assigned: none`.
- Do not include Open Roles or recruiting tickets unless the user explicitly asks for them.
- Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.
- Keep Slack formatting simple: bold section headers, bullets, no tables.
- Avoid emojis by default. If the user wants them, use at most one section-level emoji per heading.
- Prefer `Summary` over `Narrative`.
- Prefer `Needs Attention` over `Priority / Flags`. Only mention priority-labeled items when they require a human decision or action; otherwise focus on blockers, stale lanes, and concrete follow-up.
