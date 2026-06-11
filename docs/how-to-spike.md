# How To Run A Spike

This repo uses focused work spikes when a body of work needs more shared context than a normal ticket or one-off task can carry.

A spike is not just a checklist. It is a temporary collaboration space for the user and agents to build taste, vocabulary, decisions, and implementation history around a specific theme of work.

Spikes are useful here because this repo manages shared org infrastructure and automation tooling. Changes often need to answer more than "does it work?": they need to be safe for shared org state, respect write authorization boundaries, avoid leaking secrets, produce bounded and auditable output, and avoid firing unwanted notifications to real contributors.

## Authority Ladder

Use docs according to their authority:

- `AGENTS.md`, `README.md`, and active decision records are durable project rules.
- `contributor-policy.md` is a governance doc authored by Open Austin leadership; do not edit it through tooling or agent work.
- `docs/how-to-spike.md` explains this work process.
- Active spike docs explain current thinking for a theme of work.
- Active spike to-do docs track implementation state.
- `TODO.md` is the coordination map across spikes and backlog items.
- `docs/scratch/` is non-authoritative working material.
- `docs/archive/` is historical context, not current rules unless a durable doc still agrees with it.

## The Two Documents

Most active spikes use two docs:

- A **conceptual doc**, such as `docs/github-tooling.md`.
- A **to-do doc**, such as `docs/github-tooling.todo.md`.

The conceptual doc explains the work’s purpose, philosophy, boundaries, and settled model. It should help a new agent understand what kind of solution would be in character for the project.

The to-do doc tracks concrete implementation work. It should be operational: files, actions, QA notes, unresolved questions, and what has already happened.

For now, this guide lives at `docs/how-to-spike.md`. If this repo grows more process docs, move it to something like `docs/process/spikes.md` and leave a short pointer here.

## Conceptual Docs

Use the conceptual doc for:

- goals and non-goals
- project vocabulary
- engineering and tooling philosophy
- major decisions and why they were made
- relationship to other spikes
- constraints that should shape future work (auth model, write-safety rules, API surface choices, rate limit concerns)

Avoid turning the conceptual doc into a running changelog. When implementation details become durable project rules, fold them into longer-lived docs such as `README.md`, `AGENTS.md`, a decision record, a runbook, or another active reference doc.

## To-Do Docs

Use the to-do doc for:

- concrete atomic work items
- current state notes
- implementation progress
- commands and verification steps
- human QA requests
- known edge cases
- short historical notes that will help future agents reconstruct what happened

The to-do doc usually follows this rough structure:

- Background
- Project Organization
- General Principles
- Current State Overview
- To Do
- Ready for Human QA
- Done

Exact headings can flex when needed, but future agents should be able to find current work, QA work, and completed work quickly.

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

`Done` is allowed to preserve useful history. It does not need to be a perfectly compressed final summary. These docs are archived at the end of the spike, and that archive can help future agents understand why the code ended up this way, even if the notes along the way are messy or not totally current. Prefer a useful decision and implementation trail over a neat but context-poor summary. Do not sand off the rough corners of historical artifacts.

## Human QA

Use `Ready for Human QA` for things the agent cannot fully verify from the terminal:

- interaction feel and output tone
- copy tone in comments or generated content that will be visible to org members
- board or issue state in the GitHub UI after a write operation
- whether a dry-run output looks correct before approving a real write
- auth and permission behavior on the real org (cannot be safely exercised without live credentials)
- anything that fires notifications to real contributors — verify before approving

Be specific. A good QA item names the surface, command, expected output, or GitHub UI state the user should inspect.

## Scratch Docs

Use `docs/scratch/` for rough notes, copied references, draft outlines, and exploratory material that is not yet a spike or durable rule.

Scratch docs are not authoritative. Promote useful material into a spike, decision record, runbook, `README.md`, or `AGENTS.md` before relying on it.

## Decision Records

Use `docs/decisions/` for decisions that should outlive a spike. Keep them short:

- context
- decision
- consequences
- links to related spikes or docs

Prefer numbered names such as `0001-docs-workflow.md` once there is more than one decision.

## Archiving A Spike

When a spike is finished:

1. Review the conceptual and to-do docs.
2. Fold durable lessons into long-lived docs.
3. Leave spike-local detail in the spike docs.
4. Move both spike docs to `docs/archive/`.
5. Update `TODO.md` so the active work map stays current.

Archived spike docs are historical context. They may be out of date. Do not treat archived docs as current project rules unless a durable doc still says the same thing.

## Durable Lessons

Before archiving, ask:

- Did we add or rename CLI commands or MCP tools? Update `README.md` and `AGENTS.md`.
- Did we change agent workflow or write-safety rules? Update `AGENTS.md`.
- Did we settle a durable tradeoff? Add or update a decision record.
- Did we change how auth or credentials are loaded? Update `AGENTS.md` and `.env.example`.
- Did we add a repeatable manual process? Add or update a dedicated runbook.
- Did we create future roadmap work? Update `TODO.md` or create a draft in `docs/scratch/`.
- Did we learn something about API behavior, rate limits, or GraphQL quirks? Record it where future agents will find it.
- Ask more questions than just these. Always check whether the durable docs still describe the repo's real shape.

The archive keeps the texture. Durable docs keep the rule.
