---
id: USE-TOOLS
type: operational
scope: "Agent development and use of organization tooling."
status: adopted
authority: "Aslan approved the exact Open Austin initial adoption set in this chat on 2026-11-02."
revised: "2026-11-02"
depends_on: ["RESOLVE-DEPENDENCIES"]
related_to: ["BUILD-CLI", "PRESERVE-SYNC"]
---
# Use guarded organization tools
Keep organization tooling in this repository. Use `gh` and `gh api graphql` for durable GitHub reads and guarded writes; support GraphQL and opaque node IDs for Projects v2 operations. Read current organization state through `gh`; ignored `snapshot/` is scratch, not current state. Do not rebuild retired sync tooling without authorization. Add write capabilities incrementally with dry-run support and explicit approval. Interactive MCP and CLI paths follow the same write-safety rules. Follow [AGENTS](../../AGENTS.md) for exact authorization and credential boundaries.

Existing obligation and retained rationale: [retired source and retained rationale](../archive/legacy-agent-policies.md#legacy-0001).
