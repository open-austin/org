# Airtable Tooling — Conceptual
A read-first (later guarded-write) CLI wrapper for Open Austin's Airtable, so agents and contributors can inspect and manage OA's bases the same way this repo already handles GitHub and Google Docs — without passing screenshots back and forth.

Consumer / driver: the VRM prototype ([open-austin/org#528](https://github.com/open-austin/org/issues/528)) needs a People/Roles/Orgs base with an intake form and a funnel kanban. This tool is the machinery for building and inspecting that base programmatically.

## Fit
OA-owned infrastructure that follows the existing `tools/` pattern in this repo: env-loaded credentials, `run.sh` wrappers, and dry-run-first writes.

## Auth & attribution model
- **Airtable Personal Access Token (PAT)** loaded from the environment as `AIRTABLE_TOKEN`, never hardcoded or committed (same rule as `GH_TOKEN`). Documented in `.env.example`.
- **Created under aslan@open-austin.org, not the admin@ owner account.** Rationale: the person piloting the agent acts as themselves, so Airtable's change history attributes edits to the individual rather than a shared admin login, so it's a cleaner audit trail, using the aslan@open-austin.org account for the org's Google access. admin@ stays the workspace owner; aslan@ is invited as an editor.
- Scope broadly for real work (`data.records:read`, `data.records:write`, `schema.bases:read`, `schema.bases:write`; `webhook:manage` optional), granted to the specific OA workspaces/bases. The token is created and placed by the user — the agent never handles the raw secret.

## Safety & privacy boundaries
- The VRM base will hold **real people's contact info (PII)**. This repo is **public**. Therefore: never commit Airtable data, exports, or snapshots of people records; never commit the token. Any local dump is gitignored, same as `snapshot/`.
- Writes follow this repo's write-safety rules: **dry-run by default**, re-fetch before mutate, no destructive deletes, bounded/no notifications.
- Public repo carries **code only** — no data, no tokens.

## Scope
- **Phase 1 (read):** list workspaces/bases (metadata API), list tables + schema for a base, and dump records of a table to stdout or a gitignored local file. This is the "let the agent see the same structures" milestone that unblocks the workspace cleanup and the VRM build.
- **Phase 2 (guarded write):** create/update records, and create tables/fields, all `--dry-run` first — used to build the VRM base (People/Roles/Orgs, Stage field, form-backing fields).

## Non-goals
- Not a general Airtable admin panel or a UI replacement.
- Not a store for OA member PII inside the repo.
- Not a personal-productivity tool (that's a later pull-in if ever).

## Constraints
- Airtable REST API rate limit ~5 req/sec/base; the metadata API needs `schema.bases:read`.
- Free-tier limits (1,000 records/base, 5 editors/workspace) shape what's testable.

## Relationship to other work
- Drives: VRM prototype [open-austin/org#528](https://github.com/open-austin/org/issues/528) (People Systems epic #523).
- Mirrors the existing `tools/google-docs/` auth+wrapper pattern.
