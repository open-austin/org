# Docs Taxonomy Refresh To-Do
## Current State
Opened 2026-07-13. Closed and archived 2026-07-13 after human review and QA approval. The repo already had `docs/active-spikes/`, `docs/archive/`, `docs/decisions/`, `docs/scratch/misc.md`, and local workflow skills. This pass added the newer taxonomy for pinned issues, future ideas, misc intake, durable decisions, and active spikes while preserving Open Austin-specific write-safety rules.

## To Do
None. All work complete.

## Ready for Human QA
None outstanding.

## Done
- [x] Added local skills: `pin-issue`, `log-future-idea`, and `update-local-skills`.
- [x] Updated `run-project-spike` and `triage-project-misc` for the shared taxonomy.
- [x] Added `docs/pinned-issues.md` and `docs/scratch/future-ideas.md`.
- [x] Updated `AGENTS.md`, `README.md`, and `TODO.md`.
- [x] Validated local Markdown links, skill frontmatter, and secret hygiene over touched files.
- [x] Human review of the taxonomy wording in `AGENTS.md`, `README.md`, and local skills — approved 2026-07-13.
- [x] Human QA: Open Austin-specific wording around GitHub issue backlog vs. local docs holding areas reviewed and approved. No GitHub writes or external notifications were performed.

## Validation Notes
- Skill frontmatter parsed as YAML for all repo-local skills.
- Local Markdown links in touched docs and skills resolve.
- Secret scan over touched docs and skills produced no matches. `.env`, snapshots, credentials, and generated GitHub state were not modified.
