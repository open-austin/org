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
  pinned-issues.md
  scratch/
    future-ideas.md
    misc.md
  archive/
  decisions/
```

Active conceptual and to-do docs go in `docs/active-spikes/`, unresolved issues intentionally preserved for later go in `docs/pinned-issues.md`, conceptual someday material goes in `docs/scratch/future-ideas.md`, rough intake goes in `docs/scratch/misc.md`, and finished or superseded spike history goes in `docs/archive/`. Durable long-term docs (`README.md`, `AGENTS.md`, `contributor-policy.md`, decision records) stay out of active spike work.

## Authority Ladder
When docs conflict, use this order (mirrors `AGENTS.md`):

1. `AGENTS.md` (or `CLAUDE.md`) and `README.md` — durable project rules
2. `contributor-policy.md` — Open Austin governance doc; do not edit it through tooling or agent work
3. Active decision records in `docs/decisions/` — settled tradeoffs
4. Active spike docs in `docs/active-spikes/` — current thinking for a theme of work
5. Active spike to-do docs in `docs/active-spikes/` — implementation state
6. `TODO.md` — active work coordination
7. `docs/pinned-issues.md` — unresolved issues intentionally preserved for later
8. `docs/scratch/future-ideas.md` — conceptual someday material
9. `docs/scratch/misc.md` and other `docs/scratch/` files — exploratory intake, non-authoritative
10. `docs/archive/` — historical context only

Repo-local skills in `skills/` (this file included) are project authority over any similarly named global skill.

## Attention and Historical Authority
Give both spike documents explicit YAML frontmatter: `attention: live` while actively maintained, and `attention: historical` when archived. Use the repository's equivalent metadata if it already has a different convention. These values describe how to use the document, not whether its tasks are done or its proposals approved.

`live` means agents should maintain the document as work develops. It does not turn unresolved alternatives or agent proposals into adopted rules. `historical` means the document records the work as it stood at closure; its instructions and task states must not be applied as current guidance. Follow its links to maintained guidance or successor work, then verify there.

Keep the marker in each file so its authority remains visible when search retrieves the document outside its folder. At closure, also put a plain-language historical notice near the top, alongside the closure date and stable slug. Metadata helps readers and tools recognize history; it does not enforce correct retrieval or interpretation on its own.

Keep topical `tags` separate. If the repository uses `reviewed: YYYY-MM-DD`, advance it only after checking the document's claims or recorded state, not merely touching the file. Do not relabel the entire archive or introduce a broader attention taxonomy as part of an ordinary spike.

## TODO.md Role
Use `TODO.md` as an index and coordination map, not as the place for fiddly implementation detail.

It should point to active spike docs, note waiting-for-human-QA items, list recently completed or archived spikes, and hold lightweight later ideas. Detailed work items, command logs, and state transitions belong in the spike's `.todo.md`.

## The Two Documents
Active spikes use two docs:

- A conceptual doc, such as `docs/active-spikes/<topic>.md`.
- A to-do doc, such as `docs/active-spikes/<topic>.todo.md`.

The conceptual doc explains the work's purpose, philosophy, boundaries, developing alternatives, and settled model where one exists. Distinguish user-adopted positions from agent proposals and unresolved questions. It should help a new agent understand what kind of solution would be in character for the project. Substantial exploratory discussion can belong here without turning every possibility into an implementation task.

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

## Selecting Material for the Repository
Before writing spike notes, consider the repository's intended audience. Preserve project-relevant reasoning, qualifications, corrections, and useful examples without copying unnecessary or unauthorized private conversation, source packages, personal paths, or surrounding workspace details. Permission to preserve development reasoning is not permission to publish private source material. Keep user decisions distinguishable from agent suggestions; a saved proposal is not evidence of human agreement.

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

### Moving An Item Preserves It
Moving an item is a *move*, not a rewrite. Carry the item's original wording into `Done` and append what happened. Do not restate it in your own words, and do not compress it because you now know how it turned out.

**One `To Do` item becomes exactly one `Done` entry.** Never merge several items into a single synthesized entry, however naturally they were finished together. The plan and the outcome are two different artifacts: the history explains why the code looks like this, and the surviving item list is what lets a reader check the plan against the result. An agent that finished three items in one motion has three `Done` entries, each with its own note.

Unplanned work gets *added* entries — surprises, reversals, things discovered — never folded into a planned item's entry.

A `To Do` item that is dropped rather than done is moved to `Done` and marked as dropped, with the reason. Deleting it erases the fact that it was ever considered.

## Committing Spike Work
Repos differ on whether agents may commit. Follow the repo's own policy, stated in its `AGENTS.md` or its durable policies. **If the repo says nothing, do not commit and do not offer to.**

Where agent commits are permitted, use the `commit-work` skill. Do not write commit logic, staging logic, or commit messages here; hand it the spike's slug and let it own the rest. It writes a `Spike: <slug>` trailer on each commit, which is what later allows a spike's history to be reconstructed:

```sh
git log --grep='Spike: <slug>$' --reverse
```

Use `commit-work` to choose timely checkpoints for coherent changes and useful experimental states. Preserve distinct candidates and consequential corrections while keeping concurrent spikes traceable. A conversation turn ending is not itself a checkpoint, and an entire spike need not finish before committing. Human QA status is separate from checkpoint timing; an explicit request to review before committing overrides routine checkpointing until that review ends or the user authorizes the checkpoint.

The `.todo.md` edit that moves an item and a `TODO.md` update describing the same work belong in the same commit as that work when their full diffs are in scope. Shared files require checking for unrelated work from concurrent spikes; their filename alone is not a reason to split them into separate commits.

When the user confirms QA, moving items to `Done` is its own doc-only commit, batched per **approval event**: one approval is one commit, however many items it covered. It records when the work was blessed, which no other artifact does.

Never push. Pushing is the user's.

## Human QA
Use `Ready for Human QA` for things the agent cannot fully verify from the terminal:

- copy tone in comments or generated content that will be visible to org members
- board or issue state in the GitHub UI after a write operation
- whether a dry-run output looks correct before approving a real write
- auth and permission behavior on the real org (cannot be safely exercised without live credentials)
- anything that fires notifications to real contributors — verify before approving

Be specific. A good QA item names the surface, command, expected output, or GitHub UI state the user should inspect.

## Scratch Promotion
Use the shared routing taxonomy before promoting material:

- `docs/decisions/` for settled durable repo rules.
- `docs/pinned-issues.md` for unresolved issues intentionally preserved for later.
- `docs/scratch/future-ideas.md` for conceptual someday material.
- `docs/scratch/misc.md` for raw observed friction, QA nits, bugs, and issue intake.
- `docs/active-spikes/` for active scoped work.

Use `docs/scratch/` for rough notes, copied references, draft outlines, and exploratory material that is not yet a spike or durable rule.

Scratch docs are not authoritative. Promote useful material into an active spike, durable doc, or local skill before relying on it.

Promotion means move, not copy. When promoting a scratch doc into `docs/active-spikes/`, move its useful content into the active conceptual and to-do docs, then delete or clearly retire the old scratch source. Do not leave an outdated duplicate in `docs/scratch/`.

If a scratch doc contains multiple themes, split it deliberately: move each useful piece into the right destination, then remove the routed source material. Preserve nuance and concrete user phrasing while moving it.

For loose unrouted notes, use `docs/scratch/misc.md` and the `triage-project-misc` skill. For unresolved questions that should be intentionally preserved, use `docs/pinned-issues.md` and `pin-issue`. For coherent someday concepts, use `docs/scratch/future-ideas.md` and `log-future-idea`.

## Durable Guidance
Use the existing `docs/decisions/` location for current durable rules, defaults, procedures, and their rationale. Revise current guidance directly and let Git preserve its evolution; do not require an immutable ADR or a new record for every implementation choice. Keep developing alternatives in the spike until adopted. Existing governance authority and the prohibition on agent edits to `contributor-policy.md` still apply.

## Starting A Spike
1. Inspect `AGENTS.md`, `README.md`, `TODO.md`, `docs/active-spikes/`, `docs/scratch/`, `docs/archive/`, durable docs, and repo-local skills.
2. Decide whether the work belongs in an existing active spike, a new named spike, or a miscellaneous spike bucket.
3. Choose a short topic slug. For mixed work, use the repo's numbered misc convention.
4. Create or update `docs/active-spikes/<topic>.md` for conceptual context, with `attention: live` or the repository's equivalent.
5. Create or update `docs/active-spikes/<topic>.todo.md` for implementation state, with the same attention marker.
6. Add or update the spike entry in `TODO.md` as an index pointer.
7. Capture known constraints, non-goals, validation expectations, and open questions before implementation if they matter.

## During A Spike
Keep conceptual understanding in the conceptual doc and operational state in the to-do doc. Update item statuses as work moves. Preserve enough history to explain decisions, but move durable rules out of the spike when they become repo policy.

Do not let scratch notes silently become authority. Promote them deliberately.

Repair direct dependencies when actual changes land: a moved file's inbound links, an index entry, or instructions invalidated by a changed command. Keep speculative alternatives in the spike until settled or implemented; do not repeatedly rewrite durable guidance to match each possibility discussed. Reserve the broader check of affected live guidance for closure. Neither pass grants authority to edit unrelated projects or external systems.

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
4. Leave spike-local detail in the spike docs. Set both to `attention: historical` or the repository's equivalent, and add a plain-language historical notice, closure date, and stable spike slug to both; link the conceptual doc to the maintained guidance and successor work that now own the subject. If no successor or maintained guidance resulted, say so rather than inventing one.
5. Move both spike docs from `docs/active-spikes/` to `docs/archive/`. Retain the pair by default, even when all useful current guidance has been integrated elsewhere.
6. Update `TODO.md` so the active work index stays current.
7. Where agent commits are permitted, land the archival as a single commit via `commit-work`, with the spike summary as its message. Show the message to the user and commit on their approval.

Archived spike docs are historical context. They may be out of date. Use maintained docs or the current implementation to establish what applies now, even when the archive appears to agree. Keep their historical body as it stood at closure; later navigation repairs are allowed, and any necessary factual correction should be marked as a later correction rather than silently rewriting the record.

The archived pair is a discoverable entry point into the development history: ordinary file searches can find its subject and reasoning, and its stable slug connects it to `git log --grep='Spike: <slug>$' --reverse`. Git supplies the earlier versions and finer sequence. Do not delete the archived pair merely because it can be recovered from Git, or compress it into a replacement summary by default. No separate history index is required.

### The Archival Commit
The archival is itself a commit: the doc moves and the `TODO.md` update are its diff. So its message is the spike's summary, and it is the one commit in a spike worth reviewing before it lands.

That message is a **synthesis, not a rollup**. Draw on the trailer log, the conceptual doc, the to-do doc's `Done` section, and verified working context. Explain consequential alternatives, discovered constraints, and corrections needed to understand the result; do not invent a cleaner development story or infer user agreement. Earlier commits may preserve an abandoned implementation, but they cannot recover reasoning never recorded. Select only material suitable for the repository's audience.

Write the summary message and do the archival doc pass as one act, from one synthesis.

## Durable Lessons Check
Before archiving, check the live guidance affected by this spike. Search for changed paths, commands, and rules where useful; this is a bounded dependency check, not a whole-repository audit. Preserve substantial reasoning, examples, and qualifications when integrating them into maintained docs; current guidance need not be a compressed summary. Historical accounts of an old behavior are not stale instructions to rewrite.

Ask:

- Did we add or rename CLI commands or MCP tools? Update `README.md` and `AGENTS.md`.
- Did we change agent workflow or write-safety rules? Update `AGENTS.md`.
- Did we settle a durable tradeoff? Add or update a decision record.
- Did we change how auth or credentials are loaded? Update `AGENTS.md` and `.env.example`.
- Did we add a repeatable manual process? Add or update a dedicated local skill in `skills/`.
- Did we create unresolved issues that should survive the chat but not become work yet? Update `docs/pinned-issues.md`.
- Did we create conceptual someday material? Update `docs/scratch/future-ideas.md`.
- Did we create raw friction or issue intake? Update `docs/scratch/misc.md`.
- Did we create future roadmap work that is scoped enough to coordinate? Update `TODO.md` or create an active spike.
- Did we learn something about API behavior, rate limits, or GraphQL quirks? Record it where future agents will find it.
- Ask more questions than just these. Always check whether the durable docs still describe the repo's real shape.

The archive keeps the texture. Durable docs keep the rule.
