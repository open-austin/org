# 0004 — Projects v2 Board Changes Can't Trigger Repo-Level Actions
**Date:** 2026-07-08
**Status:** Accepted

## Context
Four workflows (`filled-to-close.yaml`, `done-to-close.yaml`, `open-roles-reopen.yaml`, `kanban-status-reopen.yaml`) were built to react to Projects v2 Status field changes using `on: projects_v2_item: types: [edited]`. All four parsed as valid YAML and showed as `active` in `gh workflow list`, but none of them ever actually ran. Confirmed empirically: across this repo's entire Actions run history (`gh api repos/open-austin/org/actions/runs --paginate`), the only event types that have ever triggered a run are `issues`, `push`, and `schedule` — `projects_v2_item` has never fired once.

`projects_v2_item` is a real webhook event, but it's **organization-level**, not repository-level. A repo's `.github/workflows/*.yaml` `on:` block can only subscribe to repo-scoped events (plus `schedule` and `workflow_dispatch`). There's no way to make a normal repo workflow react directly to a Projects v2 field change without an org-level webhook plus something to bridge it into `repository_dispatch` — real hosted infrastructure, which this repo deliberately avoids (see write-safety/no-hosting preference in `AGENTS.md`).

The reverse direction — issue state change (closed/reopened) driving a Projects v2 status field via `on: issues: [closed, reopened]` — works fine, because `issues` is a genuine repo-level event. That's why `closed-to-filled.yaml` and `open-role-reopened.yaml` (issue → board) always worked, while their board → issue counterparts silently never did.

Separately: GitHub Projects v2 ships built-in, no-code workflows (visible via GraphQL: `node(id: $project) { ... on ProjectV2 { workflows(first: 20) { nodes { name enabled } } } }`, or in the Project's own `···` → Workflows UI panel). One of the five built-in types is **"Auto-close issue"** — a native way to close the linked issue when a status field is set to a specific value, with zero custom Actions code. There is no built-in counterpart for the reverse ("reopen issue when moved away from a status"), so that direction still needs custom automation.

## Decision
- Use the native Projects v2 **"Auto-close issue"** built-in workflow (configured per-project, per-status, via the UI) for any "status X → close issue" automation instead of a custom Action. This replaced `filled-to-close.yaml` (Open Roles: Filled) and made `done-to-close.yaml` (Org Kanban: Done) redundant — both were deleted as dead code.
- For "status X → reopen issue" (no native equivalent exists), use a **scheduled reconciliation** workflow instead of an event trigger: poll all project items on a `schedule` cron, and enforce the invariant directly (if status is in the target set and the linked issue is closed, reopen it) rather than trying to detect the specific change that caused it. This is what `open-roles-reopen.yaml` and `kanban-status-reopen.yaml` were rewritten to do (15-minute interval, `workflow_dispatch` with `dry_run` input for manual testing, same pattern as `archive-old-done.yaml`/`archive-old-filled.yaml`).

## Consequences
- Any future automation reacting to a Projects v2 field change must be either a native built-in Projects v2 workflow (if the need fits one of the five available types) or a scheduled polling job — never `on: projects_v2_item`, which cannot work for a repo-level workflow.
- Reopening via board movement now has up to a 15-minute lag instead of being instant, since it's polling-based. Reopening the issue directly (rather than moving the board column) still takes effect on the next `issues`-triggered workflow run, which is immediate.
- Before building new project-board-reactive automation, check `workflows(first: 20) { nodes { name enabled } }` on the relevant `ProjectV2` node first — the native option may already cover the need.

## Related
- `docs/active-spikes/github-automation.md`, `docs/active-spikes/github-automation.todo.md`
- `.github/workflows/open-roles-reopen.yaml`, `.github/workflows/kanban-status-reopen.yaml`
- `AGENTS.md` — write-safety rules, no-hosting preference
