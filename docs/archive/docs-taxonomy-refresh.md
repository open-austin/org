# Docs Taxonomy Refresh
Status: closed, archived 2026-07-13 after human review and QA approval. Opened 2026-07-13 to bring this repo's local docs and skills taxonomy in line with the current personal project workflow pattern while preserving Open Austin-specific write-safety and public-org boundaries.

## Goal
Update the repo-local workflow docs so future agents can route work cleanly:

```text
docs/pinned-issues.md        unresolved org/tooling/process issues intentionally preserved for later
docs/scratch/future-ideas.md conceptual someday org/tooling/process ideas
docs/scratch/misc.md         raw observed friction / issue intake
docs/decisions/              settled durable rules
docs/active-spikes/          active scoped work
```

## Why This Matters Here
This repo manages shared Open Austin org infrastructure. Misrouting work has higher blast radius than in a private scratch repo: raw observations can become accidental roadmap, unresolved concerns can masquerade as decisions, and public-org write behavior must stay guarded.

The update should make future agents better at deciding whether something is a durable rule, a pin, a future idea, misc intake, or active work before touching GitHub issues, boards, labels, Slack summaries, or automation.

## Scope
- Add repo-local `pin-issue`, `log-future-idea`, and `update-local-skills` skills.
- Update `run-project-spike` and `triage-project-misc` with the current routing taxonomy while preserving Open Austin-specific safety guidance.
- Add starter `docs/pinned-issues.md` and `docs/scratch/future-ideas.md` files.
- Update `AGENTS.md`, `README.md`, and `TODO.md` so future agents can discover the taxonomy.

## Non-Goals
- Do not change GitHub automation behavior.
- Do not modify `.env`, snapshots, credentials, or generated GitHub state.
- Do not add global skill-feedback or skill-authoring workflows here; cross-project skill feedback belongs in the configs repo.
- Do not create GitHub issues, move board cards, post comments, or run write operations.
