# Weekly Org Summary Templates

Use these templates when drafting `snapshot/weekly-summary-<slug>.md` files for the weekly summary breakout. See `skills/weekly-org-summary/SKILL.md` for the full routing table and process. The body inside each fenced block is the Slack-ready shape.

## Per-Team Channel Template

Use this shape for every team channel draft (`weekly-summary-infrastructure.md`, `weekly-summary-engagement.md`, etc.) — a flat list of that team's matching issues, no per-team header nesting since the channel itself is the team.

```text
*{Team Name} — Weekly Update ({Month D, YYYY})*

- {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
- {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
```

## `#oa-org` Priority Digest Template

Use this shape for `weekly-summary-org.md`. This channel is priority-labeled issues only, across every team — it is no longer a full org digest with board health or per-team breakdowns. Each line is prefixed with its originating team label since issues are no longer grouped by team section.

```text
*Priority Issues — Weekly ({Month D, YYYY})*

- [{team label}] {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: none)
- [{team label}] {Issue title} | <https://github.com/open-austin/org/issues/{number}|#{number}> (assigned: {names})
```

## Style Rules

- Use Slack `mrkdwn` links, not standard Markdown links: `Issue title | <https://github.com/open-austin/org/issues/123|#123>`.
- Put the issue title first as plain text, then link only the issue number.
- Skip a channel's draft entirely (no file, no post) if it has zero matching issues that week — don't post an empty "nothing to report" message.
- This markdown is both the human-review draft and the input format for `tools/notify/render_weekly_summary_blocks.py`, which is generic across all of these files — no per-channel tooling changes needed. Use `-` markers consistently so the renderer can create Block Kit `rich_text_list` blocks.
- In the plain-text fallback path, `-` markers plus line breaks mimic lists. Do not use `*` as bullets because `*text*` is Slack bold formatting.
- For true Slack bullet rendering, post the rendered Block Kit payload with `tools/notify/post.sh SLACK_WEBHOOK_<VAR> --payload snapshot/weekly-summary-<slug>.blocks.json`.
- Use one bullet per issue. Do not pack multiple issue links into one semicolon-separated sentence.
- Keep assignment status on each issue because unowned work is useful signal: `(assigned: none)`, `(assigned: name)`, or `(assigned: name; stale 123d)`.
- Omit empty/default priority metadata such as `Priority: none`.
- Do not include Open Roles or recruiting tickets — those are covered by `role-pipeline-report.yaml` and `stale-role-warning.yaml`, not this skill.
- Do not include internal repo TODOs or tooling status unless they directly affect the org-facing work being summarized.
- Keep Slack formatting simple: bold section headers, bullets, no tables.
- Avoid emojis by default. If the user wants them, use at most one per heading.
