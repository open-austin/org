# GitHub Tooling — To Do

## Background

This spike builds the CLI sync and write tools that let agents work with the Open Austin GitHub org effectively. The sync tools are the foundation — they pull issues, boards, and labels into local `snapshot/*.md` files so agents have full context without constant API queries.

Related: `docs/github-tooling.md` (conceptual doc)

---

## Project Organization

- Sync tools live in `tools/sync/`
- Write tools (guarded, with `--dry-run`) live in `tools/write/`
- Snapshots are generated into `snapshot/` (gitignored)
- All tools use `GH_TOKEN` from `.env` for auth

---

## General Principles

- Sync tools batch API calls efficiently (5 calls total, not 30+)
- Snapshots are bounded markdown — signal-dense, not raw JSON dumps
- Write tools enforce dry-run discipline: show before/after plan, require explicit approval
- Re-fetch state before any mutation — never act on stale snapshot
- No hard deletes; prefer close/archive/relabel

---

## Current State Overview

- Auth is working: `gh` CLI authenticated with fine-grained PAT, `repo` + `project` scopes
- Discovered: Org Kanban (project #9), Open Roles (project #6), 9 total org projects
- Status field ID on Org Kanban: `PVTSSF_lADOAA7NZM4AqQF8zghh1hc`
- Current issue count: 27 open, 13 stale >365 days, 16 unassigned

---

## To Do

### Phase 1: Sync Tools (foundation)

- [x] Create `tools/sync/` directory structure
- [x] `tools/sync/issues.py` — fetch all open issues, group by label, render with: number, title, assignees, last-updated age, truncated body (200 chars)
- [x] `tools/sync/boards.py` — fetch Org Kanban + Open Roles state, render items grouped by Status
- [x] `tools/sync/labels.py` — fetch label taxonomy, render with name + description + color
- [x] `tools/sync/run.sh` — wrapper that runs all sync scripts, timestamps output
- [x] Add `snapshot/` to `.gitignore`
- [x] Test: run sync, verify snapshot files are readable and well-formatted
- [x] Validate snapshot size is reasonable (<100KB total) — **Result: ~16KB total**
- [x] Decision: Python CLI over shell scripts — better JSON handling, clearer logic, easier to extend

### Phase 2: Write Tools (guarded)

- [ ] Create `tools/write/` directory structure
- [ ] `tools/write/label.sh` — add/remove labels on issues
  - Takes: issue number, label name, action (add/remove)
  - Dry-run mode: show current labels → proposed labels
  - Write mode: re-fetch issue, confirm state, apply change
- [ ] `tools/write/close.sh` — close an issue with optional comment
  - Dry-run: show issue title, current state, who it's assigned to
  - Write mode: re-fetch, confirm open, close + comment if provided
- [ ] `tools/write/move.sh` — move board item between Status columns (Projects v2)
  - Requires GraphQL mutation with Status field ID + option IDs
  - Dry-run: show current status → proposed status
  - Write mode: re-fetch item, apply GraphQL mutation
- [ ] Test all write tools in dry-run mode on real issues
- [ ] Document write tool usage in README

### Phase 3: Integration

- [ ] Update `README.md` with tool usage examples
- [ ] Update `CONTRIBUTING.md` with sync workflow for contributors
- [ ] Agent test: run sync, analyze snapshot, draft triage proposal
- [ ] Human QA: verify snapshots load cleanly, write tools show useful dry-run output

---

## Ready for Human QA

*(Items completed by agent but needing human verification)*

---

## Done

*(Completed work)*

- [x] Auth setup: `gh` CLI with fine-grained PAT
- [x] Discovered Projects v2 board structure and field IDs
- [x] Analyzed current issue state (27 open, staleness breakdown)
- [x] Confirmed snapshot approach is valuable (context loading, consistent view, API efficiency)

---

## Open Questions

- Should sync produce one unified `snapshot/all.md` or separate files per surface? **Decision: Separate files** — easier to navigate, agent can load specific context
- How should snapshots handle issue bodies? **Decision: First 200 chars** — enough for triage context without bloat
- Do we need a `tools/write/comment.sh` or is `gh issue comment` sufficient? Probably sufficient for now — write tools focus on guarded operations (label, move, close)
