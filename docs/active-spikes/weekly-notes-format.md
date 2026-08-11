# Weekly Meeting Notes — Per-Meeting Doc Format (spike)
Status: **proposed, not started.** Blocked on agreement to change the notes format. This doc captures the design so the work can be picked up later with full context.

## Problem
The weekly organizing meeting notes live in a single, continuously growing Google Doc. One long document is hard to navigate, hard to skim for a specific week, and awkward for tooling to process, since the entire history is one blob the tools have to scroll and re-parse. The `process-weekly-meeting` skill currently has to locate the latest dated section inside that monolith.

## Proposed design
- **One Google Doc per meeting**, all stored together in a dedicated shared Drive folder.
- **Date-prefixed titles** (e.g., `YYYY-MM-DD Weekly Organizing Notes`) so the folder sorts chronologically.
- **Consistent per-meeting template**, so every week has the same shape.
- **Bidirectional links**: each meeting doc links to the previous and next meeting doc, so moving forward and backward through meeting history is one click, no scrolling a monolith.

## Per-meeting template
A single doc per meeting, with sections such as:
- Header: date, facilitator, attendees.
- Agenda / topics.
- Beat-by-beat notes.
- Decisions.
- Action items: owner, status, linked GitHub issue.
- Carry-over items: unresolved actions/agenda rolled forward from prior weeks.
- Navigation: links to the previous and next meeting docs.

## Automation (extend the `process-weekly-meeting` skill)
After a meeting, the skill would:
1. **Enhance the current week's doc** — reconcile it with the meeting handoff, fill in action items, connect actions to GitHub issues. (This is the skill's existing behavior, retargeted from a monolith to a single per-week doc.)
2. **Create next week's doc** from the template.
3. **Carry over unresolved items** — copy still-open action/agenda items into next week's doc so nothing is dropped between meetings.
4. **Wire the navigation links** — set the prev/next links between this week's and next week's docs.

## Tooling requirements
- **Add a `create-from-template` capability to `tools/google-docs`:**
  - Drive API `files.copy` to clone a template doc into the notes folder.
  - Rename the copy to the dated title.
  - Docs API `batchUpdate` to fill placeholders (carry-over items, prev/next links).
- **Config (not committed):** a template doc ID and the notes-folder ID, supplied via environment variables, consistent with how the meeting-notes doc ID is already handled (`.env`, gitignored). No IDs or links in the repo.
- The existing `tools/sync` GitHub state is still an input for connecting actions to issues.

## Open questions
- Where/how to store the template doc ID and folder ID (env var names, docs).
- How to reliably detect "unresolved" carry-over items (parse an action-status field vs. a checkbox convention).
- Create next week's doc at processing time, or on a schedule.
- Migration: keep the historical single doc as a read-only archive and start the per-week format going forward; no need to split old history.
