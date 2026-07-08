# Weekly Summary Per-Team Channels — To Do
## Background
Break out the weekly org summary into per-team Slack channels instead of one combined `#oa-org` post. See `docs/active-spikes/weekly-summary-channels.md` (conceptual doc) for the routing table and rationale.

## Current State Overview
The skill, template, and `.env.example` are updated and ready. This is blocked on Slack-side setup that only the user can do — new Incoming Webhooks don't exist yet for 7 of the 9 destination channels.

## To Do
- [ ] Create Incoming Webhooks in Slack for: `#oa-board`, `#t-infrastructure`, `#t-finance`, `#t-fundraising`, `#t-communications`, `#t-education`, `#pg-data-fellowship`
- [ ] Add the resulting URLs to `.env` as `SLACK_WEBHOOK_BOARD`, `SLACK_WEBHOOK_INFRASTRUCTURE`, `SLACK_WEBHOOK_FINANCE`, `SLACK_WEBHOOK_FUNDRAISING`, `SLACK_WEBHOOK_COMMUNICATIONS`, `SLACK_WEBHOOK_EDUCATION`, `SLACK_WEBHOOK_FELLOWSHIP`
- [ ] Run the skill end-to-end once webhooks exist; dry-run every channel before the first real post
- [ ] Confirm `#oa-org`'s new priority-only shape reads correctly to the people who relied on the old full digest — this is a real behavior change for existing subscribers, not just an addition

## Ready for Human QA
- [ ] First real run: confirm each team's post landed in the right channel with the right issues, and that `#oa-org` shows priority-labeled issues only (not the old board-health/overview content)
- [ ] Confirm an issue with two mapped team labels correctly posts to both channels, if one comes up

## Done
- [x] Design routing table with user: 8 team labels + `priority` → 9 channels
- [x] Clarified `community`/`product team` have no channel (deliberate, not a gap) and confirmed `#oa-org` drops its aggregate content entirely
- [x] Rewrote `skills/weekly-org-summary/SKILL.md` for multi-channel drafting/review/posting/archiving
- [x] Rewrote `docs/templates/weekly-summary-template.md` with per-team and priority-digest shapes
- [x] Added new webhook var placeholders to `.env.example`
- [x] Confirmed no changes needed to `tools/notify/render_weekly_summary_blocks.py` or `tools/notify/post.sh` — both were already generic across files/webhook vars
