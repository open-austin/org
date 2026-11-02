---
id: PRESERVE-SYNC
type: operational
scope: "Agent maintenance of board and issue synchronization."
status: adopted
authority: "Aslan approved the exact Open Austin initial adoption set in this chat on 2026-11-02."
revised: "2026-11-02"
depends_on: ["RESOLVE-DEPENDENCIES"]
related_to: ["DESIGN-TRIGGERS"]
---
# Preserve reviewed board synchronization
Preserve native Auto-close issue as the single non-code exception: Done closes Org Kanban issues and Filled closes Open Roles issues. Keep all other native workflows off and other paths in immediate code Actions, including initial status assignment. Card-to-reopen uses the single board-reopen-reconcile poller for both boards with five-minute cron and manual dry_run. Preserve its ten-minute fresh-close guard. Document the native configuration exception and best-effort scheduling delays. Future board-reactive automation must be native or polling, never repository projects_v2_item triggers. These existing automated behaviors do not grant agents new live-write authority.

Existing obligation and retained rationale: [retired source and retained rationale](../archive/legacy-agent-policies.md#legacy-0005).

Implementation evidence: the [reconciler](../../.github/workflows/board-reopen-reconcile.yaml) contains the timer, dry-run branch and 600-second guard. Native Auto-close configuration lives in the Projects UI; this migration does not verify or change that external setting.
