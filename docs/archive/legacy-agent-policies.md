---
attention: historical
reviewed: 2026-11-02
---
# Legacy agent policy source records
Retired 2026-11-02 by Aslan’s explicit approval of the Open Austin agent-policy adoption and removal of the old policies folder. The five numbered identities below remain reserved. These exact source blocks preserve the full sanitized pre-migration content and rationale; their instructions are historical, not operative. Current obligations are in the [agent policy index](../agent-policies/policy.index.md); human organizational governance remains in [contributor-policy.md](../../contributor-policy.md).

<a id="legacy-0001"></a>
## 0001 — retired source record
Status: retired. Authority: Aslan, explicit adoption and old-folder removal instruction in this chat, 2026-11-02. Reserved identity: `0001` (original path `docs/policies/0001-tooling-foundations.md`). Current agent obligation: `USE-TOOLS`; this mapping records the reviewed migration and does not grant authority through an alias. Original SHA-256: `22d74bca3daa16830fc9bd4ec5409c7578ae909ee43c96b3db942c6037b18e3e`.

```markdown
# 0001 — Tooling Foundations
## Current Approach
Keep organization tooling in this repository so contributors can clone and operate it independently. Use `gh` and `gh api graphql` for durable GitHub reads and guarded writes; Projects v2 operations require GraphQL and opaque node IDs. Interactive MCP access is a convenience layer over the same API, with the same write-safety rules.

Read current organization state through `gh`. This repository does not ship snapshot sync tooling; `tools/sync/` was retired on 2026-09-07. `snapshot/` is ignored scratch space, not current GitHub state.

Add new write capabilities incrementally, beginning with the smallest useful surface. Tools must support dry runs and require explicit user approval before execution. For ad-hoc `gh` writes without a wrapper, show the exact change and obtain approval before running the command. [AGENTS.md](../../AGENTS.md) owns the full authorization rules. [Python CLI policy](0002-python-cli.md) owns implementation language, and [board sync policy](0005-board-sync-architecture.md) owns the automation architecture.

## Rationale
Organization tooling acts on shared issues, boards, labels, and milestones. Keeping it colocated with the organization and using one scriptable API boundary makes it portable and auditable. Projects v2 support adds GraphQL complexity because the organization uses that workflow surface.

## Operating Notes
- Tools must support GraphQL for Projects v2 operations.
- GitHub credentials need the required repository and project scopes, plus organization SAML SSO authorization when applicable; see [CONTRIBUTING.md](../../CONTRIBUTING.md).
- Interactive MCP and CLI paths must not diverge in their write-safety rules.

## Links
- [AGENTS.md](../../AGENTS.md) — authorization and operating rules
- [Spike skill](../../project-workflows/run-project-spike/SKILL.md)
- [TODO.md](../../TODO.md) — active work index
- [Tooling history](../archive/github-tooling.md)
- [Sync retirement](../archive/retire-sync-tooling.md)
```

<a id="legacy-0002"></a>
## 0002 — retired source record
Status: retired. Authority: Aslan, explicit adoption and old-folder removal instruction in this chat, 2026-11-02. Reserved identity: `0002` (original path `docs/policies/0002-python-cli.md`). Current agent obligation: `BUILD-CLI`; this mapping records the reviewed migration and does not grant authority through an alias. Original SHA-256: `d620d130ba8d71b267a217bf0ccf2ab108826f8828367b2ad9fe0ef092391f46`.

```markdown
# 0002 — Python CLI over Shell Scripts
## Current Approach
Use Python 3 for substantive CLI tools. Thin shell wrappers may provide familiar entry points. The local example is `tools/airtable/`. Generic Google Docs operations use the separately installed Agent Hands `use-google-docs` skill; Org owns the meeting procedure and target choices. The retired `tools/google-docs/` and `tools/sync/` scripts are historical examples, not missing dependencies.

## Rationale
1. **Native JSON handling:** Python's `json` module is more intuitive than multi-stage `jq` pipelines for complex transformations
2. **Better error messages:** Python exceptions are clearer than `jq: error (at <stdin>:490): Cannot index number with string "assignees"`
3. **Easier to extend:** Future write tools will need argument parsing, validation, dry-run logic — Python's standard library handles this cleanly
4. **Testability:** Python functions can be unit tested; shell pipelines are harder to test in isolation
5. **Readability:** The logic is explicit and procedural, not spread across multiple chained commands

**Tradeoff:** Python is slightly more verbose than shell one-liners, but the improved clarity and maintainability justify the cost.

## Operating Notes
Document Python and each tool's actual runtime dependencies in its setup instructions. Prefer standard-library argument parsing, validation, JSON handling, and dry-run logic where sufficient; inspect a tool's current implementation instead of inferring its dependencies from retired sync tooling.

## Links
- [Tooling history](../archive/github-tooling.md)
- [Sync retirement](../archive/retire-sync-tooling.md)
- `docs/policies/0001-tooling-foundations.md` — foundational architectural choices
```

<a id="legacy-0003"></a>
## 0003 — retired source record
Status: retired. Authority: Aslan, explicit adoption and old-folder removal instruction in this chat, 2026-11-02. Reserved identity: `0003` (original path `docs/policies/0003-skills-based-workflow.md`). Current agent obligation: `FOLLOW-WORKFLOWS`; this mapping records the reviewed migration and does not grant authority through an alias. Original SHA-256: `3e76c77879a41f8b95ae29ed5c6710d3448a5144911de0220a8a89fa06110091`.

