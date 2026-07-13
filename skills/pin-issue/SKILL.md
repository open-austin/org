---
name: pin-issue
description: "Preserve an unresolved Open Austin org/tooling/process issue in docs/pinned-issues.md without turning it into a GitHub issue backlog item, active spike, or durable decision. Use when the user says to put a pin in something, circle back later, defer a thorny org/process/tooling question, revisit pinned issues, or route a pin into active work, future ideas, misc intake, or a decision record."
---

# Pin Issue
This is the Open Austin org repo's own pinning process. It is project authority here, not fallback seed material.

## Purpose
Use this skill to preserve unresolved org/tooling/process issues without interrupting current work. A pinned issue is something the repo is intentionally not resolving yet, but should not lose to chat history, scratch notes, or an overgrown backlog.

The register is `docs/pinned-issues.md`. Create it only when the user asks to pin, defer, circle back later, revisit, or maintain pinned issues.

## Taxonomy
Use the first matching destination:

- `docs/decisions/` for settled durable repo rules.
- `docs/pinned-issues.md` for unresolved issues intentionally preserved for later.
- `docs/scratch/future-ideas.md` for conceptual someday material.
- `docs/scratch/misc.md` for raw observed friction, QA nits, bugs, and issue intake.
- `docs/active-spikes/` for active scoped work.

Do not treat `docs/pinned-issues.md` as a pre-decision queue. Some pins become decision records; many become active work, misc notes, future ideas, or nothing.

## What Belongs Here
Pin an issue when the right handling depends on future context, such as:

- real org usage or contributor/stakeholder feedback
- GitHub platform behavior that needs observation before choosing a rule
- another spike, automation pass, board process change, or documentation phase landing first
- a write-safety, notification, permission, or governance tradeoff that would distract from current work if solved now
- a concern that is real enough to preserve but not ready to classify as a task, idea, or rule

Do not use pinned issues for ordinary GitHub issues, automation bugs, implementation details, or conceptual future ideas that already have a better home.

## Workflow
1. Read the current user request, active spike docs, `TODO.md`, and `docs/pinned-issues.md` when they exist.
2. Confirm the item is unresolved and intentionally preserved, not a task, conceptual future idea, raw misc observation, or settled rule.
3. Add a short entry under `## Current Pins`.
4. State the pinned issue, current context, and concrete revisit trigger.
5. Prefer a condition-based revisit trigger over a vague date.
6. Link to related active spikes, archived spikes, decision records, issues, or files only when the link will help future review.
7. Avoid duplicating the same work across `docs/pinned-issues.md`, `docs/scratch/`, `TODO.md`, and spike todo docs. One place should own active work.

## Revisiting Workflow
Route each reviewed pin into one outcome:

- **Keep pinned:** update the current context or revisit condition if the issue is still premature.
- **Promote to active work:** move concrete tasks into the relevant spike `.todo.md` or `TODO.md`, then remove the pin.
- **Move to future ideas:** move conceptual someday material to `docs/scratch/future-ideas.md`, then remove the pin.
- **Move to misc:** move raw issue intake or QA observations to `docs/scratch/misc.md`, then remove the pin.
- **Record durable decision:** create or update a decision record under `docs/decisions/`, then remove the pin.
- **Discard:** remove the pin if the issue is no longer relevant.

Do not include tokens, private credentials, Slack webhook URLs, private contributor data, or other public-unsafe details in pinned issues. Use placeholders or generic phrasing when a pin depends on private context.
