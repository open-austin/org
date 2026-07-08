---
name: triage-project-misc
description: "Triage a project's loose scratch inbox at docs/scratch/misc.md into addressed items, thematic scratch docs, numbered misc buckets, active spikes, or durable docs. Use when the user asks to review misc notes, route loose observations, clean up scratch material, cluster possible future work, or process a docs/scratch/misc.md inbox."
---

# Triage Project Misc
This is the Open Austin org repo's own misc-triage process. It is project authority here, not fallback seed material.

## Purpose
`docs/scratch/misc.md` is a live inbox for loose thoughts. Use it for observations that are real enough to keep but too raw to classify yet: small bugs noticed during another spike, taste reactions, possible features, visual discomforts, "this should maybe be better someday" notes, and half-formed clusters that have not earned a named spike doc.

`misc.md` is not a roadmap, not an archive, and not a dumping ground that should grow forever. It is an intake surface.

## Relationship To Spikes
The spike process explains how focused work gets promoted into conceptual and to-do docs, tracked through implementation and QA, and eventually archived.

This skill describes the earlier step: how loose notes become candidate spike material.

The flow is:

1. A thought lands in `docs/scratch/misc.md`.
2. When the user asks for a triage pass, an agent reviews `misc.md` alongside existing scratch docs.
3. Each item is deleted, moved, clustered into a thematic scratch doc, or swept into a numbered miscellaneous bucket.
4. Once a bucket becomes active implementation work, use `run-project-spike` to promote it into the two-doc active spike pattern.

## File Roles
- `docs/scratch/misc.md` is the live inbox for unrouted loose notes.
- `docs/scratch/misc-1.md`, `misc-2.md`, and so on are numbered miscellaneous buckets for real work that does not yet form a clean thematic spike.
- Thematic scratch docs such as `syntax-highlighting.md`, `brand-voice.md`, or `embed-media-support.md` are preferred when notes cluster around a coherent theme.
- Active spike docs in `docs/` exist only after a scratch topic becomes the current implementation focus.
- Archived spike docs in `docs/archive/` are historical context after a spike closes.

## What Belongs In Misc
Good `misc.md` entries are specific enough to preserve the observation:

- a visual detail that feels off
- a bug seen while testing a different surface
- a potential feature without enough shape yet
- a design or taste reaction in the user's own phrasing
- a link or reference that might matter later
- a cluster seed that may become a spike after more related items appear

Bad entries are so compressed they lose the point:

- "Improve homepage"
- "Fix mobile"
- "Make embeds better"
- "Polish stuff"

If a note starts vague, keep the user's concrete phrasing around it. The rambling often contains the actual design constraint.

## Review Process
When asked to review `misc.md`:

1. Read `docs/scratch/misc.md` in full.
2. Read existing `docs/scratch/misc-*.md` numbered buckets.
3. Read likely thematic scratch docs.
4. Search current active and archived spike docs if an item looks familiar.
5. Route each `misc.md` item.
6. Preserve nuance when moving items.
7. Delete routed or addressed items from `misc.md`.
8. Replace the `Latest Routing Session` section in `misc.md` with a short summary of the current review only.

Do not keep an infinite routing history in `misc.md`. The latest routing session summary is a handoff, not an archive. The next review should replace it.

## Routing Outcomes
### Already Addressed
If an item has already been completed or captured in a durable doc, delete it from `misc.md`.

If the routing might be confusing later, mention it briefly in the latest routing session summary.

### Existing Thematic Scratch Doc
If an item clearly belongs to an existing scratch topic, move it there.

Preserve:

- the user's concrete examples
- any uncertainty or alternatives
- references and URLs
- why the thing felt wrong or worth noticing
- visual or taste language, even if informal

Clean the prose enough to make the destination doc readable, but do not flatten the item into a generic ticket.

### New Thematic Scratch Doc
If several items cluster around a clear theme, create a new scratch doc with a descriptive name.

Shape the new thematic scratch doc like a lightweight conceptual spike doc, but keep it in `docs/scratch/` and do not create the active `.todo.md` companion yet. It should usually include:

- goal
- current context
- scope
- vocabulary, constraints, or taste notes that would shape future work
- files or systems likely involved
- open questions
- rough work items
- human QA surfaces, if visual or editorial judgment will matter

Do not create a full active spike to-do yet unless the user is actually starting that work. The thematic scratch doc is candidate conceptual context; `run-project-spike` handles active promotion.

### Numbered Miscellaneous Bucket
If an item is real but does not belong to an existing doc and does not cluster into a thematic spike, sweep it into a numbered `misc-#.md` bucket.

Use this when the work is small, mixed, or opportunistic. A numbered misc bucket can become its own active spike later, like any other scratch doc.

## Reviewing Existing Misc Buckets
Every `misc.md` review should also examine existing numbered misc docs in `docs/scratch/`.

Ask:

- Do any old misc items now cluster with the new `misc.md` items?
- Has a grab-bag item gained a clearer thematic home?
- Should an item move from `misc-#.md` into a named scratch topic?
- Has an item already been completed or superseded?

Numbered misc docs are temporary holding areas, not permanent junk drawers. If a better theme emerges, move the item out.

## Preservation Rule
Do not over-compress `misc.md` items while parting them out.

The user's loose phrasing may contain design signal: emotional reaction, uncertainty, analogy, hierarchy of importance, or a concrete example that a short task title would erase. Keep that texture in the destination doc.

The goal is not to preserve every typo or duplicate sentence. The goal is to preserve meaning, taste, references, and the reason the note existed.

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
