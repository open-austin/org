---
id: DESIGN-TRIGGERS
type: operational
scope: "Agent design of board-reactive automation."
status: adopted
authority: "Aslan approved the exact Open Austin initial adoption set in this chat on 2026-11-02."
revised: "2026-11-02"
depends_on: ["RESOLVE-DEPENDENCIES"]
related_to: ["PRESERVE-SYNC"]
---
# Respect board trigger boundaries
Do not use `on: projects_v2_item` in repository Actions for Projects v2 field changes. Check native workflows before adding custom automation. Use native capabilities where they fit or scheduled reconciliation under the existing no-hosting boundary. Preserve the reviewed native-close and scheduled-reopen architecture; a five-minute cron is not a delivery guarantee. Reopening the issue directly is the immediate issue-event route.

Existing obligation and retained rationale: [retired source and retained rationale](../archive/legacy-agent-policies.md#legacy-0004).
