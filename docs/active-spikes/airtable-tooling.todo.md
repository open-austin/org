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
- [ ] **[USER] In the Airtable UI, delete the base-template cruft fields** on each table (Assignee, Status, Attachments, Attachment Summary) — unused, and the template "Status" is distinct from our "Engagement Status". (Kept them rather than API-deleting, since deletes are destructive.)
- [ ] **[USER] Create the Views** (the API can't): a kanban by Engagement Status (the funnel), a skill-searchable Directory (public, consent-gated on `Public Listing Consent`), a Needs-follow-up view, and the public no-login Intake Form(s) writing into Intake Staging.
- [ ] Import legacy data into **Intake Staging** oldest-first (2016 survey → GitHub Contributor Profiles → Adam's roster + Liani's 2024 roster), tagged by `Import Source`, then normalize/reconcile into People (manual identity resolution; no auto-merge).
- [ ] Populate `UUID`s (write tool at import; an automation script for UI/form-created records).
- [ ] After migration, retire the GitHub Contributor Profiles + issue templates (full cutover; relates to #468/#497).
- [ ] Decide snapshot handling: Airtable people-data is PII; no committed snapshot. Gitignore any local dump.

## Ready for Human QA
- (none yet)

## Done
- **[USER] Cleaned the account + created the base** (2026-08-10): deleted the demo bases, renamed a workspace to "Open Austin", created base `Relationship Management` with tables People (record "Person"), Teams, Organizations, Roles, and Intake Staging (record "Prospect").
- **Built the base schema via the Phase-2 write tool** (2026-08-10): added `apply-fields` (dry-run by default) and created all **82 fields** across the 5 tables from `tools/airtable/relationship-management-schema.json`, zero failures. People carries UUID + Name/Legal Name, the four classification dimensions (Persona / Affiliations / Engagement Status + Disengagement Type / History Flags), placements (Teams/Roles/Organization links, CoP), Engagement fields (Skills, Languages, Availability, Location, Effort, Willingness to expand roles), Access held/requested, and evidence fields (Last Slack/GitHub activity, Repos). Teams typed (Product/Standing/CoP). Intake Staging mirrors People (Person-shaped) + Import Source / Ready to Promote / Promoted Person. Linked records auto-created reverse fields.
- **Confirmed demo-vs-real via record timestamps** (2026-08-10): Applicant Tracking = Airtable's sample applicant set (Howie Liu as interviewer; all 9 records batch-imported in a 6-minute window with backdated 2013 timestamps). Team Task Management = Airtable's museum-exhibit-planning sample (docents, gallery installs, "Top Predator" exhibit — not civic-tech, not OA). Sales Leads / PR & Communications = Airtable's demo CRM/PR sets. Project intake = real (5 Austin-org contacts sourced by Liani / Daniel Roesler, created 2013, blanks added 2016). Membership Doc = real 2016 OA membership survey.
- **Exhaustive export** (2026-08-10): all 7 bases / 23 tables / ~430 records → CSV, imported as a consolidated Google Doc into `_Archive/Pre 2026 Airtable Archive` in the OA Drive (the import tool can't upload raw .csv; raw CSVs also exported locally). Nothing lost regardless of the delete decision.
- **Base schema** agreed (base `Relationship Management`; People/Teams/Roles/Organizations/Intake; coarse Status + placements), to be documented in this repo before Phase-2.
- **[USER] Created the Airtable PAT** (under aslan@open-austin.org) and placed it in the gitignored `.env`; invited aslan@ as a workspace editor. — 2026-08-08
- Added the Airtable section to `.env.example` (scaffolding commit).
- Scaffolded `tools/airtable/` — stdlib-only Python client (`airtable.py`) + `run.sh` loading `AIRTABLE_TOKEN` from `.env`. Never prints the token.
- Phase 1 read commands: `list-bases`, `tables <base>`, `records <base> <table> [n]`, `survey`, `csv <base> <table>`. Verified against the live account (7 bases enumerated).
- Surveyed all bases (see findings above) and exported the two real datasets to CSV (kept out of the repo; PII).
- Decided Airtable over Baserow/NocoDB for the VRM build (free-tier kanban; OA already has the account). See #528.
- Decided this tool is OA-owned and lives in the org repo (outlives any one maintainer).
- Decided aslan@ attribution over admin@ for edits, with admin@ as owner.
