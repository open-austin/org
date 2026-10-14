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
- [Spike skill](../../skills/run-project-spike/SKILL.md)
- [TODO.md](../../TODO.md) — active work index
- [Tooling history](../archive/github-tooling.md)
- [Sync retirement](../archive/retire-sync-tooling.md)
