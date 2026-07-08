---
name: run-project-spike
description: "Run and bucket project work in focused spike docs with a conceptual doc, a to-do doc, TODO.md as an index, scratch promotion, human QA tracking, durable handoff notes, active-spikes placement, archival, and continuation links between related phases of work. Use when starting, continuing, promoting, superseding, archiving, or reviewing project work that should leave navigable history."
---

# Run Project Spike
This is the Open Austin org repo's own spike process. It supersedes the old `docs/how-to-spike.md` (removed) and is project authority here, not fallback seed material.

## Purpose
A spike is not just a checklist. It is a temporary collaboration space for the user and agents to build taste, vocabulary, decisions, and implementation history around a specific theme of work.

Spikes are useful here because this repo manages shared org infrastructure and automation tooling. Changes often need to answer more than "does it work?": they need to be safe for shared org state, respect write authorization boundaries, avoid leaking secrets, produce bounded and auditable output, and avoid firing unwanted notifications to real contributors.

Default toward bucketing project work into a spike so work is easy to find, continue, archive, and relate to later phases. Even small or mixed work can live in a miscellaneous spike bucket such as `misc-302` if it is real project work that should leave history.

Only skip spike bucketing for truly throwaway actions that the user clearly does not want recorded, such as answering a quick question or running a one-off read-only command.

## Where Active Work Lives
This repo uses `docs/active-spikes/`. Create and update active spike pairs there:

```text
docs/
  active-spikes/
    topic.md
    topic.todo.md
  scratch/
    misc.md
  archive/
  decisions/
  README.md
```

Active conceptual and to-do docs go in `docs/active-spikes/`, rough pre-spike material goes in `docs/scratch/`, and finished or superseded spike history goes in `docs/archive/`. Durable long-term docs (`README.md`, `AGENTS.md`, `contributor-policy.md`, decision records) stay out of active spike work.

## Authority Ladder
When docs conflict, use this order (mirrors `AGENTS.md`):

1. `AGENTS.md` (or `CLAUDE.md`) and `README.md` — durable project rules
2. `contributor-policy.md` — Open Austin governance doc; do not edit it through tooling or agent work
3. Active decision records in `docs/decisions/` — settled tradeoffs
4. Active spike docs in `docs/active-spikes/` — current thinking for a theme of work
5. Active spike to-do docs in `docs/active-spikes/` — implementation state
6. `TODO.md` — active work coordination
7. `docs/scratch/` — exploratory, non-authoritative
8. `docs/archive/` — historical context only

Repo-local skills in `skills/` (this file included) are project authority over any similarly named global skill.

## TODO.md Role
Use `TODO.md` as an index and coordination map, not as the place for fiddly implementation detail.

It should point to active spike docs, note waiting-for-human-QA items, list recently completed or archived spikes, and hold lightweight later ideas. Detailed work items, command logs, and state transitions belong in the spike's `.todo.md`.

## The Two Documents
Active spikes use two docs:

- A conceptual doc, such as `docs/active-spikes/<topic>.md`.
- A to-do doc, such as `docs/active-spikes/<topic>.todo.md`.

The conceptual doc explains the work's purpose, philosophy, boundaries, and settled model. It should help a new agent understand what kind of solution would be in character for the project.

The to-do doc tracks concrete atomic tasks for implementation work. It should be operational: files, actions, QA notes, unresolved questions, and what has already happened.

Do not collapse these into one doc when the work needs both mental model and execution tracking. The separation is functional: the conceptual doc preserves taste and constraints; the to-do doc preserves movement and state.

## Conceptual Docs
Use the conceptual doc for:

- goals and non-goals
- project vocabulary
- engineering, design, shell, setup, or product philosophy
- major decisions and why they were made
- relationship to other spikes
- constraints that should shape future work
- safety and privacy boundaries
- continuation links to predecessor or successor spikes

Avoid turning the conceptual doc into a running changelog. When implementation details become durable rules, fold them into longer-lived docs such as `README.md`, `AGENTS.md`, a decision record, a local skill in `skills/`, or another active reference doc.

## To-Do Docs
Use the to-do doc for:

- concrete atomic work items
- current state notes
- implementation progress
- commands and verification steps
- human QA requests
- known edge cases
- short historical notes that will help future agents reconstruct what happened

The to-do doc usually follows this rough shape:

- Background
- Project Organization
- General Principles
- Current State Overview
- To Do
- Ready for Human QA
- Done

Exact headings can flex, but future agents should be able to find current work, QA work, and completed work quickly.

For this repo, consider adding sections for:

- secrets and credential hygiene (never commit tokens; `.env.example` only)
- write-safety: dry-run behavior, plan-before-bulk-edit, no destructive deletes
- API surface: REST vs. GraphQL, `gh` CLI vs. MCP, rate limits
- auth and permissions: PAT scopes, SAML SSO requirements, volunteer write access boundaries
- shared org state: blast radius, notification behavior, who gets pinged
- validation commands and how to confirm a tool worked correctly
- rollback or recovery notes

## Moving Work
Work starts in `To Do`.

When an agent finishes implementation but the user needs to visually or manually verify it, move the item to `Ready for Human QA`.

When the user confirms QA, move it to `Done`.

