---
name: triage-project-misc
description: "Triage a project's loose scratch inbox at docs/scratch/misc.md into addressed items, future ideas, pinned issues, thematic scratch docs, numbered misc buckets, active spikes, or durable docs. Use when the user asks to review misc notes, route loose observations, clean up scratch material, cluster possible future work, or process a docs/scratch/misc.md inbox."
---

# Triage Project Misc
This is the Open Austin org repo's own misc-triage process. It is project authority here, not fallback seed material.

## Purpose
`docs/scratch/misc.md` is a live inbox for loose thoughts. Use it for observations that are real enough to keep but too raw to classify yet: small bugs noticed during another spike, QA nits, taste reactions, possible features, visual discomforts, board/process friction, and half-formed clusters that have not earned a named spike doc.

`misc.md` is not a roadmap, not a future-ideas list, not a pin register, not an archive, and not a dumping ground that should grow forever. It is raw observed friction and issue intake.

## Relationship To Spikes
The spike process explains how focused work gets promoted into conceptual and to-do docs, tracked through implementation and QA, and eventually archived.

This skill describes the earlier step: how loose notes become candidate spike material or get routed elsewhere.

The flow is:

1. A thought lands in `docs/scratch/misc.md`.
2. When the user asks for a triage pass, an agent reviews `misc.md` alongside existing scratch docs, pins, future ideas, and active spikes.
3. Each item is deleted, moved, clustered into a thematic scratch doc, routed to future ideas or pinned issues, or swept into a numbered miscellaneous bucket.
4. Once a bucket becomes active implementation work, use `run-project-spike` to promote it into the two-doc active spike pattern.

## Routing Taxonomy
Use the first matching destination:

- `docs/decisions/` for settled durable repo rules.
- `docs/pinned-issues.md` for unresolved issues intentionally preserved for later.
- `docs/scratch/future-ideas.md` for conceptual someday material.
- `docs/scratch/misc.md` for raw observed friction, QA nits, bugs, and issue intake.
- `docs/active-spikes/` for active scoped work.

Future ideas are conceptual and farther-horizon than misc notes. Pinned issues are unresolved concerns or tradeoffs intentionally preserved for later. Neither is a GitHub issue backlog, and neither authorizes GitHub writes.

## File Roles
- `docs/scratch/misc.md` is the live inbox for unrouted loose observations.
- `docs/scratch/future-ideas.md` holds coherent someday org/tooling/process ideas that are not active work.
- `docs/pinned-issues.md` holds unresolved concerns, questions, or tradeoffs to revisit when context changes.
- `docs/scratch/misc-1.md`, `misc-2.md`, and so on are numbered miscellaneous buckets for real work that does not yet form a clean thematic spike.
- Thematic scratch docs such as `board-onboarding.md`, `github-label-taxonomy.md`, or `org-summary-tone.md` are preferred when notes cluster around a coherent theme.
- Active spike docs in `docs/active-spikes/` exist only after a scratch topic becomes the current implementation focus.
- Decision records in `docs/decisions/` are durable project rules, not scratch or spike notes.
- Archived spike docs in `docs/archive/` are historical context after a spike closes.

## What Belongs In Misc
Good `misc.md` entries are specific enough to preserve the observation:

- a board, issue, workflow, or docs detail that feels off
- a bug seen while testing a different surface
- a potential feature without enough shape yet
- a design, process, or taste reaction in the user's own phrasing
- a link or reference that might matter later
- a cluster seed that may become a spike after more related items appear

Bad entries are so compressed they lose the point:

- "Improve board"
- "Fix labels"
- "Make summaries better"
- "Polish stuff"

If a note starts vague, keep the user's concrete phrasing around it. The rambling often contains the actual design constraint.

## Review Process
When asked to review `misc.md`:

1. Read `docs/scratch/misc.md` in full.
2. Read existing `docs/scratch/misc-*.md` numbered buckets.
3. Read `docs/scratch/future-ideas.md` and `docs/pinned-issues.md` if they exist.
4. Read likely thematic scratch docs.
5. Search current active and archived spike docs if an item looks familiar.
6. Route each `misc.md` item.
7. Preserve nuance when moving items.
8. Delete routed or addressed items from `misc.md`.
9. Replace the `Latest Routing Session` section in `misc.md` with a short summary of the current review only.

