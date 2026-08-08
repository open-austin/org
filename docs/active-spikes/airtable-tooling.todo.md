# Airtable Tooling — To Do
Conceptual doc: `docs/active-spikes/airtable-tooling.md`.

## Background
Building the VRM pilot (#528) in Airtable. We want the agent to inspect/manage the bases directly (like GitHub/Drive) instead of via screenshots. First deliverable is read access; then guarded writes to build the VRM base.

## General Principles
- Follow the repo `tools/` pattern: `tools/airtable/run.sh` wrapper + a Python client, env-loaded creds.
- Dry-run by default on any write. No destructive deletes. No committed data or tokens (public repo, PII).
- Token created under aslan@open-austin.org; agent never handles the raw secret.

## Current State Overview
Decisions settled: Airtable is the VRM tool (free tier has the kanban the funnel needs; OA already has the account); the tool lives in this repo; edits attributed via aslan@ not admin@. **Implementation is blocked on two user actions** (PAT + workspace invite) because the agent cannot create credentials. Workspace cleanup is intentionally deferred until Phase 1 read works, so it can be done with visibility.

## To Do
- [ ] **[USER — credential] Create an Airtable PAT** logged in as aslan@open-austin.org. Scopes: `data.records:read`, `data.records:write`, `schema.bases:read`, `schema.bases:write` (add `webhook:manage` only if needed). Grant it access to the OA workspaces/bases. Put it in the gitignored `.env` as `AIRTABLE_TOKEN=...`. Do not paste it into chat or commit it.
- [ ] **[USER] Invite aslan@open-austin.org as an editor** to the OA workspaces (admin@ remains owner). On the free tier this counts toward the 5-editor/workspace cap (admin@ + aslan@ = 2, fine).
- [ ] Add an Airtable section to `.env.example` (`AIRTABLE_TOKEN`, optional default base id) with scope docs. (done in the scaffolding commit)
- [ ] Scaffold `tools/airtable/` — `run.sh` + Python client reading `AIRTABLE_TOKEN`, mirroring `tools/google-docs/`.
- [ ] Phase 1 read commands: `list-bases` (metadata API), `list-tables <BASE>`, `schema <BASE>`, `records <BASE> <TABLE>` (bounded; stdout or gitignored file).
- [ ] Verify reads against the real OA bases; confirm the agent can see workspace/base/table structures.
- [ ] Then: workspace cleanup pass (with the user), now that structures are visible.
- [ ] Phase 2 guarded writes (`--dry-run` first): create/update records, create tables/fields — used to build the VRM base (People/Roles/Orgs, Stage field, form-backing fields).
- [ ] Decide snapshot handling: Airtable people-data is PII; likely no committed snapshot at all. Gitignore any local dump.

## Ready for Human QA
- (none yet)

## Done
- Decided Airtable over Baserow/NocoDB for the VRM build (free-tier kanban; OA already has the account). See #528.
- Decided this tool lives in the org repo, not personal lifeos-tools (OA-owned, outlives any one maintainer).
- Decided aslan@ attribution over admin@ for edits, with admin@ as owner.