When implementation does not need human QA, move it directly to `Done` after verification.

`Done` is allowed to preserve useful history. It should not be a perfectly compressed final summary. These docs are archived at the end of the spike, and that archive can help future agents understand why the code ended up this way, even if the notes along the way are messy or not totally current. Prefer a useful decision and implementation trail over a neat but context-poor summary. Do not sand off the rough corners of historical artifacts.

## Human QA
Use `Ready for Human QA` for things the agent cannot fully verify from the terminal:

- copy tone in comments or generated content that will be visible to org members
- board or issue state in the GitHub UI after a write operation
- whether a dry-run output looks correct before approving a real write
- auth and permission behavior on the real org (cannot be safely exercised without live credentials)
- anything that fires notifications to real contributors — verify before approving

Be specific. A good QA item names the surface, command, expected output, or GitHub UI state the user should inspect.

## Scratch Promotion
Use `docs/scratch/` for rough notes, copied references, draft outlines, and exploratory material that is not yet a spike or durable rule.

Scratch docs are not authoritative. Promote useful material into an active spike, durable doc, or local skill before relying on it.

Promotion means move, not copy. When promoting a scratch doc into `docs/active-spikes/`, move its useful content into the active conceptual and to-do docs, then delete or clearly retire the old scratch source. Do not leave an outdated duplicate in `docs/scratch/`.

If a scratch doc contains multiple themes, split it deliberately: move each useful piece into the right destination, then remove the routed source material. Preserve nuance and concrete user phrasing while moving it.

For loose unrouted notes, use `docs/scratch/misc.md` and the `triage-project-misc` skill.

## Durable Decisions
Decision records are part of the project's durable docs structure, not the spike process itself. During a spike, create or update a decision record only when a tradeoff has become a durable project rule that should outlive the spike.

Do not create decision records for every local implementation choice. Keep ordinary reasoning in the conceptual spike doc unless it needs to become long-lived project authority.

## Starting A Spike
1. Inspect `AGENTS.md`, `README.md`, `TODO.md`, `docs/active-spikes/`, `docs/scratch/`, `docs/archive/`, durable docs, and repo-local skills.
2. Decide whether the work belongs in an existing active spike, a new named spike, or a miscellaneous spike bucket.
3. Choose a short topic slug. For mixed work, use the repo's numbered misc convention.
4. Create or update `docs/active-spikes/<topic>.md` for conceptual context.
5. Create or update `docs/active-spikes/<topic>.todo.md` for implementation state.
6. Add or update the spike entry in `TODO.md` as an index pointer.
7. Capture known constraints, non-goals, validation expectations, and open questions before implementation if they matter.

## During A Spike
Keep conceptual understanding in the conceptual doc and operational state in the to-do doc. Update item statuses as work moves. Preserve enough history to explain decisions, but move durable rules out of the spike when they become repo policy.

Do not let scratch notes silently become authority. Promote them deliberately.

## Continuation Links
When work moves into a new phase instead of continuing in the same spike, link related predecessor and successor spikes so the work graph can be followed later.

Continuation is many-to-many. A spike can split into several successors, and a later spike can merge several predecessor threads.

Use one grep-friendly marker line per relationship, with stable literal repo paths rather than fragile relative links:

```md
Continues from: docs/archive/old-topic.md
Continues from: docs/archive/related-topic.md
Continues in: docs/active-spikes/new-topic.md
Continues in: docs/active-spikes/side-topic.md
```

Write `Continues from:` marker lines in successor conceptual docs. Write `Continues in:` marker lines in predecessor conceptual docs before archiving them. Add reciprocal links where practical. If linked docs later move from active to archive, keep the literal paths current during the archive pass.

Use continuation links when a spike is gated, handed off, superseded, split into a new phase, or intentionally closed while related work continues elsewhere. Do not use them for unrelated follow-up ideas.

## Archiving A Spike
When a spike is finished or superseded:

1. Review and update the conceptual and to-do docs to reflect progress.
2. Fold durable lessons into long-lived docs.
3. Add `Continues in:` / `Continues from:` links if related work continues in another spike.
4. Leave spike-local detail in the spike docs.
5. Move both spike docs from `docs/active-spikes/` to `docs/archive/`.
6. Update `TODO.md` so the active work index stays current.

Archived spike docs are historical context. They may be out of date. Do not treat archived docs as current project rules unless a durable doc still says the same thing.

## Durable Lessons Check
Before archiving, ask:

- Did we add or rename CLI commands or MCP tools? Update `README.md` and `AGENTS.md`.
- Did we change agent workflow or write-safety rules? Update `AGENTS.md`.
- Did we settle a durable tradeoff? Add or update a decision record.
- Did we change how auth or credentials are loaded? Update `AGENTS.md` and `.env.example`.
- Did we add a repeatable manual process? Add or update a dedicated local skill in `skills/`.
- Did we create future roadmap work? Update `TODO.md` or create a draft in `docs/scratch/`.
- Did we learn something about API behavior, rate limits, or GraphQL quirks? Record it where future agents will find it.
- Ask more questions than just these. Always check whether the durable docs still describe the repo's real shape.

The archive keeps the texture. Durable docs keep the rule.