```markdown
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
```

<a id="legacy-0004"></a>
## 0004 — retired source record
Status: retired. Authority: Aslan, explicit adoption and old-folder removal instruction in this chat, 2026-11-02. Reserved identity: `0004` (original path `docs/policies/0004-projects-v2-automation-triggers.md`). Current agent obligation: `DESIGN-TRIGGERS`; this mapping records the reviewed migration and does not grant authority through an alias. Original SHA-256: `a87baf558787a330f69b92fe34a8e7fad1ede1ad2ccce26b43a97feec91c2113`.

```markdown
# 0004 — Projects v2 Board Changes Can't Trigger Repo-Level Actions
## Current Approach
Do not use `on: projects_v2_item` in repository GitHub Actions workflows to react to Projects v2 field changes. Use a native Projects workflow when it fits; otherwise use scheduled reconciliation under this repository's no-hosting boundary.

Issue-state events can drive board updates through repository Actions. Board-to-issue close uses native `Auto-close issue`. Board-to-issue reopen uses the single `board-reopen-reconcile.yaml` workflow, covering both boards with a five-minute cron and a manual `dry_run` input. [0005](0005-board-sync-architecture.md) owns the current routing, native-workflow exception, and fresh-close guard. The former separate fifteen-minute reopen workflows are retired.

## Rationale
Projects v2 field-change webhooks are organization-scoped; repository Actions cannot subscribe directly to them. The earlier workflows parsed as valid YAML but never ran. A hosted webhook bridge would add infrastructure this repository avoids. Native close and scheduled reopen respect that platform boundary.

## Operating Notes
Before building board-reactive automation, check the project's native workflows. Scheduled reconciliation is best-effort and may be delayed; the five-minute cron is not a delivery guarantee. Reopening the issue directly uses the immediate issue-event path.

## Links
- `docs/archive/github-automation.md`, `docs/archive/github-automation.todo.md` (since archived)
- [.github/workflows/board-reopen-reconcile.yaml](../../.github/workflows/board-reopen-reconcile.yaml)
- [Current board sync policy](0005-board-sync-architecture.md)
- `AGENTS.md` — write-safety rules, no-hosting preference
```

<a id="legacy-0005"></a>
## 0005 — retired source record
Status: retired. Authority: Aslan, explicit adoption and old-folder removal instruction in this chat, 2026-11-02. Reserved identity: `0005` (original path `docs/policies/0005-board-sync-architecture.md`). Current agent obligation: `PRESERVE-SYNC`; this mapping records the reviewed migration and does not grant authority through an alias. Original SHA-256: `e474deffd2089991f51bb9583d7b8cb8ded1d5ec7f0f97b07e07538f9b144d65`.

```markdown
# 0005 — Board ↔ Issue Sync Architecture
## Current Approach
1. **Card → close** uses the native **`Auto-close issue`** workflow (Org Kanban → close on `Done`; Open Roles → close on `Filled`). This is the single, deliberate exception to "everything in code," accepted because closing-by-drag is common and instant beats a poll lag. It is documented here and in the README so its lack of a workflow file is not a surprise.
2. **Card → reopen** is the only behavior forced onto a timer (no native, no instant-code path). It is a single scheduled reconciliation Action, `board-reopen-reconcile.yaml`, covering both boards, `*/5` cron, with `workflow_dispatch` + `dry_run`.
3. **Everything else is immediate code Actions**, and **all other native Projects workflows are turned off** (`Auto-add to project`, `Item added to project`, `Item closed`, `Item reopened`), so code is the only actor except the one `Auto-close` exception. Because native "Item added to project" is off, `open-role-add.yaml` and `add-issue-to-kanban.yaml` set initial board status in code.
4. The reopen reconciler's durable safeguard is a **fresh-close guard** that skips issues closed within the last 10 minutes, so a just-closed issue mid-sync isn't spuriously reopened.

## Rationale
Issue events can trigger repository Actions immediately; board field changes cannot. The architecture prioritizes auditable code, immediate behavior where available, and one actor per direction. Native `Auto-close issue` is the deliberate exception to code ownership because closing by dragging a card is common; scheduled reopening handles the direction without a native equivalent. No hosted infrastructure is required.

## Operating Notes
- Exactly one piece of board logic lives outside the repo (the native `Auto-close issue` config in each Project's Workflows UI). It is not version-controlled and leaves no history if changed — an accepted, documented trade for instant close.
- Reopening via a board move lags at least ~5 minutes. **GitHub scheduled workflows are best-effort and frequently delayed** — 10–30+ minutes is normal, and the first run after a schedule is added is the slowest to start (confirmed during rollout: the first scheduled reopen took ~25+ minutes to fire). Reopening the issue directly is immediate and is the reliable path when timing matters.
- The reconciler uses a five-minute cron (`*/5`), with `workflow_dispatch` and `dry_run` for manual checks.
- Any future board-reactive automation must be native or a poll — never `on: projects_v2_item` (per 0004). Before adding a custom Action, check whether a native built-in already covers it.

## Links
- `docs/policies/0004-projects-v2-automation-triggers.md` — the platform constraint this builds on
- `docs/archive/board-sync-redesign.md` / `.todo.md` — the design and execution (since archived)
- `.github/workflows/board-reopen-reconcile.yaml`, `open-role-add.yaml` (the one-time `baseline-terminal-cleanup.yaml` was removed after rollout)
```

