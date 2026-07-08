# Weekly Summary Per-Team Channels
## Goal
Break the single `#oa-org` weekly summary into per-team posts, so each team sees only its own active issues in its own channel, and `#oa-org` becomes a priority-only feed instead of a full org digest.

## Why
The single combined weekly summary buried team-specific signal in one long post to a channel most team members don't read closely. Team chairs want their own team's issues in their own channel; `#oa-org` should be reserved for cross-team priority items that need broader visibility, not routine team-level updates.

## Routing
See `skills/weekly-org-summary/SKILL.md` Routing section for the authoritative table. Summary:

- `board` → `#oa-board`
- `infrastructure` → `#t-infrastructure`
- `finance` → `#t-finance`
- `fundraising` → `#t-fundraising`
- `communications` → `#t-communications`
- `education` → `#t-education`
- `engagement` (excluding issues also labeled `product team` or `open role`) → `#t-engagement`
- `fellowship` → `#pg-data-fellowship`
- `priority` (any team) → `#oa-org`

## Deliberate Exclusions
Two decisions made explicitly with the user (2026-07-07), not oversights:

- `community` and `product team` labels have no dedicated channel and aren't routed anywhere. Their non-priority issues don't appear in any weekly post.
- `#oa-org` dropped its old board-health/overview/aggregate content entirely — it now posts priority-labeled issues only.

## Non-Goals
- Not changing `role-pipeline-report.yaml` or `stale-role-warning.yaml` — open roles stay on their existing monthly/weekly cadence, untouched by this change.
- Not building new rendering or posting tooling. `tools/notify/render_weekly_summary_blocks.py` and `tools/notify/post.sh` were already generic across input files and webhook vars; this only changes what content the skill generates and how many times it calls them.
- Not automating this on a cron — still manually triggered, per the existing skill's Frequency section.

## Open Questions
- Should any of the new team channels eventually get their own automation (e.g. a scheduled version), or does this stay agent-triggered indefinitely? No decision needed yet — revisit if a team chair asks.
- If an issue carries two mapped team labels (e.g. `infrastructure` + `finance`), it posts to both channels. Nobody has flagged this as a problem; revisit if it becomes noisy.
