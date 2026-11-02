---
id: BUILD-CLI
type: operational
scope: "Agent implementation of substantive CLI tools."
status: adopted
authority: "Aslan approved the exact Open Austin initial adoption set in this chat on 2026-11-02."
revised: "2026-11-02"
depends_on: ["RESOLVE-DEPENDENCIES"]
related_to: ["USE-TOOLS"]
---
# Build substantive CLI tools in Python
Use Python 3 for substantive CLI tools; thin shell wrappers may provide familiar entry points. Prefer standard-library argument parsing, validation, JSON handling and dry-run logic where sufficient. Document actual runtime dependencies and inspect current implementations rather than inferring dependencies from retired tooling. Delegate generic Google Docs operations to installed Agent Hands; keep organization meeting procedures and target selection local.

Existing obligation and retained rationale: [retired source and retained rationale](../archive/legacy-agent-policies.md#legacy-0002).
