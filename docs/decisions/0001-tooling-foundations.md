# 0001 — Tooling Foundations

**Date:** 2026-06-10
**Status:** Accepted

---

## Context

We are building automation tooling to manage the Open Austin GitHub org: reading and acting on issues, project boards, labels, and milestones. This is analogous to the LifeOS personal tooling in `configs/`, but pointed at shared org infrastructure with a much higher blast radius.

Several foundational choices needed to be made before any implementation work could proceed.

---

## Decisions

### 1. GitHub Projects v2 board support from the start

We will support the full Projects v2 surface (board columns, custom fields like Status/Priority/Size, iterations) in addition to plain issues, labels, and milestones.

Projects v2 requires the GraphQL API and opaque node IDs; it cannot be driven by REST alone. This is accepted complexity in exchange for full power over the org's actual workflow surface.

### 2. Tools live in this repo

The tooling lives inside the `open-austin/org` repo, not a separate personal harness. This makes the tools portable and colocated with the org they manage, and makes them available to other Open Austin contributors.

### 3. `gh` CLI as the durable sync and write boundary

The `gh` CLI (and `gh api graphql`) is the durable, scriptable path for snapshot generation and guarded write commands. It is the source of truth for any automated or repeatable behavior.

Rationale: deterministic, auditable, composable, works in CI or a cron-free local flow — same reasoning that led the LifeOS work to prefer the CLI over desktop-app MCP connectors for persistent automation.

### 4. MCP server as the interactive desktop-app layer

The GitHub MCP server is the right fit for interactive "analyze and act" sessions in Claude Desktop or similar. It is not a second source of truth; it wraps and exposes the same underlying GitHub API.

The CLI is authoritative for durable behavior. MCP is a convenience layer on top.

### 5. Read-only sync before guarded writes

v1 will deliver read-only snapshot generation and agent analysis. Write tools are added incrementally, starting with the lowest-blast-radius mutations (label, comment) before moves and closes, and always with `--dry-run` support.

---

## Consequences

- Tools must support GraphQL for Projects v2 operations.
- All write tools must have a `--dry-run` flag and require explicit user approval before executing.
- `GH_TOKEN` must have both `repo` and `project` scopes, and must be SAML SSO-authorized for the `open-austin` org if required.
- The interactive MCP path and the CLI path must not diverge in their write-safety rules.

---

## Related

- `AGENTS.md` — agent rules derived from these decisions
- `docs/how-to-spike.md` — spike process
- `TODO.md` — active work tracking
- `docs/github-tooling.md` — spike conceptual doc (when created)
