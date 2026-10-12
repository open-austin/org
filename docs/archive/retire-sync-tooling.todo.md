---
attention: historical
---
# Retire The Sync Tooling — To Do
## Background
Remove `tools/sync/`, rewrite the weekly-summary skill around the process rather than the tools, and update the docs that reference either. Conceptual doc: `docs/active-spikes/retire-sync-tooling.md`.

## Current State
- Spike opened 2026-09-07, immediately after a final weekly summary run posted to all seven team channels and was archived to `docs/weekly-review-archive/2026-09-07/`.
- That run is the last one this repo's own tooling will produce.

## To Do
- (none)

## Done
- [x] Remove `tools/sync/`. — Done. Also removed the `tools/sync/run.sh` call and `--no-sync` plumbing from `tools/issues/create.sh`, which would otherwise have broken issue creation silently.
- [x] Rewrite `skills/weekly-org-summary/SKILL.md`. — Rewritten to describe the process with an explicit tool-shaped hole, then **retired entirely on 2026-09-07** at Aslan's direction. Kept as the reimplementation record: the routing table, message shapes, review gate, and Slack mrkdwn rules exist nowhere else.
- [x] Update `README.md` and `AGENTS.md`. — Both now describe reading org state through `gh`, and both say the absence of a sync tool is deliberate, because an agent that finds a missing tool tends to rebuild it.
- [x] Confirm nothing else references `tools/sync`. — Checked; `skills/process-weekly-meeting/SKILL.md` also depended on it and got the same treatment.
- [x] Unplanned: removed `tools/issues/create.sh` as well. The capability moved to the maintainer's own tooling as `lifeos github create-issue`. Its value was the dry-run gate, which is now a rule in AGENTS.md rather than a mechanism — a weaker guarantee, and the recorded cost of the removal.
- [x] Unplanned: ran a final weekly summary to all seven channels on 2026-09-07 before removing anything, archived under `docs/weekly-review-archive/2026-09-07/`.
- [x] Verify what actually depends on the sync tooling before removing it. — `skills/weekly-org-summary/SKILL.md` step 1 was the only dependency.
- [x] Check whether the CONTRIBUTING PAT setup and Write Safety sections were sync-specific. — **They are not, and both stay.** `tools/airtable/` needs `gh` auth, and Write Safety governs the Google-Docs write path.

## Ready for Human QA
- (none yet)

## Done
- [x] Verify what actually depends on the sync tooling before removing it. — `skills/weekly-org-summary/SKILL.md` step 1 was the only dependency. `tools/notify/`, `tools/issues/`, `tools/google-docs/`, `tools/airtable/`, and all thirteen Actions workflows are independent of it.
- [x] Check whether the CONTRIBUTING PAT setup and Write Safety sections were sync-specific, as originally assumed. — **They are not, and both stay.** `tools/issues/create.sh` and `tools/airtable/` need `gh` auth, and Write Safety governs the issue-creation and Google-Docs write paths. `tools/sync/` was read-only and was never what those rules protected against.
