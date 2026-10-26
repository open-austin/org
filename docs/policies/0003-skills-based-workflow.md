# 0003 — Skills-Based Agent Workflow
## Current Approach
Use `project-workflows/<name>/SKILL.md` for the seven adopted project procedures, and `skills/<name>/SKILL.md` for organization-specific workflows. Project-local procedures govern this project; global workflows are fallback seeds. Use `project-workflows/update-project-workflows/SKILL.md` to reconcile the collection while preserving the authority ladder, write-safety rules, and organization-specific QA guidance.

The weekly summary workflow lives in `skills/weekly-org-summary/SKILL.md`; the recurring meeting workflow lives in `skills/process-weekly-meeting/SKILL.md`. Read each skill's current scope and status rather than treating its presence as permission to run a retired workflow.

Active spike conceptual/to-do pairs live in `docs/active-spikes/`; current durable guidance lives in `docs/policies/`; rough exploration belongs in `docs/scratch/`; closed or superseded spike history belongs in `docs/archive/`. [AGENTS.md](../../AGENTS.md) and the [spike skill](../../project-workflows/run-project-spike/SKILL.md) own the process. Revise policies directly while Git retains their history. The original maintainer's checkout path is not a setup requirement.

## Rationale
One workflow mechanism gives agents explicit trigger descriptions and a clear update path. Separating active work, current policies, rough notes, and historical records prevents exploratory or retired instructions from competing with maintained guidance.

## Operating Notes
Keep organization-specific repeatable workflows with their local skill owner; reconcile reusable project procedures through the adopted collection. Keep `TODO.md` as the coordination index. The former `docs/how-to-spike.md` and weekly-summary runbook have been replaced by local skills.

## Links
- `project-workflows/run-project-spike/SKILL.md`
- `project-workflows/triage-project-misc/SKILL.md`
- `skills/weekly-org-summary/SKILL.md`
- `docs/archive/github-automation.md`, `docs/archive/wiki-migration.md` (both since archived)
- `AGENTS.md` — Authority Ladder and Skills sections
