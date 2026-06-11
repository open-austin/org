# Backlog Triage

**Status: Complete — archived June 11, 2026**

## Goal

Get the Open Austin issue tracker and project boards into a state that actually reflects the org's current reality — and establish a label/structure system that incoming team chairs can use immediately when they're seated.

The starting state: 27 open issues, 0 updated in the last 30 days, 13 untouched for over a year, 59% with no assignee, and a label system that predated the Refactor 2026 governance restructuring.

## What Was Done

- Created team-jurisdiction labels: `finance`, `fundraising`, `communications`, `engagement`, `education`, `infrastructure`, `product team`, `community`, `priority`. Updated `board` to black (#000000). Kept `fellowship`, `open role`, `open guide`.
- Retired old labels: `operations`, `accounting`, `products`, `practices`
- Relabeled all 25 open issues with team jurisdiction labels
- Labeled all closed open role issues with `product team` / `engagement` for completeness
- Closed #393 (prior board onboarding doc — superseded by wiki migration spike)
- #413 was already closed
- Confirmed 0 open issues unboarded after triage
- Done column cleanup and "To Do" column review deferred to GitHub Automation spike (auto-archive) and human triage with Liani

---

---

## Non-Goals

- This is not about automating governance or board decisions.
- We are not nagging people with automated reminders. The goal is to do real triage — close what's dead, clarify what's live, restructure what's stale — not to generate noise.
- We are not migrating the wiki here. That's a separate spike (`docs/wiki-migration.md`).

---

## Context: The New Org Structure

As of Refactor 2026 (resolved ~June 8, 2026), Open Austin organizes work through:

**Standing Teams** (Board-authorized, each led by a Chair):
- Finance Team
- Fundraising Team
- Communications Team
- Engagement Team (oversees Product Teams)
- Education Team
- Infrastructure Team

**Product Teams** — autonomous teams with project champions, spun up/down by the Engagement Team. Most open roles are for product teams, not standing teams.

**Communities of Practice** — recurring community spaces (Dev CoP, Design CoP, Data CoP), continuing as-is.

Most standing teams are currently **unseated** — the one-month chair selection process is underway (closes ~July 8, 2026). That makes it especially important to have a clean tracker ready when chairs arrive.

---

## Problems to Solve

### 1. Label system doesn't map to new structure

Current labels: `operations`, `open role`, `open guide`, `fundraising`, `board`, `practices`

These were created under the old structure. They don't tell a team chair "this is your work." We need team-jurisdiction labels so issues are routable.

Proposed new label set (to discuss/refine):

| Label | Maps to |
|---|---|
| `team: finance` | Finance Team |
| `team: fundraising` | Fundraising Team |
| `team: communications` | Communications Team |
| `team: engagement` | Engagement Team / Product Teams |
| `team: education` | Education Team |
| `team: infrastructure` | Infrastructure Team |
| `team: board` | Board-level (governance, resolutions) |
| `open role` | Keep — but add team label alongside |
| `open guide` | Keep — content/documentation work |
| `operations` | Retire or keep as catch-all for unclassified |

Existing type/nature labels (`open role`, `open guide`, `fundraising`) can coexist with team labels — they're orthogonal. An issue can be `open role` + `team: communications`.

### 2. Dead issues clogging the tracker

13 issues haven't been touched in over a year. Some are probably done-but-unclosed, some are abandoned, some are genuinely still valid but nobody's looked at them. Each needs a human call:
- Close as complete
- Close as won't do / no longer relevant
- Keep open, update with current status
- Reassign to a team

No bulk-closing without a reviewed plan. An agent can draft the disposition for each; user approves before any writes.

### 3. Org Kanban board is mostly a graveyard

21 of 30 items are "Done." The 7 in "Todo" haven't moved in 400–500 days. The board doesn't give a useful real-time view of what's active.

Options:
- Archive old Done items (keep the issues open/closed as appropriate, just remove from board view)
- Add a "Backlog" column to separate "acknowledged but not active" from "actively next up"
- Ensure the Todo column only contains things that are genuinely next actions

### 4. Open Roles are stale and unowned

8 roles have been sitting "Open" for months to years (Backend Dev: 417 days). Without a mechanism to review them periodically, they accumulate and lose meaning.

Each open role needs:
- A team label (or `product team` label) indicating who owns the hiring decision
- A periodic review — if a role has been open >90 days with no movement, it should be flagged
- When filled: close the issue → automation moves it to "Filled" on the board (see github-tooling spike)

### 5. Issues not on any board

Several open issues exist only in the issue list with no board placement, no label, and no assignee. They're invisible to any workflow. Triage should surface these and decide: add to a board, label and assign, or close.

---

## Approach

1. **Agent-assisted triage draft** — run a sync snapshot, have an agent produce a disposition proposal for every open issue (close / keep / reassign / relabel). No writes until proposal is reviewed.
2. **User reviews and approves** — go through the proposal, adjust calls.
3. **Apply in batches** — labels first (low blast radius), then closes, then board moves.
4. **New label system** — create team labels before applying them to issues.
5. **Board cleanup** — after issue triage is clean, restructure the Org Kanban to reflect active work.

---

## Open Questions

- Do we want a `product team` label for issues owned by specific product teams (OpenMapper, Landlord Mapper, etc.)? Or should those issues live in their own repos rather than the org repo?
- Should "Backlog" be a board column, or should issues not yet being worked just stay unlisted on the board?
- Who is the right person to approve triage calls for issues that are currently unassigned? (Probably you for now, until team chairs are seated.)