Do not keep an infinite routing history in `misc.md`. The latest routing session summary is a handoff, not an archive. The next review should replace it.

## Routing Outcomes
### Already Addressed
If an item has already been completed or captured in a durable doc, delete it from `misc.md`.

If the routing might be confusing later, mention it briefly in the latest routing session summary.

### Future Idea
If an item is a coherent someday org/tooling/process concept, move it to `docs/scratch/future-ideas.md`.

Use this when the note is conceptual enough to reread later as an idea, but not scoped enough to become an active spike. Do not create a GitHub issue, board item, or write operation unless the user is actually starting that work.

### Pinned Issue
If an item is an unresolved concern, question, or tradeoff that should be intentionally preserved until context changes, move it to `docs/pinned-issues.md`.

A pin should include the current context and a concrete revisit trigger. Do not use pins as ordinary backlog, and do not let pins masquerade as decisions.

### Durable Decision
If triage reveals that a rule is already settled and should guide future agents, create or update a decision record under `docs/decisions/`.

Decision records should be rare and durable. Do not create them for every implementation note or unresolved question.

### Existing Thematic Scratch Doc
If an item clearly belongs to an existing scratch topic, move it there.

Preserve:

- the user's concrete examples
- any uncertainty or alternatives
- references and URLs
- why the thing felt wrong or worth noticing
- visual, process, governance, or taste language, even if informal

Clean the prose enough to make the destination doc readable, but do not flatten the item into a generic ticket.

### New Thematic Scratch Doc
If several items cluster around a clear theme, create a new scratch doc with a descriptive name.

Shape the new thematic scratch doc like a lightweight conceptual spike doc, but keep it in `docs/scratch/` and do not create the active `.todo.md` companion yet. It should usually include:

- goal
- current context
- scope
- vocabulary, constraints, or taste notes that would shape future work
- files, tools, GitHub surfaces, or org processes likely involved
- open questions
- rough work items
- human QA surfaces, if visual, editorial, governance, or notification judgment will matter

Do not create a full active spike to-do yet unless the user is actually starting that work. The thematic scratch doc is candidate conceptual context; `run-project-spike` handles active promotion.

### Numbered Miscellaneous Bucket
If an item is real but does not belong to an existing doc and does not cluster into a thematic spike, sweep it into a numbered `misc-#.md` bucket.

Use this when the work is small, mixed, or opportunistic. A numbered misc bucket can become its own active spike later, like any other scratch doc.

## Reviewing Existing Misc Buckets
Every `misc.md` review should also examine existing numbered misc docs in `docs/scratch/`.

Ask:

- Do any old misc items now cluster with the new `misc.md` items?
- Has a grab-bag item gained a clearer thematic home?
- Should an item move from `misc-#.md` into a named scratch topic, future ideas, pinned issues, decisions, or active work?
- Has an item already been completed or superseded?

Numbered misc docs are temporary holding areas, not permanent junk drawers. If a better theme emerges, move the item out.

## Preservation Rule
Do not over-compress `misc.md` items while parting them out.

The user's loose phrasing may contain design signal: emotional reaction, uncertainty, analogy, hierarchy of importance, or a concrete example that a short task title would erase. Keep that texture in the destination doc.

The goal is not to preserve every typo or duplicate sentence. The goal is to preserve meaning, taste, references, and the reason the note existed.

## Public Org Safety
This repo touches a public GitHub org and real contributors. Do not route misc notes into GitHub comments, issue edits, board moves, Slack posts, or other external writes during triage unless the user explicitly approves a specific write plan.

Do not include tokens, private credentials, Slack webhook URLs, private contributor data, or other public-unsafe details in scratch docs. Use generic phrasing when private context matters.

## Misc Template
Use this shape:

```md
# Misc Inbox
Live inbox for loose observations.

## Unrouted Items
- ...

## Latest Routing Session
Reviewed YYYY-MM-DD.

- Moved ...
- Deleted ...
- Created ...
```

The `Latest Routing Session` section should be replaced on each review. It is only the latest handoff.
