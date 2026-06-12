# Weekly Org Summary Template

Use this template when drafting `snapshot/weekly-summary.md` for the weekly org summary. The body inside the fenced block is the Slack-ready shape.

```text
*Weekly Org Summary - {Month D, YYYY}*

*Active Issues by Team*
- *Finance* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Fundraising* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Communications* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Engagement* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Education* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Infrastructure* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Community* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.
- *Board* ({count}): <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>. Priority: {none or linked priority issue}. Assigned: {names or none}.

*Board Health*
- Org Kanban: {done_count} Done, {in_progress_count} In Progress, {todo_count} To Do.
- In Progress: <https://github.com/open-austin/org/issues/{number}|{Issue title}> ({assignee}, stale {days}d); <https://github.com/open-austin/org/issues/{number}|{Issue title}> ({assignee}, stale {days}d).
- Notable To Do: <https://github.com/open-austin/org/issues/{number}|{Issue title}>; <https://github.com/open-austin/org/issues/{number}|{Issue title}>.

*Priority / Flags*
- <https://github.com/open-austin/org/issues/{number}|{Issue title}>: {why it matters or what decision is needed}.
- {Brief blocker/staleness note, only if it needs human attention.}

*Summary*
{Two concise sentences: one on what seems to be moving, one on what most needs attention this week.}
```

## Style Rules

- Use human-readable issue titles with Slack links; avoid bare issue numbers.
- Omit teams with no active in-scope issues.
- Do not include Open Roles or recruiting tickets unless the user explicitly asks for them.
- Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.
- Keep Slack formatting simple: bold section headers, bullets, no tables.
- Avoid emojis by default. If the user wants them, use at most one section-level emoji per heading.
- Prefer `Summary` over `Narrative`.
- Keep `Priority / Flags` actionable; do not list observations that are merely true.
