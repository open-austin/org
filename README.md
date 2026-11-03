# Open Austin Org Tooling
This repo contains tools, documentation, and automation for managing the [Open Austin](https://www.open-austin.org/) GitHub organization.

**Purpose:** Maintain repository tooling, retained Open Roles automation and public collaboration documentation. General organizational tasks are tracked in Slack Lists; Engagement intake and contributor records retain their existing owners.

## Quick Start
### For Contributors
See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions (GitHub CLI, auth, spike workflow).

### For Agents
See [AGENTS.md](AGENTS.md) or [CLAUDE.md](CLAUDE.md) for rules, boundaries, and write safety requirements.

## Reading Org State
This repo does not ship a sync tool. It had one until 2026-09-07; `tools/sync/` was removed because it existed to feed one maintainer's private knowledge system and had no other users. Read current org state through the GitHub UI, or `gh` directly:

```bash
gh issue list --limit 200 --state open --json number,title,labels,assignees
gh project item-list 6 --owner open-austin --format json   # Open Roles
```

`snapshot/` remains gitignored scratch space that `tools/notify/` reads from. Nothing here regenerates it from GitHub any more. See `docs/archive/retire-sync-tooling.md`.

## Write Operations
Guarded writes happen through the **board-automation workflows** described below, the repo's narrow dry-run-first tools, and the **`gh` CLI** for ad-hoc changes that do not yet justify a wrapper. Use `gh issue create` for issue creation and Agent Hands `use-google-docs` for bounded shared-Doc reads and exact-match replacements. See [AGENTS.md](AGENTS.md) for the approval and write-safety rules.

All write operations follow the write-safety rules: dry-run first where supported, and explicit approval before anything that mutates shared org state.

### Issue Creation
```bash
gh issue create --repo open-austin/org --title "Task title" --body-file /tmp/issue.md --label infrastructure --assignee @me
```

The wrapper that used to front this (`tools/issues/create.sh`, dry-run by default) was removed 2026-09-07 along with the rest of the single-maintainer tooling — see `docs/archive/retire-sync-tooling.md`. `gh` does the work; the approval discipline it enforced is stated in [AGENTS.md](AGENTS.md) and is a rule rather than a script. **Confirm the exact title, body, labels, and assignees with a human before creating an issue.**

### Shared Google Docs
Use the installed Agent Hands setup-google-services and use-google-docs skills for an explicitly selected account/document and supported reads or exact replacements. Preserve existing external credentials and canonical authorship. Follow AGENTS’ reviewed-plan and readback rules. This repo no longer supplies a weekly-meeting processing skill or automatically routes organizational meeting actions into GitHub.

## Open Roles automation
The current retirement patch removes general Org Kanban automation while retaining Open Roles. **Deployment is pending:** local source changes do not disable hosted Actions or close the live Project. The [refresh spike](docs/active-spikes/org-workflow-refresh.md) owns exact publication, Project retirement and issue-cleanup receipts.

Open-role issues route to Open Roles when labeled. Code assigns initial Open status, closing sets Filled, and reopening sets Open. Native Auto-close issue is the one external configuration exception: moving a card to Filled closes its issue. The retained board-reopen-reconcile poller checks only Open Roles every five minutes, preserves the ten-minute fresh-close guard and supports manual dry_run. Scheduled delivery is best-effort; reopening an issue directly uses the immediate issue-event path. Native configuration and live scheduling outcomes must be verified separately from source checks.

| Workflow | Purpose |
| --- | --- |
| open-role-add | Add labeled role issues to Open Roles and set Open. |
| label-open-role-from-form | Apply the role form’s team labels. |
| closed-to-filled | Move closed role issues to Filled. |
| open-role-reopened | Move reopened role issues to Open. |
| board-reopen-reconcile | Reopen closed Roles issues moved out of Filled, after the fresh-close guard. |
| archive-old-filled | Weekly archive of Filled roles older than one year. |
| stale-role-warning | Weekly stale-role notice under its existing cadence and guards. |
| role-pipeline-report | Monthly role-pipeline Slack report under its existing first-Monday guard. |

The retired weekly-org-summary remains a historical reimplementation record. Notify helpers retain explicitly approved manual webhook/Block Kit use; the monthly role report posts directly from its workflow. The removed Kanban files and meeting procedure remain recoverable from Git history.

## Documentation
- **Active spikes:** `docs/active-spikes/` — current work with accompanying `.todo.md` files
- **Agent policies:** [docs/agent-policies/policy.index.md](docs/agent-policies/policy.index.md) — explicitly adopted obligations for agents
- **Human governance:** [contributor-policy.md](contributor-policy.md) — organizational governance, protected from agent edits
- **Retired policy sources:** [legacy source records](docs/archive/legacy-agent-policies.md) — reserved numbered identities, exact originals and rationale
- **Saved for later:** individual `docs/scratch/` subject notes — possibilities or parked questions, without a commitment to start work
- **Misc intake:** `docs/scratch/misc.md` — raw observed friction and issue intake
- **Scratch:** `docs/scratch/` — exploratory drafts
- **Archive:** `docs/archive/` — historical context

See [project-workflows/run-project-spike/SKILL.md](project-workflows/run-project-spike/SKILL.md) for the full workflow, and [skills/](skills/) for the repo's other agent-assisted workflows.

## Project Workflows adoption
Use the adopted [contribution procedure](project-workflows/coordinate-project-contribution/SKILL.md) and [collaborator quick start](project-workflows/README.md#join-an-existing-project) for human-directed review across separate agent-owned spikes. A branch may carry several spikes/issues and later PRs; Commit Work retains atomic scope. Existing governance, canonical shared records and explicit external-write approval rules remain authoritative. This update enables no new forge automation.

The complete collection lives in `project-workflows/` on `project/org`; the parent pins its exact commit. Use its [update procedure](project-workflows/update-project-workflows/SKILL.md) for reconciliation, with project rules in [AGENTS.md](AGENTS.md). Initialize the recorded workflow revision with `git submodule update --init -- project-workflows`; client discovery and service access are separate checks. [Reconciliation and validation](docs/active-spikes/project-workflows-adoption.md) · [remaining steps](docs/active-spikes/project-workflows-adoption.todo.md).
