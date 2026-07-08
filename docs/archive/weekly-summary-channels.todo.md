# Weekly Summary Per-Team Channels — To Do
## Background
Break out the weekly org summary into per-team Slack channels instead of one combined `#oa-org` post. See `docs/active-spikes/weekly-summary-channels.md` (conceptual doc) for the routing table and rationale.

## Current State Overview
Status: Complete. User confirmed the spike is done and ready to close (2026-07-08) after the first real run posted successfully on 2026-07-07.

## To Do
(none — see Done)

## Ready for Human QA
(none)

## Done
- [x] Design routing table with user: 8 team labels + `priority` → 9 channels
- [x] Clarified `community`/`product team` have no channel (deliberate, not a gap) and confirmed `#oa-org` drops its aggregate content entirely
- [x] Rewrote `skills/weekly-org-summary/SKILL.md` for multi-channel drafting/review/posting/archiving
- [x] Rewrote `docs/templates/weekly-summary-template.md` with per-team and priority-digest shapes
- [x] Added new webhook var placeholders to `.env.example`
- [x] Confirmed no changes needed to `tools/notify/render_weekly_summary_blocks.py` or `tools/notify/post.sh` — both were already generic across files/webhook vars
- [x] User created all 7 new Slack Incoming Webhooks and added URLs to `.env`
- [x] First real run (2026-07-07): synced fresh snapshot, drafted 7 non-empty channels (education and fellowship had zero matching issues, correctly skipped), user reviewed and approved all drafts, rendered + dry-ran + posted all 7, archived to `docs/weekly-review-archive/2026-07-07/`
- [x] User confirmed closure (2026-07-08)

Not explicitly re-confirmed before closing — carried forward here rather than assumed verified:
- Whether #396 and #463 (each carrying two mapped team labels) correctly appeared in both of their respective channels
- Whether including open-role-labeled issues in non-engagement team channels (came up with #461 in `#t-communications`) is the behavior to keep long-term, or whether the exclusion rule should be broadened beyond just `engagement`
