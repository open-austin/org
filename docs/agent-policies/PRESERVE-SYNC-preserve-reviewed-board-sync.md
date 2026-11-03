---
id: PRESERVE-SYNC
type: operational
scope: "Agent maintenance of retained Open Roles synchronization."
status: adopted
authority: "Aslan approved the initial set and requested Org Kanban retirement while preserving Roles, intake and contributor records on 2026-11-02; scope recorded in org-workflow-refresh."
revised: "2026-11-02"
depends_on: ["RESOLVE-DEPENDENCIES"]
related_to: ["DESIGN-TRIGGERS"]
---
# Preserve reviewed Open Roles synchronization
Preserve native Auto-close issue as the single non-code exception for Open Roles: Filled closes the issue. Keep other native Open Roles workflows off and retained issue-event paths in code Actions, including initial Open status assignment. Card-to-reopen uses board-reopen-reconcile for Open Roles with five-minute cron and manual dry_run. Preserve its ten-minute fresh-close guard and document best-effort scheduling delays. Org Kanban’s routing, status, archive, blocker and reconciliation behavior is retired under the authorized workflow refresh; it must not be recreated incidentally. Preserve Engagement intake and contributor records until separately changed. These automated behaviors grant no new live-write authority.

Existing obligation and retained rationale: [retired source and retained rationale](../archive/legacy-agent-policies.md#legacy-0005).

Implementation evidence: the [reconciler](../../.github/workflows/board-reopen-reconcile.yaml) contains the timer, dry-run branch and 600-second guard. Native Auto-close configuration lives in the Projects UI; this migration does not verify or change that external setting.
