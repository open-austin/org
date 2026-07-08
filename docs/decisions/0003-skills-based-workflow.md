# 0003 — Skills-Based Agent Workflow
**Date:** 2026-07-07
**Status:** Accepted

## Context
The repo's agent workflow had grown into two parallel, ad hoc mechanisms: `docs/how-to-spike.md` (a standalone process doc for the spike workflow) and a `## Runbooks` table in `AGENTS.md` pointing at `docs/runbook-weekly-summary.md`. Both were repo-specific customizations of patterns the user maintains as reusable skills (`run-project-spike`, `triage-project-misc`) in a personal seed library at `~/configs/skills/`. Keeping the repo's copies as free-standing docs meant they'd drift from the seed patterns without a clear mechanism for reconciling them, and meant agent-discoverable workflows lived in two different shapes (a doc link vs. a table entry) instead of one.

Separately, active spike docs lived flat under `docs/` (e.g. `docs/github-automation.md` + `.todo.md`), while `docs/scratch/wiki-migration.md` was informally tracked as an "Active Spike" in `TODO.md` despite living in scratch with no `.todo.md` companion — an inconsistency the user wanted to eliminate.

## Decision
1. Adopt `skills/` as the single mechanism for repo-local agent workflows. Vendor `run-project-spike` and `triage-project-misc` from `~/configs/skills/` into `skills/`, adapted with this repo's authority ladder, write-safety rules, and GitHub/org-specific QA guidance (previously in `docs/how-to-spike.md`, now removed).
2. Rewrite the weekly summary runbook as `skills/weekly-org-summary/SKILL.md` (previously `docs/runbook-weekly-summary.md`, now removed). Its frontmatter `description` carries the trigger phrases that used to live in `AGENTS.md`'s Runbooks table.
3. Adopt `docs/active-spikes/` for active spike doc pairs, migrating `docs/github-automation.{md,todo.md}` there and promoting `docs/scratch/wiki-migration.md` into a proper `docs/active-spikes/wiki-migration.{md,todo.md}` pair.

## Consequences
- `AGENTS.md` now points to `skills/run-project-spike/SKILL.md` for the spike process and lists all repo-local skills in a `## Skills` section instead of a separate `## Runbooks` table.
- Future repeatable agent workflows should be added as new `skills/<name>/SKILL.md` folders rather than standalone docs.
- Active spike docs are found in `docs/active-spikes/`, not flat under `docs/`.
- `docs/how-to-spike.md` and `docs/runbook-weekly-summary.md` no longer exist; their content lives in `skills/`.

## Related
- `skills/run-project-spike/SKILL.md`
- `skills/triage-project-misc/SKILL.md`
- `skills/weekly-org-summary/SKILL.md`
- `docs/active-spikes/github-automation.md`, `docs/active-spikes/wiki-migration.md`
- `AGENTS.md` — Authority Ladder and Skills sections
