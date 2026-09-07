# Retire The Sync Tooling — To Do
## Background
Remove `tools/sync/`, rewrite the weekly-summary skill around the process rather than the tools, and update the docs that reference either. Conceptual doc: `docs/active-spikes/retire-sync-tooling.md`.

## Current State
- Spike opened 2026-09-07, immediately after a final weekly summary run posted to all seven team channels and was archived to `docs/weekly-review-archive/2026-09-07/`.
- That run is the last one this repo's own tooling will produce.

## To Do
- [ ] Remove `tools/sync/` (`issues.py`, `boards.py`, `labels.py`, `issues.sh`, `run.sh`).
- [ ] Rewrite `skills/weekly-org-summary/SKILL.md` — keep routing, style rules, review gate, archive step; replace tool invocations with a described process and an explicit note about the missing sync step.
- [ ] Update `README.md` — drop the Sync Tools section, keep Write Operations.
- [ ] Update `AGENTS.md` — drop sync tool references from the tool table and the snapshot description.
- [ ] Confirm nothing else references `tools/sync`.

## Ready for Human QA
- (none yet)

## Done
- [x] Verify what actually depends on the sync tooling before removing it. — `skills/weekly-org-summary/SKILL.md` step 1 was the only dependency. `tools/notify/`, `tools/issues/`, `tools/google-docs/`, `tools/airtable/`, and all thirteen Actions workflows are independent of it.
- [x] Check whether the CONTRIBUTING PAT setup and Write Safety sections were sync-specific, as originally assumed. — **They are not, and both stay.** `tools/issues/create.sh` and `tools/airtable/` need `gh` auth, and Write Safety governs the issue-creation and Google-Docs write paths. `tools/sync/` was read-only and was never what those rules protected against.
