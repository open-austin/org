# Board ↔ Issue Sync Redesign
Continues from: docs/archive/github-automation.md

Archived 2026-07-08 — complete and QA-confirmed live. Durable outcomes live in `README.md` (Board Automation) and decision records `0004`/`0005`.

## Goal
Re-architect the board↔issue sync layer so it is (in priority order): auditable and version-controlled in this repo, immediate wherever the platform allows, and minimal in surface area — one system doing the work, not custom Actions and native Projects workflows fighting each other.

## Why
The original design leaned on `on: projects_v2_item` triggers that never fired (see `docs/decisions/0004-projects-v2-automation-triggers.md`), and it ran alongside GitHub's native Projects workflows, producing the visible sprawl the user flagged during testing:
- A new issue was added to Org Kanban by native "Auto-add to project", then moved to To Do by a custom Action — two actors for one outcome.
- An open-role issue was added to *both* boards by native auto-add, then removed from Org Kanban by a custom Action — added wrong, then cleaned up, instead of routed right the first time.

## The Hard Platform Constraint
This shapes the whole design, so it's stated once here:
- **Issue → board** (open/close/reopen/label an issue) are real repository events. Code Actions catch them immediately. No native needed, no timer.
- **Board → issue** (drag a card) is **not deliverable to a repo-level Action at all** — `projects_v2_item` is an org-level event, and reaching it needs a hosted webhook receiver we deliberately don't run. So board→issue has only two possible implementations: a **native** Projects workflow (instant, but configured in the UI, not code) or a **scheduled poll** (code, but timer-based).
- Native ships **`Auto-close issue`** (status → close issue) but has **no** "auto-reopen." So card→reopen has no native and no instant-code path — it is physically forced onto a timer. Card→close is the only board→issue behavior with a choice.

## Decision
- **Card → close** (Done/Filled → close issue): use the **native `Auto-close issue`** workflow. Instant. This is the single deliberate exception to "everything in code," accepted because closing-by-drag is common and instant beats a poll lag here.
- **Card → reopen** (non-terminal column while issue closed → reopen): the **one** scheduled reconciliation poller, in code, every 5 minutes. This is the only piece forced onto a timer, and it does the minimum a timer is required to do.
- **Everything else** (all issue→board sync, routing, initial status): immediate code Actions.
- **All other native Projects workflows are turned OFF**, so code is the only actor for everything except the one `Auto-close` exception. This is what removes the sprawl.

## Target Architecture
| Behavior | Direction | Implementation | Timing |
|---|---|---|---|
| New non-open-role issue → Org Kanban + To Do | issue→board | code (`add-issue-to-kanban`) | immediate |
| New/late open-role issue → Open Roles + Open, remove from Kanban | issue→board | code (`open-role-add`) | immediate |
| Team labels from open-role form | issue→board | code (`label-open-role-from-form`) | immediate |
| Issue closed → Done / Filled | issue→board | code (`close-to-done`, `closed-to-filled`) | immediate |
| Issue reopened → To Do / Open | issue→board | code (`reopened-to-todo`, `open-role-reopened`) | immediate |
| Card → Done/Filled → **close** issue | board→issue | **native `Auto-close issue`** (the exception) | instant |
| Card → non-terminal while closed → **reopen** issue | board→issue | code, one merged reconciliation poller | ~5 min |
| Archive old Done/Filled | maintenance | code (`archive-old-done`, `archive-old-filled`) | weekly |
| Stale-role warning, pipeline report | reporting | code | weekly / monthly |

## The Native Exception (document prominently)
Exactly one piece of board logic lives outside the repo: the native **`Auto-close issue`** workflow on each board (Org Kanban → close on `Done`; Open Roles → close on `Filled`). It is configured in each Project's Workflows UI, is not version-controlled, and has no history if changed. It must be recorded in the README and a decision record so a future maintainer isn't surprised that "close on drag" has no corresponding workflow file. Every other native Projects workflow is intentionally **disabled**.

## Legacy & Race Safety for the Reopen Poller
State-based reconciliation can't tell "deliberately dragged out of Done" from "closed long ago and never synced." Two safeguards:
1. **One-time baseline cleanup before enabling the poller:** move every currently-closed issue to its terminal column (Done/Filled). After this, the only way an item becomes "closed + non-terminal" is a deliberate drag — a real reopen signal.
2. **Fresh-close guard in the poller:** skip items whose issue was closed very recently (e.g. `closedAt` within ~10 min), so a just-closed issue that `close-to-done`/`closed-to-filled` is still moving to Done/Filled isn't spuriously reopened by a poll firing in that few-second window.

## Non-Goals
- Not changing the reporting/Slack layer (`stale-role-warning`, `role-pipeline-report`) beyond the fixes already applied.
- Not moving archive jobs to native "Auto-archive items" — kept in code for the custom age thresholds and auditability (revisit later if desired).
- Not adding any hosted infrastructure or org-level webhooks.
- Not building card→reopen as anything other than a poll — the platform leaves no other option.

## Open Questions
- Timing: does an open-role issue created via the form have its `open role` label present in the `issues: opened` payload, so `add-issue-to-kanban`'s guard correctly skips it and it never briefly hits the Kanban? Needs a live test before we trust routing without native auto-add.
- Does `open-role-add` currently set the Open Roles status to "Open" explicitly, or did it rely on native "Item added to project"? If the latter, it must set status in code once native is off.
- Poll reliability: GitHub scheduled workflows can run late under load, so "5 min" is a floor, not a guarantee. Acceptable for reopen; documented.
