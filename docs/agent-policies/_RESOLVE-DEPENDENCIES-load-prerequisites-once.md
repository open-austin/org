---
id: RESOLVE-DEPENDENCIES
type: kernel
scope: "Agent discovery and loading of applicable adopted policy prerequisites."
status: adopted
authority: "Aslan approved the exact Open Austin initial adoption set in this chat on 2026-11-02."
revised: "2026-11-02"
depends_on: ["ADOPT-POLICIES", "PRESERVE-IDENTITY"]
related_to: []
---
# Resolve prerequisites before loading
The actual project's AGENTS routing identifies its `policy.index.md`. The index links each policy's ID, imperative title, one-line scope, status and substantive revision date without duplicating its body. A provider's bundled index is not an adopting project's operative index.

An adopted policy's `depends_on` prerequisites must exist and be adopted. Multiple parents are allowed, but the dependency graph, including proposed changes, must be acyclic. Missing/inactive prerequisites or cycles invalidate loading; cycles require repair of their actual meaning, not arbitrary ordering or relabeling a genuine prerequisite. `related_to` expresses reference only and confers no prerequisite, adoption or authority.

Applicable adopted policies are loaded with their complete prerequisite closure, prerequisites before dependents and each selected node once. Lexical ID order among currently ready nodes makes that order deterministic. Changed policy bodies/scopes require renewed dependent and applicability review; one-time loading does not justify stale instructions. Loading order, graph depth, IDs, filenames and dates never confer precedence.

Substantive contradictions require human resolution rather than last-loaded or newest-rule override. Independent authorized work may continue while affected work is unresolved. Structural checks can establish graph/index properties, not semantic consistency, authentic human intent, agent compliance or tool enforcement. An invalid set supplies no partial loading plan.
