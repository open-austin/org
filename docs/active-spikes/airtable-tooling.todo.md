# Airtable Tooling — To Do
Conceptual doc: `docs/active-spikes/airtable-tooling.md`.

## Background
Building the VRM pilot (#528) in Airtable. We want the agent to inspect/manage the bases directly (like GitHub/Drive) instead of via screenshots. First deliverable is read access; then guarded writes to build the VRM base.

## General Principles
- Follow the repo `tools/` pattern: `tools/airtable/run.sh` wrapper + a Python client, env-loaded creds.
- Dry-run by default on any write. No destructive deletes. No committed data or tokens (public repo, PII).
- Token created under aslan@open-austin.org; agent never handles the raw secret.

## Current State Overview
Phase 1 read tooling is built and working (`tools/airtable/`, stdlib-only client + run.sh). Surveyed all 7 bases. Finding: the account is essentially an abandoned ~2016 Airtable-evaluation sandbox full of default demo templates, with ONE genuinely real dataset (the 2016 membership survey) and a handful of real Austin-org names buried in an otherwise-template CRM. Real data has been exported to CSV. Next: user archives the CSVs to Drive + deletes the junk (destructive, user's action), then we build the VRM base fresh in a clean workspace.

## Survey findings (2026-08-08)
- **Membership Doc → Imported Table (45 records)** — REAL. The 2016 OA membership survey (names, emails, interests, skills, how-they-heard). The one clearly valuable historical artifact. Exported → `oa-membership-survey-2016.csv`.
- **Project intake → Contacts (7 records)** — HALF-REAL. 5 real Austin-org names (League of Women Voters, Austin Mutual Aid, The Austin Commons, AURA, YWCA) + who sourced them (Liani/Daniel Roesler) + LinkedIn URLs, but the notes/stages are leftover Airtable "Personal CRM" template junk (lorem/Wikipedia text). The base's other tables (Companies/Cities/Trips) are pure template. Exported → `oa-project-intake-contacts.csv` (thin salvage).
- **Publicity** — empty template. Junk.
- **Applicant Tracking** — Airtable's demo Applicant Tracker (Howie Liu, Elva Heimer, 2013 dates). Junk.
- **Sales Leads** — Airtable's demo Sales CRM (New Yorker / Condé Nast / lorem ipsum). Junk.
- **PR & Communications** — Airtable's demo PR base (Everlane/Zady/209 Condé Nast press contacts). Junk.
- **Team Task Management** — Airtable's demo task base (2014 museum exhibit data). Junk.

## To Do
- [ ] **[USER] Archive the two exported CSVs** to the OA Google Drive archive (durable record before deletion).
- [ ] **[USER] Delete the junk** bases (Publicity, Applicant Tracking, Sales Leads, PR & Communications, Team Task Management) and the template scaffolding in Project intake. Deletion is destructive and the agent does not do it.
- [ ] Collapse to one clean workspace for OA (the three current workspaces are demo-era cruft).
- [ ] Phase 2 guarded writes (`--dry-run` first): create/update records, create tables/fields — build the VRM base (People/Roles/Orgs, Stage field, form-backing fields) fresh.
- [ ] Decide snapshot handling: Airtable people-data is PII; likely no committed snapshot at all. Gitignore any local dump.

## Ready for Human QA
- (none yet)

## Done
- **[USER] Created the Airtable PAT** (under aslan@open-austin.org) and placed it in the gitignored `.env`; invited aslan@ as a workspace editor. — 2026-08-08
- Added the Airtable section to `.env.example` (scaffolding commit).
- Scaffolded `tools/airtable/` — stdlib-only Python client (`airtable.py`) + `run.sh` loading `AIRTABLE_TOKEN` from `.env`. Never prints the token.
- Phase 1 read commands: `list-bases`, `tables <base>`, `records <base> <table> [n]`, `survey`, `csv <base> <table>`. Verified against the live account (7 bases enumerated).
- Surveyed all bases (see findings above) and exported the two real datasets to CSV (kept out of the repo; PII).
- Decided Airtable over Baserow/NocoDB for the VRM build (free-tier kanban; OA already has the account). See #528.
- Decided this tool lives in the org repo, not personal lifeos-tools (OA-owned, outlives any one maintainer).
- Decided aslan@ attribution over admin@ for edits, with admin@ as owner.
